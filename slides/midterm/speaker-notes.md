# Ghi chú thuyết trình giữa kỳ KOA Agentic-RAG System

Ngôn ngữ: tiếng Việt. 15 slide. Thời lượng dự kiến: 18 phút 35 giây.
Scientific snapshot: `ac4ade796e56377882b8069d0fb7a14809e8180b`.
Scientific source SHA-256: `5aa87228b07ead1c4ecde48e7330e62771a86dbed7ac0fc4097f50152d306f5b`.
Integration SHA-256: `0155dc81df270dc5b6413ce6587aa52ed69e3cb7f415cd5146bf1188431ac927`.
Protocol: `e1-v2.refined-full-primary.v2`. Lock SHA-256: `98ad86c861986f3794d9b5818cafe44d396967340faf3631d6fb06d91006e5a3`.
Đây là tài liệu trình bày tiến độ tại baseline đã nêu, không phải kết quả thí nghiệm mới. Ngày biên soạn không thay đổi scientific snapshot.

## Slide 01. KOA Agentic-RAG System

**Thời lượng gợi ý:** 00:40

Báo cáo trình bày tiến độ của KOA Agentic-RAG System theo snapshot khoa học ac4ade7. Mục tiêu là một prototype truy xuất và kiểm chứng bằng chứng từ guideline thoái hóa khớp gối. Phần chính tập trung vào thiết kế framework, ranh giới benchmark, cơ chế PRE/POST và protocol E1-v2. Các kết quả hiện có là qualification kỹ thuật offline với MOCK. Chất lượng lâm sàng và ưu thế giữa các nhánh vẫn chưa có kết luận. Logo lấy nguyên bản từ website chính thức TDTU. Bố cục này là TDTU-inspired academic theme, chưa có căn cứ gọi là template chính thức của trường.

**Nguồn:**

- docs/midterm/content-contract.md (scientific baseline ac4ade796e56377882b8069d0fb7a14809e8180b)
- Logo official, unaltered: https://www.tdtu.edu.vn/sites/www/files/logo_2.png; source page https://www.tdtu.edu.vn/; retrieved 2026-10-21. Design colors are choices, not official brand specifications.

## Slide 02. Yêu cầu của QA trên guideline KOA

**Thời lượng gợi ý:** 01:05

Một đoạn được truy xuất có thể liên quan đến câu hỏi nhưng chưa đủ để tạo câu trả lời có căn cứ. Trong đề tài, yêu cầu cần tách thành phạm vi nguồn, nghĩa vụ thông tin và hỗ trợ ở mức phát biểu. Ví dụ về mặt cấu trúc, khi câu hỏi có nhiều phần, hệ thống phải xem bằng chứng có bao phủ từng phần hay không. Đây là ví dụ về hợp đồng thông tin, không đưa ra hướng dẫn điều trị. Framework vì vậy đặt một cổng trước khi sinh để xét mức đủ bằng chứng và một cổng sau khi sinh để xét nội dung câu trả lời. Quyết định chấp nhận nội bộ vẫn cần đánh giá độc lập nếu muốn kết luận về chất lượng lâm sàng.

**Nguồn:**

- docs/midterm/content-contract.md (scientific baseline ac4ade796e56377882b8069d0fb7a14809e8180b)
- Lewis et al. Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks. NeurIPS 2020. https://arxiv.org/abs/2005.11401
- Xiong et al. Benchmarking Retrieval-Augmented Generation for Medicine. Findings ACL 2024:6233-6251. https://aclanthology.org/2024.findings-acl.372/

## Slide 03. Cơ sở phương pháp và khoảng trống thiết kế

**Thời lượng gợi ý:** 01:05

RAG cung cấp nền tảng truy xuất kết hợp sinh. Self-RAG cho thấy cách đưa phản tư vào quyết định truy xuất và sinh. Corrective RAG gợi ý đánh giá chất lượng bằng chứng và cơ chế truy xuất điều chỉnh. FActScore đặt trọng tâm vào từng phát biểu nguyên tử. Đề tài sử dụng các hướng này làm cơ sở thiết kế, rồi nối nghĩa vụ từ câu hỏi với kiểm tra bằng chứng trước khi sinh và hỗ trợ claim sau khi sinh. Phần bổ sung là hợp đồng kiểu dữ liệu và guard xác định cho hành động. Đây là mục tiêu thiết kế của nghiên cứu, chưa phải kết luận rằng hệ thống mới hơn hoặc tốt hơn những phương pháp đã công bố.

**Nguồn:**

- docs/midterm/content-contract.md (scientific baseline ac4ade796e56377882b8069d0fb7a14809e8180b)
- Lewis et al. Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks. NeurIPS 2020. https://arxiv.org/abs/2005.11401
- Asai et al. Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection. ICLR 2024. https://arxiv.org/abs/2310.11511
- Yan et al. Corrective Retrieval Augmented Generation. 2024 preprint. https://arxiv.org/abs/2401.15884
- Min et al. FActScore: Fine-grained Atomic Evaluation of Factual Precision in Long Form Text Generation. EMNLP 2023. https://aclanthology.org/2023.emnlp-main.741/

## Slide 04. Câu hỏi nghiên cứu và đóng góp dự kiến

**Thời lượng gợi ý:** 01:15

RQ1 là so sánh chính giữa A1 và G. Hai nhánh khác nhau theo cả gói policy PRE, gồm biểu diễn, readiness gating và cách tạo truy vấn bổ sung. Vì vậy không diễn giải thành tác động nhân quả của một thành phần riêng lẻ. RQ2 so sánh A1 và A0 để khảo sát việc hiển thị câu hỏi gốc tại PRE khi giữ cùng Plan, E0, instruction, schema và gating. Readiness là hành vi của controller, không phải độ chính xác lâm sàng. RQ3 giữ vai trò hỗ trợ giữa A0 và G. Các đóng góp dự kiến kết nối hợp đồng dữ liệu, kiến trúc kiểm chứng hai giai đoạn và kiểm soát hành động với protocol có thể kiểm toán. Tất cả vẫn là câu hỏi và đóng góp cần đánh giá.

**Nguồn:**

- docs/midterm/content-contract.md (scientific baseline ac4ade796e56377882b8069d0fb7a14809e8180b)
- docs/experimental-design.md; assets/diagrams/05-experimental-arms.svg/.mmd

## Slide 05. Khung nghiên cứu tổng thể

**Thời lượng gợi ý:** 01:10

Sơ đồ này là bản trình bày native, rút gọn từ hình research framework đã xác minh. Bên trái là nguồn guideline và KOA-GuidelineBench với quy trình quản trị riêng. Ở giữa là phương pháp DV-OGEC-RAG, chỉ nhận các trường runtime nằm trong allowlist. Kết quả đi sang phía đánh giá độc lập cùng thông tin truy vết. Canonical obligations, đáp án tham chiếu và nhãn đánh giá không đi vào suy luận. Task B xét các bundle đã hiển thị cố định. Task C thực hiện truy xuất trên corpus rồi kiểm tra bằng chứng động. Hai task có hợp đồng khác nhau. Việc nối benchmark với runtime không chuyển quyền sở hữu hoặc quyền truy cập đối với tài sản evaluator của benchmark.

**Nguồn:**

- docs/midterm/content-contract.md (scientific baseline ac4ade796e56377882b8069d0fb7a14809e8180b)
- assets/diagrams/01-research-framework.svg/.mmd; native editable derivative retaining runtime/evaluator separation.

## Slide 06. Corpus và hợp đồng tác vụ

**Thời lượng gợi ý:** 01:15

Corpus rc0.2.0 gồm năm nguồn và 276 EvidenceUnits. Tổng số theo nguồn là 32, 39, 24, 84 và 97. Phiên bản EULAR là bản cập nhật 2023 công bố năm 2024. CURRENT và HISTORICAL chỉ mô tả frozen source registry, không phải đánh giá trực tiếp tính hiện hành của khuyến cáo y khoa hôm nay. Có 170 SemanticIntent metadata records, không phải 170 câu hỏi đã chấm. Task B gồm năm cặp, mười lượt xuất hiện bundle và chín bundle riêng thuộc bốn intents. Bốn intents này chỉ thuộc phạm vi Task B. Task C có 16 ca DEV tiếng Anh cho nghiên cứu E1-v2. Không cộng hai task thành 21 câu hỏi độc lập. rc0.2.0 hiện là internal review candidate, public_release=false.

**Nguồn:**

- docs/midterm/content-contract.md (scientific baseline ac4ade796e56377882b8069d0fb7a14809e8180b)
- ACSQHC registry: https://www.safetyandquality.gov.au/resources/osteoarthritis-knee-clinical-care-standard-2024
- BYT registry metadata: https://kcb.vn/van-ban/huong-dan-chan-doan-va-dieu-tri-cac-benh-co-xuong-khop.html
- EULAR: https://doi.org/10.1136/ard-2023-225041
- NICE: https://www.nice.org.uk/guidance/ng226/
- VA/DoD frozen registry 2026: https://www.healthquality.va.gov/HEALTHQUALITY/guidelines/CD/OA/index.asp

## Slide 07. Ranh giới dữ liệu và chống rò rỉ đánh giá

**Thời lượng gợi ý:** 01:05

BA1-D1 giữ canonical benchmark obligations ở ngoài runtime, còn BA1-D2 chia dữ liệu theo ba mức hiển thị. Cột runtime bao gồm câu hỏi, source scope, evidence hợp lệ và thông tin trích dẫn. Hai cột còn lại là các loại dữ liệu evaluator và audit, chỉ trình bày tên loại, không trình bày nội dung hạn chế. Planner phải dự đoán MaterialObligation từ chính văn bản câu hỏi. Cơ chế input allowlist loại gold và evaluator internals khỏi suy luận. Ngoài ra, nhãn sufficiency của Task B chỉ áp dụng cho bundle cố định của task đó. Không thể lấy nhãn này làm gold cho E0 hoặc E1 được truy xuất động trong E1-v2. Đánh giá độc lập cần một EvaluationContext được cấp quyền riêng.

**Nguồn:**

- docs/midterm/content-contract.md (scientific baseline ac4ade796e56377882b8069d0fb7a14809e8180b)
- assets/diagrams/04-benchmark-evaluation-boundary.svg/.mmd; native editable derivative.

## Slide 08. Kiến trúc DV-OGEC-RAG

**Thời lượng gợi ý:** 01:40

DV-OGEC-RAG viết đầy đủ là Dual-Verification Obligation-Guided Evidence-Controlled RAG. Planner nhận câu hỏi và tạo Plan có kiểu, sau đó đóng băng plan identity. Retrieval cục bộ lấy E0 với source filtering trước scoring và lưu provenance trong EvidenceMemory. PRE kiểm tra mức đủ bằng chứng. Nếu thiếu và còn ngân sách, controller cho truy xuất bổ sung tối đa một lần, hợp nhất memory rồi bắt buộc kiểm tra PRE lại. Chỉ PRE đạt mới cho Generator hoạt động. Candidate đi qua Claim Decomposer và staged POST v4. Nếu POST yêu cầu sửa và cho phép sửa, Reviser dùng memory hiện có, tối đa một lần. Hệ thống hủy claims và POST cũ, phân rã và kiểm tra lại. Mỗi hành động có hiệu lực đều qua control plane xác định. ACCEPT, ABSTAIN và FAILED là các loại kết thúc khác nhau, sẽ nói rõ ở slide sau.

**Nguồn:**

- docs/midterm/content-contract.md (scientific baseline ac4ade796e56377882b8069d0fb7a14809e8180b)
- docs/system-architecture.md; assets/diagrams/02-agentic-rag-architecture.svg/.mmd
- docs/agentic-workflow.md; assets/diagrams/03-controller-state-machine.svg/.mmd
- Native editable derivative of verified Figures 02 and 03. Feedback bounds are upper limits, not mandatory steps.

## Slide 09. PRE và vòng truy xuất bổ sung

**Thời lượng gợi ý:** 01:30

Với A0 và A1, PRE trả observation có cấu trúc theo từng obligation. Reducer xác định READY khi mọi nghĩa vụ được COVERED, nguồn hợp lệ và không còn discrepancy chưa giải quyết. Mọi nghĩa vụ trong Plan đều tham gia cổng FULL, kể cả nghĩa vụ planner gắn optional. G dùng boolean sufficiency và generic gaps theo hợp đồng riêng. Nếu chưa đủ và còn lượt, query builder xác định tạo truy vấn theo obligation cho A0/A1 hoặc theo gap cho G. Sau corrective retrieval, E1 hợp nhất vào E0 và PRE phải kiểm tra lại. Không có đường từ corrective retrieval bỏ qua recheck để vào Generator. Nếu cổng vẫn thiếu, controller xin phép ABSTAIN qua guard. Lỗi schema hoặc lỗi truy xuất đi sang FAILED, không tự đổi thành abstention.

**Nguồn:**

- docs/midterm/content-contract.md (scientific baseline ac4ade796e56377882b8069d0fb7a14809e8180b)
- docs/agentic-workflow.md; assets/diagrams/03-controller-state-machine.svg/.mmd
- assets/diagrams/02-agentic-rag-architecture.svg/.mmd and 03-controller-state-machine.svg/.mmd, native PRE detail.

## Slide 10. POST, revision và PolicyGuard

**Thời lượng gợi ý:** 01:30

Generator tạo candidate có citations phân giải được trong memory, rồi Decomposer tạo claims nguyên tử có kiểu. POST v4 có các bước pair, diagnosis và remedies, tiếp theo là canonical validation xác định. Cổng chấp nhận đòi hỏi mọi claim SUPPORTED, nghĩa vụ ADDRESSED, nguồn và provenance hợp lệ, không có hard failure. Khi NEEDS_REVISION và còn lượt sửa, Reviser chỉ dùng EvidenceMemory hiện có. Không truy xuất trong revision. Claims và POST cũ bị hủy, câu trả lời mới phải qua decomposition và POST mới. Control plane gồm ValidActionSet, deterministic RulesPolicy, PolicyGuard và Executor. Guard kiểm tra mọi action có hiệu lực, không chỉ ACCEPT. ACCEPT ánh xạ COMPLETED_ANSWER, ABSTAIN ánh xạ COMPLETED_ABSTAIN. Lỗi provider, schema, retrieval hoặc guard rejection là FAILED_*, tách khỏi abstention. Model confidence không được vượt hard guard.

**Nguồn:**

- docs/midterm/content-contract.md (scientific baseline ac4ade796e56377882b8069d0fb7a14809e8180b)
- docs/agentic-workflow.md; assets/diagrams/03-controller-state-machine.svg/.mmd
- Kamath et al. Selective Question Answering under Domain Shift. ACL 2020. https://aclanthology.org/2020.acl-main.503/
- Terminal mapping: ACCEPT=COMPLETED_ANSWER; ABSTAIN=COMPLETED_ABSTAIN; technical errors=FAILED_*. Guard rejection is FAILED_CONTRACT.

## Slide 11. Thiết kế ba nhánh E1-v2

**Thời lượng gợi ý:** 01:40

Mỗi question-replicate block gọi Planner và initial retrieval một lần, khóa cùng Plan, E0 và source scope trước khi chia ba nhánh. A0 thấy Plan và E0 tại PRE nhưng không thấy câu hỏi gốc. A1 thêm câu hỏi gốc với cùng FULL instruction, schema và gating. G thấy câu hỏi, E0, public SourcePolicy và prior generic gaps, không nhận Plan ở PRE. Sau PRE, G nhận lại chính Plan chung cho generation, decomposition, POST, revision và guard. So sánh chính là A1 với G, ablation là A1 với A0, hỗ trợ là A0 với G. Protocol dùng sáu hoán vị thứ tự luân phiên, mỗi hoán vị tám block. Đây là counterbalancing xác định. Phân tích tổng hợp theo câu hỏi với replicates lồng bên trong, không coi 144 cells là 144 câu hỏi. A1/G là so sánh cả gói policy.

**Nguồn:**

- docs/midterm/content-contract.md (scientific baseline ac4ade796e56377882b8069d0fb7a14809e8180b)
- docs/experimental-design.md; assets/diagrams/05-experimental-arms.svg/.mmd
- Native table derived from assets/diagrams/05-experimental-arms.svg/.mmd. Planned comparisons remain unexecuted on real providers at admitted baseline.

## Slide 12. Triển khai và khả năng tái lập

**Thời lượng gợi ý:** 01:15

Retrieval chạy cục bộ với hai encoder MedCPT đã pin và FAISS IndexFlatIP. Index có 276 vectors, 768 chiều, float32 CPU, top-k bằng tám và không dùng reranker. Source filtering diễn ra trước scoring. Các vai trò giao tiếp qua contracts có kiểu, còn RunStore giữ version identities và provenance để tái lập. Budget được reserve trước request dispatch. Một cận trên của pipeline là 34 physical LLM requests mỗi arm cell, cộng một Planner request dùng chung mỗi block. Đây là trần accounting, không phải chi phí thông thường đã đo. Jev vẫn tùy chọn và waitlist, nằm ngoài integration và kết quả đủ điều kiện. Protocol dự kiến bootstrap question-cluster 20.000 lần, seed 401, nhưng chỉ cho qualified LIVE đủ gates. MOCK có contrasts và confidence intervals bằng null.

**Nguồn:**

- docs/midterm/content-contract.md (scientific baseline ac4ade796e56377882b8069d0fb7a14809e8180b)
- docs/system-architecture.md; assets/diagrams/02-agentic-rag-architecture.svg/.mmd
- docs/experimental-design.md; assets/diagrams/05-experimental-arms.svg/.mmd
- Jin et al. MedCPT: Contrastive Pre-trained Transformers with Large-scale PubMed Search Logs for Zero-shot Biomedical Information Retrieval. Bioinformatics 2023;39(11):btad651. https://doi.org/10.1093/bioinformatics/btad651
- Johnson et al. Billion-Scale Similarity Search with GPUs. IEEE TBD 2021;7(3):535-547. https://arxiv.org/abs/1702.08734
- Planned bootstrap is not executed for this authoring task. No dependency installation or model/provider calls.

## Slide 13. Kết quả kỹ thuật tại baseline ac4ade7

**Thời lượng gợi ý:** 01:35

Bảng là các receipt đã có tại baseline, không phải tests chạy lại khi làm slide. MOCK pilot hoàn tất chín trên chín cells với ba preparations. MOCK full hoàn tất 144 cells với 48 preparations. Fake SDK điều khiển nhánh correction và revision trên retrieval và controller thật. Counts đối xứng giữa các nhánh được script sẵn, không chứng minh ngang bằng hoặc ưu thế về y khoa. Critical selection có 129 trên 129 PASS, không fail, error hoặc skip. Regression là composite PARTIAL với 103 trên 109 modules, 1.400 PASS, 21 SKIP và sáu modules chưa chạy vì resource admission. SKIP không phải PASS. E1-v2 real provider vẫn NOT_EXECUTED. Clinical-quality scoring là NOT_EVALUABLE vì có 0 trên 16 public items đủ điều kiện, không phải độ chính xác 0 phần trăm. Không có biểu đồ chất lượng lâm sàng từ số test này.

**Nguồn:**

- docs/midterm/content-contract.md (scientific baseline ac4ade796e56377882b8069d0fb7a14809e8180b)
- docs/current-results.md; baseline aggregate receipts qualification/reports/koa_final_closure/
- closure-pilot-final.receipt.json; closure-parent-final.receipt.json; closure-critical-final.tests.json; regression-reconciled.json. These are existing baseline receipts, not rerun in artifact production.

## Slide 14. Giới hạn và bước tiếp theo

**Thời lượng gợi ý:** 01:15

Thiết kế hiện có nhiều giới hạn: tập DEV nhỏ, đã có lịch sử hiệu chỉnh DEV, quan hệ giữa intents hoặc cases chưa cho phép khẳng định độc lập lâm sàng, gating chịu ảnh hưởng cách Planner dự đoán nghĩa vụ, và giới hạn ngôn ngữ của retrieval. So sánh A1/G còn gộp nhiều khác biệt trong policy. Milestone kỹ thuật kế tiếp đã xác định là hoàn thành sáu qualification modules bị resource-blocked trên host có ít nhất ba GiB Windows commit headroom, đồng thời giữ kiểm tra baseline và version. Các bước sau như provider và financial readiness, LIVE pilot, full E1-v2 và owner scoring là những gate riêng cần cấp quyền đúng phạm vi. Quyền biên soạn báo cáo hiện tại không tự kích hoạt chúng. License và khả năng redistribution guideline vẫn UNVERIFIED, nên bản công bố chỉ dùng metadata cùng aggregate đã làm sạch.

**Nguồn:**

- docs/midterm/content-contract.md (scientific baseline ac4ade796e56377882b8069d0fb7a14809e8180b)
- docs/current-results.md; baseline aggregate receipts qualification/reports/koa_final_closure/
- Six pending modules: test_e1_recovery; test_e1_rolling_accounting; test_e1_v2; test_e1_v2_release; test_i5_real_construction; test_koa_system.

## Slide 15. Kết luận và trao đổi

**Thời lượng gợi ý:** 00:35

Kết quả giữa kỳ là framework có kiểu, hai cổng kiểm chứng, hai vòng phản hồi bị chặn số lần và control plane xác định, đi cùng protocol ba nhánh có thể kiểm toán. MOCK cho bằng chứng vận hành kỹ thuật và khả năng đi qua các nhánh. Các câu hỏi RQ1 đến RQ3 vẫn cần thực thi đủ điều kiện và đánh giá độc lập trước khi có kết luận về chất lượng. Điểm muốn trao đổi là độ phù hợp của nghĩa vụ do Planner dự đoán, ranh giới đánh giá snapshot bằng chứng động và cách xây dựng scoring context đủ quyền trong giai đoạn sau.

**Nguồn:**

- docs/midterm/content-contract.md (scientific baseline ac4ade796e56377882b8069d0fb7a14809e8180b)
- docs/system-architecture.md; assets/diagrams/02-agentic-rag-architecture.svg/.mmd
- docs/agentic-workflow.md; assets/diagrams/03-controller-state-machine.svg/.mmd
- docs/experimental-design.md; assets/diagrams/05-experimental-arms.svg/.mmd
- docs/current-results.md; baseline aggregate receipts qualification/reports/koa_final_closure/
