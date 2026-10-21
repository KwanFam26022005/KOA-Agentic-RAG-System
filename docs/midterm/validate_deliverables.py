"""Read-only acceptance checks for the two midterm artifact pairs.

Uses standard-library OOXML inspection and the already-installed PyMuPDF.
Does not import the scientific runtime, execute inference, or validate medicine.
Visual and independent scientific reviews remain separate release gates.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import sys
import unicodedata
import xml.etree.ElementTree as ET
from zipfile import ZipFile

import fitz

ROOT = Path(__file__).resolve().parents[2]
NS = {
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
}
FILES = {
    "report_source": ROOT / "report/midterm/KOA_Midterm_Report_TDTU.docx",
    "report_pdf": ROOT / "report/midterm/KOA_Midterm_Report_TDTU.pdf",
    "presentation_source": ROOT / "slides/midterm/KOA_Midterm_Presentation_TDTU.pptx",
    "presentation_pdf": ROOT / "slides/midterm/KOA_Midterm_Presentation_TDTU.pdf",
    "speaker_notes": ROOT / "slides/midterm/speaker-notes.md",
}


def norm(text: str) -> str:
    return unicodedata.normalize("NFC", text)


def compact(text: str) -> str:
    return re.sub(r"\s+", "", norm(text))


def inspect_package(path: Path, kind: str) -> dict:
    with ZipFile(path) as package:
        if package.testzip() is not None:
            raise ValueError(f"Corrupt ZIP: {path.name}")
        names = package.namelist()
        for name in names:
            if name.endswith((".xml", ".rels")):
                ET.fromstring(package.read(name))
        text_tag = "w:t" if kind == "docx" else "a:t"
        if kind == "docx":
            parts = ["word/document.xml"]
        else:
            parts = sorted(
                [n for n in names if re.fullmatch(r"ppt/slides/slide\d+\.xml", n)],
                key=lambda n: int(re.search(r"(\d+)\.xml$", n).group(1)),
            )
        texts = []
        for part in parts:
            xml = ET.fromstring(package.read(part))
            texts.append(norm(" ".join(x.text or "" for x in xml.findall(".//" + text_tag, NS))))
        detail = {
            "xml_parts_parsed": sum(n.endswith((".xml", ".rels")) for n in names),
            "text": "\n".join(texts),
            "embedded_files": [n for n in names if "/embeddings/" in n],
            "media_count": sum("/media/" in n and not n.endswith("/") for n in names),
            "macro_parts": [n for n in names if n.lower().endswith("vbaproject.bin")],
        }
        if kind == "pptx":
            pxml = ET.fromstring(package.read("ppt/presentation.xml"))
            size = pxml.find("p:sldSz", NS)
            detail["slide_size_emu"] = [int(size.get("cx")), int(size.get("cy"))]
            detail["slide_count"] = len(parts)
            detail["slide_text_lengths"] = [len(t) for t in texts]
            detail["notes_count"] = sum(bool(re.fullmatch(r"ppt/notesSlides/notesSlide\d+\.xml", n)) for n in names)
            detail["native_tables"] = sum(package.read(n).count(b"<a:tbl>") for n in parts)
        else:
            dxml = ET.fromstring(package.read("word/document.xml"))
            instructions = " ".join(x.text or "" for x in dxml.findall(".//w:instrText", NS))
            detail["toc_field_present"] = "TOC" in instructions
            detail["table_count"] = len(dxml.findall(".//w:tbl", NS))
        return detail


def inspect_pdf(path: Path) -> dict:
    with fitz.open(path) as pdf:
        pages = [norm(p.get_text()) for p in pdf]
        fonts = sorted({f[3] for p in pdf for f in p.get_fonts()})
        main_starts = [i for i,t in enumerate(pages) if t.splitlines()[0:1] == ['1'] and 'CHƯƠNG1GIỚITHIỆU' in compact(t)]
        reference_starts = [i for i,t in enumerate(pages) if len(t.splitlines()) > 1 and t.splitlines()[0].isdigit() and compact(t.splitlines()[1]) == 'TÀILIỆUTHAMKHẢO']
        main_pages = reference_starts[0]-main_starts[0] if main_starts and reference_starts else None
        return {
            "pages": len(pdf),
            "main_content_pages": main_pages,
            "dimensions_pt": sorted({(round(p.rect.width, 2), round(p.rect.height, 2)) for p in pdf}),
            "text": "\n".join(pages),
            "page_text_lengths": [len(t) for t in pages],
            "fonts": fonts,
            "replacement_glyphs": sum(t.count("\ufffd") for t in pages),
        }


def run() -> dict:
    failures: list[str] = []
    checks: list[dict] = []

    def check(label: str, passed: bool) -> None:
        checks.append({"check": label, "passed": bool(passed)})
        if not passed:
            failures.append(label)

    for name, path in FILES.items():
        check(f"{name}: present and nonempty", path.is_file() and path.stat().st_size > 100)
    if failures:
        return {"status": "FAIL", "checks": checks, "failures": failures}

    report = inspect_package(FILES["report_source"], "docx")
    deck = inspect_package(FILES["presentation_source"], "pptx")
    rpdf = inspect_pdf(FILES["report_pdf"])
    spdf = inspect_pdf(FILES["presentation_pdf"])
    check("deck: 15 editable slides", deck["slide_count"] == 15 and min(deck["slide_text_lengths"]) > 80)
    check("deck: 16:9 canvas", abs(deck["slide_size_emu"][0] / deck["slide_size_emu"][1] - 16 / 9) < 0.005)
    check("deck PDF: 15 pages", spdf["pages"] == 15)
    check("deck: presenter notes embedded", deck["notes_count"] == 15)
    check("deck: native editable evidence tables", deck["native_tables"] >= 2)
    check("report: substantive page inventory", 30 <= rpdf["pages"] <= 60)
    check("report: 25–35 main content pages", rpdf['main_content_pages'] is not None and 25 <= rpdf['main_content_pages'] <= 35)
    check("report: editable text", len(report["text"]) > 35000)
    check("report: table of contents field", report["toc_field_present"])
    check("report: native evidence tables", report["table_count"] >= 5)
    check("packages: no macros or embedded documents", not any(x["macro_parts"] or x["embedded_files"] for x in [report, deck]))

    facts = {
        "corpus 276": "276",
        "corpus intents 170": "170",
        "MOCK pilot 9/9": "9/9",
        "MOCK full 144/144": "144/144",
        "critical 129/129": "129/129",
        "regression 103/109": "103/109",
        "provider pending": "NOT_EXECUTED",
        "scoring pending": "NOT_EVALUABLE",
        "eligible 0/16": "0/16",
        "author Khoa": "PhạmHồngĐăngKhoa",
        "author Khang": "NguyễnHoàngKhang",
    }
    for artifact_name, artifact in [("report DOCX", report), ("report PDF", rpdf), ("deck PPTX", deck), ("deck PDF", spdf)]:
        value = compact(artifact["text"])
        for fact_name, literal in facts.items():
            check(f"{artifact_name}: {fact_name}", literal.casefold() in value.casefold())
        check(f"{artifact_name}: Vietnamese replacement glyphs absent", "\ufffd" not in value)
        check(
            f"{artifact_name}: unrelated template metadata absent",
            not any(x.casefold() in value.casefold() for x in ["FIMLab", "Apriori", "DoãnXuânThanh", "52300119"]),
        )

    # Restricted material is checked through source/media review separately.
    # This scan detects credential-shaped values without printing any match.
    credential = re.compile(r"(?:sk-(?:proj-|svcacct-)?[A-Za-z0-9_-]{24,}|ghp_[A-Za-z0-9]{25,}|github_pat_[A-Za-z0-9_]{30,}|xox[baprs]-[A-Za-z0-9-]{20,}|-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----)")
    for name, data in [("report", report["text"]), ("deck", deck["text"]), ("notes", FILES["speaker_notes"].read_text(encoding="utf-8"))]:
        check(f"{name}: credential-pattern scan", not credential.search(data))

    hashes = {
        name: {"path": path.relative_to(ROOT).as_posix(), "bytes": path.stat().st_size, "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
        for name, path in FILES.items()
    }
    for obj in [report, deck, rpdf, spdf]:
        obj.pop("text")
    return {
        "status": "PASS" if not failures else "FAIL",
        "scope": "Artifact integrity and required-fact presence; not a substitute for visual/scientific review",
        "checks": checks,
        "failures": failures,
        "files": hashes,
        "report_ooxml": report,
        "report_pdf": rpdf,
        "presentation_ooxml": deck,
        "presentation_pdf": spdf,
    }


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    result = run()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    sys.exit(0 if result["status"] == "PASS" else 1)
