"""Rebuild the Vietnamese midterm report from public-safe authored content.

Uses installed python-docx, PyMuPDF and dedicated, invisible Microsoft Word.
No model calls, network access, experiments, or restricted benchmark text.
"""
from pathlib import Path
import re, json, sys, hashlib, subprocess, shutil
import fitz
import xml.etree.ElementTree as ET
from docx import Document
from docx.shared import Cm, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.section import WD_SECTION_START, WD_ORIENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent.parent
BUILD = ROOT / '_build'
BUILD.mkdir(exist_ok=True)
FONT = 'Times New Roman'
OUT = ROOT / 'KOA_Midterm_Report_TDTU.docx'

def font(run, size=None, bold=None):
    run.font.name=FONT
    run._element.get_or_add_rPr().get_or_add_rFonts().set(qn('w:eastAsia'),FONT)
    if size: run.font.size=Pt(size)
    if bold is not None: run.bold=bold
    return run

def field(p, code, cached=''):
    r=OxmlElement('w:r'); b=OxmlElement('w:fldChar'); b.set(qn('w:fldCharType'),'begin'); r.append(b); p._p.append(r)
    r=OxmlElement('w:r'); i=OxmlElement('w:instrText'); i.set(qn('xml:space'),'preserve'); i.text=' '+code+' ';r.append(i);p._p.append(r)
    r=OxmlElement('w:r'); s=OxmlElement('w:fldChar');s.set(qn('w:fldCharType'),'separate');r.append(s);p._p.append(r)
    font(p.add_run(cached),13)
    r=OxmlElement('w:r');e=OxmlElement('w:fldChar');e.set(qn('w:fldCharType'),'end');r.append(e);p._p.append(r)

def section_layout(s, landscape=False, start=None, fmt=None):
    s.orientation=WD_ORIENT.LANDSCAPE if landscape else WD_ORIENT.PORTRAIT
    s.page_width=Cm(29.7 if landscape else 21)
    s.page_height=Cm(21 if landscape else 29.7)
    s.left_margin=Cm(3.5 if not landscape else 2)
    s.right_margin=Cm(2)
    s.top_margin=Cm(3.5 if not landscape else 2.2)
    s.bottom_margin=Cm(2.5 if not landscape else 1.8)
    s.header_distance=Cm(1.5)
    s.footer_distance=Cm(1.2)
    if start is not None or fmt:
        n=s._sectPr.find(qn('w:pgNumType'))
        if n is None: n=OxmlElement('w:pgNumType');s._sectPr.append(n)
        if start is not None:n.set(qn('w:start'),str(start))
        else:n.attrib.pop(qn('w:start'),None)
        if fmt:n.set(qn('w:fmt'),fmt)
        else:n.attrib.pop(qn('w:fmt'),None)

def paragraph(text, style=None, indent=True):
    global pending_break
    p=doc.add_paragraph(style=style)
    if pending_break:p.paragraph_format.page_break_before=True;pending_break=False
    if style is None:
        p.alignment=WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.first_line_indent=Cm(.75) if indent else Cm(0)
    font(p.add_run(text))
    return p

def table(lines):
    rows=[[c.strip() for c in l.strip().strip('|').split('|')] for l in lines]
    t=doc.add_table(rows=1,cols=len(rows[0]));t.autofit=False
    usable=25.7 if current_land else 15.5
    widths = [4.2, usable-4.2] if rows[0][0] == 'Thuật ngữ' else [usable/len(rows[0])]*len(rows[0])
    for col,width in zip(t.columns,widths):col.width=Cm(width)
    for j,row in enumerate(rows):
        cells=t.rows[0].cells if j==0 else t.add_row().cells
        for c,txt,width in zip(cells,row,widths):
            c.width=Cm(width)
            c.text='';p=c.paragraphs[0];p.paragraph_format.space_after=Pt(4);p.paragraph_format.space_before=Pt(3)
            p.paragraph_format.line_spacing=1.12
            if rows[0][0] == 'Thuật ngữ':
                p.paragraph_format.space_before=Pt(2);p.paragraph_format.space_after=Pt(2)
                p.paragraph_format.line_spacing=1.05
            font(p.add_run(txt),11.5,j==0)
            tcPr=c._tc.get_or_add_tcPr()
            m=OxmlElement('w:tcMar')
            for tag in ('top','left','bottom','right'):
                e=OxmlElement('w:'+tag);e.set(qn('w:w'),'65');e.set(qn('w:type'),'dxa');m.append(e)
            tcPr.append(m)
            borders=OxmlElement('w:tcBorders')
            for tag in ('top','left','bottom','right'):
                e=OxmlElement('w:'+tag);e.set(qn('w:val'),'single');e.set(qn('w:sz'),'4');e.set(qn('w:color'),'777777');borders.append(e)
            tcPr.append(borders)
        trPr=t.rows[j]._tr.get_or_add_trPr()
        no=OxmlElement('w:cantSplit');trPr.append(no)
        if j==0:
            h=OxmlElement('w:tblHeader');trPr.append(h)
    p=doc.add_paragraph();p.paragraph_format.space_after=Pt(0);p.paragraph_format.line_spacing=Pt(2)
    font(p.add_run(''),1)

def asset(name, detail=False):
    src=REPO/'assets'/'diagrams'/name
    suffix='-detail' if detail else ''
    out=BUILD/(src.stem+suffix+'.png')
    source_sha=hashlib.sha256(src.read_bytes()+str(detail).encode()).hexdigest()
    marker=out.with_suffix('.browser-rendered')
    if out.exists() and marker.exists() and marker.read_text(encoding='utf-8')==source_sha:return out
    svg=src.read_text(encoding='utf-8')
    vb=re.search(r'viewBox="0 0 (\d+) (\d+)"',svg)
    width,height=map(int,vb.groups())
    if detail:
        # Omit only context headers that would be bisected at the crop edge.
        # Preserve every node, condition, connector and scientific label.
        tree=ET.fromstring(svg)
        for el in list(tree):
            tag=el.tag.rsplit('}',1)[-1]
            xy=(el.get('x'),el.get('y'))
            if (tag=='rect' and xy in {('1015','48'),('1025','58'),('35','58'),('35','370')}) or (tag=='text' and xy in {('42','72'),('42','384'),('1032','72')}):
                tree.remove(el)
        ET.register_namespace('', 'http://www.w3.org/2000/svg')
        svg=ET.tostring(tree,encoding='unicode')
    html=BUILD/(src.stem+suffix+'.html')
    html.write_text('<!doctype html><html><meta charset="utf-8"><style>html,body{margin:0;padding:0;overflow:hidden;width:'+str(width)+'px;height:'+str(height)+'px}</style>'+svg+'</html>',encoding='utf-8')
    subprocess.run([r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe','--headless=new','--disable-gpu','--hide-scrollbars','--no-first-run','--no-default-browser-check','--force-device-scale-factor=2','--user-data-dir='+str(BUILD/'edge-profile'),'--window-size='+str(width)+','+str(height),'--screenshot='+str(out),html.as_uri()],capture_output=True,timeout=30,check=True)
    marker.write_text(source_sha,encoding='utf-8')
    return out

def image_line(text):
    name,cap=text[2:].split('|',1)
    p=doc.add_paragraph();p.alignment=WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.line_spacing=1.0
    p.paragraph_format.space_after=Pt(4)
    width=22.5 if current_land else 15.3
    p.add_run().add_picture(str(asset(name.strip())),width=Cm(width))
    p=doc.add_paragraph(style='Caption');p.alignment=WD_ALIGN_PARAGRAPH.CENTER
    font(p.add_run(cap.strip()),11.5)
    p.paragraph_format.keep_with_next=False

def detail_line(text):
    from PIL import Image
    name,coords,cap=text.split('|',2)
    box=tuple(int(v)*2 for v in coords.split(','))
    im=Image.open(asset(name.strip(),detail=True)).crop(box)
    out=BUILD/(name.strip().replace('.svg','')+'-'+coords.replace(',','-').strip()+'.png');im.save(out)
    p=doc.add_paragraph();p.alignment=WD_ALIGN_PARAGRAPH.CENTER;p.paragraph_format.space_after=Pt(3)
    p.paragraph_format.line_spacing=1.0
    p.add_run().add_picture(str(out),width=Cm(22 if current_land else 15.3))
    p=doc.add_paragraph(style='Caption');p.alignment=WD_ALIGN_PARAGRAPH.CENTER;font(p.add_run(cap.strip()),11.5)
    p.paragraph_format.keep_with_next=False

doc=Document()
normal=doc.styles['Normal'];normal.font.name=FONT;normal.font.size=Pt(13)
normal.paragraph_format.line_spacing=1.15
normal.paragraph_format.space_after=Pt(5)
normal.paragraph_format.widow_control=True
for name,size in [('Title',17),('Heading 1',16),('Heading 2',14),('Heading 3',13)]:
    s=doc.styles[name];s.font.name=FONT;s.font.size=Pt(size);s.font.bold=True;s.font.color.rgb=RGBColor(0,0,0)
    for border in list(s.element.findall('.//'+qn('w:pBdr'))):border.getparent().remove(border)
    s.paragraph_format.space_before=Pt(8 if name!='Heading 1' else 0)
    s.paragraph_format.space_after=Pt(8)
    s.paragraph_format.keep_with_next=True
    s.paragraph_format.keep_together=True
for name in ('TOC 1','TOC 2'):
    try:
        s=doc.styles[name];s.font.name=FONT;s.font.size=Pt(12)
    except KeyError: pass
doc.styles['Caption'].font.name=FONT
doc.styles['Caption'].font.size=Pt(11.5)
doc.styles['Caption'].font.italic=False
doc.styles['Caption'].font.bold=False
doc.styles['Caption'].font.color.rgb=RGBColor(0,0,0)
for name in ('Normal','Title','Heading 1','Heading 2','Heading 3','Caption'):
    for fill in list(doc.styles[name].element.findall('.//'+qn('w14:textFill'))):fill.getparent().remove(fill)
s=doc.sections[0];section_layout(s)
s.header.paragraphs[0].text=''
doc.core_properties.title='KOA Agentic RAG System'
doc.core_properties.subject='Báo cáo giữa kỳ nghiên cứu về DV OGEC RAG và KOA GuidelineBench'
doc.core_properties.author='Phạm Hồng Đăng Khoa; Nguyễn Hoàng Khang'
doc.core_properties.keywords='KOA, RAG, dual verification, midterm'
doc.core_properties.comments=''

# Unaltered logo downloaded by the presentation author from the official site.
logo=BUILD/'tdtu-logo-official.png'
shutil.copy2(REPO/'slides'/'midterm'/'assets'/'tdtu-footer-official.png',logo)
for txt,size,bold,after in [
('TỔNG LIÊN ĐOÀN LAO ĐỘNG VIỆT NAM',13,False,4),
('TRƯỜNG ĐẠI HỌC TÔN ĐỨC THẮNG',14,True,20)]:
    p=doc.add_paragraph();p.alignment=WD_ALIGN_PARAGRAPH.CENTER;p.paragraph_format.space_after=Pt(after);font(p.add_run(txt),size,bold)
p=doc.add_paragraph();p.alignment=WD_ALIGN_PARAGRAPH.CENTER;p.add_run().add_picture(str(logo),width=Cm(3.7));p.paragraph_format.space_after=Pt(12)
for txt,size,bold,after in [
('PHẠM HỒNG ĐĂNG KHOA\nNGUYỄN HOÀNG KHANG',13,True,26),
('BÁO CÁO GIỮA KỲ NGHIÊN CỨU',17,True,17),
('KOA Agentic-RAG System',17,True,10),
('Evidence-Grounded Agentic Retrieval-Augmented Generation for Knee Osteoarthritis Clinical Guidelines',14,True,18),
('Hệ thống Agentic RAG dựa trên bằng chứng\ncho hướng dẫn lâm sàng thoái hóa khớp gối',13,False,45),
('THÀNH PHỐ HỒ CHÍ MINH',13,True,0)]:
    p=doc.add_paragraph(style='Title' if txt=='KOA Agentic-RAG System' else None);p.alignment=WD_ALIGN_PARAGRAPH.CENTER;p.paragraph_format.line_spacing=1.15;p.paragraph_format.space_after=Pt(after);font(p.add_run(txt),size,bold)

# Front matter uses roman folios; the supplied reference has no TOC convention.
s=doc.add_section(WD_SECTION_START.NEW_PAGE);section_layout(s,start=1,fmt='lowerRoman')
s.header.is_linked_to_previous=False
p=s.header.paragraphs[0];p.alignment=WD_ALIGN_PARAGRAPH.CENTER;field(p,'PAGE','i')
current_land=False
pending_break=False
pages=(ROOT/'report-content.md').read_text(encoding='utf-8').split('\n<!-- PAGE -->\n')
main_started=False
headings=[];captions=[];page_meta=[]
for idx,chunk in enumerate(pages):
    lines=chunk.strip().splitlines()
    meta=json.loads(lines.pop(0)[5:])
    is_main=meta.get('main',False);land=meta.get('landscape',False)
    if is_main and not main_started:
        s=doc.add_section(WD_SECTION_START.NEW_PAGE);section_layout(s,land,start=1,fmt='decimal');main_started=True
        current_land=land
    elif idx>0:
        if land!=current_land:
            s=doc.add_section(WD_SECTION_START.NEW_PAGE);section_layout(s,land,fmt='decimal' if main_started else 'lowerRoman');current_land=land
        else:pending_break=True
    page_meta.append(meta)
    if meta.get('toc'):
        paragraph('MỤC LỤC',style='Title',indent=False)
        p=doc.add_paragraph();field(p,'TOC \\o "1-2" \\h \\z \\u','Mục lục sẽ được Word cập nhật khi dựng bản hoàn chỉnh')
        continue
    j=0
    while j<len(lines):
        line=lines[j].strip()
        if not line:j+=1;continue
        if line.startswith('|'):
            tl=[]
            while j<len(lines) and lines[j].strip().startswith('|'):tl.append(lines[j].strip());j+=1
            table(tl);continue
        if line.startswith('# '):
            in_toc=is_main or meta.get('part') in ('lists','abbreviations','references','appendix')
            paragraph(line[2:],'Heading 1' if in_toc else 'Title',False)
        elif line.startswith('## '):paragraph(line[3:],'Heading 2',False)
        elif line.startswith('### '):paragraph(line[4:],'Heading 3',False)
        elif line.startswith('@FIG '):image_line(line[3:])
        elif line.startswith('@DETAIL '):detail_line(line[8:])
        elif line.startswith('@CAP '):
            p=paragraph(line[5:],'Caption',False);p.alignment=WD_ALIGN_PARAGRAPH.CENTER
        elif line.startswith('@SMALL '):
            p=paragraph(line[7:],indent=False)
            for r in p.runs:font(r,11)
            p.paragraph_format.line_spacing=1.15
        elif line.startswith('@FORMULA '):
            p=paragraph(line[9:],indent=False);p.alignment=WD_ALIGN_PARAGRAPH.CENTER
        else:paragraph(line)
        j+=1

# Vietnamese proofing language, monochrome titles and globally consistent runs.
for p in doc.paragraphs:
    for r in p.runs:
        font(r)
        lang=OxmlElement('w:lang');lang.set(qn('w:val'),'vi-VN');r._element.get_or_add_rPr().append(lang)
settings=doc.settings.element
u=OxmlElement('w:updateFields');u.set(qn('w:val'),'true');settings.append(u)
doc.save(OUT)
(BUILD/'page-plan.json').write_text(json.dumps(page_meta,ensure_ascii=False,indent=2),encoding='utf-8')
print('Created',OUT)
print('Authored page blocks',len(pages),'main',sum(m.get('main',False) for m in page_meta))
