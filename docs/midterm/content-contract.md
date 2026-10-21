# Shared scientific content contract for the KOA midterm artifacts

## 1. Authority and scope

This contract is the shared content authority for `report/midterm/` and `slides/midterm/`. It summarizes the existing methodology; it does not introduce a new research methodology or authorize new experiments.

- Research-facing publication repository: `KwanFam26022005/KOA-Agentic-RAG-System`, starting HEAD `55b43da567a0eb0d8ddb26613f17763c3df05796`.
- Scientific baseline: `ac4ade796e56377882b8069d0fb7a14809e8180b` in the read-only original research repository.
- Scientific source identity: `5aa87228b07ead1c4ecde48e7330e62771a86dbed7ac0fc4097f50152d306f5b`.
- Integration identity: `0155dc81df270dc5b6413ce6587aa52ed69e3cb7f415cd5146bf1188431ac927`.
- Prospective protocol: `e1-v2.refined-full-primary.v2`; lock SHA-256 `98ad86c861986f3794d9b5818cafe44d396967340faf3631d6fb06d91006e5a3`.
- Use baseline Git objects and matching aggregate receipts. The original working tree contains later changes; those changes and newer LIVE reports are excluded from this midterm snapshot because their protocol/provenance has not been admitted here.
- The documents describe progress at this baseline. Production date is not an experiment date or evidence of a newer scientific state.

## 2. Identity and attribution

- Report heading: **BÁO CÁO GIỮA KỲ NGHIÊN CỨU**.
- Approved project title: **KOA Agentic-RAG System: Evidence-Grounded Agentic Retrieval-Augmented Generation for Knee Osteoarthritis Clinical Guidelines**.
- Authors: **Phạm Hồng Đăng Khoa** and **Nguyễn Hoàng Khang**.
- Institution for requested presentation/report identity: **Trường Đại học Tôn Đức Thắng / Ton Duc Thang University (TDTU)**.
- Do not invent supervisor, student IDs, research faculty affiliation, course, academic year, approval or endorsement. The unrelated template's supervisor/course metadata is not KOA attribution. Omit unverified metadata cleanly.
- The method/runtime and research-facing documentation attribution above does not transfer ownership of the separately governed benchmark's sealed evaluator assets.
- Language: Vietnamese, retaining technical terms and exact protocol/status identifiers where useful.

## 3. Narrative and research questions

Clinical guideline QA requires source-scoped evidence, coverage of question-derived material obligations, and support for atomic claims. A relevant passage alone does not establish sufficiency or answer correctness. The research connects a separately governed benchmark with an agentic method and a prospective evaluation protocol.

- **RQ1 — Primary policy comparison, A1 vs G:** Does refined obligation-guided PRE produce better evidence-grounded decision quality than matched generic PRE? This is a hypothesis about two implemented policy bundles. Their differences include representation, readiness gating and corrective queries; it does not isolate one causal component. Clinical quality requires independent scoring.
- **RQ2 — Question-visibility ablation, A1 vs A0:** How does showing the original question alongside the same Plan and E0 change initial PRE readiness, with the same FULL instructions/schema/gating? Readiness is controller behavior, not clinical accuracy.
- **RQ3 — Supporting comparison, A0 vs G:** Characterize original plan-only FULL PRE against matched generic PRE on the same downstream v4 substrate. Supporting, not a second primary comparison.

Expected contributions are benchmark governance/task contracts, typed obligation-guided dual verification with bounded feedback, deterministic action control, and a reproducible prospective comparison. No novelty-first, state-of-the-art, safety or superiority claim is established.

## 4. Verified benchmark facts

**KOA-GuidelineBench rc0.2.0** is an internal review candidate (`public_release = false`), not an openly released clinical corpus.

| Item | Exact scope |
|---|---|
| Guideline sources | 5 |
| EvidenceUnit corpus | 276 retrievable units |
| SemanticIntent corpus | 170 metadata records; not 170 scored DEV questions |
| Task C | 16 English Recovery DEV cases; E1-v2 study population |
| Task B | 5 paired sufficiency contrasts, 10 bundle appearances, 9 distinct displayed bundles, 4 semantic intents |
| Quality-eligible E1-v2 public items | 0/16 |

| Frozen source registry identity | Version | Units | Language | Registry scope |
|---|---|---:|---|---|
| ACSQHC | 2024 | 32 | EN | CURRENT |
| BYT Vietnam | 2014 | 39 | VI | HISTORICAL |
| EULAR | 2023 update, published 2024 | 24 | EN | CURRENT |
| NICE NG226 | 2022 | 84 | EN | CURRENT |
| VA/DoD | 2026 | 97 | EN | CURRENT |

`CURRENT`/`HISTORICAL` describe the frozen registry, not a live assessment of current medical advice. Counts sum to 276. The 4 Task B intents must not be asserted as the total intent count of Task C. Never combine Tasks B and C as 21 independent clinical questions.

EvidenceUnit structure: stable identity, source reference, quotation selector/hash, document SHA-256, page/section/context locators, provenance. Describe the structure without reproducing guideline quotations. SemanticIntent groups information needs/question variants/source scope. Do not reproduce owner reference answers or canonical obligations.

Task B judges fixed displayed bundles. Task C performs corpus retrieval and evidence gating. Task B labels cannot be transferred to dynamically retrieved E0/E1 snapshots.

Exposure layers: `RUNTIME_VISIBLE` (`runtime/`), `EVALUATOR_ONLY` (`evaluator/`), `REVIEWER_AUDIT_ONLY` (`audit_provenance/`). `BA1-D1` withholds canonical benchmark obligations; `BA1-D2` partitions exposure. Runtime predicts its own obligations from question text. An input allowlist excludes benchmark gold and evaluator internals.

Release manifest SHA-256: `eda0e26c1832f41150b37da7780076f9ea04f55927765faaee3b4a2047e5985b`.
Corpus SHA-256: `f9cdcccd5a0e97784ee59ceeb43292a6a8419c61ed6825180e37256e66e1de52`.

## 5. Verified method: DV-OGEC-RAG

Full name: **Dual-Verification Obligation-Guided Evidence-Controlled RAG**.

1. Question-only LLM **Obligation Planner** predicts typed `MaterialObligation[]`. Freeze `plan_identity`; bind source constraints deterministically.
2. Local **MedCPT + FAISS** initial retrieval produces E0. Filter eligible sources before scoring. EvidenceMemory preserves deduplicated evidence and provenance.
3. **PRE**: A0/A1 produce structured per-obligation observations. A deterministic reducer requires every planned obligation to be covered, valid source alignment and zero unresolved discrepancies. Even planner-optional obligations gate FULL readiness. G uses its generic boolean sufficiency and gaps.
4. If insufficient and budget available, a deterministic query builder triggers **corrective retrieval <= 1**. A0/A1 target obligations; G targets generic gaps. Merge E0 union E1 and mandatorily recheck PRE.
5. Failed PRE sufficiency yields authorized `ABSTAIN`; generation only follows a passing PRE gate.
6. **Generator** creates a candidate using eligible EvidenceMemory and resolvable citations.
7. **Claim Decomposer** creates closed typed atomic claims with obligation and evidence IDs.
8. **Staged POST v4** (`e1.member-bound-staged-post.v4`): member-bound `pair` verification, semantic `diagnosis` with code-owned aliases, grounded `remedies`/coverage; deterministic canonical validation checks identities/references and acceptance constraints.
9. If `NEEDS_REVISION`, revision is possible and budget remains, **grounded revision <= 1** uses existing memory only, with no retrieval. Invalidate old claims/POST, then decompose and verify again.
10. **POST gate** and **PolicyGuard** permit ACCEPT only with supported claims, addressed obligations, valid provenance/source scope and zero hard failures. Otherwise authorize legitimate abstention. Provider/schema/retrieval/guard errors are distinct technical failures.

Every effectful action follows `ValidActionSet -> DeterministicRulesPolicy -> PolicyGuard -> WorkflowActionExecutor`. Policy proposes, deterministic guard authorizes, executor acts. The qualified DecisionPolicy is deterministic, not an LLM. Model confidence cannot override hard guards. Jev is optional, waitlisted and outside qualified integration/results.

Terminal mapping: `ACCEPT = COMPLETED_ANSWER`; `ABSTAIN = COMPLETED_ABSTAIN`; technical failure `FAILED_*`. Acceptance is not independently verified clinical correctness. Technical failure is not abstention or an imputed negative answer.

Agentic rationale: question-derived subgoals, memory/state-dependent corrective acquisition, diagnosed revision feedback and guarded actions. Bounded loops differ from a single-pass Retrieve -> Generate pipeline.

Retrieval configuration: `koa-frozen-medcpt-v1`, 276 vectors, 768 dimensions, float32 CPU, FAISS `IndexFlatIP`, top-k 8, no reranker, offline pinned MedCPT query/article encoders. Initial retrieval <= 1, corrective <= 1, revision <= 1; worst-case physical LLM requests <= 34 per arm cell, plus one shared Planner request per block. A request ceiling is not measured typical cost.

## 6. E1-v2 design and inference boundaries

| Arm | PRE input | PRE policy/correction | Downstream |
|---|---|---|---|
| A0 | Plan + E0; original question hidden at PRE | FULL per-obligation gating; targeted correction | Shared Plan, Generator, Decomposer, POST v4, revision, guard |
| A1 | Question + same Plan + same E0 | Same FULL instructions/schema/gating as A0; targeted correction | Same as A0 |
| G | Question + E0 + public SourcePolicy + prior generic gaps; no Plan at PRE | Generic sufficiency boolean; generic-gap correction | Receives the same shared Plan downstream |

- 16 Task C DEV questions x 3 replicates = **48 shared preparations**; x 3 arms = **144 planned arm cells**.
- Planner and initial retrieval run once in each question/replicate block. Same Plan/E0 and locked source scope are bound before arm dispatch.
- Six rotating arm-order permutations, eight blocks each. Counterbalanced order is not an independently sampled clinical population.
- Primary A1 vs G; ablation A1 vs A0; supporting A0 vs G.
- Question-level aggregation with replicates nested within questions. Do not treat 48 preparations or 144 cells as independent clinical questions; do not claim established clinical independence of the 16 cases.
- Registered readiness contrast: mean over 16 questions of the mean paired binary readiness difference across 3 replicates.
- Exploratory paired question-cluster bootstrap: 20,000 resamples, seed 401, 95% percentile interval, only qualified LIVE with complete gates for both arms. This is a planned analysis, not an analysis performed in this artifact task. MOCK contrasts/CIs remain null.
- Metrics: (1) independent reference-scored quality; (2) controller-observed behavior; (3) diagnostic transitions/failures; (4) technical/accounting telemetry. Do not promote tiers 2-4 to clinical quality.
- Missing/unattempted cells remain missing. Do not recode as abstention. No new model runs, scorer construction or benchmark download are part of this authoring task.

## 7. Verified engineering evidence at the baseline

These are existing receipts verified for publication, not tests rerun during document production.

| Qualification | Verified result | Receipt / identity |
|---|---|---|
| Native MOCK pilot | 9/9 terminal cells; 3 shared preparations | `closure-pilot-final.receipt.json`; run `20261020T124525034329Z-c18d0afc7ed84f2d` |
| Native MOCK full | 144/144 terminal cells; 48 shared preparations | `closure-parent-final.receipt.json`; run `20261020T124618087083Z-031bcc4e5ec34fed` |
| Critical tests | 129/129 PASS, zero fail/error/skip | `closure-critical-final.tests.json` |
| Reconciled regression | PARTIAL: 103/109 modules; 1,400 PASS, 21 SKIP, 6 RESOURCE_BLOCKED | `regression-reconciled.json`; composite execution, not a complete single full-suite pass |
| Provider schemas (optional supporting result) | 14/14 QUALIFIED_OFFLINE, fictional client | `provider-compatibility-final.json`; not real-provider qualification |

Receipt directory: `qualification/reports/koa_final_closure/` in the authorized original repository. Baseline closure narrative: `docs/experiments/KOA_FINAL_ENGINEERING_AND_RESEARCH_CLOSURE.md`. Matching receipt identities use source/integration/protocol hashes in section 1. Real provider calls in these MOCK receipts are zero.

The deterministic fake SDK exercises correction/revision branches with the actual local retrieval/controller. Symmetric arm counts are scripted, not evidence of parity, accuracy or superiority. No clinical chart may be made from these pass counts. If using telemetry (107 pilot fake requests / 1,137 full fake requests; 52.015 s / 416.140 s), label it native MOCK engineering telemetry and avoid performance or savings generalization.

Remaining modules: `test_e1_recovery`, `test_e1_rolling_accounting`, `test_e1_v2`, `test_e1_v2_release`, `test_i5_real_construction`, `test_koa_system`. Baseline admission guard requires >= 3 GiB available Windows commit headroom. The 21 SKIPs concern optional schema validation and owner-boundary conditions; they are not passes.

## 8. Scientific limitations and status

- **E1-v2 REAL PROVIDER: NOT_EXECUTED** at this admitted baseline.
- **Independent clinical-quality scoring: NOT_EVALUABLE**; **0/16** eligible public E1-v2 items. This is lack of evaluation eligibility, not 0% accuracy.
- No established A1 > G or A1 > A0 clinical-quality conclusion; no validated patient safety, clinical effectiveness, cost saving or bilingual consistency claim.
- Small DEV slice, DEV iteration history, potential related intents/cases, planner-dependent all-obligation gating, MedCPT language/domain limits, and bundled A1/G differences limit generalization.
- Provider model alias/transport/financial readiness remains a separate gate. Offline schema compatibility is insufficient. No task authorization here activates paid inference.
- Owner-referenced dynamic sufficiency, answer/claim truth and a qualified three-arm scoring context are missing in public scope.
- Third-party guideline license/redistribution status is UNVERIFIED. Publish metadata and sanitized aggregates only, never guideline quotations, original PDFs, gold, owner reference content, private runtime source or raw traces.
- Historical two-arm E1 v1/v3 LIVE observations may be mentioned as historical design motivation only. Prefer qualitative context, and do not pool them with prospective v4 E1-v2.

## 9. Progress and remaining milestones

Completed: benchmark structures/governance, method implementation, bounded controller integration, native offline qualification, prospective E1-v2 protocol, RunStore/provenance management and the research documentation/figures.

Next single engineering milestone: complete the six resource-blocked native qualification modules on an adequately provisioned host, retaining baseline/version checks. Future gated work: legitimate provider and financial readiness; separately authorized LIVE pilot; qualified full E1-v2; independent owner scoring context; comparisons/ablations and error/validity analysis; final research conclusions. Do not invent dates or percentage progress.

## 10. Artifact production and formatting agreement

- Report: editable DOCX + PDF, eight requested chapters, substantive target 25-35 main-content pages excluding cover/front matter/references/appendices. Numbered figures/tables, bibliography and source provenance.
- Presentation: editable PPTX + PDF, 15 slides, 16:9, Vietnamese, notes for 15-20 minutes; concise readable native text/tables/diagrams.
- Report formatting authority: user-provided 18-page A4 PDF. Inspected cover and body pages: Times New Roman body 13 pt, bold hierarchy, top-centered page numbers after covers, captions beneath figures, restrained tables. Actual PDF has no evident TOC/bibliography model; create academic front matter/references as an explicit adaptation. Measure margins from the PDF rather than assert an unseen official standard.
- Institution identity must use unaltered authorized local or official TDTU logo. Without a verified brand manual, label the deck **TDTU-inspired academic theme**, not an official university template. Exact design colors are choices, not official color specifications.
- Existing diagrams 01-05 are verified publication figures. Reuse them; dense figures require legible landscape/detail views. Native presentation derivatives must retain bounded correction, fresh PRE recheck, memory-only revision with re-decomposition/POST, deterministic guard and three terminal outcomes.
- Publication checks exclude secrets, restricted text, gold and private traces. Do not copy the original formatting PDF to the public repository.

## 11. Source map and bibliography

Existing research-facing sources read: `README.md`; `docs/research-overview.md`; `docs/system-architecture.md`; `docs/agentic-workflow.md`; `docs/benchmark.md`; `docs/experimental-design.md`; `docs/implementation.md`; `docs/current-results.md`; `docs/reproducibility.md`; `docs/references.md`; `report/research-report-outline.md`; `slides/presentation-storyboard.md`; `assets/diagrams/01` through `05` (.svg/.mmd).

Scientific primary authority: baseline Git protocol/closure/contracts and matching aggregate receipts. Public documentation is an auditable summary, not a substitute for owner gold or missing clinical evaluation.

Use verified scholarly metadata and cite these works where relevant; do not assert evaluated superiority over their systems:

1. Lewis et al., RAG, NeurIPS 2020, https://arxiv.org/abs/2005.11401.
2. Asai et al., Self-RAG, ICLR 2024, https://arxiv.org/abs/2310.11511.
3. Yan et al., Corrective RAG, 2024 preprint, https://arxiv.org/abs/2401.15884.
4. Min et al., FActScore, EMNLP 2023, https://aclanthology.org/2023.emnlp-main.741/.
5. Kamath et al., Selective Question Answering under Domain Shift, ACL 2020, https://aclanthology.org/2020.acl-main.503/.
6. Jin et al., MedCPT, Bioinformatics 2023;39(11):btad651, https://doi.org/10.1093/bioinformatics/btad651.
7. Johnson et al., Billion-Scale Similarity Search with GPUs, IEEE TBD 2021;7(3):535-547, https://arxiv.org/abs/1702.08734.
8. Xiong et al., Benchmarking Retrieval-Augmented Generation for Medicine, Findings ACL 2024:6233-6251, https://aclanthology.org/2024.findings-acl.372/.
9. ACSQHC, Osteoarthritis of the Knee Clinical Care Standard, 2024, https://www.safetyandquality.gov.au/resources/osteoarthritis-knee-clinical-care-standard-2024.
10. Bộ Y tế, Hướng dẫn chẩn đoán và điều trị các bệnh cơ xương khớp, QĐ 361/QĐ-BYT, 25/01/2014; registry metadata, https://kcb.vn/van-ban/huong-dan-chan-doan-va-dieu-tri-cac-benh-co-xuong-khop.html.
11. Moseng et al., EULAR 2023 update, Ann Rheum Dis 2024;83:730-740, https://doi.org/10.1136/ard-2023-225041.
12. NICE, NG226, 2022, https://www.nice.org.uk/guidance/ng226/.
13. VA/DoD, Non-Surgical Management of Hip & Knee Osteoarthritis, frozen registry 2026, https://www.healthquality.va.gov/HEALTHQUALITY/guidelines/CD/OA/index.asp.

Record live source-verification discrepancies transparently. External website changes must not silently relabel frozen corpus identities. Exact TDTU asset provenance and artifact-specific formatting/render checks belong in the production review records.
