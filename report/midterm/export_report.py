"""Native invisible Word export and complete page rasterization for review."""
from pathlib import Path
import json,sys
import fitz
import win32com.client
from PIL import Image, ImageOps, ImageDraw
sys.stdout.reconfigure(encoding='utf-8')
root=Path(__file__).resolve().parent
build=root/'_build';build.mkdir(exist_ok=True)
docx=root/'KOA_Midterm_Report_TDTU.docx';pdf=root/'KOA_Midterm_Report_TDTU.pdf'
word=win32com.client.DispatchEx('Word.Application')
word.Visible=False;word.DisplayAlerts=0
try:
    word.AutomationSecurity=3
    word.Options.UpdateLinksAtOpen=False
    d=word.Documents.Open(str(docx),ReadOnly=False,AddToRecentFiles=False,ConfirmConversions=False)
    for name in ['TOC 1','TOC 2']:
        try:
            s=d.Styles(name);s.Font.Name='Times New Roman';s.Font.Size=12;s.Font.Color=0
            s.ParagraphFormat.SpaceAfter=3;s.ParagraphFormat.SpaceBefore=0
            s.ParagraphFormat.LineSpacingRule=0
        except Exception:pass
    d.Fields.Update()
    for toc in d.TablesOfContents:toc.Update()
    d.Repaginate()
    d.Save()
    d.ExportAsFixedFormat(str(pdf),17,OpenAfterExport=False,OptimizeFor=0,CreateBookmarks=1,DocStructureTags=True,BitmapMissingFonts=False,UseISO19005_1=False)
    print('Word pages',d.ComputeStatistics(2),'TOCs',d.TablesOfContents.Count)
    d.Close(False)
finally:
    try:word.Quit()
    except (AttributeError, Exception):pass

p=fitz.open(pdf);out=build/'pages';out.mkdir(exist_ok=True)
stats=[];thumbs=[]
for i,page in enumerate(p):
    page.get_pixmap(matrix=fitz.Matrix(1.6,1.6),alpha=False).save(out/f'page-{i+1:02}.png')
    text=page.get_text()
    stats.append({'pdf_page':i+1,'width':round(page.rect.width,2),'height':round(page.rect.height,2),'characters':len(text),'text_start':text[:160],'text_end':text[-160:]})
    im=Image.open(out/f'page-{i+1:02}.png');im.thumbnail((240,330))
    cell=Image.new('RGB',(260,360),'#ddd');cell.paste(im,((260-im.width)//2,20));ImageDraw.Draw(cell).text((8,3),str(i+1),fill='black');thumbs.append(cell)
for start in range(0,len(thumbs),12):
    sheet=Image.new('RGB',(260*4,360*3),'white')
    for j,im in enumerate(thumbs[start:start+12]):sheet.paste(im,((j%4)*260,(j//4)*360))
    sheet.save(build/f'contact-{start+1:02}.png')
(build/'page-stats.json').write_text(json.dumps(stats,ensure_ascii=False,indent=2),encoding='utf-8')
(build/'report-text.txt').write_text('\n\n'.join('PAGE '+str(i+1)+'\n'+page.get_text() for i,page in enumerate(p)),encoding='utf-8')
print('PDF pages',len(p))
for s in stats:print(s['pdf_page'],s['characters'],s['text_start'].splitlines()[:2])
