# Rà soát khoa học bản giữa kỳ KOA

Ngày rà soát: 21/10/2026. Trạng thái: **đã xác minh baseline; chờ đối chiếu báo cáo và slide hoàn chỉnh**.

## Phạm vi và phương pháp

Rà soát claim, đơn vị đếm, thiết kế thí nghiệm và giới hạn diễn giải theo `docs/midterm/content-contract.md`. Reviewer không sửa nội dung báo cáo/slide. Chỉ dùng Git objects tại baseline `ac4ade796e56377882b8069d0fb7a14809e8180b` và receipt tổng hợp phù hợp trong kho nghiên cứu gốc; không dùng working tree đang có thay đổi mới. Không đọc gold, evaluator capsule, private trace hoặc guideline full text. Không gọi provider, tải dữ liệu hoặc chạy lại thí nghiệm.

Skill áp dụng: `research-plugin:evidence-review` và working principles đi kèm. Đây là kiểm tra nguồn/provenance và tính nhất quán khoa học của tài liệu; không phải thẩm định lâm sàng độc lập.

## Bằng chứng đã trực tiếp kiểm tra

| Nguồn tại baseline | Kiểm tra đã thực hiện | Kết quả |
|---|---|---|
| `qualification/reports/koa_final_closure/final-evidence.json` | So sánh SHA-256 của từng Git blob với các map receipt, không xuất nội dung source | 186/186 mục `source_files` và 54/54 mục `integration_files` khớp; không thiếu/khác. Hai map có thể giao nhau, không cộng thành số file phân biệt. |
| `experiments/e1_pre_v2/protocol.lock.json` | Tính SHA-256 trực tiếp trên bytes từ `git show`; đọc metadata protocol | Khớp `98ad86c861986f3794d9b5818cafe44d396967340faf3631d6fb06d91006e5a3`; version `e1-v2.refined-full-primary.v2`, rc0.2.0, Task C DEV EN, 16 IDs, A0/A1/G. |
| `docs/experiments/E1_V2_SCIENTIFIC_PROTOCOL.md` | So sánh raw Git blob với document hash trong lock; đọc các điều khoản thiết kế/inference | Khớp `ffaf239a000fc299a8e31c5eaf82aeb3a86a78b9ef086d222cc0538be5dc42ed`. Primary A1–G; ablation A1–A0; supporting A0–G. |
| `experiments/e1_pre_v2/config.yaml` | Tính raw Git SHA-256 | Khớp config identity `5ce81a22cf4cbb828f9d20a1698934fa8add4697076d13b4dfd2a989754ed5cd`. |
| `closure-pilot-final.receipt.json`, `closure-parent-final.receipt.json` | Đối chiếu source/integration/protocol, exit, thời gian, real-call count với `final-evidence.json` | MOCK pilot 9/9 và full 144/144 terminal; exit 0, source drift false, zero real calls; 52.015 s và 416.140 s. |
| `closure-critical-final.tests.json` và receipt tương ứng | Đếm test IDs duy nhất và kết quả | 129 unique successful IDs; 129 PASS, zero fail/error/skip. |
| `regression-reconciled.json` | Đọc module/test counts, missingness và loại execution | PARTIAL: 103/109 modules, 1,400 PASS, 21 SKIP, 6 RESOURCE_BLOCKED; 1,421 tests started. Composite inventory; single full invocation vẫn FAIL do resource missingness. |
| `release-gates.json` | Đọc quyết định chính thức tại baseline | ENGINEERING_PARTIAL; SCIENTIFIC_SCORING_NOT_EVALUABLE; SUBMISSION_RC_BLOCKED. |
| `owner_evaluation_registry.json` | Parse JSON, đếm contracts | 0 contracts; không diễn giải thành 0% clinical accuracy. |
| `KOA_FINAL_ENGINEERING_AND_RESEARCH_CLOSURE.md` | Đối chiếu narrative với các receipt trên | Cùng số liệu/quy ước; chất lượng độc lập 0/16 eligible, provider thật NOT_EXECUTED cho E1-v2. |
| Public docs: `current-results.md`, `research-overview.md`, `experimental-design.md`, `benchmark.md`, `references.md`, `reproducibility.md` | Đọc các claims, bibliography metadata và boundaries liên quan | Số liệu cốt lõi đồng nhất; các điểm cần hiệu chỉnh thuật ngữ được ghi bên dưới. |

Source identity trong các receipt: `5aa87228b07ead1c4ecde48e7330e62771a86dbed7ac0fc4097f50152d306f5b`; integration identity: `0155dc81df270dc5b6413ce6587aa52ed69e3cb7f415cd5146bf1188431ac927`. Receipt capture ghi HEAD lịch sử `49f240…` khi có thay đổi chưa commit. Việc so sánh map từng blob ở trên xác nhận baseline `ac4ade7…` chứa đúng nội dung đã qualification; không đồng nhất hai Git commit chỉ bằng tên gọi.

Kiểm tra số học bằng Python standard library: **10/10 điều kiện đúng**: tổng nguồn 276; 16×3×3=144; 16×3=48; 3×1×3=9; 5×2=10 appearances; 103+6=109; 1,400+21=1,421; pilot ceiling 323; full ceiling 4,944; 129 critical IDs duy nhất. Đây là kiểm tra tài liệu/receipt, không phải chạy lại runtime test suite.

## Checklist khoa học cho hai artifact

| Nội dung bắt buộc | Kết luận nguồn | Điều kiện nghiệm thu bản cuối |
|---|---|---|
| Tác giả và đơn vị | Contract: Phạm Hồng Đăng Khoa; Nguyễn Hoàng Khang; Trường Đại học Tôn Đức Thắng / Ton Duc Thang University | Giữ nguyên dấu/tên; không thêm supervisor, student IDs hoặc university endorsement. |
| Benchmark và đơn vị đếm | rc0.2.0; 5 nguồn, 276 EvidenceUnits, 170 SemanticIntent metadata; Task C 16 English DEV; Task B 5 pairs/9 distinct bundles/4 intents | Không gọi 170 scored questions hoặc 21 independent clinical questions; không gán 4 Task B intents cho toàn bộ Task C. |
| A0/A1/G | A0 Plan+E0; A1 Question+same Plan+same E0; G Question+E0+SourcePolicy+generic gaps, không Plan ở PRE nhưng có shared Plan downstream | Primary A1–G; ablation A1–A0; giữ causal caveat cho hai policy bundles A1/G. |
| Replication và lịch chạy | 48 shared preparations, 144 arm cells; six rotating permutations | Question-level aggregation; nested replicates. Không gọi randomization hoặc khẳng định clinical independence đã được thiết lập. |
| Agentic workflow | PRE, bounded correction, PRE recheck; generation/decomposition; POST; memory-only bounded revision và POST mới | Sơ đồ phải giữ correction≤1, revision≤1, guard deterministic và ba terminal outcomes; technical failure khác ABSTAIN. |
| Gold separation | Method tự dự đoán nghĩa vụ từ câu hỏi; benchmark canonical obligations/evaluator ngoài runtime | Không có mũi tên gold/evaluator vào Planner, PRE, Generator hoặc policy. Task B labels không chuyển sang E0/E1 động. |
| Ý nghĩa kết quả | MOCK/qualification là bằng chứng kỹ thuật | Không vẽ biểu đồ clinical accuracy từ test passes, không suy ra parity/superiority từ symmetric fake counts. |
| Evaluation status | E1-v2 real provider NOT_EXECUTED; independent quality NOT_EVALUABLE; 0/16 eligible public items | Không đổi 0/16 thành zero accuracy, không khái quát NOT_EXECUTED cho mọi historical E1 LIVE run. |
| Regression | 103/109 modules; 1,400 PASS; 21 SKIP; 6 RESOURCE_BLOCKED | Luôn giữ nhãn PARTIAL/composite; không tuyên bố full suite all green. |
| Giới hạn | DEV tuning, related cases, planner sensitivity, bundled A1/G differences, missing independent scoring, unverified redistribution rights | Không claim safety, cost saving, bilingual consistency hoặc working Jev integration. |
| Next milestone | Sáu module native đang RESOURCE_BLOCKED tại baseline | Ghi một milestone kế tiếp; LIVE và owner scoring là công việc có gate riêng, không được xem là đã được task này cấp quyền. |

## Các vấn đề ở tài liệu nền cần tránh truyền sang bản mới

Các vấn đề sau được ghi nhận để người biên soạn sửa trong phạm vi artifact mới; reviewer không sửa sáu tài liệu nền.

1. **`docs/reproducibility.md:46`: thuật ngữ “block-randomized”.** Baseline protocol chỉ định sáu permutations xoay vòng trên sorted blocks. Dùng “shared-preparation blocked design with deterministic counterbalancing”; không tuyên bố randomization. Contract giữa kỳ đã diễn đạt đúng.
2. **`docs/reproducibility.md:28`: sai đường dẫn config.** Hash `5ce81a…` thuộc `experiments/e1_pre_v2/config.yaml`; không có `experiments/e1_pre_v2/config.json` ở baseline.
3. **`docs/reproducibility.md:34`, `docs/benchmark.md:32`: cần phân biệt assignment digest và file digest.** `987f2b…` là digest của typed DEV recovery-record projection, theo `benchmarks/dev_e1.py:172`; không phải raw SHA-256 của file Python đó. Gọi “typed DEV assignment digest”.
4. **`docs/experimental-design.md:49`: “independent statistical unit”.** Protocol quy định question-level aggregation; không xác lập clinical independence của 16 DEV cases. Dùng “question-level aggregation unit; replicates nested within questions”. Contract đã có caveat phù hợp.
5. **`docs/experimental-design.md:101`: phrasing “16 questions across 4 ... intents in Task B”.** Bốn intents được xác nhận cho Task B; không suy ra tổng hoặc sự phân bố intents của Task C. Contract đã tách rõ.
6. **`docs/current-results.md:31`: “compiled controller”.** Nên gọi implemented/native runtime controller; receipt không chứng minh một compiler build. Đây là vấn đề từ ngữ nhỏ, không thay đổi kết quả qualification.
7. **Research-gap claims trong `docs/research-overview.md:21–25`.** Các từ như “typically” và “rarely” không được kiểm chứng bằng một systematic literature review trong task này. Bản giữa kỳ nên so sánh cụ thể các công trình được trích và trình bày proposed design focus, không tuyên bố mọi nghiên cứu trước đều thiếu guard/obligation verification.

Không thấy bằng chứng hỗ trợ A1 superiority. Không có lỗi số học cốt lõi trong các số liệu baseline đã kiểm tra.

## Những việc chưa thực hiện

- Chưa kiểm tra báo cáo DOCX/PDF và deck PPTX/PDF cuối cùng, captions, diễn giải sơ đồ hoặc speaker notes; đang chờ draft.
- Chưa kiểm chứng website/paper metadata trực tuyến hoặc đọc full text các công trình tham chiếu; không gọi bibliography này là một kiểm chứng literature độc lập.
- Không đọc raw corpus để tái đếm; corpus/task cardinalities được kiểm tra ở cấp protocol/aggregate closure/public documentation.
- Không chạy lại clinical evaluation, provider probe, paid inference, native tests hoặc full regression.
- Không thẩm định chất lượng lâm sàng, legal rights hoặc tính hiện hành của guideline. CURRENT/HISTORICAL chỉ là frozen-registry metadata.

## Kết luận tạm thời

**Baseline claims: supported with the qualifications above. Final artifact review: pending.** Chỉ có bằng chứng kỹ thuật và thiết kế prospective tại snapshot này; chưa có kết luận comparative clinical quality. Bước tiếp theo trong chính task biên soạn là đối chiếu report/slide hoàn chỉnh với checklist và contract, sau đó cập nhật kết luận của file này.
## Rà soát hiện vật cuối ngày 22/10/2026

**Kết luận: supported with stated limitations; không còn blocker nội dung khoa học trong bộ hiện vật cuối đã kiểm tra.** Mục bổ sung này hoàn tất phần đối chiếu artifact đang ghi pending ở trên. Bằng chứng baseline và các giới hạn của lần xác minh trước được giữ nguyên; reviewer hiện tại không tái thực hiện những kiểm tra Git blob, receipt hay runtime test đó.

### Phạm vi thực sự đã rà soát

Reviewer đọc toàn bộ `report/midterm/report-content.md`, trích nội dung OOXML của DOCX và PPTX bằng Python standard library, trích PDF bằng PyMuPDF, đọc toàn bộ `slides/midterm/speaker-notes.md` và đối chiếu nội dung theo `content-contract.md`. Bộ cuối là `KOA_Midterm_Report_TDTU.docx/.pdf` và `KOA_Midterm_Presentation_TDTU.pptx/.pdf`; candidate dưới `_build/` chỉ là phiên bản trung gian.

Đã xem hình nghiên cứu 01–05 dùng trong báo cáo; các slide 5, 7–11, 13 liên quan đến ranh giới dữ liệu, vòng phản hồi, thiết kế và kết quả; sau sửa, xem lại trang PDF báo cáo 9/17/26/27 và slide 11. Đây là rà soát nội dung khoa học giữa hiện vật, không thay thế kiểm tra toàn bộ bố cục của người biên soạn hoặc thẩm định lâm sàng độc lập. Không đọc kho nghiên cứu gốc trong lượt này, không truy cập gold/evaluator internals, không gọi mạng/provider và không chạy thí nghiệm.

### Đối chiếu claim giữa báo cáo và deck

| Nội dung | Bằng chứng cụ thể trong bộ cuối | Kết luận |
|---|---|---|
| RQ và phạm vi suy luận | Báo cáo §1.3, §5.2, §8.2; slide 4 và notes | A1–G là primary giữa hai policy bundles; A1–A0 là question-visibility ablation với cùng FULL instruction/schema/gating; A0–G là supporting. Chưa có comparative clinical-quality conclusion. |
| Corpus và tác vụ | Báo cáo §3.1–3.6, Bảng 3.1–3.2; slide 5–7 | 5 nguồn/276 EvidenceUnits; 170 SemanticIntent là metadata. Task B: 5 pairs, 10 appearances, 9 distinct bundles, 4 intents; Task C: 16 English Recovery DEV cases. Không gộp thành 21 câu hỏi độc lập hoặc chuyển Task B gold sang E0/E1 động. CURRENT/HISTORICAL được giới hạn ở frozen registry. |
| G và chuẩn bị dùng chung | `report-content.md:294`, §4.6, §5.3–5.4; slide 11 và notes | G không nhận Plan ở PRE; vẫn nhận đúng shared Plan ở downstream. Planner/initial retrieval dùng chung mỗi question–replicate block, không phải ba Plan độc lập. |
| PRE và correction | Báo cáo §4.3, §4.6, §4.15; slide 8–9 và notes | FULL gate bao gồm mọi planned obligation kể cả optional; correction ≤1, merge E0/E1, PRE recheck bắt buộc. Không có đường correction đi tắt vào Generator. |
| POST và revision | Báo cáo §4.8–4.12, §4.16; slide 8/10 và notes | Claim decomposition, staged POST v4 pair/diagnosis/remedies, canonical checks. Revision ≤1 chỉ dùng memory hiện có, hủy claims/POST cũ và chạy decomposition/POST mới. |
| Control plane và terminal | Báo cáo §4.14 và Phụ lục C; slide 8/10 | Policy đề xuất, deterministic PolicyGuard cấp quyền, executor thực thi. ACCEPT=COMPLETED_ANSWER; ABSTAIN=COMPLETED_ABSTAIN; lỗi provider/retrieval/schema/guard thuộc FAILED_*. Confidence không vượt hard guard; Jev chỉ tùy chọn/waitlist. |
| Đơn vị đếm và thiết kế | Báo cáo §5.4–5.7; slide 11–12 và notes | 16×3=48 shared preparations, 48×3=144 arm cells. Sáu permutations xoay vòng xác định, tám block mỗi permutation; không phải randomization. Question-level aggregation với nested replicates; chưa xác lập clinical independence. |
| Phân tích dự kiến | Báo cáo §5.5–5.7; notes slide 12 | Paired question-cluster bootstrap 20.000 resamples, seed 401, percentile 95% chỉ cho qualified LIVE đủ gates. Chưa chạy bootstrap; MOCK contrasts/CIs null. Missing/UNATTEMPTED không đổi thành ABSTAIN. |
| Qualification và chất lượng | Bảng 6.1, §6.3/6.5, §8.2; slide 13–15 và notes | MOCK pilot 9/9, full 144/144; 129 critical PASS. Regression vẫn PARTIAL/composite: 103/109 modules, 1.400 PASS, 21 SKIP, 6 RESOURCE_BLOCKED. Symmetric fake outcomes không chứng minh parity/superiority. E1-v2 REAL PROVIDER NOT_EXECUTED; quality NOT_EVALUABLE; 0/16 là eligibility, không phải accuracy. |
| Cấu hình, trần và giới hạn | Báo cáo §4.4/4.13, §6.5–6.6, §7.1; slide 12/14 và notes | MedCPT/FAISS IndexFlatIP, 276×768, float32 CPU, top-k 8, no reranker; trần 34 physical LLM requests/cell +1 shared Planner/block không phải measured typical cost. Giữ DEV iteration/planner/language/bundled-policy caveats và giới hạn redistribution UNVERIFIED. |
| Trích dẫn | Báo cáo Chương 2 và 17 mục [1–13], [P1–P4]; source lists trong notes | Các công trình được dùng làm cơ sở thiết kế, không thành bằng chứng superiority của KOA. Guideline versions được đọc theo frozen registry. Đối chiếu với contract/local bibliography; không phải xác minh full text hoặc website độc lập. |

### Vấn đề phát hiện và đã đóng trước verdict

1. **Slide 11, ký pháp mẫu số.** Candidate ghép “16 câu hỏi × 3 replicates = 48 preparations × 3 arms = 144 cells”, tạo chuỗi đẳng thức sai. Bản PPTX/PDF cuối đã tách hai đẳng thức đúng: `16×3=48 preparations` và `48 preparations×3 arms=144 cells`. Đã kiểm tra text và ảnh final; số lượng nghiên cứu không đổi.
2. **Provenance trong Hình 1.1 và 3.1.** `01-research-framework.svg:297` và `04-benchmark-evaluation-boundary.svg:191` từng gọi scientific source identity `5aa87228b...` là release SHA; SVG04:57 và MMD04:6 còn gọi là commit. Bản sửa dùng release manifest SHA-256 `eda0e26c...`, nhất quán với contract/Phụ lục A. Đã kiểm tra SVG/MMD, PNG mới nhúng trong DOCX và hình trên PDF cuối. Đây là hiệu chỉnh nhãn provenance, không đổi dataset, protocol, phương pháp hoặc kết quả nghiên cứu.
3. **Terminal labels trong Hình 3.1.** SVG04:145 từng trộn `ACCEPT` với `COMPLETED_ABSTAIN` dưới nhãn terminal status. Bản cuối thống nhất `COMPLETED_ANSWER | COMPLETED_ABSTAIN | FAILED_*`. Đây là sửa thuật ngữ ánh xạ, không đổi controller behavior.

Các chỉnh bố cục cuối chỉ dời tag Fresh Decomposition/POST của SVG02 khỏi Reviser, bỏ header ngoài vùng focus của ảnh detail và đưa nhãn Air-gap của SVG04 vào đúng wall; không đổi connector, gate, nguồn dữ liệu hoặc kết quả. Đã xem lại detail PRE/POST ở PDF trang 26/27 và wall ở trang 17. Metadata Title/Author của PPTX cũng đã khớp tên dự án và hai tác giả; đây không phải thay đổi khoa học.

### Kiểm tra đã thực hiện và kết quả

- Đối chiếu văn bản chuẩn hóa khoảng trắng: cả DOCX và PDF báo cáo đều chứa đủ **156 đoạn văn, 200 ô bảng và 17 mục bibliography** từ Markdown; không có mục thiếu trong phép kiểm này.
- PPTX cuối có **15 slides**, PDF có **15 trang**; **233 native text runs** đều hiện diện trong trang PDF tương ứng. Cả **15 đoạn thuyết trình chính** và **53 source entries** của notes hiện diện trong notes OOXML của slide tương ứng.
- DOCX chứa đúng bytes của cả **5 PNG hình nghiên cứu** hiện hành. PDF chuyển đổi/downsample ảnh nên không dùng phép so sánh bytes để kết luận đồng nhất PDF; các sửa label ở trang 9/17 được kiểm tra bằng ảnh trang thực tế.
- Python kiểm tra số học/timing **10/10 điều kiện đúng**: tổng nguồn 276; 16×3=48; 16×3×3=144; 6×8=48; 2×8=16 appearances/arm/position; 5×2=10 Task B appearances; 103+6=109; 1.400+21=1.421; 15 timing entries; tổng notes 1.115 giây = **18 phút 35 giây**.
- Các con số 129 PASS và regression trong tài liệu vẫn là bằng chứng receipt baseline, **không phải tests reviewer vừa chạy**. Không chạy lại native/regression/clinical evaluation, bootstrap, provider qualification, paid inference hoặc kiểm chứng literature trực tuyến.

### Định danh hiện vật đã rà soát

| Hiện vật | SHA-256 |
|---|---|
| `report/midterm/KOA_Midterm_Report_TDTU.docx` | `362c547b492f812664ffe0e7e18b8f62ea6290b464e27f22f5995657a504f8f0` |
| `report/midterm/KOA_Midterm_Report_TDTU.pdf` | `4fbb660e00f3a5ce6f6ee4a2edcf16b26d0e33deab55956bdc6e84c1882be827` |
| `slides/midterm/KOA_Midterm_Presentation_TDTU.pptx` | `840ea23e7ca0bb32f59e224ea2416f3a64d93551ab5b6a65714f1be1cc9f71e4` |
| `slides/midterm/KOA_Midterm_Presentation_TDTU.pdf` | `6f710226d2012891e2ceae15ce054d5f6314add4d16ee9da4e6e28fbcf114567` |
| `report/midterm/report-content.md` | `d468f7a2f941b0a780306216254ca2d862a710d4c0c442ca7e93afa361bef9ee` |
| `slides/midterm/speaker-notes.md` | `b315f8275a36f82dacde83f95c596ee3de6d4143f9a3f2cb0d9c93ef81f95002` |

**Verdict cuối cho nội dung:** bộ báo cáo/deck hỗ trợ cách trình bày tiến độ framework và qualification kỹ thuật tại baseline, giữ RQ1–RQ3 ở trạng thái chưa được trả lời bằng quality evaluation. Không còn correction khoa học phải chờ trong các hiện vật gắn hash trên. Giới hạn chưa đổi: chưa có E1-v2 real-provider execution, độc lập clinical scoring, verified guideline redistribution hoặc kết luận safety/cost/bilingual superiority. Mốc nghiên cứu/kỹ thuật kế tiếp được tài liệu chỉ ra vẫn là hoàn tất sáu native modules RESOURCE_BLOCKED trên host đủ tài nguyên; task review này không thực thi hay cấp thêm quyền cho mốc đó.
