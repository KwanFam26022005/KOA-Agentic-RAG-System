META {"part":"summary"}
# TÓM TẮT NGHIÊN CỨU

KOA Agentic-RAG System nghiên cứu cách kiểm soát bằng chứng khi trả lời câu hỏi về hướng dẫn lâm sàng thoái hóa khớp gối. Vấn đề trung tâm là một đoạn văn có liên quan chưa bảo đảm bộ bằng chứng đủ để trả lời toàn bộ câu hỏi, và một câu trả lời có trích dẫn chưa bảo đảm mọi phát biểu đều được nguồn hỗ trợ. Nghiên cứu nối cấu trúc benchmark có quản trị độc lập với một phương pháp kiểm chứng trước và sau sinh câu trả lời.

Phương pháp DV-OGEC-RAG dự đoán các nghĩa vụ thông tin từ câu hỏi, truy xuất bằng MedCPT và FAISS, kiểm tra mức bao phủ trước sinh ở PRE, rồi phân rã câu trả lời thành phát biểu nguyên tử để kiểm chứng ở POST. Bộ điều khiển cho phép tối đa một lần truy xuất sửa thiếu và một lần sửa câu trả lời trên bộ nhớ hiện có. Mọi hành động đều qua chính sách quy tắc và PolicyGuard xác định; quan sát từ mô hình không tự cấp quyền hành động.

KOA-GuidelineBench rc0.2.0 là bản ứng viên rà soát nội bộ, gồm 276 EvidenceUnit từ năm nguồn và 170 hồ sơ SemanticIntent. Nghiên cứu E1-v2 sử dụng 16 trường hợp Task C DEV tiếng Anh, ba lần chuẩn bị cho mỗi câu hỏi và ba nhánh A0, A1, G. So sánh chính là A1 với G; đối chiếu A1 với A0 khảo sát khả năng nhìn thấy câu hỏi gốc tại PRE. Đây là thiết kế thăm dò đã định trước, chưa phải kết quả so sánh lâm sàng.

Ở baseline được tiếp nhận, pilot MOCK đạt 9/9 ô kết thúc và full MOCK đạt 144/144 ô kết thúc. Có 129/129 kiểm thử trọng yếu PASS. Hồi quy đối soát còn PARTIAL với sáu mô đun bị chặn tài nguyên. REAL PROVIDER E1-v2 chưa thực hiện; đánh giá chất lượng lâm sàng độc lập chưa đủ điều kiện, với 0/16 mục công khai đủ điều kiện chấm. Vì vậy, kết luận giữa kỳ là tính vận hành của cơ chế kiểm soát đã có bằng chứng kỹ thuật, còn hiệu quả khoa học vẫn cần thí nghiệm và tham chiếu độc lập. [P1–P4]

Từ khóa: thoái hóa khớp gối; RAG; nghĩa vụ thông tin; kiểm chứng kép; truy xuất sửa thiếu; từ chối trả lời có kiểm soát.

<!-- PAGE -->
META {"part":"toc","toc":true}

<!-- PAGE -->
META {"part":"lists"}
# DANH MỤC HÌNH VÀ BẢNG

## Danh mục hình

Hình 1.1 Khung nghiên cứu và các ranh giới suy luận ................................ 3

Hình 3.1 Benchmark và ranh giới đánh giá độc lập .................................. 11

Hình 4.1 Kiến trúc thực thi DV-OGEC-RAG ............................................ 12

Hình 4.2 Máy trạng thái và kiểm soát hành động .................................... 19

Hình 4.3 Chi tiết PRE và correction từ Hình 4.1 ....................................... 20

Hình 4.4 Chi tiết POST và revision từ Hình 4.1 ....................................... 21

Hình 5.1 Ba nhánh E1-v2 và chuẩn bị dùng chung ................................... 23

Hình C.1 Chi tiết PolicyGuard và đầu ra từ Hình 4.1 ................................ 36

## Danh mục bảng

Bảng 1.1 Câu hỏi nghiên cứu và cách diễn giải ........................................ 2

Bảng 2.1 Liên hệ giữa công trình nền và lựa chọn thiết kế ....................... 7

Bảng 3.1 Các nguồn trong registry đóng băng ......................................... 8

Bảng 3.2 Đơn vị đếm và phạm vi sử dụng .............................................. 10

Bảng 4.1 Hợp đồng trạng thái và điều kiện chấp nhận ............................ 18

Bảng 5.1 Bốn tầng chỉ số và điều kiện sử dụng ..................................... 25

Bảng 6.1 Bằng chứng qualification tại baseline .................................... 26

Bảng 7.1 Các mốc còn lại và điều kiện chuyển bước .............................. 29

Các hình được tái sử dụng từ bộ sơ đồ nghiên cứu 01–05 của dự án, giữ nguyên nội dung và tỉ lệ. Những trang chứa sơ đồ được trình bày ngang để đọc được luồng điều khiển. Danh mục trỏ đến số trang nội dung, bắt đầu từ Chương 1.

<!-- PAGE -->
META {"part":"abbreviations"}
# DANH MỤC TỪ VIẾT TẮT

| Thuật ngữ | Diễn giải trong báo cáo |
| KOA | Knee osteoarthritis, thoái hóa khớp gối |
| RAG | Retrieval-Augmented Generation, sinh tăng cường truy xuất |
| DV-OGEC-RAG | Dual-Verification Obligation-Guided Evidence-Controlled RAG |
| PRE | Kiểm tra mức đủ bằng chứng trước khi sinh câu trả lời |
| POST | Kiểm tra phát biểu và mức hoàn thành sau khi sinh |
| LLM | Large language model, mô hình ngôn ngữ lớn |
| DEV | Tập phát triển được dùng trong phạm vi nghiên cứu |
| MOCK | Chế độ kỹ thuật dùng SDK giả xác định |
| LIVE | Chế độ thực thi với nhà cung cấp mô hình thật |
| FAISS | Thư viện tìm kiếm tương tự trên biểu diễn véc tơ |
| E0, E1 | Bằng chứng truy xuất đầu và truy xuất sửa thiếu |
| A0, A1, G | Ba nhánh PRE trong giao thức E1-v2 |
| FAR | False Abstention Rate, cần tham chiếu độc lập để chấm |
| SHA-256 | Hàm băm dùng ràng buộc định danh và phiên bản |

Trong toàn báo cáo, ACCEPT chỉ quyết định chấp nhận của bộ điều khiển; ABSTAIN là kết thúc từ chối hợp lệ; FAILED_* là lỗi kỹ thuật. Ba nhóm này có ý nghĩa và mẫu số khác nhau. “CURRENT” và “HISTORICAL” mô tả registry đóng băng, không phải xác nhận tính cập nhật của tư vấn y khoa tại thời điểm đọc.

<!-- PAGE -->
META {"main":true,"page":1,"chapter":1}
# CHƯƠNG 1 GIỚI THIỆU NGHIÊN CỨU

## 1.1 Bài toán hỏi đáp theo hướng dẫn lâm sàng

Hỏi đáp theo hướng dẫn lâm sàng đòi hỏi trả lời đúng nhu cầu thông tin trong phạm vi nguồn đã xác định. Một câu hỏi có thể đồng thời chứa đối tượng áp dụng, điều kiện đi kèm, phạm vi khuyến nghị và yêu cầu so sánh giữa nguồn. Truy xuất một đoạn có từ khóa phù hợp chỉ cho thấy sự liên quan về văn bản. Hệ thống vẫn phải xác định đoạn đó có hỗ trợ các điều kiện quan trọng hay không và có đủ để hoàn thành câu trả lời hay không.

RAG kết hợp truy xuất tài liệu với sinh văn bản, tạo nền tảng để mô hình sử dụng tri thức ngoài tham số. Công trình của Lewis và cộng sự mô tả cách kết hợp bộ nhớ tham số và bộ nhớ phi tham số cho các tác vụ giàu tri thức [1]. Trong phạm vi báo cáo này, giá trị của RAG được xem xét ở khả năng gắn câu trả lời với nguồn cụ thể; khả năng đó chưa tự động xác lập sự đầy đủ hoặc tính đúng lâm sàng.

Nghiên cứu chọn hướng dẫn về thoái hóa khớp gối làm miền khảo sát để phát triển cơ chế kiểm soát bằng chứng. Hệ thống phục vụ nghiên cứu hỏi đáp trên tài liệu công khai và cấu trúc benchmark được quản trị. Nó không được định vị là công cụ chẩn đoán, kê đơn, xử lý cấp cứu hay thay thế bác sĩ. Báo cáo không đưa khuyến nghị điều trị cho một bệnh nhân cụ thể và không diễn giải kết quả kỹ thuật thành chứng cứ an toàn cho người bệnh.

## 1.2 Mục tiêu và phạm vi giữa kỳ

Mục tiêu là xây dựng và mô tả một cơ chế có thể kiểm toán: dự đoán những nội dung cần trả lời từ câu hỏi, kiểm tra bằng chứng trước sinh, kiểm chứng từng phát biểu sau sinh, rồi chỉ cho phép hành động khi các ràng buộc xác định đều đạt. Tên phương pháp là Dual-Verification Obligation-Guided Evidence-Controlled RAG, viết tắt DV-OGEC-RAG.

Phạm vi giữa kỳ gồm cấu trúc và quản trị KOA-GuidelineBench, phương pháp đã hiện thực, qualification ngoại tuyến và giao thức E1-v2 đã định trước. Snapshot khoa học được ràng buộc tại baseline ac4ade7; dữ liệu thực nghiệm mới hơn không được nhập vào kết luận. Kết quả trọng tâm là trạng thái triển khai có thể đối soát và các điều kiện còn thiếu trước đánh giá khoa học. [P1–P4]

<!-- PAGE -->
META {"main":true,"page":2,"chapter":1}
## 1.3 Câu hỏi nghiên cứu và giả thuyết

RQ1 xem xét liệu refined obligation-guided PRE ở A1 có cải thiện chất lượng quyết định dựa trên bằng chứng so với matched generic PRE ở G. Đây là giả thuyết về hai gói chính sách đã hiện thực. Hai nhánh khác nhau cả biểu diễn ở PRE, cách xác lập readiness và cách tạo truy vấn sửa thiếu. Vì thế, một chênh lệch quan sát được trong tương lai không thể quy riêng cho một thành phần nguyên tử.

RQ2 khảo sát ảnh hưởng của việc hiển thị câu hỏi gốc ở PRE. A1 nhận câu hỏi cùng Plan và E0; A0 chỉ nhận cùng Plan và E0. Hướng dẫn FULL, schema và quy tắc gating được giữ giống nhau. Đại lượng trực tiếp là readiness ban đầu. Nếu readiness thay đổi, kết quả mô tả hành vi kiểm tra bằng chứng của bộ điều khiển; muốn kết luận về độ đúng câu trả lời vẫn phải chấm tham chiếu độc lập.

@CAP Bảng 1.1 Câu hỏi nghiên cứu và cách diễn giải
| Câu hỏi | Đối chiếu | Vai trò và giới hạn |
| RQ1 | A1 so với G | So sánh chính giữa hai gói PRE; chất lượng cần chấm độc lập |
| RQ2 | A1 so với A0 | Ablation khả năng nhìn thấy câu hỏi gốc tại PRE |
| RQ3 | A0 so với G | So sánh hỗ trợ của FULL plan-only với generic trên cùng nền v4 |

## 1.4 Đóng góp dự kiến và giá trị kiểm chứng

Đóng góp thứ nhất là hợp đồng tác vụ và cơ chế phân lớp thông tin của benchmark, giúp xác định rõ đầu vào nào được phép xuất hiện khi suy luận. Đóng góp thứ hai là chuỗi kiểm chứng nghĩa vụ và phát biểu có kiểu dữ liệu đóng, kèm vòng phản hồi bị chặn số lần. Đóng góp thứ ba là phân tách chính sách đề xuất, guard cấp quyền và executor thực thi để các quan sát xác suất không bỏ qua ràng buộc cứng.

Giao thức ba nhánh tạo một cách so sánh có thể tái lập khi đủ điều kiện chạy thật và chấm điểm. Các đóng góp này hiện được trình bày như thiết kế và kết quả kỹ thuật. Báo cáo chưa xác lập tính mới vượt mọi công trình trước, ưu thế state-of-the-art, hiệu quả lâm sàng hay mức tiết kiệm chi phí. Việc ghi rõ ranh giới kết luận giúp người đọc biết mỗi loại bằng chứng có thể hỗ trợ nhận định nào. [P2–P4]

<!-- PAGE -->
META {"main":true,"page":3,"chapter":1,"landscape":true}
## 1.5 Khung nghiên cứu tổng thể

@FIG 01-research-framework.svg | Hình 1.1 Khung nghiên cứu và các ranh giới suy luận của KOA Agentic-RAG System

Benchmark quy định tác vụ và nguồn; runtime thực hiện phương pháp; đánh giá độc lập xác định chất lượng theo tham chiếu. Gold không đi vào Planner, PRE hay Generator. Qualification kỹ thuật và đánh giá khoa học có điều kiện nghiệm thu riêng. Nguồn: assets/diagrams/01-research-framework.svg và Mermaid cùng tên. [P1–P4]

<!-- PAGE -->
META {"main":true,"page":4,"chapter":2}
# CHƯƠNG 2 CƠ SỞ LÝ THUYẾT VÀ CÔNG TRÌNH LIÊN QUAN

## 2.1 Truy xuất và sinh tăng cường tri thức

Trong RAG, bộ truy xuất chọn một tập tài liệu hoặc đoạn văn liên quan để điều kiện hóa bộ sinh. Lewis và cộng sự kết hợp retriever với mô hình sinh cho các bài toán giàu tri thức [1]. Công trình cung cấp nền tảng cho việc tách tri thức tài liệu khỏi tham số mô hình. Tuy nhiên, mục tiêu của một hệ thống hỏi đáp theo nguồn còn bao gồm xác định nguồn nào có thẩm quyền và điều kiện nào của câu hỏi đã được bằng chứng hỗ trợ.

Có thể phân biệt ba quan hệ cần kiểm tra. Relevance là mức liên quan giữa truy vấn và đoạn truy xuất. Sufficiency là mức đủ của toàn bộ tập bằng chứng để đáp ứng nhu cầu thông tin. Support là quan hệ giữa một phát biểu trong câu trả lời và bằng chứng cụ thể. Một đoạn có relevance cao vẫn có thể thiếu điều kiện áp dụng. Một tập đủ nội dung vẫn có thể bị bộ sinh diễn đạt sai. DV-OGEC-RAG vì vậy đặt PRE và POST tại hai thời điểm khác nhau.

## 2.2 Biểu diễn y sinh và tìm kiếm véc tơ

MedCPT là mô hình truy xuất y sinh tiền huấn luyện tương phản từ nhật ký tìm kiếm PubMed quy mô lớn [6]. Trong hệ thống này, encoder truy vấn và encoder tài liệu được ghim phiên bản, chạy cục bộ ngoại tuyến. Chúng tạo biểu diễn để xếp hạng các EvidenceUnit. Báo cáo không suy ra từ kết quả công bố của MedCPT rằng retriever đã được xác nhận tối ưu trên kho guideline hoặc trên tiếng Việt.

FAISS cung cấp các cấu trúc và thuật toán tìm kiếm tương tự véc tơ; Johnson và cộng sự trình bày nền tảng tìm kiếm quy mô lớn bằng GPU [7]. Cấu hình đang khảo sát sử dụng IndexFlatIP trên CPU cho 276 véc tơ, không phải hệ thống tìm kiếm xấp xỉ hàng tỷ véc tơ. Cần tách khả năng của thư viện khỏi cấu hình thực tế được dùng.

Ở mức phương pháp, việc lọc nguồn trước xếp hạng bảo đảm tập ứng viên tuân thủ phạm vi nguồn khóa. Đây là một ràng buộc về tính hợp lệ của truy xuất. Nó không bảo đảm top-k đã chứa mọi bằng chứng cần thiết, nên bộ kiểm tra PRE vẫn cần hoạt động trên E0 đã nhận. [P2]

<!-- PAGE -->
META {"main":true,"page":5,"chapter":2}
## 2.3 Truy xuất phản hồi và tự kiểm tra

Self-RAG của Asai và cộng sự tích hợp khả năng truy xuất, sinh và tự phê bình qua các reflection token trong cơ chế học và suy luận của phương pháp [2]. Công trình gợi ra hướng liên kết quyết định sử dụng nguồn với việc đánh giá câu trả lời. Không nên đồng nhất toàn bộ cách học và biểu diễn của Self-RAG với một pipeline gọi nhiều vai trò LLM. DV-OGEC-RAG sử dụng hợp đồng quan sát có cấu trúc và bộ điều khiển xác định thay vì tuyên bố tái hiện cơ chế huấn luyện của Self-RAG.

Corrective RAG của Yan và cộng sự nghiên cứu cách đánh giá chất lượng tài liệu truy xuất và thực hiện hành động sửa phù hợp [3]. Bản được trích dẫn ở đây là preprint năm 2024. Liên hệ với nghiên cứu hiện tại nằm ở ý tưởng dùng đánh giá bằng chứng để điều kiện hóa bước thu nhận bổ sung. DV-OGEC-RAG ràng buộc bước này vào nghĩa vụ còn thiếu hoặc generic gaps và giới hạn tối đa một lần truy xuất sửa thiếu. Báo cáo không so sánh kết quả thực nghiệm với CRAG.

Hai hướng trên cho thấy kiểm soát sau truy xuất có thể được xem là một phần của chính sách suy luận. Nghiên cứu hiện tại cụ thể hóa chính sách bằng trạng thái có thể kiểm tra: nghĩa vụ nào còn thiếu, nguồn nào được phép dùng, ngân sách nào còn lại và điều kiện nào cần đạt trước khi sinh. Truy xuất bổ sung chỉ là một hành động có điều kiện, không phải chu trình mở để mô hình tìm kiếm đến khi tự thấy hài lòng.

## 2.4 Nghĩa vụ thông tin và mức hoàn thành

MaterialObligation trong DV-OGEC-RAG là dự đoán nội dung cần thiết từ câu hỏi. Nó không phải canonical obligation của benchmark. Việc tạo nghĩa vụ trước khi đọc bằng chứng giúp xác lập mục tiêu kiểm tra, nhưng vẫn phụ thuộc cách Planner diễn giải câu hỏi. Một kế hoạch thiếu nghĩa vụ có thể khiến kiểm tra sau đó bỏ sót nội dung; một kế hoạch quá rộng có thể làm tăng từ chối theo quy tắc all-obligation.

Do đó, “mọi nghĩa vụ đều được bao phủ” luôn phải đọc kèm “mọi nghĩa vụ do Planner dự đoán”. Đây là một điều kiện vận hành có thể kiểm toán, chưa phải chứng minh rằng mọi yêu cầu lâm sàng thật đã được nhận diện. Sự khác nhau này là một trong các giới hạn được giữ xuyên suốt thiết kế và đánh giá. [P2–P3]

<!-- PAGE -->
META {"main":true,"page":6,"chapter":2}
## 2.5 Kiểm chứng ở mức phát biểu nguyên tử

FActScore của Min và cộng sự phân rã văn bản dài thành các sự kiện nguyên tử để đánh giá độ chính xác thực tế theo nguồn [4]. Đơn vị nhỏ giúp tránh một phán quyết tổng quát che khuất phát biểu sai trong một đoạn nhìn chung hợp lý. Nghiên cứu hiện tại tiếp nhận nguyên tắc kiểm tra từng phát biểu, nhưng không tuyên bố FActScore đã được hiệu chuẩn cho guideline KOA hoặc đang cung cấp điểm chuẩn lâm sàng cho dự án.

Trong DV-OGEC-RAG, AtomicClaim có định danh riêng, nội dung, obligation_ids và citation_evidence_ids. Những liên kết này cho phép kiểm tra quan hệ giữa nội dung cần hoàn thành, phát biểu đã sinh và EvidenceMemory. POST v4 tiếp tục tách kiểm tra cặp claim–evidence, chẩn đoán vấn đề và đề xuất biện pháp sửa có căn cứ. Kiểm tra cấu trúc xác định bổ sung cho nhận định ngữ nghĩa của mô hình.

## 2.6 Từ chối trả lời và phạm vi đánh giá y khoa

Selective Question Answering under Domain Shift của Kamath và cộng sự xem xét việc lựa chọn trả lời hay từ chối khi phân bố thay đổi [5]. Công trình cho thấy selective QA là một bài toán đánh giá riêng. Với hệ thống hiện tại, ABSTAIN là một kết thúc hợp lệ khi bằng chứng hoặc câu trả lời không đạt gate. Tỷ lệ từ chối không tự cho biết lựa chọn đó có đúng với khả năng trả lời theo nguồn hay không.

Để đo false abstention, cần biết trường hợp nào có thể trả lời theo tham chiếu phù hợp. Dữ liệu controller chỉ ghi được hệ thống đã từ chối, đã sinh hay đã chấp nhận. Nó không cung cấp nhãn độc lập để quyết định từ chối đó là sai. Vì vậy, FAR thuộc tầng đánh giá chất lượng cần owner reference context; chưa thể ước lượng từ pass count của kiểm thử hoặc từ terminal status.

MIRAGE của Xiong và cộng sự cung cấp một khảo sát benchmark RAG cho y học [8]. Công trình làm cơ sở để đặt nghiên cứu trong lĩnh vực medical RAG. KOA-GuidelineBench có phạm vi hẹp hơn, tập trung hợp đồng sufficiency và recovery theo nguồn. Báo cáo không suy rộng các kết quả của benchmark khác thành hiệu quả của hệ thống KOA, và không biến các tập có cấu trúc khác nhau thành các đối chứng định lượng chưa thực hiện.

<!-- PAGE -->
META {"main":true,"page":7,"chapter":2}
## 2.7 Tổng hợp cơ sở lựa chọn thiết kế

Các công trình nền hỗ trợ từng khía cạnh của thiết kế. Chúng không đồng thời xác nhận tính đúng của một lần trả lời, mức đủ của bộ nhớ, quyền sử dụng nguồn và hợp lệ của hành động. Nghiên cứu tập trung làm rõ các mối nối đó bằng hợp đồng có kiểu và gate xác định, rồi chuẩn bị một phép so sánh có thể kiểm toán. [1–8]

@CAP Bảng 2.1 Liên hệ giữa công trình nền và lựa chọn thiết kế
| Công trình | Khía cạnh liên quan | Cách sử dụng trong nghiên cứu |
| RAG [1] | Sinh có truy xuất tài liệu | Nền tảng tách retriever và generator |
| Self-RAG [2] | Truy xuất và phản hồi | Bối cảnh cho suy luận có tự kiểm tra |
| CRAG [3] | Đánh giá rồi sửa truy xuất | Đặt correction sau quan sát thiếu bằng chứng |
| FActScore [4] | Đánh giá phát biểu nguyên tử | Phân rã câu trả lời trước POST |
| Selective QA [5] | Trả lời có lựa chọn | Phân biệt từ chối hợp lệ với lỗi và chất lượng |
| MedCPT [6], FAISS [7] | Truy xuất y sinh và véc tơ | Nền cục bộ có phiên bản xác định |
| MIRAGE [8] | Đánh giá medical RAG | Bối cảnh benchmark và giới hạn khái quát |

Điểm cần khảo sát là liệu kiểm tra trước sinh theo các nghĩa vụ dự đoán có thay đổi chất lượng quyết định khi giữ chung nền truy xuất và phần sau PRE. Đó là câu hỏi thực nghiệm, chưa được trả lời chỉ bằng việc ghép các thành phần. So sánh A1–G được giữ ở cấp gói chính sách, còn A1–A0 dành cho khả năng nhìn thấy câu hỏi.

Từ cơ sở này, benchmark phải tách đầu vào runtime khỏi nhãn đánh giá; phương pháp phải lưu liên kết từ câu hỏi đến nghĩa vụ và từ claim đến bằng chứng; thí nghiệm phải tách readiness khỏi độ đúng lâm sàng. Ba yêu cầu đó dẫn sang cấu trúc KOA-GuidelineBench và kiến trúc DV-OGEC-RAG ở các chương tiếp theo. Không có kết quả vượt trội so với tám công trình nền được khẳng định ở giai đoạn giữa kỳ.

<!-- PAGE -->
META {"main":true,"page":8,"chapter":3}
# CHƯƠNG 3 KOA GUIDELINEBENCH

## 3.1 Mục đích và phạm vi phiên bản

KOA-GuidelineBench rc0.2.0 phục vụ nghiên cứu mức đủ bằng chứng và truy xuất phục hồi theo hướng dẫn KOA. Trạng thái là ứng viên rà soát nội bộ, public_release = false. Kho công khai chỉ mô tả cấu trúc, số lượng, nguồn thư mục và định danh băm. Nó không phát hành toàn văn guideline, đoạn trích EvidenceUnit, nhãn chuẩn hay câu trả lời tham chiếu của chủ sở hữu. [P1]

Kho tri thức có 276 đơn vị truy xuất từ năm nguồn. Nguồn bao gồm bốn tài liệu tiếng Anh và một tài liệu tiếng Việt trong registry; bảng dưới dùng đúng năm và phạm vi của bản đóng băng. EULAR mang tên bản cập nhật 2023 nhưng bài báo được xuất bản năm 2024. Mốc 2026 của VA/DoD là định danh registry được dùng trong snapshot. [9–13]

@CAP Bảng 3.1 Các nguồn trong registry đóng băng
| Nguồn | Phiên bản | Ngôn ngữ | Phạm vi registry | Số unit |
| ACSQHC | 2024 | EN | CURRENT | 32 |
| Bộ Y tế | 2014 | VI | HISTORICAL | 39 |
| EULAR | Cập nhật 2023, xuất bản 2024 | EN | CURRENT | 24 |
| NICE NG226 | 2022 | EN | CURRENT | 84 |
| VA/DoD | 2026 | EN | CURRENT | 97 |
| Tổng | 5 nguồn | EN và VI | Theo registry | 276 |

CURRENT và HISTORICAL là nhãn phạm vi của registry, không thay thế đánh giá y khoa hiện hành. Khi một nguồn được khóa trong câu hỏi, retriever và guard phải tuân thủ khóa đó thay vì tự chọn guideline “mới hơn”. Tình trạng giấy phép và phân phối lại của năm nguồn vẫn là UNVERIFIED trong phạm vi được tiếp nhận. Do đó, báo cáo trình bày cấu trúc và metadata mà không tái tạo nội dung hạn chế.

<!-- PAGE -->
META {"main":true,"page":9,"chapter":3}
## 3.2 EvidenceUnit và chuỗi nguồn gốc

EvidenceUnit là đơn vị văn bản có định danh ổn định để truy xuất và trích dẫn. Một unit liên kết source reference với quotation selector, hash của phần trích, SHA-256 tài liệu gốc và locator theo trang, mục hoặc ngữ cảnh. Những trường này tạo đường đối soát từ bằng chứng được dùng trở về tài liệu và phiên bản cụ thể. Báo cáo chỉ mô tả cấu trúc, không chép quotation selector chứa nội dung guideline.

Định danh ổn định giải quyết một vấn đề khác với độ tương tự véc tơ. Retriever có thể xếp hạng một unit cao, nhưng runtime vẫn phải xác nhận source_id được phép, locator giải được và document hash khớp corpus đã ràng buộc. Nếu chỉ giữ nội dung văn bản mà mất provenance, một trích dẫn có thể trông hợp lý nhưng không còn gắn được với nguồn đã khóa. POST và PolicyGuard vì vậy sử dụng reference identity bên cạnh quan sát ngữ nghĩa.

## 3.3 SemanticIntent và nghĩa vụ do phương pháp dự đoán

Kho có 170 hồ sơ SemanticIntent để nhóm nhu cầu thông tin, biến thể câu hỏi và phạm vi nguồn. Đây là metadata cấp corpus, không phải 170 câu DEV đã có điểm chuẩn. Số hồ sơ intent, số trường hợp Task C và số cặp Task B mô tả các đơn vị khác nhau. Việc báo cáo riêng từng loại tránh phóng đại quy mô nghiên cứu.

Canonical obligation của benchmark được giữ ở lớp đánh giá. Runtime phải tự dự đoán MaterialObligation từ câu hỏi model-visible. Vì vậy, một obligation_id của phương pháp không phải khóa dùng để lấy một đáp án chuẩn bị sẵn. Sự tách biệt này làm phép kiểm tra có ý nghĩa: hệ thống cần tự xác định nội dung phải đáp ứng, còn người đánh giá độc lập có thể xem nó bỏ sót điều gì khi có quyền tham chiếu.

## 3.4 Định danh bản phát hành

Release manifest và corpus được ràng buộc bằng SHA-256. Hash giúp phát hiện khác biệt phiên bản hoặc nội dung; bản thân hash không chứng minh chất lượng lâm sàng hay quyền phân phối. Danh tính release, corpus và baseline đầy đủ được ghi trong phụ lục để người đọc phân biệt snapshot giữa kỳ với các thay đổi phát sinh sau đó.

Ở mỗi shared preparation, hệ thống cần giữ cùng định danh Plan, E0, nguồn khóa và substrate cho ba nhánh. Nếu một định danh thay đổi, đó là sai khác điều kiện thí nghiệm cần chặn hoặc điều tra. Đường provenance vì vậy vừa phục vụ kiểm toán tài liệu, vừa là điều kiện ghép cặp trong thiết kế E1-v2. [P1–P3]

<!-- PAGE -->
META {"main":true,"page":10,"chapter":3}
## 3.5 Tác vụ sufficiency và recovery

Task B đánh giá mức đủ của các displayed bundle cố định. DEV có năm cặp đối chiếu, mười lượt bundle xuất hiện nhưng chín bundle phân biệt, gắn với bốn semantic intent. Các cặp chung intent có thể phụ thuộc nhau. Đây không phải năm câu hỏi truy xuất mở độc lập; bundle được hiển thị là một phần của điều kiện đánh giá.

Task C đánh giá truy xuất và evidence gating từ corpus. E1-v2 sử dụng 16 trường hợp Recovery DEV tiếng Anh. Hệ thống nhận câu hỏi và phạm vi nguồn khóa rồi tạo E0, có thể thêm E1 nếu PRE chưa đủ. Bộ bằng chứng động thay đổi theo câu hỏi, replicate và correction của nhánh. Vì thế, nhãn Task B của một bundle cố định không phải gold sufficiency của E0 hoặc E0 hợp E1. [P1]

@CAP Bảng 3.2 Đơn vị đếm và phạm vi sử dụng
| Tài sản hoặc tác vụ | Số lượng | Ý nghĩa đúng |
| EvidenceUnit | 276 | Đơn vị có thể truy xuất |
| SemanticIntent | 170 | Hồ sơ metadata cấp corpus |
| Task B DEV | 5 cặp | Đối chiếu bundle cố định |
| Bundle Task B | 10 lượt, 9 phân biệt | Có một bundle lặp giữa hai cặp |
| Intent Task B | 4 | Chỉ mô tả các cặp Task B |
| Task C DEV | 16 trường hợp EN | Quần thể nghiên cứu E1-v2 |
| Mục đủ điều kiện chấm E1-v2 công khai | 0/16 | Thiếu điều kiện đánh giá độc lập |

Không cộng Task B và Task C thành 21 câu hỏi lâm sàng độc lập. Cũng không gán bốn intent của Task B cho toàn bộ Task C. Trong E1-v2, 16 câu hỏi là cụm tổng hợp thống kê; chưa có bằng chứng rằng chúng độc lập về mặt nội dung lâm sàng. Ba replicate lồng trong câu hỏi nhằm quan sát biến thiên của quy trình, không tạo thêm 48 câu hỏi mới.

Phân biệt tác vụ còn ảnh hưởng cách công bố. Một hệ thống có thể kiểm tra đúng bundle trong Task B mà chưa thu hồi được bằng chứng cần thiết ở Task C. Ngược lại, truy xuất có liên quan chưa cho phép tái sử dụng nhãn sufficient của một bộ hiển thị khác. Đánh giá cần gắn đúng đầu vào, snapshot và hợp đồng từng tác vụ.

<!-- PAGE -->
META {"main":true,"page":11,"chapter":3,"landscape":true}
## 3.6 Phân lớp thông tin và chống rò rỉ đánh giá

@FIG 04-benchmark-evaluation-boundary.svg | Hình 3.1 Benchmark và ranh giới đánh giá độc lập

BA1-D1 giữ canonical obligations ở EVALUATOR_ONLY; BA1-D2 tách runtime/, evaluator/ và audit_provenance/. Allowlist loại answer key trước dispatch. Ngữ cảnh chấm độc lập còn thiếu: 0/16 đủ điều kiện không có nghĩa 0% accuracy. Nguồn: assets/diagrams/04-benchmark-evaluation-boundary.svg và Mermaid cùng tên. [P1, P3]

<!-- PAGE -->
META {"main":true,"page":12,"chapter":4,"landscape":true}
# CHƯƠNG 4 PHƯƠNG PHÁP DV OGEC RAG

## 4.1 Kiến trúc kiểm chứng kép có điều khiển

@FIG 02-agentic-rag-architecture.svg | Hình 4.1 Kiến trúc thực thi DV-OGEC-RAG

PRE kiểm tra bằng chứng; POST kiểm tra câu trả lời. Hai vòng phản hồi có giới hạn và đều phải kiểm chứng lại. Các mục 4.2–4.16 cùng Hình 4.3–4.4 giải thích chi tiết. Nguồn: assets/diagrams/02-agentic-rag-architecture.svg. [P2]

<!-- PAGE -->
META {"main":true,"page":13,"chapter":4}
## 4.2 Planner chỉ nhìn câu hỏi

Obligation Planner nhận RuntimeQuestion gồm định danh và question_text, không nhận gold, canonical obligation hoặc bằng chứng truy xuất. Nó trả về Plan chứa MaterialObligation[]. Mỗi nghĩa vụ có định danh, mô tả yêu cầu và loại nghĩa vụ; các trường ràng buộc có thể mô tả nguồn, quần thể, thời gian hoặc qualifier. Cấu trúc đóng giúp phát hiện trường lạ và định danh trùng trước khi các bước sau sử dụng.

Plan phải hoàn chỉnh theo hợp đồng trước khi được chấp nhận. Runtime đóng băng plan_identity từ biểu diễn chuẩn hóa và kiểm tra lại trong chu trình. Nếu nội dung Plan thay đổi sau khi đóng băng, kết quả phải được coi là vi phạm hợp đồng. Không thể âm thầm bỏ một nghĩa vụ khó đáp ứng để làm PRE trở nên ready hoặc làm POST đạt coverage.

## 4.3 Ràng buộc nguồn và readiness toàn nghĩa vụ

Nguồn trong câu hỏi và source_constraint của nghĩa vụ được gắn xác định với registry qua AuthorityBinding. SourcePolicy xác lập những tài liệu được phép tham gia. Việc gắn nguồn thuộc control/runtime, không giao cho confidence của mô hình. Một mô hình tự tin rằng hai guideline tương đương không có quyền thay thế nguồn bị khóa bằng nguồn khác.

Trong chế độ FULL, mọi nghĩa vụ có trong Plan đều tham gia readiness, kể cả khi Planner đánh dấu required_for_completion = false. Quy tắc này cần được nêu rõ vì tên trường có thể khiến người đọc nghĩ một nghĩa vụ “optional” sẽ không chặn hoàn thành. Ở baseline, reducer không sử dụng cờ đó để miễn gate. Planner_confidence chỉ là telemetry và không thay đổi ngưỡng cấp quyền.

Lựa chọn all-obligation làm điều kiện vận hành rõ ràng: bất kỳ nghĩa vụ dự đoán nào chưa được đáp ứng đều ngăn ready. Mặt khác, readiness trở nên nhạy với độ đầy đủ và cách diễn đạt Plan. Nếu Planner tạo một nghĩa vụ quá rộng so với câu hỏi, hệ thống có thể từ chối dù người chấm thấy câu hỏi trả lời được. Nếu Planner bỏ sót qualifier, mọi nghĩa vụ dự đoán có thể đạt mà nhu cầu thật vẫn thiếu. Đây là lý do phải giữ evaluation độc lập với Plan của phương pháp.

Trong E1-v2, Plan dùng chung được tạo một lần cho mỗi block câu hỏi–replicate, rồi gắn với ba nhánh. Như vậy, khác biệt giữa A0, A1 và G không bắt đầu từ ba kế hoạch độc lập. G không nhìn Plan tại PRE nhưng vẫn nhận cùng Plan ở phần sinh và kiểm chứng phía sau. [P2–P3]

<!-- PAGE -->
META {"main":true,"page":14,"chapter":4}
## 4.4 Truy xuất ban đầu và EvidenceMemory

Nền truy xuất koa-frozen-medcpt-v1 dùng encoder truy vấn và encoder tài liệu MedCPT đã ghim phiên bản, chạy offline trên CPU ở float32. Chỉ mục FAISS IndexFlatIP có 276 véc tơ, mỗi véc tơ 768 chiều. Mỗi lượt truy xuất lấy top-k = 8 và không dùng reranker. Cấu hình cố định giúp kiểm soát điều kiện so sánh; báo cáo không khẳng định đây là cấu hình tối ưu cho mọi câu hỏi KOA. [6–7, P2]

Tập nguồn hợp lệ được lọc trước khi tính điểm. Cách này tránh trường hợp lấy top-k toàn kho rồi loại phần lớn kết quả vì sai nguồn, khiến bộ nhớ cuối phụ thuộc một quy trình lọc khác với phạm vi đã khóa. Dù vậy, số lượng kết quả và điểm tương tự vẫn chưa nói lên sufficiency. PRE phải đánh giá trực tiếp các bằng chứng được nhận dưới ràng buộc nghĩa vụ.

E0 được đưa vào EvidenceMemory cùng evidence_id, source reference, locator trang/mục, document hash và dấu vết lượt truy xuất. Bộ nhớ giữ các mục đã khử trùng lặp. Khi correction xảy ra, E1 được hợp vào E0 thay vì ghi đè âm thầm hoặc làm mất provenance của lượt đầu. Cặp bằng chứng trùng nội dung hoặc trùng định danh phải được xử lý theo hợp đồng để liên kết claim về sau vẫn giải được.

## 4.5 Ý nghĩa của bộ nhớ bằng chứng

EvidenceMemory là trạng thái được các vai trò downstream sử dụng. Generator có thể trích dẫn evidence_id trong bộ nhớ hợp lệ; POST có thể kiểm tra claim với member cụ thể; guard có thể kiểm tra phạm vi nguồn. Nếu chỉ chuyển một khối văn bản nối lại giữa các bước, những phép kiểm tra này khó xác định cùng một mục nguồn đang được nói đến hay một đoạn đã bị thay đổi.

Bộ nhớ không phải nhãn chuẩn. Một unit xuất hiện trong memory không có nghĩa nó hỗ trợ mọi claim được trích dẫn đến nó. Ngược lại, một unit không xuất hiện có thể là bằng chứng bị retriever bỏ lỡ. Hai khả năng đó được xử lý ở hai bước khác nhau: PRE xác định thiếu cho nhu cầu dự đoán và POST xác định quan hệ hỗ trợ cho nội dung đã sinh.

Giới hạn initial retrieval ≤ 1 và corrective retrieval ≤ 1 cho phép tối đa hai lượt thu nhận trong một arm cell. Đó là ranh giới thực thi, không phải kết luận rằng hai lượt luôn đủ. Khi bộ bằng chứng vẫn thiếu và không còn lượt correction, hệ thống phải đi đến từ chối hợp lệ theo gate thay vì mở rộng phạm vi nguồn hay ngân sách. [P2]

<!-- PAGE -->
META {"main":true,"page":15,"chapter":4}
## 4.6 PRE và truy xuất sửa thiếu

Ở A0 và A1, PRE trả về quan sát có cấu trúc cho từng nghĩa vụ. Tập obligation_id phải khớp một–một với Plan, và mọi evidence_id được viện dẫn phải giải được trong EvidenceMemory. Reducer xác định readiness khi tất cả nghĩa vụ đều COVERED, nguồn phù hợp và không còn discrepancy chưa giải quyết. Một nhận định “có vẻ đủ” của mô hình không thay thế được phép kết hợp các điều kiện này.

G dùng GenericPreState gồm boolean sufficient và missing_information. Nó nhận câu hỏi, E0, SourcePolicy công khai và generic gaps trước đó, không nhận Plan ở PRE. Đây là đối chứng có cùng nền truy xuất và phần downstream, nhưng khác gói chính sách PRE. Các khác biệt về schema, cách biểu diễn nguồn và lịch sử gaps phải được giữ trong diễn giải so sánh.

Nếu PRE chưa đủ và còn ngân sách, query builder xác định tạo truy vấn correction. A0/A1 nhắm các nghĩa vụ chưa được bao phủ; G nhắm generic gaps. Builder phải giữ ràng buộc nguồn và giới hạn truy vấn. Vi phạm hợp đồng hoặc chiều dài không được giải quyết bằng cắt bỏ âm thầm điều kiện quan trọng; đó là lỗi kỹ thuật cần ghi đúng loại.

Sau một lượt correction, E1 hợp vào E0 và PRE bắt buộc chạy lại trên memory mới. Có thêm tài liệu không đồng nghĩa đã đủ bằng chứng. Bộ điều khiển không cho đi tắt từ truy xuất bổ sung sang Generator. Khi recheck vẫn chưa đạt, PRE evidence gate cấp luồng từ chối hợp lệ, kết thúc COMPLETED_ABSTAIN mà không gọi Generator.

## 4.7 Phân biệt thông tin thiếu và lỗi vận hành

PRE insufficient là quan sát về bộ bằng chứng theo chính sách. FAILED_PROVIDER, FAILED_RETRIEVAL hoặc FAILED_CONTRACT là lỗi thực thi. Một JSON sai schema không phải bằng chứng rằng corpus thiếu nội dung. Tương tự, lỗi truy xuất không chứng minh một câu hỏi không thể trả lời. Việc giữ riêng các trạng thái này cho phép phân tích ở bước nào luồng bị chặn và tránh gán thất bại hạ tầng thành hành vi từ chối của phương pháp.

Trong bản MOCK, SDK giả được thiết kế để kích hoạt cả nhánh correction và revision, còn retriever/controller cục bộ thật được thực thi. Điều này kiểm tra đường chuyển trạng thái và ràng buộc, không chấm tính đúng của phán quyết sufficiency do mô hình thật tạo. Nguồn: đặc tả workflow và hợp đồng E1-v2 ở baseline. [P2–P4]

<!-- PAGE -->
META {"main":true,"page":16,"chapter":4}
## 4.8 Sinh câu trả lời có trích dẫn

Generator chỉ được gọi sau PRE gate đạt. Đầu vào bao gồm câu hỏi, Plan dùng chung, memory hợp lệ và trạng thái kiểm tra bằng chứng. Đầu ra AnswerObservation có answer_id, text và citation_evidence_ids. Runtime kiểm tra văn bản không rỗng và mọi trích dẫn thuộc memory. Như vậy, một tài liệu ngoài nguồn khóa hoặc một ID do mô hình tự tạo không thể trở thành trích dẫn hợp lệ chỉ bằng cách xuất hiện trong câu trả lời.

Kiểm tra ID là điều kiện cấu trúc. Nó không xác nhận văn bản đã diễn đạt đúng bằng chứng. Một claim có thể dẫn tới một EvidenceUnit có thật nhưng thêm điều kiện không có trong unit hoặc làm mất qualifier. POST cần xử lý quan hệ hỗ trợ ở mức phát biểu, thay vì chỉ xác nhận danh sách citation tồn tại.

## 4.9 Phân rã thành AtomicClaim

Claim Decomposer chuyển candidate answer thành tập AtomicClaim đóng. Mỗi claim chứa claim_id, text, obligation_ids và citation_evidence_ids. Claim ID phải duy nhất; tập claim không rỗng. Việc liên kết về nghĩa vụ giúp kiểm tra câu trả lời đã thực sự đáp ứng những mục nào của Plan. Việc liên kết về bằng chứng giúp POST kiểm tra đúng member, thay vì coi cả memory như một khối hỗ trợ chung.

Một câu ngữ pháp có thể chứa nhiều khẳng định; đơn vị kiểm chứng cần đủ nhỏ để phán quyết support có nghĩa. Nếu một phần được hỗ trợ và phần còn lại không rõ, gán một nhãn cho cả câu có thể che mất vấn đề. Khái niệm nguyên tử trong phương pháp nhằm làm rõ đơn vị này, có liên hệ với đánh giá sự kiện ở FActScore [4]. Tuy nhiên, độ đúng của chính phép phân rã vẫn là một giới hạn mô hình, không được bảo đảm chỉ bằng schema.

Tại bước này, câu trả lời vẫn là candidate. Generator và Decomposer đều tạo quan sát; không vai trò nào tự phát hành câu trả lời cuối. Trước ACCEPT còn có POST, kiểm tra canonical và PolicyGuard. Cách phân vai giúp xác định một lỗi là lỗi sinh nội dung, lỗi phân rã, lỗi nguồn hay vi phạm hợp đồng, thay vì gom mọi vấn đề vào một nhãn “answer wrong”.

Mọi nghĩa vụ trong Plan cần được tập claim bao phủ ở gate cuối. Điều này bổ sung cho support: các claim có thể đều có căn cứ nhưng tổng thể câu trả lời vẫn bỏ sót một yêu cầu. Ngược lại, câu trả lời có nhắc mọi nghĩa vụ nhưng một claim không được bằng chứng hỗ trợ vẫn không đủ điều kiện ACCEPT. [P2]

<!-- PAGE -->
META {"main":true,"page":17,"chapter":4}
## 4.10 POST theo ba giai đoạn

POST sử dụng hợp đồng e1.member-bound-staged-post.v4. Giai đoạn pair gắn claim với các member bằng chứng cụ thể theo wire binding do mã quản lý. Ý nghĩa của member-bound là phán quyết phải quy về thành viên và định danh đã ràng buộc, không chỉ một lời xác nhận tổng quát rằng “memory hỗ trợ”. Tham chiếu không giải được hoặc không đúng binding là vi phạm hợp đồng.

Giai đoạn diagnosis xác định vấn đề ngữ nghĩa, mâu thuẫn, vi phạm nguồn hoặc qualifier cần giữ. Các identity alias do code sở hữu giúp ánh xạ chẩn đoán về đúng đối tượng trong quan sát. Mô hình không có quyền tự đặt một alias khiến vấn đề của claim này được coi là đã giải quyết cho claim khác. Kiểm tra binding và alias không thay thế chẩn đoán ngữ nghĩa, nhưng ngăn một số sai lệch cấu trúc làm lệch verdict.

Giai đoạn remedies và coverage ghi mức hỗ trợ từng claim, mức đáp ứng toàn câu trả lời, các obligation chưa được xử lý và khả năng sửa. ClaimSupport gồm SUPPORTED, UNSUPPORTED, CONTRADICTED và UNCERTAIN. AnswerCoverage phân biệt ADDRESSED, PARTIALLY_ADDRESSED và UNADDRESSED. Các trạng thái này cho phép giữ lại uncertainty thay vì ép mọi phán đoán thành đúng hoặc sai.

## 4.11 Canonical validation và điều kiện đạt POST

Validator xác định kiểm tra số lượng và danh tính claim, reference bằng chứng, ràng buộc nguồn và cấu trúc quan sát. Trước ACCEPT, mọi claim phải SUPPORTED với evidence IDs không rỗng và giải được; answer coverage phải ADDRESSED; không còn nghĩa vụ chưa xử lý hoặc hard failure. Tập nghĩa vụ của Plan phải nằm trong tập nghĩa vụ được claim mapping bao phủ.

Một verdict PASS không được dùng khi canonical validation thất bại. Cũng không thể dùng điểm confidence cao để bỏ qua claim không hỗ trợ. Đây là ranh giới giữa nhận định mô hình và tính hợp lệ của trạng thái. Nếu phán quyết không đủ căn cứ hoặc còn thiếu nội dung, luồng có thể sửa hoặc từ chối theo điều kiện; nếu reference/schema sai, cần ghi lỗi kỹ thuật thay vì coi đó là một từ chối khoa học.

POST v4 tạo bằng chứng kiểm toán chi tiết hơn một phán quyết tổng thể. Tuy nhiên, sự chi tiết không tự xác lập độ đúng của verifier. Để đánh giá khả năng phát hiện unsupported claim, vẫn cần truth độc lập và ngữ cảnh chấm hợp lệ. Báo cáo không dùng số claim được controller đánh dấu SUPPORTED làm thay thế điểm chất lượng lâm sàng. [P2–P3]

<!-- PAGE -->
META {"main":true,"page":18,"chapter":4}
## 4.12 Sửa câu trả lời có căn cứ

Revision cần POST là NEEDS_REVISION, revision_possible đúng và còn ngân sách. Reviser dùng câu hỏi, Plan, memory, candidate cũ và diagnosis, không truy xuất thêm. Candidate sửa có answer_id mới và revision_of đúng; claims và POST cũ bị vô hiệu hóa. Decomposer và toàn bộ POST chạy lại. Nếu vẫn chưa đạt khi hết lượt, POST gate dẫn tới ABSTAIN.

@CAP Bảng 4.1 Hợp đồng trạng thái và điều kiện chấp nhận
| Đối tượng | Điều kiện kiểm tra | Ý nghĩa khi không đạt |
| Plan | Identity đóng băng, nghĩa vụ duy nhất | Sai hợp đồng, không sửa Plan để vượt gate |
| PRE | Mọi nghĩa vụ bao phủ, đúng nguồn, không discrepancy | Correction nếu còn lượt; nếu vẫn thiếu thì ABSTAIN |
| Answer và claim | ID hợp lệ, trích dẫn giải được | Lỗi hợp đồng hoặc cần chẩn đoán nội dung |
| POST | Support, coverage, zero hard failure | Revision có điều kiện hoặc ABSTAIN |
| Candidate sửa | ID mới, revision_of đúng, POST mới | Không tái dùng verdict cũ |
| ACCEPT | Toàn bộ gate và provenance hợp lệ | Guard không cấp quyền phát hành |

## 4.13 Ngân sách và khả năng kiểm toán

Mỗi arm cell có tối đa một initial retrieval, một corrective retrieval và một revision; trần 34 yêu cầu LLM vật lý, cộng một Planner request chung mỗi block. Đây là cận trên kế toán, không phải chi phí thường dùng đã đo. Guard kiểm tra ngân sách trước dispatch; reservation và usage được đối soát riêng, kể cả khi gián đoạn. MOCK không chứng minh chi phí hoặc độ trễ của provider thật. [P2–P4]

<!-- PAGE -->
META {"main":true,"page":19,"chapter":4,"landscape":true}
## 4.14 Chính sách xác định và ba trạng thái kết thúc

@FIG 03-controller-state-machine.svg | Hình 4.2 Máy trạng thái và kiểm soát hành động

ValidActionSet → DeterministicRulesPolicy → PolicyGuard → WorkflowActionExecutor. ACCEPT và ABSTAIN là hai kết thúc hợp lệ; lỗi provider, retrieval, schema hay guard thuộc FAILED_*. Jev còn waitlist, chưa thuộc tích hợp đã qualification. Nguồn: assets/diagrams/03-controller-state-machine.svg; chi tiết ở mục 4.6–4.13. [P2]

<!-- PAGE -->
META {"main":true,"page":20,"chapter":4,"landscape":true}
## 4.15 Chi tiết vòng truy xuất sửa thiếu

@DETAIL 02-agentic-rag-architecture.svg | 400,45,1040,343 | Hình 4.3 Chi tiết PRE và correction từ Hình 4.1

Vùng phóng to giữ nguyên nội dung nguồn và cho thấy hai điều kiện riêng: có lượt correction không đồng nghĩa ready, và PRE phải đọc lại memory đã hợp E1. Plan đã đóng băng không được lập lại để bỏ nghĩa vụ khó. Nếu vẫn chưa đủ sau lượt sửa thiếu, đường hợp lệ là ABSTAIN. Phần hành động và terminal nằm ngoài vùng cắt này được trình bày đầy đủ ở Hình 4.1–4.2.

<!-- PAGE -->
META {"main":true,"page":21,"chapter":4,"landscape":true}
## 4.16 Chi tiết vòng sửa và kiểm chứng lại

@DETAIL 02-agentic-rag-architecture.svg | 195,350,980,585 | Hình 4.4 Chi tiết POST và revision từ Hình 4.1

Vùng phóng to thể hiện chuỗi pair → diagnosis → remedies và vòng sửa có giới hạn. Reviser dùng memory hiện có, xóa claims cũ rồi đưa candidate mới qua phân rã và POST lại. Không có đường đi trực tiếp từ sửa câu sang ACCEPT; mọi kết quả tiếp tục qua POST gate và PolicyGuard. Các điều kiện typed/canonical cùng ba kết thúc được diễn giải ở mục 4.10–4.14.

<!-- PAGE -->
META {"main":true,"page":22,"chapter":5}
# CHƯƠNG 5 TRIỂN KHAI VÀ THIẾT KẾ E1 V2

## 5.1 Baseline triển khai và lưu vết

Snapshot khoa học của báo cáo gắn với Git baseline ac4ade796e56377882b8069d0fb7a14809e8180b. Các tài liệu công khai là bản diễn giải phục vụ nghiên cứu, không thay thế mã nguồn, giao thức khóa và aggregate receipts có định danh tương ứng. Trong đợt sản xuất báo cáo, không chạy thêm mô hình, scorer hay thực nghiệm lâm sàng. [P2–P4]

Runtime phân vai qua immutable typed contracts cho Plan, evidence, PRE, AnswerObservation, AtomicClaim và staged POST. Control plane không giao hành động trực tiếp cho LLM. RunStore tách mỗi chiến dịch vào một run directory, gắn manifest với phiên bản khoa học, tích hợp, protocol, cấu hình, model/index và định danh dữ liệu. Cell observations và tiến độ được lưu theo cơ chế append-only để đối soát đã thử, đã ghi và còn thiếu.

Ở biên provider, transport và schema là các điều kiện kỹ thuật riêng. Offline compatibility sử dụng fictional client để kiểm tra hình dạng đầu vào–đầu ra; nó không chứng minh một model alias thật đang sẵn có, credential hợp lệ hoặc chi phí được chấp thuận. Giao thức LIVE chỉ được mở sau khi các gate về nhà cung cấp và tài chính được đáp ứng đúng thẩm quyền.

## 5.2 Mục đích của E1-v2

Giao thức e1-v2.refined-full-primary.v2 là nghiên cứu thành phần thăm dò trên DEV đã có lịch sử tinh chỉnh. Nó định trước so sánh chính, chuẩn bị dùng chung, thứ tự dispatch và cách tổng hợp trước khi chạy E1-v2 với real provider trên nền POST v4. Việc có protocol lock không có nghĩa thí nghiệm đã được thực hiện hoặc kết quả đã được xác nhận.

Thiết kế gồm A0, A1 và G. A1–G là so sánh chính giữa hai gói PRE. A1–A0 khảo sát khả năng nhìn thấy câu hỏi gốc khi giữ cùng hướng dẫn FULL, schema và gating. A0–G là so sánh hỗ trợ. Những quan sát LIVE hai nhánh của thiết kế trước chỉ có thể làm bối cảnh lịch sử; chúng không được gộp với nghiên cứu ba nhánh v4 này.

Các trường định danh đầy đủ nằm trong phụ lục. Digest của public typed DEV assignment là hash của tập typed records, không phải hash thô của tệp mã dev_e1.py. Config identity liên quan config.yaml. Giữ đúng loại đối tượng băm là cần thiết để người khác có thể tái lập đối soát. [P3]

<!-- PAGE -->
META {"main":true,"page":23,"chapter":5,"landscape":true}
## 5.3 Ba nhánh và chuẩn bị dùng chung

@FIG 05-experimental-arms.svg | Hình 5.1 Ba nhánh E1-v2 và chuẩn bị dùng chung

A0 dùng Plan+E0; A1 thêm Question, giữ FULL schema/gating; G dùng Question+E0 với generic PRE. Mỗi block dùng chung một Plan và E0; cả ba nhánh dùng cùng downstream. Chuẩn bị chung không xác lập độc lập lâm sàng giữa các ô. Nguồn: assets/diagrams/05-experimental-arms.svg; định nghĩa chi tiết ở mục 5.2 và 5.4. [P3]

<!-- PAGE -->
META {"main":true,"page":24,"chapter":5}
## 5.4 Replicate và thứ tự thực thi

Mười sáu câu hỏi Task C DEV, mỗi câu ba replicate, tạo 48 shared preparations. Ba nhánh cho mỗi preparation tạo 144 planned arm cells. Một cell là một lần thực thi của một nhánh trong một block, không phải một câu hỏi mới. Việc đếm 144 phải luôn gắn với “ô nhánh”, tránh nhầm thành kích thước mẫu lâm sàng.

Sáu hoán vị thứ tự A0, A1 và G được xoay vòng xác định, mỗi hoán vị xuất hiện tám lần trong 48 block. Cách này là counterbalancing xác định. Nó không phải phân nhóm ngẫu nhiên độc lập hay block randomization. Planned order và actual order cần được lưu để phát hiện sai khác thực thi.

## 5.5 Đại lượng readiness đã đăng ký

Với hai nhánh X và Y, lấy chênh lệch readiness nhị phân ban đầu trong cùng câu hỏi và replicate. Trung bình ba chênh lệch cho mỗi câu, sau đó trung bình trên 16 câu. Cách tổng hợp tôn trọng replicate lồng trong câu hỏi và phản ánh matched preparation. [P3]

@FORMULA d(q) = (1/3) Σr [I(initial_PRE_ready(q,r,X)) − I(initial_PRE_ready(q,r,Y))]
@FORMULA Δready(X,Y) = (1/16) Σq d(q)

Đây là đại lượng hành vi của controller. Một giá trị dương, nếu được quan sát trong điều kiện hợp lệ, cho biết nhánh X ready thường hơn trên E0 dùng chung; chưa nói nhánh đó đúng hơn hay ít false abstention hơn. Readiness tăng có thể đi cùng việc đánh giá đủ rộng hoặc bỏ sót thiếu sót; phân biệt các khả năng đó cần tham chiếu độc lập.

Giao thức dự kiến bootstrap ghép cặp theo cụm câu hỏi với 20.000 lần lấy mẫu lại, seed 401 và khoảng percentile 95%. Chỉ tính trong qualified LIVE khi đủ cả ba gate của 16 câu cho hai nhánh được đối chiếu. Báo cáo này không chạy bootstrap; MOCK contrasts và CI vẫn null. Cụm câu hỏi là đơn vị tổng hợp được chọn, không phải khẳng định đã chứng minh độc lập lâm sàng giữa 16 trường hợp.

Quy mô DEV nhỏ và có lịch sử tinh chỉnh khiến mọi phân tích tương lai cần được diễn giải thăm dò. Không dùng số replicate hay tính cân bằng thứ tự để che giới hạn của tập câu hỏi. Những kết luận khái quát hơn cần một thiết kế đánh giá ngoài phạm vi giữa kỳ được cấp quyền riêng.

<!-- PAGE -->
META {"main":true,"page":25,"chapter":5}
## 5.6 Hệ chỉ số và xử lý thiếu dữ liệu

@CAP Bảng 5.1 Bốn tầng chỉ số và điều kiện sử dụng
| Tầng | Đại lượng tiêu biểu | Điều kiện diễn giải |
| 1 Chất lượng độc lập | Độ đúng câu trả lời, support, completeness, FAR | Owner reference context và scorer đủ điều kiện |
| 2 Hành vi controller | Initial/final PRE readiness, correction, revision, ACCEPT, ABSTAIN | Quan sát hành vi; không thay accuracy |
| 3 Chẩn đoán | Chuyển INSUFFICIENT sang READY, lỗi theo giai đoạn | Giải thích luồng và điểm thất bại |
| 4 Kỹ thuật và kế toán | Cell inventory, request, token, reservation, chi phí, thời gian | Gắn chế độ và phạm vi thực thi |

Chất lượng cần tham chiếu độc lập cho chính điều kiện động của E1-v2. Các nhãn của displayed bundle Task B không lấp được thiếu hụt đó. Khi chưa có reference-scoring eligibility, scalar quality estimate và khoảng tin cậy chất lượng phải để null hoặc ghi chưa thể đánh giá. 0/16 đủ điều kiện không tạo một mẫu số accuracy bằng 16.

Mọi cell dự kiến cần có trạng thái tồn kho: đã thử, đã ghi, hợp lệ, lỗi hoặc chưa thử. Missing và UNATTEMPTED giữ nguyên là thiếu. Không chuyển một cell chưa chạy thành ABSTAIN, không coi lỗi provider là câu trả lời âm, và không impute một gate còn thiếu để làm tròn mẫu đối chiếu. Nếu điều kiện complete gates không đạt, không xuất contrast hoặc bootstrap CI đã đăng ký.

## 5.7 Điều kiện phân tích và công bố

Khi có LIVE hợp lệ trong tương lai, báo cáo phải phân biệt initial readiness trên cùng E0 với final readiness sau correction. Chỉ số sau correction bao gồm ảnh hưởng của truy vấn sửa thiếu theo chính sách từng nhánh. Vì vậy, chúng trả lời câu hỏi khác với ablation hiển thị câu hỏi trên đầu vào ban đầu.

Kế toán cũng cần giữ riêng physical request, token, reservation và settled cost. Trần 34 request mỗi arm cell không thể dùng làm giá trung bình. Telemetry MOCK không phải độ trễ provider thật. Mọi bảng kết quả cần kèm chế độ, protocol identity và mẫu số đúng. Quy tắc này cho phép phân tích kỹ thuật mà không vô tình nâng các tầng 2–4 thành kết luận lâm sàng. [P3–P4]

<!-- PAGE -->
META {"main":true,"page":26,"chapter":6}
# CHƯƠNG 6 TIẾN ĐỘ VÀ BẰNG CHỨNG ĐÃ XÁC MINH

## 6.1 Qualification kỹ thuật tại baseline

Các số liệu dưới đây là aggregate receipts đã có tại baseline ac4ade7 và đã được đối soát cho tài liệu giữa kỳ. Chúng không phải kiểm thử chạy lại trong quá trình dựng DOCX/PDF. Định danh khoa học, tích hợp và protocol trong receipts khớp snapshot được tiếp nhận. Các lượt gọi nhà cung cấp thật trong những receipts MOCK này bằng không. [P4]

@CAP Bảng 6.1 Bằng chứng qualification tại baseline
| Phạm vi | Kết quả đã ghi nhận | Giới hạn diễn giải |
| Native MOCK pilot | 9/9 terminal cells; 3 shared preparations | Qualification đường chạy nhỏ |
| Native MOCK full | 144/144 terminal cells; 48 shared preparations | Đủ ô theo kế hoạch MOCK |
| Critical tests | 129/129 PASS; 0 fail/error/skip | Bằng chứng kiểm thử trọng yếu |
| Regression đối soát | PARTIAL; 103/109 mô đun; 1.400 PASS; 21 SKIP; 6 RESOURCE_BLOCKED | Thực thi tổng hợp, không phải full-suite hoàn tất |
| Provider schemas | 14/14 QUALIFIED_OFFLINE | Fictional client, chưa xác nhận provider thật |

SDK giả xác định kích hoạt nhánh correction và revision trên controller và retriever cục bộ thật. Vì vậy, qualification có giá trị đối với việc nối các thành phần, giới hạn vòng lặp, reference binding và trạng thái kết thúc. Các phân bố kết quả giữa nhánh do kịch bản giả điều khiển; chúng không chứng minh ba chính sách tương đương, một nhánh chính xác hơn hoặc không còn rủi ro lâm sàng.

Critical tests có zero fail/error/skip trong receipt riêng. Regression đối soát có 21 SKIP và sáu mô đun bị chặn tài nguyên; SKIP không được tính thành PASS. Dữ liệu regression đến từ composite execution, không nên viết “toàn bộ test suite đã pass”. Việc giữ đúng mức qualification là điều kiện để xác định công việc kỹ thuật tiếp theo thay vì đóng nghiên cứu sớm.

<!-- PAGE -->
META {"main":true,"page":27,"chapter":6}
## 6.2 Những phần đã hoàn thành

Ở baseline được tiếp nhận, cấu trúc và governance benchmark đã được mô tả; runtime nghĩa vụ, PRE, correction, Generator, Decomposer, POST v4 và revision đã được nối với controller có guard. Giao thức ba nhánh đã định trước so sánh và điều kiện tổng hợp. RunStore cùng định danh nguồn, tích hợp và protocol hỗ trợ đối soát lại các aggregate receipts. Bộ tài liệu và sơ đồ nghiên cứu giải thích các ranh giới này bằng hiện vật có thể rà soát. [P1–P4]

Tính “agentic” trong phạm vi kỹ thuật được thể hiện qua Plan chứa subgoals, bộ nhớ thay đổi theo truy xuất, hành động correction phụ thuộc trạng thái và phản hồi diagnosis dẫn đến revision. Các hành động có giới hạn và đều chịu guard. Nó không có nghĩa hệ thống được tự trị trong thực hành y khoa hoặc có quyền tự quyết định ngoài nhiệm vụ hỏi đáp theo nguồn.

## 6.3 Những kết luận khoa học còn chờ

Tại baseline ac4ade7, E1-v2 REAL PROVIDER là NOT_EXECUTED. Independent clinical-quality scoring là NOT_EVALUABLE; có 0/16 mục công khai đủ điều kiện chấm theo hợp đồng. Chưa có bằng chứng A1 tốt hơn G hoặc A0 về độ đúng lâm sàng. Cũng chưa có xác nhận về hiệu quả người bệnh, an toàn ứng dụng, tiết kiệm chi phí hoặc tính nhất quán song ngữ.

Trạng thái chưa thể chấm không phải một kết quả xấu của mô hình. Nó mô tả giới hạn thẩm quyền và khả năng quy chiếu: thiếu owner-referenced dynamic sufficiency, truth của answer/claim và ngữ cảnh chấm ba nhánh phù hợp. Tạo một scorer tự động từ chính outputs rồi gọi đó là independent gold sẽ làm mất ý nghĩa của evaluation boundary.

Một ACCEPT ở MOCK chứng minh nhánh kịch bản đi qua gate hợp lệ theo điều kiện được thiết lập. Một ACCEPT ở LIVE, nếu có trong tương lai, vẫn chỉ là controller acceptance cho đến khi được chấm độc lập. Cách dùng thuật ngữ nhất quán này ngăn số terminal cells bị hiểu thành số câu đúng.

## 6.4 Tiến độ không quy đổi thành phần trăm

Báo cáo không gán phần trăm hoàn thành chung cho cả kỹ thuật và khoa học. Hai loại công việc có gate khác nhau, nên tổng hợp thành một tỷ lệ dễ che điều kiện còn thiếu. Tiến độ được trình bày bằng hạng mục hoàn thành, bằng chứng tương ứng và mốc kế tiếp đủ điều kiện. Ngày sản xuất tài liệu không phải ngày chạy thí nghiệm và không cập nhật scientific snapshot.

<!-- PAGE -->
META {"main":true,"page":28,"chapter":6}
## 6.5 Nguy cơ đối với tính hợp lệ

Giới hạn đầu tiên là tập DEV nhỏ và có lịch sử dùng để tinh chỉnh. Những thay đổi sau quan sát trên cùng DEV có thể làm kết quả tương lai phụ thuộc các trường hợp đã biết. Ba replicate không sửa được giới hạn phạm vi câu hỏi. Counterbalancing thứ tự cũng không tạo thêm tính đại diện hoặc chứng minh độc lập lâm sàng giữa các case.

Giới hạn thứ hai nằm ở Planner và chính sách FULL. All-obligation gating phụ thuộc nghĩa vụ dự đoán; sai lệch của Planner có thể ảnh hưởng cả PRE lẫn tiêu chí hoàn thành POST. A1 và G còn khác nhau nhiều yếu tố gói chính sách. Nếu xuất hiện chênh lệch, phân tích không được quy riêng cho việc có Plan mà bỏ qua query builder, schema hoặc biểu diễn lịch sử.

Giới hạn thứ ba là nền truy xuất. Encoder y sinh và kho guideline nhỏ có miền và ngôn ngữ khác với nhiều bối cảnh y khoa thực tế. E1-v2 dùng 16 câu tiếng Anh; sự hiện diện của 39 EvidenceUnit tiếng Việt không đủ xác lập năng lực hỏi đáp song ngữ. Không có phép thử song ngữ được suy ra từ số lượng nguồn hoặc cấu trúc SemanticIntent.

## 6.6 Quyền truy cập và giới hạn công bố

Giấy phép và trạng thái phân phối lại guideline còn UNVERIFIED trong snapshot. Báo cáo vì vậy chỉ công bố metadata, số đếm và aggregate đã làm sạch. Nó không chứa toàn văn guideline, evidence quotations, owner reference answers, canonical obligations, private runtime source hoặc raw traces. Có thể mô tả đường provenance mà không tái phân phối nội dung nguồn.

Đầu vào không chứa dữ liệu bệnh nhân thật. Đánh giá nghiên cứu theo nguồn không được chuyển thành khuyến nghị xử trí trường hợp cá nhân. Kết quả kỹ thuật cần được sử dụng trong đúng phạm vi nhiệm vụ, nhất là khi thuật ngữ “clinical guidelines” xuất hiện trong tên dự án. Tên miền nghiên cứu không đồng nghĩa sự chấp thuận sử dụng lâm sàng.

Jev còn waitlist và là adapter tùy chọn. Các receipts đủ điều kiện dùng DeterministicRulesPolicy. Khả năng tích hợp tương lai không được tính vào tiến độ đã xác minh. Bằng cách ghi riêng giới hạn dữ liệu, mô hình, thiết kế và quyền truy cập, báo cáo giữ được một đường rõ ràng từ kết quả hiện có đến những gì vẫn cần kiểm tra. [P1–P4]

<!-- PAGE -->
META {"main":true,"page":29,"chapter":7}
# CHƯƠNG 7 KẾ HOẠCH CÒN LẠI THEO ĐIỀU KIỆN

## 7.1 Mốc kỹ thuật kế tiếp

Mốc kỹ thuật kế tiếp duy nhất là hoàn thành sáu mô đun qualification native đang RESOURCE_BLOCKED trên host đủ tài nguyên, đồng thời giữ kiểm tra baseline và version identities. Các mô đun gồm test_e1_recovery, test_e1_rolling_accounting, test_e1_v2, test_e1_v2_release, test_i5_real_construction và test_koa_system. Admission guard ở baseline yêu cầu ít nhất 3 GiB Windows commit headroom khả dụng. [P4]

Mốc này giải quyết độ bao phủ qualification còn thiếu, không kích hoạt mô hình trả phí hoặc tự tạo kết luận khoa học. Điều kiện hoàn thành là có kết quả từng mô đun cùng receipt đúng snapshot và phân loại rõ PASS, SKIP, lỗi hay tiếp tục bị chặn. Nếu môi trường chưa đủ, giữ trạng thái tài nguyên thay vì diễn giải thành lỗi thuật toán.

@CAP Bảng 7.1 Các mốc còn lại và điều kiện chuyển bước
| Mốc | Điều kiện trước bước | Sản phẩm để rà soát |
| Hoàn tất 6 mô đun native | Host đủ tài nguyên, version khớp | Receipt và đối soát qualification |
| Sẵn sàng provider và tài chính | Alias/transport hợp lệ, ngân sách được cấp quyền | Hồ sơ readiness, chưa phải kết quả chất lượng |
| LIVE pilot riêng | Có ủy quyền thí nghiệm và gate đạt | RunStore và inventory pilot hợp lệ |
| Full E1-v2 | Pilot đủ điều kiện, kế hoạch khóa | 144 ô dự kiến được đối soát trạng thái |
| Chấm độc lập | Owner scoring context ba nhánh đủ điều kiện | Điểm và provenance đánh giá |
| Phân tích khoa học | Dữ liệu và missingness đáp ứng protocol | So sánh, ablation, lỗi và giới hạn |

Các bước sau là công việc tương lai có điều kiện, không được xem là đã phê duyệt thực thi chỉ vì được liệt kê trong báo cáo. Không gán thời hạn tùy đoán hoặc tỷ lệ tiến độ chưa đo. Việc chuyển gate cần bằng chứng phù hợp với đúng loại thẩm quyền: kỹ thuật, tài chính, dữ liệu và khoa học.

<!-- PAGE -->
META {"main":true,"page":30,"chapter":7}
## 7.2 Điều kiện cho thí nghiệm và đánh giá

Provider readiness cần xác nhận model alias, transport, schema và điều kiện tài chính bằng quy trình được cho phép. Offline schema compatibility là thông tin hỗ trợ, chưa đủ mở LIVE. Sau khi có ủy quyền riêng, pilot mới kiểm tra được các điều kiện thực tế như khả năng hoàn thành role calls và đối soát usage. Nếu billing không xác định sau gián đoạn, cơ chế kế toán phải giữ reservation và dừng fail-closed theo hợp đồng.

Full E1-v2 cần giữ nguyên chuẩn bị chung, ba nhánh, counterbalancing và phiên bản POST. Kết quả phải báo đủ inventory 144 ô, không che cell thiếu bằng số terminal quan sát được. Những sửa đổi ảnh hưởng điều kiện so sánh cần được quản lý như thay đổi giao thức, không lặng lẽ trộn kết quả khác nền vào cùng một phân tích.

Chấm chất lượng cần một EvaluationContext hợp lệ với owner projection đúng release, split và các định danh liên quan. Dynamic sufficiency và claim truth phải được quy chiếu độc lập với quan sát controller. Chỉ khi điều kiện này đạt mới có thể đánh giá FAR, correctness hoặc support theo nghĩa khoa học. Không xây dựng một bộ gold mới trong tác vụ sản xuất báo cáo.

## 7.3 Phân tích và quyết định sau khi đủ điều kiện

Phân tích dự kiến bắt đầu từ kiểm tra provenance và missingness, sau đó báo tầng chỉ số riêng. So sánh chính A1–G cần được diễn giải ở cấp gói chính sách; A1–A0 giải thích vai trò khả năng nhìn thấy câu hỏi; A0–G hỗ trợ bối cảnh. Các chuyển trạng thái PRE và diagnosis POST giúp tìm loại lỗi cụ thể, nhưng không tự chứng minh cơ chế nào gây khác biệt chất lượng.

Bootstrap readiness chỉ được chạy nếu qualified LIVE có complete gates theo protocol. Các kết quả lâm sàng phải có mẫu số và điều kiện chấm độc lập rõ ràng. Với DEV nhỏ, báo cáo cuối cần giữ tính thăm dò, trình bày uncertainty và các trường hợp không đánh giá được. Một kết luận không vượt trội cũng là kết quả hợp lệ nếu điều kiện thực nghiệm và phân tích được tuân thủ.

Kế hoạch này ưu tiên hoàn tất lỗ hổng qualification đã biết trước khi mở các bước tốn tài nguyên hoặc đòi thẩm quyền mới. Nó không mở rộng sang huấn luyện mô hình, hạ tầng đám mây hay tải benchmark khác. Công việc đang được phê duyệt ở giai đoạn này vẫn là mốc kỹ thuật sáu mô đun; các mốc khoa học tiếp theo giữ điều kiện cấp quyền riêng. [P3–P4]

<!-- PAGE -->
META {"main":true,"page":31,"chapter":8}
# CHƯƠNG 8 KẾT LUẬN

## 8.1 Kết quả của giai đoạn giữa kỳ

Nghiên cứu đã hình thành một hệ thống hỏi đáp theo bằng chứng có ranh giới tác vụ, cấu trúc dữ liệu và điều khiển rõ ràng. KOA-GuidelineBench tách bằng chứng runtime khỏi nhãn đánh giá; DV-OGEC-RAG tách lập kế hoạch, truy xuất, kiểm tra trước sinh, sinh và phân rã claim, kiểm chứng sau sinh, sửa có căn cứ và cấp quyền hành động. Các vai trò nối bằng typed contracts thay vì một chuỗi văn bản không có định danh. [P1–P2]

Hai điểm kỹ thuật quan trọng là recheck PRE sau correction và vô hiệu hóa claims/POST cũ sau revision. Chúng giữ cho quyết định dựa trên đúng snapshot hiện tại. PolicyGuard tiếp tục kiểm tra legality, source scope, provenance và ngân sách trước hành động. Bởi vậy, một phán quyết hoặc confidence của mô hình không tự bỏ qua nghĩa vụ chưa bao phủ hay claim thiếu hỗ trợ.

Qualification native MOCK đã có receipts cho pilot 9 ô và full 144 ô, cùng 129 kiểm thử trọng yếu PASS. Regression vẫn PARTIAL, còn sáu mô đun bị chặn tài nguyên. Các con số xác nhận một phạm vi vận hành kỹ thuật tại baseline ac4ade7; chúng không phải bằng chứng so sánh chất lượng lâm sàng hoặc tương đương giữa các nhánh. [P4]

## 8.2 Kết luận khoa học được phép rút ra

Tại baseline được tiếp nhận, chưa thực hiện E1-v2 với nhà cung cấp thật và chưa đủ điều kiện chấm chất lượng độc lập trong phạm vi công khai. Vì thế, ba câu hỏi nghiên cứu vẫn mở. Không thể kết luận A1 vượt G, readiness tăng làm accuracy tăng, hoặc cơ chế từ chối đã tối ưu cho người dùng y khoa. Khả năng kiểm toán của thiết kế là điều kiện hỗ trợ kiểm nghiệm những giả thuyết đó, không thay thế kiểm nghiệm.

Giao thức E1-v2 đã chỉ rõ so sánh chính, ablation, chuẩn bị dùng chung, mẫu số và quy tắc thiếu dữ liệu. Khi các gate kỹ thuật, provider, tài chính và owner scoring được đáp ứng đúng thẩm quyền, nghiên cứu có thể tiến tới kết luận thực nghiệm có giới hạn rõ. Mốc kế tiếp là hoàn thành sáu mô đun qualification native trên host đủ tài nguyên và giữ nguyên kiểm tra phiên bản. [P3–P4]

<!-- PAGE -->
META {"part":"references"}
# TÀI LIỆU THAM KHẢO

@SMALL [1] Lewis P, Perez E, Piktus A, Petroni F, Karpukhin V, Goyal N, và cộng sự. Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks. Advances in Neural Information Processing Systems. 2020;33:9459–9474. https://arxiv.org/abs/2005.11401.

@SMALL [2] Asai A, Wu Z, Wang Y, Sil A, Hajishirzi H. Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection. Twelfth International Conference on Learning Representations. 2024. https://arxiv.org/abs/2310.11511.

@SMALL [3] Yan S-Q, Gu J-C, Zhu Y, Ling Z-H. Corrective Retrieval Augmented Generation. arXiv preprint. 2024. https://arxiv.org/abs/2401.15884. Phiên bản dẫn trong báo cáo được xác định là preprint, không suy diễn trạng thái xuất bản khác.

@SMALL [4] Min S, Krishna K, Lyu X, Lewis M, Yih W-t, Koh PW, Iyyer M, Zettlemoyer L, Hajishirzi H. FActScore: Fine-grained Atomic Evaluation of Factual Precision in Long Form Text Generation. Proceedings of EMNLP. 2023:12076–12100. https://aclanthology.org/2023.emnlp-main.741/.

@SMALL [5] Kamath A, Jia R, Liang P. Selective Question Answering under Domain Shift. Proceedings of ACL. 2020:5684–5696. https://aclanthology.org/2020.acl-main.503/.

@SMALL [6] Jin Q, Kim W, Chen Q, Comeau DC, Yeganova L, Wilbur WJ, Lu Z. MedCPT: Contrastive Pre-trained Transformers with large-scale PubMed search logs for zero-shot biomedical information retrieval. Bioinformatics. 2023;39(11):btad651. https://doi.org/10.1093/bioinformatics/btad651.

@SMALL [7] Johnson J, Douze M, Jégou H. Billion-Scale Similarity Search with GPUs. IEEE Transactions on Big Data. 2021;7(3):535–547. https://arxiv.org/abs/1702.08734.

@SMALL [8] Xiong G, Jin Q, Lu Z, Zhang A. Benchmarking Retrieval-Augmented Generation for Medicine. Findings of ACL. 2024:6233–6251. https://aclanthology.org/2024.findings-acl.372/.

<!-- PAGE -->
META {"part":"references"}
# TÀI LIỆU THAM KHẢO TIẾP THEO

@SMALL [9] Australian Commission on Safety and Quality in Health Care. Osteoarthritis of the Knee Clinical Care Standard. 2024. https://www.safetyandquality.gov.au/resources/osteoarthritis-knee-clinical-care-standard-2024.

@SMALL [10] Bộ Y tế. Hướng dẫn chẩn đoán và điều trị các bệnh cơ xương khớp. Quyết định số 361/QĐ-BYT ngày 25/01/2014. Metadata registry và trang nguồn: https://kcb.vn/van-ban/huong-dan-chan-doan-va-dieu-tri-cac-benh-co-xuong-khop.html.

@SMALL [11] Moseng T, Vliet Vlieland TPM, Battista S, Beckwee D, Boyadzhieva V, Conaghan PG, và cộng sự. EULAR recommendations for the non-pharmacological core management of hip and knee osteoarthritis: 2023 update. Annals of the Rheumatic Diseases. 2024;83:730–740. https://doi.org/10.1136/ard-2023-225041.

@SMALL [12] National Institute for Health and Care Excellence. Osteoarthritis in over 16s: diagnosis and management. NICE guideline NG226. 2022. https://www.nice.org.uk/guidance/ng226/.

@SMALL [13] U.S. Department of Veterans Affairs, Department of Defense. Non-Surgical Management of Hip & Knee Osteoarthritis. Phiên bản registry đóng băng 2026. https://www.healthquality.va.gov/HEALTHQUALITY/guidelines/CD/OA/index.asp.

@SMALL [P1] KOA-GuidelineBench rc0.2.0. Benchmark manifests, exposure contracts và task structure; diễn giải công khai tại docs/benchmark.md. Release manifest SHA-256 eda0e26c1832f41150b37da7780076f9ea04f55927765faaee3b4a2047e5985b. Bản ứng viên nội bộ, public_release = false.

@SMALL [P2] KOA Agentic-RAG System. Method/runtime tại baseline ac4ade796e56377882b8069d0fb7a14809e8180b. Diễn giải: docs/system-architecture.md, docs/agentic-workflow.md và docs/implementation.md. Không phát hành private runtime source trong báo cáo.

@SMALL [P3] E1-v2 scientific protocol. e1-v2.refined-full-primary.v2. Protocol lock SHA-256 98ad86c861986f3794d9b5818cafe44d396967340faf3631d6fb06d91006e5a3. Diễn giải công khai tại docs/experimental-design.md; contract giữa kỳ giải quyết các chỗ diễn đạt cần giới hạn.

@SMALL [P4] KOA final engineering/research closure và aggregate qualification receipts tại baseline. closure-pilot-final.receipt.json, closure-parent-final.receipt.json, closure-critical-final.tests.json, regression-reconciled.json và provider-compatibility-final.json. Danh tính và phạm vi đối soát xem Phụ lục A; trạng thái tóm tắt tại docs/current-results.md và docs/midterm/content-contract.md.

<!-- PAGE -->
META {"part":"appendix"}
# PHỤ LỤC A ĐỊNH DANH VÀ NGUỒN BẰNG CHỨNG

## A1 Định danh snapshot giữa kỳ

Các chuỗi sau xác định hiện vật được tiếp nhận cho báo cáo. Chúng là định danh đối soát, không phải thang đo chất lượng. Scientific source identity và integration identity đã được đối chiếu với receipts ở baseline; các thay đổi mới hơn trong working tree gốc nằm ngoài snapshot này.

@SMALL Publication repository: KwanFam26022005/KOA-Agentic-RAG-System. Starting HEAD: 55b43da567a0eb0d8ddb26613f17763c3df05796.

@SMALL Scientific baseline: ac4ade796e56377882b8069d0fb7a14809e8180b.

@SMALL Scientific source SHA-256: 5aa87228b07ead1c4ecde48e7330e62771a86dbed7ac0fc4097f50152d306f5b.

@SMALL Integration SHA-256: 0155dc81df270dc5b6413ce6587aa52ed69e3cb7f415cd5146bf1188431ac927.

@SMALL Protocol: e1-v2.refined-full-primary.v2. Lock SHA-256: 98ad86c861986f3794d9b5818cafe44d396967340faf3631d6fb06d91006e5a3.

@SMALL Config config.yaml SHA-256: 5ce81a22cf4cbb828f9d20a1698934fa8add4697076d13b4dfd2a989754ed5cd.

@SMALL Release manifest SHA-256: eda0e26c1832f41150b37da7780076f9ea04f55927765faaee3b4a2047e5985b.

@SMALL Corpus SHA-256: f9cdcccd5a0e97784ee59ceeb43292a6a8419c61ed6825180e37256e66e1de52.

@SMALL Typed DEV assignment SHA-256: 987f2bb21f0844ea1b9a041f686bec66296f60bc05883bd629c429ad5c1458f7. Đây là digest của typed records, không phải SHA-256 thô của tệp dev_e1.py.

## A2 Aggregate receipts được viện dẫn

@SMALL Pilot run: 20261020T124525034329Z-c18d0afc7ed84f2d; full run: 20261020T124618087083Z-031bcc4e5ec34fed. Receipts thuộc qualification/reports/koa_final_closure/ của baseline gốc. Chỉ các tổng hợp đã làm sạch được dùng trong báo cáo; không nhúng raw traces, prompt hoặc benchmark owner content.

Các receipts nêu trên là bằng chứng kỹ thuật đã tồn tại, không phải lệnh kiểm thử vừa chạy khi sản xuất tài liệu. Bản báo cáo không tái xác nhận provider thật hay chất lượng lâm sàng từ MOCK. Số SKIP và RESOURCE_BLOCKED được giữ nguyên theo phạm vi qualification.

<!-- PAGE -->
META {"part":"appendix"}
# PHỤ LỤC B NGUỒN HÌNH VÀ QUY ƯỚC TRÌNH BÀY

## B1 Hình nghiên cứu có thể truy nguyên

Hình 1.1 lấy từ assets/diagrams/01-research-framework.svg; Hình 3.1 từ 04-benchmark-evaluation-boundary.svg; Hình 4.1 từ 02-agentic-rag-architecture.svg; Hình 4.2 từ 03-controller-state-machine.svg; Hình 5.1 từ 05-experimental-arms.svg. Mỗi tệp có Mermaid cùng tên để rà soát nội dung. Sơ đồ gốc được giữ tỷ lệ; phần giải thích chi tiết trong chương tương ứng trình bày lại điều kiện chuyển bước bằng văn bản và bảng.

Các sơ đồ mô tả phương pháp và thiết kế nghiên cứu, không phải biểu đồ kết quả lâm sàng. Không có trục accuracy, chênh lệch chất lượng hoặc khoảng tin cậy được suy ra từ pass count. Quy tắc bounded correction, PRE recheck, memory-only revision, fresh decomposition/POST và ba trạng thái kết thúc được giữ trong diễn giải.

## B2 Mẫu trình bày và nhận diện trường

Bố cục tham khảo PDF do người dùng cung cấp: khổ A4, Times New Roman cỡ 13 cho thân bài, tiêu đề đậm, số trang đầu trang ở giữa và chú thích dưới hình. Vùng thân đo trên trang nội dung có mép trái xấp xỉ 3,5 cm và mép phải 2 cm. Báo cáo áp dụng bố cục bìa theo trật tự cơ quan, trường, logo, tác giả, tên báo cáo và đề tài; bỏ metadata môn học, giảng viên và mã số chưa được xác nhận.

Logo TDTU giữ nguyên tỷ lệ và màu từ tài sản chính thức của trường. Nguồn xác minh: trang https://www.tdtu.edu.vn/ và ảnh https://www.tdtu.edu.vn/sites/www/files/logo_2.png. Việc sử dụng nhận diện trong báo cáo học thuật không được hiểu là phê duyệt khoa học hoặc chứng nhận sản phẩm bởi nhà trường.

Mẫu tham khảo không thể hiện một quy ước mục lục, danh mục hoặc bibliography riêng. Các phần đó được bổ sung cho báo cáo nghiên cứu: front matter đánh số La Mã, nội dung chính dùng số Ả Rập, tài liệu tham khảo dạng đánh số và nguồn nội bộ tách ký hiệu P. Trang ngang là điều chỉnh có chủ đích để đọc sơ đồ. Tệp mẫu gốc không được đưa vào gói công bố.

## B3 Phạm vi kiểm tra hiện vật

Kiểm tra sản xuất gồm mở/xuất bằng Word, dựng ảnh PDF, xem bố cục và kiểm tra Unicode. Nhật ký được lưu cùng bộ báo cáo; đây là kiểm tra tài liệu, không phải chạy lại thí nghiệm hoặc xác nhận kết quả y khoa.

<!-- PAGE -->
META {"part":"appendix"}
# PHỤ LỤC C CHI TIẾT KIỂM SOÁT HÀNH ĐỘNG

@DETAIL 02-agentic-rag-architecture.svg | 1030,360,1420,680 | Hình C.1 Chi tiết PolicyGuard và đầu ra từ Hình 4.1

Đây là vùng phóng to nguyên bản của phần control plane, không phải thêm một cơ chế mới. PolicyGuard kiểm tra legality theo phase, ngân sách, source policy, provenance và điều kiện ACCEPT. Guard rejection là lỗi kỹ thuật thuộc FAILED_*; một ABSTAIN hợp lệ phải được cấp quyền theo gate và trạng thái. ACCEPT là quyết định phát hành của controller, cần chấm độc lập mới biết độ đúng lâm sàng. Nguồn: assets/diagrams/02-agentic-rag-architecture.svg. [P2]
