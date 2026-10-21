from pathlib import Path
import json, time, hashlib, sys, shutil
import win32com.client
import pythoncom

sys.stdout.reconfigure(encoding='utf-8')
BASE = Path(__file__).resolve().parent
BUILD = BASE / '_build'
RENDERS = BUILD / 'renders'
BASE.mkdir(parents=True, exist_ok=True)
BUILD.mkdir(exist_ok=True)
RENDERS.mkdir(exist_ok=True)

def rgb(hexvalue):
    v=hexvalue.lstrip('#')
    r,g,b=(int(v[i:i+2],16) for i in (0,2,4))
    return r+(g<<8)+(b<<16)

BLUE = rgb('#194B93')
INK = rgb('#172B43')
GRAY = rgb('#506074')
LIGHT = rgb('#EAF0F7')
RULE = rgb('#C9D3DF')
RED = rgb('#D5222A')
PALE_RED = rgb('#FBEFF0')
WHITE = rgb('#FFFFFF')
GREEN = rgb('#286553')
PALE_GREEN = rgb('#EEF6F2')
AMBER = rgb('#875A11')
PALE_AMBER = rgb('#FFF7E9')
FONT = 'Arial'
W,H=960,540
ALL_TEXT=[]
SLIDE_RECORDS=[]

app = win32com.client.DispatchEx('PowerPoint.Application')
pre_existing_count = app.Presentations.Count
pres = app.Presentations.Add(0)
pres.PageSetup.SlideWidth=W
pres.PageSetup.SlideHeight=H

def txt(slide, text, x, y, w, h, size=22, color=INK, bold=False, align=1, margin=0, name=None, valign=1):
    s=slide.Shapes.AddTextbox(1,x,y,w,h)
    if name: s.Name=name
    tf=s.TextFrame
    tf.MarginLeft=tf.MarginRight=margin
    tf.MarginTop=tf.MarginBottom=margin
    tf.WordWrap=-1
    tf.AutoSize=0
    tf.VerticalAnchor=valign
    tr=tf.TextRange
    tr.Text=text
    tr.Font.Name=FONT
    tr.Font.Size=size
    tr.Font.Bold=-1 if bold else 0
    tr.Font.Color.RGB=color
    tr.ParagraphFormat.Alignment=align
    tr.ParagraphFormat.SpaceBefore=0
    tr.ParagraphFormat.SpaceAfter=0
    # Use a fixed relative leading that remains readable in Vietnamese.
    tr.ParagraphFormat.SpaceWithin=1.04
    # Keep the authored native geometry after PowerPoint applies text defaults.
    tf.AutoSize=0
    s.Left,s.Top,s.Width,s.Height=x,y,w,h
    ALL_TEXT.append((slide.SlideIndex,s.Name,text))
    return s

def line(slide,x1,y1,x2,y2,color=RULE,width=1.3,arrow=False,dash=False):
    s=slide.Shapes.AddLine(x1,y1,x2,y2)
    s.Line.ForeColor.RGB=color
    s.Line.Weight=width
    if arrow: s.Line.EndArrowheadStyle=3
    if dash: s.Line.DashStyle=4
    return s

def route(slide,pts,color=BLUE,width=1.6,arrow=True,dash=False):
    for i in range(len(pts)-1):
        line(slide,*pts[i],*pts[i+1],color,width,arrow and i==len(pts)-2,dash)

def box(slide,text,x,y,w,h,size=20,fill=LIGHT,stroke=BLUE,color=INK,bold=False):
    s=slide.Shapes.AddShape(1,x,y,w,h)
    s.Fill.ForeColor.RGB=fill
    s.Line.ForeColor.RGB=stroke
    s.Line.Weight=1.35
    tf=s.TextFrame
    tf.MarginLeft=tf.MarginRight=9
    tf.MarginTop=tf.MarginBottom=5
    tf.WordWrap=-1
    tf.AutoSize=0
    tf.VerticalAnchor=3
    tr=tf.TextRange
    tr.Text=text
    tr.Font.Name=FONT
    tr.Font.Size=size
    tr.Font.Bold=-1 if bold else 0
    tr.Font.Color.RGB=color
    tr.ParagraphFormat.Alignment=2
    tr.ParagraphFormat.SpaceBefore=0
    tr.ParagraphFormat.SpaceAfter=0
    tr.ParagraphFormat.SpaceWithin=1.02
    ALL_TEXT.append((slide.SlideIndex,s.Name,text))
    return s

def table(slide,headers,rows,x,y,widths,heights,sizes=18):
    nrows=1+len(rows)
    shape=slide.Shapes.AddTable(nrows,len(headers),x,y,sum(widths),sum(heights))
    t=shape.Table
    for j,w in enumerate(widths,1):t.Columns(j).Width=w
    for i,h in enumerate(heights,1):t.Rows(i).Height=h
    for i,row in enumerate([headers]+rows,1):
        for j,value in enumerate(row,1):
            cell=t.Cell(i,j)
            cs=cell.Shape
            cs.Fill.ForeColor.RGB=BLUE if i==1 else (WHITE if i%2 else LIGHT)
            tf=cs.TextFrame
            tf.MarginLeft=tf.MarginRight=8
            tf.MarginTop=tf.MarginBottom=5
            tf.VerticalAnchor=3
            tf.WordWrap=-1
            # PowerPoint rejects TextFrame.AutoSize on native table cells.
            tr=tf.TextRange
            tr.Text=str(value)
            tr.Font.Name=FONT
            tr.Font.Size=sizes
            tr.Font.Bold=-1 if i==1 else 0
            tr.Font.Color.RGB=WHITE if i==1 else INK
            tr.ParagraphFormat.Alignment=1
            tr.ParagraphFormat.SpaceBefore=0
            tr.ParagraphFormat.SpaceAfter=0
            tr.ParagraphFormat.SpaceWithin=1.0
            for side in (1,2,3,4):
                cell.Borders(side).ForeColor.RGB=RULE
                cell.Borders(side).Weight=0.7
            ALL_TEXT.append((slide.SlideIndex,f'table-{i}-{j}',str(value)))
    return shape

def notes(slide,text,sources,duration):
    source_text='\n'.join(f'- {s}' for s in sources)
    body=f'Thời lượng gợi ý: {duration}\n\n{text}\n\nNguồn và giới hạn:\n{source_text}'
    slide.NotesPage.Shapes.Placeholders(2).TextFrame.TextRange.Text=body
    SLIDE_RECORDS[-1].update(notes=text,sources=sources,duration=duration)

def new(title,source):
    s=pres.Slides.Add(pres.Slides.Count+1,12)
    s.FollowMasterBackground=0
    s.Background.Fill.ForeColor.RGB=WHITE
    line(s,45,25,915,25,BLUE,2.2)
    txt(s,title,45,42,870,52,32,BLUE,True,name='Slide title')
    line(s,45,504,915,504,RULE,0.8)
    txt(s,source,45,512,815,18,11.2,GRAY,name='Source footer')
    txt(s,f'{s.SlideIndex:02d} / 15',862,510,54,20,12,GRAY,align=3,name='Page number')
    SLIDE_RECORDS.append({'number':s.SlideIndex,'title':title,'source_footer':source})
    return s

CONTRACT='docs/midterm/content-contract.md (scientific baseline ac4ade796e56377882b8069d0fb7a14809e8180b)'
ARCH='docs/system-architecture.md; assets/diagrams/02-agentic-rag-architecture.svg/.mmd'
WORK='docs/agentic-workflow.md; assets/diagrams/03-controller-state-machine.svg/.mmd'
EXP='docs/experimental-design.md; assets/diagrams/05-experimental-arms.svg/.mmd'
RESULT='docs/current-results.md; baseline aggregate receipts qualification/reports/koa_final_closure/'
LEWIS='Lewis et al. Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks. NeurIPS 2020. https://arxiv.org/abs/2005.11401'
SELF='Asai et al. Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection. ICLR 2024. https://arxiv.org/abs/2310.11511'
CRAG='Yan et al. Corrective Retrieval Augmented Generation. 2024 preprint. https://arxiv.org/abs/2401.15884'
FACT='Min et al. FActScore: Fine-grained Atomic Evaluation of Factual Precision in Long Form Text Generation. EMNLP 2023. https://aclanthology.org/2023.emnlp-main.741/'
SELECT='Kamath et al. Selective Question Answering under Domain Shift. ACL 2020. https://aclanthology.org/2020.acl-main.503/'
MEDCPT='Jin et al. MedCPT: Contrastive Pre-trained Transformers with Large-scale PubMed Search Logs for Zero-shot Biomedical Information Retrieval. Bioinformatics 2023;39(11):btad651. https://doi.org/10.1093/bioinformatics/btad651'
FAISS='Johnson et al. Billion-Scale Similarity Search with GPUs. IEEE TBD 2021;7(3):535-547. https://arxiv.org/abs/1702.08734'
MEDRAG='Xiong et al. Benchmarking Retrieval-Augmented Generation for Medicine. Findings ACL 2024:6233-6251. https://aclanthology.org/2024.findings-acl.372/'

# 01. Cover, using only the official, unmodified institutional asset.
s=pres.Slides.Add(1,12)
s.FollowMasterBackground=0
s.Background.Fill.ForeColor.RGB=WHITE
line(s,45,25,915,25,BLUE,2.2)
txt(s,'TRƯỜNG ĐẠI HỌC TÔN ĐỨC THẮNG',45,47,720,36,24,BLUE,True)
s.Shapes.AddPicture(str(BASE/'assets/tdtu-footer-official.png'),0,-1,816,40,100,100)
txt(s,'BÁO CÁO GIỮA KỲ NGHIÊN CỨU',45,138,860,32,18,GRAY,True)
txt(s,'KOA Agentic-RAG System',45,190,870,65,44,BLUE,True,name='Deck title')
txt(s,'Evidence-Grounded Agentic Retrieval-Augmented Generation\nfor Knee Osteoarthritis Clinical Guidelines',45,270,850,80,24,INK)
line(s,45,385,150,385,RED,3)
txt(s,'Phạm Hồng Đăng Khoa\nNguyễn Hoàng Khang',45,409,700,60,22,INK)
txt(s,'Scientific snapshot: ac4ade7     E1-v2 prospective protocol',45,480,860,20,12,GRAY)
txt(s,'TDTU-inspired academic theme',45,508,815,18,11.2,GRAY)
txt(s,'01 / 15',862,507,54,20,12,GRAY,align=3)
SLIDE_RECORDS.append({'number':1,'title':'KOA Agentic-RAG System','source_footer':'Scientific snapshot ac4ade7'})
notes(s,'Báo cáo trình bày tiến độ của KOA Agentic-RAG System theo snapshot khoa học ac4ade7. Mục tiêu là một prototype truy xuất và kiểm chứng bằng chứng từ guideline thoái hóa khớp gối. Phần chính tập trung vào thiết kế framework, ranh giới benchmark, cơ chế PRE/POST và protocol E1-v2. Các kết quả hiện có là qualification kỹ thuật offline với MOCK. Chất lượng lâm sàng và ưu thế giữa các nhánh vẫn chưa có kết luận. Logo lấy nguyên bản từ website chính thức TDTU. Bố cục này là TDTU-inspired academic theme, chưa có căn cứ gọi là template chính thức của trường.',[CONTRACT,'Logo official, unaltered: https://www.tdtu.edu.vn/sites/www/files/logo_2.png; source page https://www.tdtu.edu.vn/; retrieved 2026-10-21. Design colors are choices, not official brand specifications.'],'00:40')

# 02. Motivation.
s=new('Yêu cầu của QA trên guideline KOA','Nguồn: content contract §3; Lewis et al. (2020); Xiong et al. (2024)')
box(s,'Câu hỏi về\nguideline',45,128,245,88,24)
box(s,'Đoạn bằng chứng\nliên quan',357,128,245,88,24)
box(s,'Câu trả lời\nđủ căn cứ?',670,128,245,88,24)
route(s,[(290,172),(357,172)])
route(s,[(602,172),(670,172)])
txt(s,'Các điều kiện cần kiểm chứng',45,258,870,34,25,BLUE,True)
for y,label,detail in [(313,'Nguồn','Phù hợp phạm vi và phiên bản đã khóa'),(366,'Nội dung','Bao phủ các nghĩa vụ thông tin từ câu hỏi'),(419,'Phát biểu','Từng claim có bằng chứng và trích dẫn truy vết')]:
    txt(s,label,45,y,160,31,22,BLUE,True)
    txt(s,detail,220,y,695,39,22)
notes(s,'Một đoạn được truy xuất có thể liên quan đến câu hỏi nhưng chưa đủ để tạo câu trả lời có căn cứ. Trong đề tài, yêu cầu cần tách thành phạm vi nguồn, nghĩa vụ thông tin và hỗ trợ ở mức phát biểu. Ví dụ về mặt cấu trúc, khi câu hỏi có nhiều phần, hệ thống phải xem bằng chứng có bao phủ từng phần hay không. Đây là ví dụ về hợp đồng thông tin, không đưa ra hướng dẫn điều trị. Framework vì vậy đặt một cổng trước khi sinh để xét mức đủ bằng chứng và một cổng sau khi sinh để xét nội dung câu trả lời. Quyết định chấp nhận nội bộ vẫn cần đánh giá độc lập nếu muốn kết luận về chất lượng lâm sàng.',[CONTRACT,LEWIS,MEDRAG],'01:05')

# 03. Related work and the design gap, with native evidence table.
s=new('Cơ sở phương pháp và khoảng trống thiết kế','Tham chiếu: Lewis (2020); Asai (2024); Yan (2024); Min (2023)')
table(s,['Hướng tiếp cận','Cơ chế tham chiếu'],[
 ['RAG','Truy xuất để hỗ trợ sinh câu trả lời'],
 ['Self-RAG','Phản tư về truy xuất và nội dung sinh'],
 ['Corrective RAG','Đánh giá bằng chứng và truy xuất sửa lỗi'],
 ['FActScore','Đánh giá hỗ trợ ở mức phát biểu nguyên tử']
],45,124,[225,645],[43,54,54,54,54],20)
txt(s,'Khoảng trống đặt ra trong đề tài',45,405,870,32,25,BLUE,True)
txt(s,'Nối nghĩa vụ từ câu hỏi với PRE, kiểm chứng claim ở POST\nvà kiểm soát hành động bằng guard xác định.',45,445,870,52,21)
notes(s,'RAG cung cấp nền tảng truy xuất kết hợp sinh. Self-RAG cho thấy cách đưa phản tư vào quyết định truy xuất và sinh. Corrective RAG gợi ý đánh giá chất lượng bằng chứng và cơ chế truy xuất điều chỉnh. FActScore đặt trọng tâm vào từng phát biểu nguyên tử. Đề tài sử dụng các hướng này làm cơ sở thiết kế, rồi nối nghĩa vụ từ câu hỏi với kiểm tra bằng chứng trước khi sinh và hỗ trợ claim sau khi sinh. Phần bổ sung là hợp đồng kiểu dữ liệu và guard xác định cho hành động. Đây là mục tiêu thiết kế của nghiên cứu, chưa phải kết luận rằng hệ thống mới hơn hoặc tốt hơn những phương pháp đã công bố.',[CONTRACT,LEWIS,SELF,CRAG,FACT],'01:05')

# 04. Questions and expected contributions.
s=new('Câu hỏi nghiên cứu và đóng góp dự kiến','Nguồn: content contract §3 và §6; protocol e1-v2.refined-full-primary.v2')
for y,rq,contrast,body in [
 (127,'RQ1','A1 so với G','So sánh chất lượng quyết định dựa trên bằng chứng\ngiữa hai policy PRE đã hiện thực'),
 (236,'RQ2','A1 so với A0','Ảnh hưởng của việc hiển thị câu hỏi gốc tại PRE\nvới cùng Plan, E₀, instruction và schema'),
 (345,'RQ3','A0 so với G','So sánh hỗ trợ cho FULL PRE nguyên bản\ntrên cùng downstream v4')]:
    txt(s,rq,45,y,75,34,26,BLUE,True)
    txt(s,contrast,143,y,190,34,23,BLUE,True)
    txt(s,body,354,y,561,66,20)
    line(s,143,y+84,915,y+84,RULE,0.9)
txt(s,'Đóng góp dự kiến: hợp đồng benchmark, dual verification,\nguard xác định và protocol so sánh có thể tái lập.',45,454,870,48,19)
notes(s,'RQ1 là so sánh chính giữa A1 và G. Hai nhánh khác nhau theo cả gói policy PRE, gồm biểu diễn, readiness gating và cách tạo truy vấn bổ sung. Vì vậy không diễn giải thành tác động nhân quả của một thành phần riêng lẻ. RQ2 so sánh A1 và A0 để khảo sát việc hiển thị câu hỏi gốc tại PRE khi giữ cùng Plan, E0, instruction, schema và gating. Readiness là hành vi của controller, không phải độ chính xác lâm sàng. RQ3 giữ vai trò hỗ trợ giữa A0 và G. Các đóng góp dự kiến kết nối hợp đồng dữ liệu, kiến trúc kiểm chứng hai giai đoạn và kiểm soát hành động với protocol có thể kiểm toán. Tất cả vẫn là câu hỏi và đóng góp cần đánh giá.',[CONTRACT,EXP],'01:15')

# 05. Scientific framework derivative from Figure 01.
s=new('Khung nghiên cứu tổng thể','Phỏng theo Hình 01: research framework; content contract §4–6')
txt(s,'Nguồn guideline và benchmark được quản trị riêng',45,112,870,31,23,BLUE,True)
box(s,'5 nguồn guideline\n276 EvidenceUnits\n170 SemanticIntents',45,167,260,127,22)
box(s,'DV-OGEC-RAG\nPRE và POST\nHành động có guard',350,167,260,127,22)
box(s,'Đánh giá độc lập\nCần owner reference\nvà scorer đủ điều kiện',655,167,260,127,21,fill=PALE_RED,stroke=RED)
route(s,[(305,230),(350,230)])
route(s,[(610,230),(655,230)])
txt(s,'Chỉ trường runtime\ntrong allowlist',282,308,195,52,18,GRAY,align=2)
txt(s,'Dự đoán và\nprovenance',564,308,180,52,18,GRAY,align=2)
box(s,'Task B: bundle cố định\nTask C: truy xuất và evidence gating',45,386,565,74,21)
txt(s,'Gold / tham chiếu chuẩn\nngoài runtime',655,385,260,66,20,RED,True)
notes(s,'Sơ đồ này là bản trình bày native, rút gọn từ hình research framework đã xác minh. Bên trái là nguồn guideline và KOA-GuidelineBench với quy trình quản trị riêng. Ở giữa là phương pháp DV-OGEC-RAG, chỉ nhận các trường runtime nằm trong allowlist. Kết quả đi sang phía đánh giá độc lập cùng thông tin truy vết. Canonical obligations, đáp án tham chiếu và nhãn đánh giá không đi vào suy luận. Task B xét các bundle đã hiển thị cố định. Task C thực hiện truy xuất trên corpus rồi kiểm tra bằng chứng động. Hai task có hợp đồng khác nhau. Việc nối benchmark với runtime không chuyển quyền sở hữu hoặc quyền truy cập đối với tài sản evaluator của benchmark.',[CONTRACT,'assets/diagrams/01-research-framework.svg/.mmd; native editable derivative retaining runtime/evaluator separation.'],'01:10')

# 06. Native source registry table and exact task scope.
s=new('Corpus và hợp đồng tác vụ','Nguồn: content contract §4; KOA-GuidelineBench rc0.2.0 (internal review candidate)')
txt(s,'276 EvidenceUnits',45,111,365,33,27,BLUE,True)
txt(s,'170 SemanticIntents là metadata',430,115,485,30,21,GRAY)
table(s,['Nguồn','Phiên bản','EU','Ngôn ngữ','Registry scope'],[
 ['ACSQHC','2024','32','EN','CURRENT'],
 ['BYT Vietnam','2014','39','VI','HISTORICAL'],
 ['EULAR','2023 update / 2024','24','EN','CURRENT'],
 ['NICE NG226','2022','84','EN','CURRENT'],
 ['VA/DoD','2026','97','EN','CURRENT']
],45,156,[180,235,65,125,265],[36,35,35,35,35,35],18)
txt(s,'Task B',45,386,104,31,22,BLUE,True)
txt(s,'5 cặp sufficiency, 10 lượt bundle, 9 bundle riêng, 4 intents',162,386,753,54,20)
txt(s,'Task C',45,444,104,31,22,BLUE,True)
txt(s,'16 ca Recovery DEV tiếng Anh cho E1-v2',162,444,753,31,20)
notes(s,'Corpus rc0.2.0 gồm năm nguồn và 276 EvidenceUnits. Tổng số theo nguồn là 32, 39, 24, 84 và 97. Phiên bản EULAR là bản cập nhật 2023 công bố năm 2024. CURRENT và HISTORICAL chỉ mô tả frozen source registry, không phải đánh giá trực tiếp tính hiện hành của khuyến cáo y khoa hôm nay. Có 170 SemanticIntent metadata records, không phải 170 câu hỏi đã chấm. Task B gồm năm cặp, mười lượt xuất hiện bundle và chín bundle riêng thuộc bốn intents. Bốn intents này chỉ thuộc phạm vi Task B. Task C có 16 ca DEV tiếng Anh cho nghiên cứu E1-v2. Không cộng hai task thành 21 câu hỏi độc lập. rc0.2.0 hiện là internal review candidate, public_release=false.',[CONTRACT,'ACSQHC registry: https://www.safetyandquality.gov.au/resources/osteoarthritis-knee-clinical-care-standard-2024','BYT registry metadata: https://kcb.vn/van-ban/huong-dan-chan-doan-va-dieu-tri-cac-benh-co-xuong-khop.html','EULAR: https://doi.org/10.1136/ard-2023-225041','NICE: https://www.nice.org.uk/guidance/ng226/','VA/DoD frozen registry 2026: https://www.healthquality.va.gov/HEALTHQUALITY/guidelines/CD/OA/index.asp'],'01:15')

# 07. Exposure partition, derivative of Figure 04.
s=new('Ranh giới dữ liệu và chống rò rỉ đánh giá','Phỏng theo Hình 04: benchmark/evaluation boundary; BA1-D1 và BA1-D2')
txt(s,'Runtime chỉ nhận dữ liệu trong allowlist',45,113,870,34,25,BLUE,True)
xs=[45,345,645]
labels=['RUNTIME_VISIBLE','EVALUATOR_ONLY','REVIEWER_AUDIT_ONLY']
bodies=[
 'Câu hỏi và source scope\n\nEvidenceUnits hợp lệ\n\nCitation locators',
 'Canonical obligations\n\nReference answers\n\nGold dispositions',
 'Audit provenance\n\nIdentity và hashes\n\nDấu vết adjudication'
]
for i,(x,label,body) in enumerate(zip(xs,labels,bodies)):
    txt(s,label,x,177,270,31,18,BLUE if i==0 else RED,True)
    line(s,x,216,x+270,216,BLUE if i==0 else RED,1.6)
    txt(s,body,x,240,270,167,20)
txt(s,'Planner dự đoán MaterialObligation[] từ câu hỏi',45,438,870,34,25,BLUE,True)
notes(s,'BA1-D1 giữ canonical benchmark obligations ở ngoài runtime, còn BA1-D2 chia dữ liệu theo ba mức hiển thị. Cột runtime bao gồm câu hỏi, source scope, evidence hợp lệ và thông tin trích dẫn. Hai cột còn lại là các loại dữ liệu evaluator và audit, chỉ trình bày tên loại, không trình bày nội dung hạn chế. Planner phải dự đoán MaterialObligation từ chính văn bản câu hỏi. Cơ chế input allowlist loại gold và evaluator internals khỏi suy luận. Ngoài ra, nhãn sufficiency của Task B chỉ áp dụng cho bundle cố định của task đó. Không thể lấy nhãn này làm gold cho E0 hoặc E1 được truy xuất động trong E1-v2. Đánh giá độc lập cần một EvaluationContext được cấp quyền riêng.',[CONTRACT,'assets/diagrams/04-benchmark-evaluation-boundary.svg/.mmd; native editable derivative.'],'01:05')

# 08. Editable scientific architecture with both bounded feedback loops.
s=new('Kiến trúc DV-OGEC-RAG','Phỏng theo Hình 02 và 03; method baseline ac4ade7; nội dung rút gọn')
box(s,'Câu hỏi',45,125,150,75,22)
box(s,'Obligation\nPlanner',230,125,180,75,22)
box(s,'MedCPT + FAISS\nInitial ≤ 1',445,125,190,75,20)
box(s,'PRE gate\nFail sau recheck: ABSTAIN',670,125,245,75,18.5)
for a,b in [(195,230),(410,445),(635,670)]:route(s,[(a,162),(b,162)])
route(s,[(792,200),(792,220),(135,220),(135,329)])
txt(s,'READY',154,226,85,25,18,BLUE,True)
txt(s,'EvidenceMemory\nE₀ hoặc E₀ ∪ E₁ + provenance',255,245,375,65,20,GRAY)
box(s,'Nếu thiếu và còn lượt\nCorrective retrieval ≤ 1\nMerge và PRE kiểm lại',665,241,250,81,18)
route(s,[(915,148),(934,148),(934,282),(915,282)])
route(s,[(665,282),(646,282),(646,185),(670,185)])
box(s,'Generator',45,329,180,72,22)
box(s,'Claim\nDecomposer',270,329,180,72,20)
box(s,'Staged POST v4',495,329,180,72,20)
box(s,'POST gate + PolicyGuard\nACCEPT / ABSTAIN',720,329,195,84,18)
for a,b in [(225,270),(450,495),(675,720)]:route(s,[(a,365),(b,365)])
box(s,'Revision ≤ 1, chỉ memory hiện có\nDecompose và POST mới',270,420,405,55,18)
route(s,[(585,401),(585,420)])
route(s,[(270,447),(246,447),(246,365),(270,365)])
txt(s,'Mọi action có hiệu lực đều qua guard xác định. Lỗi kỹ thuật: FAILED_*',45,480,870,24,18,RED)
notes(s,'DV-OGEC-RAG viết đầy đủ là Dual-Verification Obligation-Guided Evidence-Controlled RAG. Planner nhận câu hỏi và tạo Plan có kiểu, sau đó đóng băng plan identity. Retrieval cục bộ lấy E0 với source filtering trước scoring và lưu provenance trong EvidenceMemory. PRE kiểm tra mức đủ bằng chứng. Nếu thiếu và còn ngân sách, controller cho truy xuất bổ sung tối đa một lần, hợp nhất memory rồi bắt buộc kiểm tra PRE lại. Chỉ PRE đạt mới cho Generator hoạt động. Candidate đi qua Claim Decomposer và staged POST v4. Nếu POST yêu cầu sửa và cho phép sửa, Reviser dùng memory hiện có, tối đa một lần. Hệ thống hủy claims và POST cũ, phân rã và kiểm tra lại. Mỗi hành động có hiệu lực đều qua control plane xác định. ACCEPT, ABSTAIN và FAILED là các loại kết thúc khác nhau, sẽ nói rõ ở slide sau.',[CONTRACT,ARCH,WORK,'Native editable derivative of verified Figures 02 and 03. Feedback bounds are upper limits, not mandatory steps.'],'01:40')

# 09. PRE reducer, mandatory correction recheck, and abstention.
s=new('PRE và vòng truy xuất bổ sung','Nguồn: workflow Steps 2–4; FULL readiness áp dụng cho A0/A1')
box(s,'PRE trên E₀',45,125,240,73,23)
box(s,'Readiness\nreducer',360,125,235,73,21)
box(s,'GENERATE',740,125,175,73,21)
route(s,[(285,161),(360,161)])
route(s,[(595,161),(740,161)])
txt(s,'READY',627,127,93,26,16,BLUE,True,align=2)
box(s,'Corrective retrieval ≤ 1\nQuery theo obligation/gap',360,266,235,75,18)
box(s,'PRE kiểm lại bắt buộc\ntrên E₀ ∪ E₁',670,266,245,75,20)
route(s,[(477,198),(477,266)])
txt(s,'INSUFFICIENT\nvà còn lượt',500,210,170,52,18,GRAY)
route(s,[(595,303),(670,303)])
box(s,'PRE gate',670,391,245,63,21)
box(s,'ABSTAIN',360,391,235,63,21,fill=PALE_AMBER,stroke=AMBER,color=AMBER)
route(s,[(792,341),(792,391)])
route(s,[(670,423),(595,423)],color=AMBER)
txt(s,'chưa đủ',597,432,76,26,16,AMBER,align=2)
route(s,[(915,423),(934,423),(934,161),(915,161)])
txt(s,'Điều kiện FULL',45,248,265,32,23,BLUE,True)
txt(s,'Tất cả obligations COVERED\nNguồn hợp lệ\n0 discrepancy chưa giải quyết',45,295,279,109,19)
txt(s,'Kể cả nghĩa vụ planner gắn optional',45,462,870,30,21,BLUE,True)
notes(s,'Với A0 và A1, PRE trả observation có cấu trúc theo từng obligation. Reducer xác định READY khi mọi nghĩa vụ được COVERED, nguồn hợp lệ và không còn discrepancy chưa giải quyết. Mọi nghĩa vụ trong Plan đều tham gia cổng FULL, kể cả nghĩa vụ planner gắn optional. G dùng boolean sufficiency và generic gaps theo hợp đồng riêng. Nếu chưa đủ và còn lượt, query builder xác định tạo truy vấn theo obligation cho A0/A1 hoặc theo gap cho G. Sau corrective retrieval, E1 hợp nhất vào E0 và PRE phải kiểm tra lại. Không có đường từ corrective retrieval bỏ qua recheck để vào Generator. Nếu cổng vẫn thiếu, controller xin phép ABSTAIN qua guard. Lỗi schema hoặc lỗi truy xuất đi sang FAILED, không tự đổi thành abstention.',[CONTRACT,WORK,'assets/diagrams/02-agentic-rag-architecture.svg/.mmd and 03-controller-state-machine.svg/.mmd, native PRE detail.'],'01:30')

# 10. POST with grounded revision and deterministic control.
s=new('POST, revision và PolicyGuard','Nguồn: staged POST v4; workflow Steps 5–8; Kamath et al. (2020)')
box(s,'Claim\nDecomposer',45,124,180,76,20)
box(s,'POST v4\npair, diagnosis, remedies',280,124,290,76,19)
route(s,[(225,162),(280,162)])
box(s,'Canonical POST gate\nClaims SUPPORTED\nObligations ADDRESSED\n0 hard failure',280,229,290,112,18.5)
route(s,[(425,200),(425,229)])
box(s,'Grounded revision ≤ 1\nChỉ memory hiện có, hủy claims/POST cũ',45,355,525,63,19)
route(s,[(280,273),(240,273),(240,355)])
txt(s,'NEEDS_REVISION\nvà có thể sửa',45,284,190,55,18,GRAY)
route(s,[(45,386),(25,386),(25,107),(135,107),(135,124)])
txt(s,'Control plane xác định',625,112,290,36,23,BLUE,True)
for y,lab in [(161,'ValidActionSet'),(216,'DeterministicRulesPolicy'),(271,'PolicyGuard'),(326,'ActionExecutor')]:
    txt(s,lab,625,y,290,35,21,BLUE,True,align=2)
    if y<326:route(s,[(770,y+35),(770,y+53)])
txt(s,'Mỗi action có hiệu lực\nđều cần guard cho phép',625,373,290,49,18,RED,True,align=2)
box(s,'ACCEPT\nCOMPLETED_ANSWER',45,433,280,64,18,fill=PALE_GREEN,stroke=GREEN,color=GREEN)
box(s,'ABSTAIN\nCOMPLETED_ABSTAIN',340,433,280,64,18,fill=PALE_AMBER,stroke=AMBER,color=AMBER)
box(s,'FAILED_*\nLỗi kỹ thuật',635,433,280,64,18,fill=PALE_RED,stroke=RED,color=RED)
notes(s,'Generator tạo candidate có citations phân giải được trong memory, rồi Decomposer tạo claims nguyên tử có kiểu. POST v4 có các bước pair, diagnosis và remedies, tiếp theo là canonical validation xác định. Cổng chấp nhận đòi hỏi mọi claim SUPPORTED, nghĩa vụ ADDRESSED, nguồn và provenance hợp lệ, không có hard failure. Khi NEEDS_REVISION và còn lượt sửa, Reviser chỉ dùng EvidenceMemory hiện có. Không truy xuất trong revision. Claims và POST cũ bị hủy, câu trả lời mới phải qua decomposition và POST mới. Control plane gồm ValidActionSet, deterministic RulesPolicy, PolicyGuard và Executor. Guard kiểm tra mọi action có hiệu lực, không chỉ ACCEPT. ACCEPT ánh xạ COMPLETED_ANSWER, ABSTAIN ánh xạ COMPLETED_ABSTAIN. Lỗi provider, schema, retrieval hoặc guard rejection là FAILED_*, tách khỏi abstention. Model confidence không được vượt hard guard.',[CONTRACT,WORK,SELECT,'Terminal mapping: ACCEPT=COMPLETED_ANSWER; ABSTAIN=COMPLETED_ABSTAIN; technical errors=FAILED_*. Guard rejection is FAILED_CONTRACT.'],'01:30')

# 11. Three arms as a native table, retaining G downstream Plan.
s=new('Thiết kế ba nhánh E1-v2','Nguồn: protocol e1-v2.refined-full-primary.v2; phỏng theo Hình 05')
txt(s,'16 câu hỏi × 3 replicates = 48 preparations\n48 preparations × 3 arms = 144 cells',45,105,870,51,19,BLUE,True)
table(s,['Nhánh','Đầu vào tại PRE','PRE và corrective retrieval'],[
 ['A0','Plan + E₀\nẨn câu hỏi gốc tại PRE','FULL theo từng obligation\nQuery theo obligation'],
 ['A1','Câu hỏi + cùng Plan + cùng E₀','Cùng instruction/schema/gating A0\nQuery theo obligation'],
 ['G','Câu hỏi + E₀ + public SourcePolicy\n+ prior gaps; không có Plan tại PRE','Generic sufficiency boolean\nQuery theo generic gaps']
],45,170,[85,440,345],[40,76,76,92],18)
txt(s,'Cả 3 nhánh nhận cùng Plan ở downstream: Generator, POST v4, revision và guard',45,464,870,38,18,BLUE,True)
notes(s,'Mỗi question-replicate block gọi Planner và initial retrieval một lần, khóa cùng Plan, E0 và source scope trước khi chia ba nhánh. A0 thấy Plan và E0 tại PRE nhưng không thấy câu hỏi gốc. A1 thêm câu hỏi gốc với cùng FULL instruction, schema và gating. G thấy câu hỏi, E0, public SourcePolicy và prior generic gaps, không nhận Plan ở PRE. Sau PRE, G nhận lại chính Plan chung cho generation, decomposition, POST, revision và guard. So sánh chính là A1 với G, ablation là A1 với A0, hỗ trợ là A0 với G. Protocol dùng sáu hoán vị thứ tự luân phiên, mỗi hoán vị tám block. Đây là counterbalancing xác định. Phân tích tổng hợp theo câu hỏi với replicates lồng bên trong, không coi 144 cells là 144 câu hỏi. A1/G là so sánh cả gói policy.',[CONTRACT,EXP,'Native table derived from assets/diagrams/05-experimental-arms.svg/.mmd. Planned comparisons remain unexecuted on real providers at admitted baseline.'],'01:40')

# 12. Implementation and reproducibility with native configuration table.
s=new('Triển khai và khả năng tái lập','Nguồn: architecture; experimental design; content contract §5–6')
txt(s,'Retrieval cục bộ đã pin',45,118,420,34,25,BLUE,True)
table(s,['Thuộc tính','Cấu hình'],[
 ['Encoders','MedCPT query / article'],
 ['FAISS','IndexFlatIP'],
 ['Kích thước','276 vectors × 768 chiều'],
 ['Runtime','float32 CPU, offline'],
 ['Truy xuất','top-k = 8, không reranker']
],45,169,[160,290],[38,42,42,42,42,42],18)
txt(s,'Hợp đồng và kiểm toán',545,118,370,34,25,BLUE,True)
txt(s,'Typed interfaces giữa các vai trò\n\nRunStore giữ identities và provenance\n\nBudget được giữ trước dispatch\n\nJev: tùy chọn, đang waitlist',545,172,370,253,21)
txt(s,'Cận trên: initial ≤ 1, corrective ≤ 1, revision ≤ 1\nTối đa 34 LLM requests / cell + 1 Planner chung / block',45,452,870,48,19,GRAY)
notes(s,'Retrieval chạy cục bộ với hai encoder MedCPT đã pin và FAISS IndexFlatIP. Index có 276 vectors, 768 chiều, float32 CPU, top-k bằng tám và không dùng reranker. Source filtering diễn ra trước scoring. Các vai trò giao tiếp qua contracts có kiểu, còn RunStore giữ version identities và provenance để tái lập. Budget được reserve trước request dispatch. Một cận trên của pipeline là 34 physical LLM requests mỗi arm cell, cộng một Planner request dùng chung mỗi block. Đây là trần accounting, không phải chi phí thông thường đã đo. Jev vẫn tùy chọn và waitlist, nằm ngoài integration và kết quả đủ điều kiện. Protocol dự kiến bootstrap question-cluster 20.000 lần, seed 401, nhưng chỉ cho qualified LIVE đủ gates. MOCK có contrasts và confidence intervals bằng null.',[CONTRACT,ARCH,EXP,MEDCPT,FAISS,'Planned bootstrap is not executed for this authoring task. No dependency installation or model/provider calls.'],'01:15')

# 13. Native results table, explicitly engineering only.
s=new('Kết quả kỹ thuật tại baseline ac4ade7','Tại baseline ac4ade7. Nguồn: aggregate receipts đã có, không chạy lại khi biên soạn')
txt(s,'Native MOCK qualification, 0 real-provider API calls',45,110,870,35,24,BLUE,True)
table(s,['Hạng mục','Kết quả baseline','Diễn giải'],[
 ['MOCK pilot','9/9 terminal cells\n3 shared preparations','Vận hành controller và retrieval'],
 ['MOCK full','144/144 terminal cells\n48 shared preparations','Kịch bản fake SDK xác định'],
 ['Critical tests','129/129 PASS\n0 fail / error / skip','Kiểm tra kỹ thuật có receipt'],
 ['Regression','PARTIAL: 103/109 modules\n1.400 PASS, 21 SKIP\n6 RESOURCE_BLOCKED','Composite inventory\nChưa hoàn tất full suite']
],45,157,[185,350,335],[38,53,53,53,78],18)
txt(s,'E1-v2 REAL PROVIDER: NOT_EXECUTED',45,446,870,27,22,RED,True)
txt(s,'Clinical quality: NOT_EVALUABLE, 0/16 items đủ điều kiện',45,477,870,25,20,RED,True)
notes(s,'Bảng là các receipt đã có tại baseline, không phải tests chạy lại khi làm slide. MOCK pilot hoàn tất chín trên chín cells với ba preparations. MOCK full hoàn tất 144 cells với 48 preparations. Fake SDK điều khiển nhánh correction và revision trên retrieval và controller thật. Counts đối xứng giữa các nhánh được script sẵn, không chứng minh ngang bằng hoặc ưu thế về y khoa. Critical selection có 129 trên 129 PASS, không fail, error hoặc skip. Regression là composite PARTIAL với 103 trên 109 modules, 1.400 PASS, 21 SKIP và sáu modules chưa chạy vì resource admission. SKIP không phải PASS. E1-v2 real provider vẫn NOT_EXECUTED. Clinical-quality scoring là NOT_EVALUABLE vì có 0 trên 16 public items đủ điều kiện, không phải độ chính xác 0 phần trăm. Không có biểu đồ chất lượng lâm sàng từ số test này.',[CONTRACT,RESULT,'closure-pilot-final.receipt.json; closure-parent-final.receipt.json; closure-critical-final.tests.json; regression-reconciled.json. These are existing baseline receipts, not rerun in artifact production.'],'01:35')

# 14. Limitations and the one next engineering milestone.
s=new('Giới hạn và bước tiếp theo','Nguồn: content contract §8–9; các bước LIVE/scoring cần gate riêng')
txt(s,'Giới hạn suy luận',45,121,415,34,26,BLUE,True)
txt(s,'16 ca DEV, lịch sử hiệu chỉnh DEV\n\nCó thể có intents hoặc ca liên quan\n\nGating phụ thuộc Plan dự đoán\n\nGiới hạn ngôn ngữ của MedCPT\n\nA1/G khác nhau theo cả gói policy',45,176,430,273,21)
line(s,500,121,500,464,RULE,1)
txt(s,'Milestone kỹ thuật kế tiếp',545,121,370,57,26,BLUE,True)
txt(s,'Hoàn tất 6 modules\nRESOURCE_BLOCKED\ntrên host đủ tài nguyên',545,193,370,104,25,INK,True)
txt(s,'Giữ kiểm tra version/baseline\nCommit headroom ≥ 3 GiB',545,321,370,66,20,GRAY)
txt(s,'Provider và LIVE cần gate riêng.\nOwner scoring trước kết luận so sánh.',545,420,370,69,19)
notes(s,'Thiết kế hiện có nhiều giới hạn: tập DEV nhỏ, đã có lịch sử hiệu chỉnh DEV, quan hệ giữa intents hoặc cases chưa cho phép khẳng định độc lập lâm sàng, gating chịu ảnh hưởng cách Planner dự đoán nghĩa vụ, và giới hạn ngôn ngữ của retrieval. So sánh A1/G còn gộp nhiều khác biệt trong policy. Milestone kỹ thuật kế tiếp đã xác định là hoàn thành sáu qualification modules bị resource-blocked trên host có ít nhất ba GiB Windows commit headroom, đồng thời giữ kiểm tra baseline và version. Các bước sau như provider và financial readiness, LIVE pilot, full E1-v2 và owner scoring là những gate riêng cần cấp quyền đúng phạm vi. Quyền biên soạn báo cáo hiện tại không tự kích hoạt chúng. License và khả năng redistribution guideline vẫn UNVERIFIED, nên bản công bố chỉ dùng metadata cùng aggregate đã làm sạch.',[CONTRACT,RESULT,'Six pending modules: test_e1_recovery; test_e1_rolling_accounting; test_e1_v2; test_e1_v2_release; test_i5_real_construction; test_koa_system.'],'01:15')

# 15. Conclusion without superiority claims.
s=new('Kết luận và trao đổi','Scientific baseline ac4ade7; E1-v2 real-provider execution và clinical scoring còn chờ')
txt(s,'Kiểm soát bằng chứng\ntrước và sau sinh câu trả lời',45,127,870,103,34,BLUE,True)
line(s,45,267,150,267,RED,3)
txt(s,'Framework có typed contracts và guard xác định',45,301,870,38,25)
txt(s,'Native MOCK xác nhận vận hành kỹ thuật',45,359,870,38,25)
txt(s,'RQ1–RQ3 cần thực thi và đánh giá độc lập',45,417,870,38,25)
txt(s,'Trao đổi',765,465,150,35,23,BLUE,True,align=3)
notes(s,'Kết quả giữa kỳ là framework có kiểu, hai cổng kiểm chứng, hai vòng phản hồi bị chặn số lần và control plane xác định, đi cùng protocol ba nhánh có thể kiểm toán. MOCK cho bằng chứng vận hành kỹ thuật và khả năng đi qua các nhánh. Các câu hỏi RQ1 đến RQ3 vẫn cần thực thi đủ điều kiện và đánh giá độc lập trước khi có kết luận về chất lượng. Điểm muốn trao đổi là độ phù hợp của nghĩa vụ do Planner dự đoán, ranh giới đánh giá snapshot bằng chứng động và cách xây dựng scoring context đủ quyền trong giai đoạn sau.',[CONTRACT,ARCH,WORK,EXP,RESULT],'00:35')

assert pres.Slides.Count == 15
pres.BuiltInDocumentProperties('Title').Value = 'KOA Agentic-RAG System — Báo cáo giữa kỳ nghiên cứu'
pres.BuiltInDocumentProperties('Author').Value = 'Phạm Hồng Đăng Khoa; Nguyễn Hoàng Khang'
pres.BuiltInDocumentProperties('Subject').Value = 'DV-OGEC-RAG; scientific baseline ac4ade7'
pres.BuiltInDocumentProperties('Keywords').Value = 'KOA, Agentic-RAG, TDTU-inspired, midterm, ac4ade7'
draft=BASE/'KOA_Midterm_Presentation_TDTU.pptx'
pres.SaveAs(str(draft),24)
# PowerPoint's own export is also the visual rendering source.
pdf=BASE/'KOA_Midterm_Presentation_TDTU.pdf'
pres.SaveAs(str(pdf),32)
for i in range(1,16):
    pres.Slides(i).Export(str(RENDERS/f'slide-{i:02d}.png'),'PNG',1600,900)

geometry=[]
for i in range(1,16):
    slide=pres.Slides(i)
    native_tables=0
    native_text=0
    shapes=[]
    for shape in slide.Shapes:
        record={'name':shape.Name,'type':shape.Type,'left':round(shape.Left,2),'top':round(shape.Top,2),'width':round(shape.Width,2),'height':round(shape.Height,2)}
        try:
            if shape.HasTable:
                native_tables+=1
                record['table']={'rows':shape.Table.Rows.Count,'columns':shape.Table.Columns.Count}
        except Exception:pass
        try:
            if shape.HasTextFrame and shape.TextFrame.HasText:
                native_text+=1
                record['text']=shape.TextFrame.TextRange.Text
                record['font_size']=shape.TextFrame.TextRange.Font.Size
                record['bound_width']=round(shape.TextFrame.TextRange.BoundWidth,2)
                record['bound_height']=round(shape.TextFrame.TextRange.BoundHeight,2)
                record['available_height']=round(shape.Height-shape.TextFrame.MarginTop-shape.TextFrame.MarginBottom,2)
        except Exception:pass
        shapes.append(record)
    geometry.append({'slide':i,'native_tables':native_tables,'native_text_shapes':native_text,'total_shapes':slide.Shapes.Count,'shapes':shapes})
(BUILD/'geometry.json').write_text(json.dumps(geometry,ensure_ascii=False,indent=2),encoding='utf-8')
(BUILD/'slide-content.json').write_text(json.dumps(SLIDE_RECORDS,ensure_ascii=False,indent=2),encoding='utf-8')
notes_md=['# Ghi chú thuyết trình giữa kỳ KOA Agentic-RAG System','',
'Ngôn ngữ: tiếng Việt. 15 slide. Thời lượng dự kiến: 18 phút 35 giây.',
'Scientific snapshot: `ac4ade796e56377882b8069d0fb7a14809e8180b`.',
'Scientific source SHA-256: `5aa87228b07ead1c4ecde48e7330e62771a86dbed7ac0fc4097f50152d306f5b`.',
'Integration SHA-256: `0155dc81df270dc5b6413ce6587aa52ed69e3cb7f415cd5146bf1188431ac927`.',
'Protocol: `e1-v2.refined-full-primary.v2`. Lock SHA-256: `98ad86c861986f3794d9b5818cafe44d396967340faf3631d6fb06d91006e5a3`.',
'Đây là tài liệu trình bày tiến độ tại baseline đã nêu, không phải kết quả thí nghiệm mới. Ngày biên soạn không thay đổi scientific snapshot.','']
for rec in SLIDE_RECORDS:
    notes_md += [f"## Slide {rec['number']:02d}. {rec['title']}",'',f"**Thời lượng gợi ý:** {rec['duration']}",'',rec['notes'],'','**Nguồn:**','']
    notes_md += ['- '+source for source in rec['sources']]
    notes_md += ['']
(BASE/'speaker-notes.md').write_text('\n'.join(notes_md),encoding='utf-8')
pres.Close()
# Re-open the generated package in native PowerPoint. Never touch unrelated open presentations.
app = win32com.client.DispatchEx('PowerPoint.Application')
opened=app.Presentations.Open(str(draft),-1,0,0)
open_check={'slide_count':opened.Slides.Count,'width_pt':opened.PageSetup.SlideWidth,'height_pt':opened.PageSetup.SlideHeight,'native_powerpoint_reopen':True,'prior_presentations_count':pre_existing_count}
opened.Close()
if pre_existing_count==0 and app.Presentations.Count==0:
    app.Quit()
(BUILD/'native-powerpoint-check.json').write_text(json.dumps(open_check,indent=2),encoding='utf-8')
print(json.dumps({'draft_pptx':str(draft),'draft_pdf':str(pdf),'notes':str(BASE/'speaker-notes.md'),'native_check':open_check},ensure_ascii=False))
