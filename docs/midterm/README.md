# KOA midterm report and presentation

This artifact set presents the **admitted scientific snapshot at `ac4ade796e56377882b8069d0fb7a14809e8180b`**, not the latest mutable state of the original research workspace. Authors: Phạm Hồng Đăng Khoa and Nguyễn Hoàng Khang.

- [Editable Vietnamese report](../../report/midterm/KOA_Midterm_Report_TDTU.docx)
- [Report PDF](../../report/midterm/KOA_Midterm_Report_TDTU.pdf)
- [Editable 15-slide presentation](../../slides/midterm/KOA_Midterm_Presentation_TDTU.pptx)
- [Presentation PDF](../../slides/midterm/KOA_Midterm_Presentation_TDTU.pdf)
- [Presenter notes](../../slides/midterm/speaker-notes.md)

Scientific content is governed by [the shared contract](content-contract.md). [The independent review](science-review.md) records evidence checks and the final cross-document verdict. [Source verification](source-verification.md) identifies primary references and formatting provenance. [The production plan](production-plan.md) records artifact ownership and release gates.

The report adapts the supplied university PDF's observed A4 typography, margins, cover arrangement and pagination to a research report. Unverified course, supervisor, student and affiliation metadata are omitted. The presentation is a **TDTU-inspired academic theme**, using an unaltered official website logo; it is not represented as an official university template or endorsement.

The public artifact set contains scientific descriptions, citations, original project diagrams and sanitized engineering aggregates. The original formatting PDF, guideline full text, benchmark gold, owner references, private runtime source and raw traces remain excluded. E1-v2 real-provider and independent clinical-quality evaluation are pending at the admitted baseline.

Run the read-only artifact acceptance checks from this repository with the already-installed PyMuPDF dependency:

```powershell
python -X utf8 docs/midterm/validate_deliverables.py
```

This checks OOXML integrity, artifact counts, editable text/tables, notes, required facts, Unicode extraction and credential-shaped strings. It does not replace visual inspection, scientific review, clinical scoring or the private runtime regression suite. The final production receipt records which checks were actually run.

The finished report contains **42 total pages, including 31 main-content pages**; the deck contains **15 editable slides**. [Production receipt](production-receipt.json), [visual QA](visual-qa.md) and [scientific review](science-review.md) record the actual checks and limitations. Rebuild instructions and artifact sources are in the report and presentation directories.

Final review also corrected provenance/terminal labels in diagrams 01/04 and two label positions in diagrams 02/04. These changes preserve the method and the admitted scientific snapshot.
