# Presentation Storyboard — KOA Agentic-RAG System (14 Slides)

**Presentation Title:** *KOA Agentic-RAG System: Evidence-Grounded Agentic Retrieval-Augmented Generation for Knee Osteoarthritis Clinical Guidelines*  
**Presenters / Authors:** Phạm Hồng Đăng Khoa, Nguyễn Hoàng Khang  
**Target Duration:** 20–25 minutes (Academic Defense / Research Seminar / Lecturer Review)

---

## Slide-by-Slide Storyboard Overview

| Slide | Title | Core Scientific Message | Primary Visual / Diagram | Source Document |
| :---: | :--- | :--- | :--- | :--- |
| **01** | Title & Research Identity | Introduce the connected benchmark (`KOA-GuidelineBench rc0.2.0`) and agentic method (`DV-OGEC-RAG`) contributions and explicit non-clinical scope. | Title card + system badge summary | [`README.md`](../README.md) |
| **02** | Clinical QA Motivation & Failure Modes | Why standard top-$k$ RAG fails on multi-authority clinical practice guidelines (partial coverage, source mixing, ungrounded composite claims). | 3-column failure taxonomy illustration | [`docs/research-overview.md`](../docs/research-overview.md) |
| **03** | Research Gap & Design Philosophy | Contrast closed-form medical QA and unconstrained self-reflection with obligation-guided dual verification and deterministic guards. | Comparison matrix: Standard RAG vs. Self-RAG/CRAG vs. `DV-OGEC-RAG` | [`docs/research-overview.md`](../docs/research-overview.md) |
| **04** | Two Connected Research Contributions | Clearly separate Contribution 1 (`KOA-GuidelineBench` governance & task contracts) from Contribution 2 (`DV-OGEC-RAG` method & engine). | Two-pillar contribution diagram | [`docs/research-overview.md`](../docs/research-overview.md) |
| **05** | Overall Research Framework | End-to-end flow from 5 guideline authorities to benchmark tasks, gold-free DEV runtime inputs, method execution, and owner-separated evaluation. | **[Diagram 01 — Overall Research Framework](../assets/diagrams/01-research-framework.svg)** | [`docs/research-overview.md`](../docs/research-overview.md) |
| **06** | `KOA-GuidelineBench` (`rc0.2.0`) Corpus & Tasks | 5 authorities (ACSQHC, BYT, EULAR, NICE, VA/DoD), 276 evidence units, 170 intents; Task B (5 pairs / 9 bundles / 4 intents) vs. Task C (16 DEV cases). | Source table + cardinality breakdown callout | [`docs/benchmark.md`](../docs/benchmark.md) |
| **07** | Three-Layer Exposure Governance (`BA1-D1` / `BA1-D2`) | How `RUNTIME_VISIBLE`, `EVALUATOR_ONLY`, and `REVIEWER_AUDIT_ONLY` prevent gold leakage and enforce $\text{Canonical MO} \neq \text{Predicted MO}$. | **[Diagram 04 — Benchmark vs. Runtime vs. Evaluation](../assets/diagrams/04-benchmark-evaluation-boundary.svg)** | [`docs/benchmark.md`](../docs/benchmark.md) |
| **08** | `DV-OGEC-RAG` Agentic Architecture (Core Figure) | Full execution lifecycle: shared Planner & $E_0$, PRE sufficiency, conditional correction ($\le 1$), generation, atomic decomposition, Staged POST `v4`, revision ($\le 1$), and `PolicyGuard`. | **[Diagram 02 — DV-OGEC-RAG Agentic Architecture](../assets/diagrams/02-agentic-rag-architecture.svg)** | [`docs/system-architecture.md`](../docs/system-architecture.md) |
| **09** | Pre-Generation Sufficiency (`PRE`) & Bounded Correction | How planned obligations gate generation deterministically, how corrective queries are built (`A0`/`A1` vs. `G`), and why $E_0 \cup E_1$ always undergoes PRE recheck. | Zoomed PRE + Corrective Retrieval sub-flow & readiness truth table | [`docs/agentic-workflow.md`](../docs/agentic-workflow.md) |
| **10** | Atomic Decomposition, Staged POST `v4` & Revision | How candidate answers are decomposed into `AtomicClaim[]`, verified via `pair` $\rightarrow$ `diagnosis` $\rightarrow$ `remedies` passes, and revised ($\le 1$) using existing memory only. | 3-stage POST `v4` pipeline & state-invalidation loop | [`docs/agentic-workflow.md`](../docs/agentic-workflow.md) |
| **11** | Controller State Machine & Deterministic `PolicyGuard` | `ValidActionSet` $\rightarrow$ `DeterministicRulesPolicy` $\rightarrow$ `PolicyGuard`; execution bounds ($\le 1, \le 1, \le 1$) and separating `ABSTAIN` from `FAILED_*`. | **[Diagram 03 — Controller State Machine](../assets/diagrams/03-controller-state-machine.svg)** | [`docs/agentic-workflow.md`](../docs/agentic-workflow.md) |
| **12** | Prospective `E1-v2` Experimental Design (`A0`, `A1`, `G`) | 16 questions $\times$ 3 replicates = 48 shared preparations $\times$ 3 arms = 144 cells; 6 permutations; primary (`A1` vs. `G`), ablation (`A1` vs. `A0`), and supporting (`A0` vs. `G`) roles. | **[Diagram 05 — E1-v2 Experimental Arms](../assets/diagrams/05-experimental-arms.svg)** | [`docs/experimental-design.md`](../docs/experimental-design.md) |
| **13** | Verified Engineering Results & Scientific Status | Report verified `MOCK` (`9/9` pilot, `144/144` full), critical tests (`129/129`), and regression (`103/109`, `1,400 PASS`, `21 SKIP`, `6 RESOURCE_BLOCKED`), alongside `REAL_PROVIDER: NOT_EXECUTED` and quality `0/16 NOT_EVALUABLE`. | Two-panel table: Engineering Receipts vs. Scientific Eligibility Matrix | [`docs/current-results.md`](../docs/current-results.md) |
| **14** | Limitations, Public Release Governance & Roadmap | Summarize validity threats, copyright/data-rights protections, and the exact single-gate sequence toward live execution and owner-reconciled scoring. | Milestone checklist & governance boundary summary | [`docs/reproducibility.md`](../docs/reproducibility.md) |

---

## Detailed Slide Specifications

### Slide 01 — Title & Research Identity
- **Headline:** *KOA Agentic-RAG System: Evidence-Grounded Agentic Retrieval-Augmented Generation for Knee Osteoarthritis Clinical Guidelines*
- **Key Bullets:**
  - Connected research delivery: **`KOA-GuidelineBench` (`rc0.2.0`)** $\times$ **`DV-OGEC-RAG`**.
  - Authors: Phạm Hồng Đăng Khoa (`KwanFam26022005`), Nguyễn Hoàng Khang.
  - Scope: Audited architecture, benchmark governance, prospective `E1-v2` experimental protocol, and offline engineering qualification.

### Slide 02 — Clinical QA Motivation & Failure Modes
- **Headline:** *Why Clinical Guideline QA Requires More Than Top-$k$ Retrieval*
- **Key Bullets:**
  - Clinical practice guidelines specify conditional recommendations (population, comorbidity, modality, source authority).
  - **Failure Mode 1 (Pre-Generation):** Initial retrieval ($E_0$) misses material obligations or retrieves out-of-scope guidelines.
  - **Failure Mode 2 (Post-Generation):** LLM synthesis introduces unsupported sub-claims or drops mandatory clinical qualifiers.
  - **Failure Mode 3 (Control):** Softmax confidence or unguarded self-reflection cannot guarantee provenance or budget bounds.

### Slide 03 — Research Gap & Design Philosophy
- **Headline:** *From Unstructured Self-Reflection to Obligation-Guided Dual Verification*
- **Key Bullets:**
  - Medical QA benchmarks (e.g., multiple-choice datasets in MIRAGE) test option selection, not multi-obligation guideline synthesis and abstention.
  - Reflective RAG (Self-RAG, CRAG) critiques relevance holistically, without explicit question-derived material obligation tracking.
  - `DV-OGEC-RAG` separates **LLM structured observations** from **deterministic Python action guards (`PolicyGuard`)**.

### Slide 04 — Two Connected Research Contributions
- **Headline:** *Separating Benchmark Governance from Agentic Method Design*
- **Key Bullets:**
  - **Contribution 1 (`KOA-GuidelineBench rc0.2.0`):** Multi-authority KOA corpus (276 units, 5 sources), Task B & Task C contracts, and `BA1-D1`/`BA1-D2` exposure adjudication.
  - **Contribution 2 (`DV-OGEC-RAG`):** Obligation planner, PRE verification, bounded corrective retrieval ($\le 1$), atomic claim decomposition, Staged POST `v4`, bounded revision ($\le 1$), and deterministic `PolicyGuard`.
  - Independent attribution and strict zero-leakage interface (`GoldFreeRuntimeInput`).

### Slide 05 — Overall Research Framework
- **Headline:** *End-to-End Architecture Across Benchmark, Runtime, and Evaluation*
- **Visual:** Embed [`assets/diagrams/01-research-framework.svg`](../assets/diagrams/01-research-framework.svg).
- **Speaker Notes:** Emphasize the one-way boundary from `KOA-GuidelineBench` `runtime/` inputs into `DV-OGEC-RAG`, and the completely separate flow of sealed `EVALUATOR_ONLY` references into the owner reconciliation scorer.

### Slide 06 — `KOA-GuidelineBench` (`rc0.2.0`) Corpus & Tasks
- **Headline:** *Multi-Authority KOA Corpus and Exact Statistical Units*
- **Key Bullets:**
  - **5 Sources (276 EvidenceUnits):** ACSQHC 2024 (32), BYT Vietnam 2014 (39, `HISTORICAL`), EULAR 2023 (24), NICE NG226 2022 (84), VA/DoD 2026 (97).
  - **Task C (Recovery & Evidence Gating):** 16 English DEV cases (`locked_source_scope`).
  - **Task B (Displayed-Bundle Sufficiency):** 5 DEV pairs across 9 unique bundles and 4 semantic intents (never summed with Task C as "21 independent questions"; never used as gold for dynamic $E_0$/$E_1$ retrieval).

### Slide 07 — Three-Layer Exposure Governance (`BA1-D1` / `BA1-D2`)
- **Headline:** *Preventing Benchmark Leakage via Cryptographic Exposure Contracts*
- **Visual:** Embed [`assets/diagrams/04-benchmark-evaluation-boundary.svg`](../assets/diagrams/04-benchmark-evaluation-boundary.svg).
- **Key Bullets:**
  - `BA1-D1`: Canonical benchmark obligations are withheld; the method predicts its own `MaterialObligation[]`.
  - `BA1-D2`: `RUNTIME_VISIBLE` vs. `EVALUATOR_ONLY` vs. `REVIEWER_AUDIT_ONLY` (`RUNTIME_EXPOSURE_CONTRACT.json`).

### Slide 08 — `DV-OGEC-RAG` Agentic Architecture (Core Figure)
- **Headline:** *The `DV-OGEC-RAG` Agentic Execution Lifecycle*
- **Visual:** Embed [`assets/diagrams/02-agentic-rag-architecture.svg`](../assets/diagrams/02-agentic-rag-architecture.svg).
- **Speaker Notes:** Walk through the colour-coded components: blue LLM roles (`Planner`, `PRE`, `Generator`, `Decomposer`, `POST`, `Reviser`), green local MedCPT+FAISS retrieval ($E_0$, $E_1$), yellow deterministic reducers/gates/`PolicyGuard`, and the three terminal outcomes (`ACCEPT`, `ABSTAIN`, `TECHNICAL FAILURE`).

### Slide 09 — Pre-Generation Sufficiency (`PRE`) & Bounded Correction
- **Headline:** *All-Obligation Readiness Gating and Targeted Corrective Retrieval ($\le 1$)*
- **Key Bullets:**
  - Planner output is frozen (`plan_identity`) and bound to the source registry (`AuthorityBinding`).
  - Deterministic readiness requires **every** planned obligation to be `COVERED` with valid source alignment and zero unresolved discrepancies.
  - If insufficient and `corrective_used == 0`, deterministic query builder executes at most one corrective retrieval ($E_1$), merges $E_0 \cup E_1$, and forces a PRE recheck before `PRE_EVIDENCE_GATE`.

### Slide 10 — Atomic Decomposition, Staged POST `v4` & Grounded Revision
- **Headline:** *Member-Bound Atomic Claim Verification and Grounded Self-Correction ($\le 1$)*
- **Key Bullets:**
  - Candidate answers are decomposed into closed typed `AtomicClaim[]` objects.
  - `e1.member-bound-staged-post.v4` executes three structured passes: `pair` binding $\rightarrow$ semantic `diagnosis` (via code-owned aliases) $\rightarrow$ grounded `remedies`.
  - If `NEEDS_REVISION` and `revision_possible`, `reviser` runs at most once using **existing `EvidenceMemory` only**, invalidates old claims/POST, and re-runs `DECOMPOSE` + `ATOMIC_VERIFICATION`.

### Slide 11 — Controller State Machine & Deterministic `PolicyGuard`
- **Headline:** *Deterministic Action Control and Failure Taxonomy*
- **Visual:** Embed [`assets/diagrams/03-controller-state-machine.svg`](../assets/diagrams/03-controller-state-machine.svg).
- **Key Bullets:**
  - Every effectful step requires `ValidActionSet` $\rightarrow$ `DeterministicRulesPolicy` $\rightarrow$ `PolicyGuard` $\rightarrow$ `WorkflowActionExecutor`.
  - Hard bounds: `initial <= 1`, `corrective <= 1`, `revision <= 1`, `model_calls <= 34/arm`.
  - Legitimate abstention (`COMPLETED_ABSTAIN`) is strictly separated from technical/contract failure (`FAILED_*`).

### Slide 12 — Prospective `E1-v2` Experimental Design (`A0`, `A1`, `G`)
- **Headline:** *Controlled Three-Arm Comparison on Shared Preparations*
- **Visual:** Embed [`assets/diagrams/05-experimental-arms.svg`](../assets/diagrams/05-experimental-arms.svg).
- **Key Bullets:**
  - 16 Task C DEV questions $\times$ 3 replicates = **48 shared `(Plan, E0)` preparations** $\times$ 3 arms = **144 cells**, counterbalanced across 6 permutations.
  - **Primary (`A1` vs. `G`):** Refined question-visible FULL PRE vs. matched generic PRE policy bundle.
  - **Mechanistic Ablation (`A1` vs. `A0`):** Isolates original-question visibility in PRE under identical obligation policy and schema.

### Slide 13 — Verified Engineering Results & Scientific Status
- **Headline:** *What Has Been Verified vs. What Remains Scientifically Unverified*
- **Key Bullets:**
  - **Verified Offline Engineering (`PASS`):** Native `MOCK` Pilot (`9/9` cells, `107` fake calls), Native `MOCK` Full (`144/144` cells, `1,137` fake calls), Critical Tests (`129/129 PASS`), Provider Static Schemas (`14/14 PASS`).
  - **Reconciled Regression (`PARTIAL`):** `103/109` modules completed (`1,400 PASS`, `21 SKIP`, `0 FAIL`, `6 RESOURCE_BLOCKED` by 3 GiB Windows commit guard).
  - **Scientific Status:** `REAL_PROVIDER: NOT_EXECUTED`; Independent clinical quality (`A1` vs. `G`, `A1` vs. `A0`): **`NOT_EVALUABLE` (`0/16` in public scope)**. No clinical superiority is claimed.

### Slide 14 — Limitations, Public Release Governance & Next Milestones
- **Headline:** *Rigorous Research Governance and Path to Scientific Closure*
- **Key Bullets:**
  - **Public Repository Safety:** Publishes architecture, protocols, hashes, and sanitized aggregates; withholds licensed guideline text, sealed owner gold, and private runtime source.
  - **Next Single Approved Engineering Gate:** Complete the 6 remaining native module qualifications on a host with $\ge 3\text{ GiB}$ commit headroom.
  - **Future Scientific Gates:** Separate financial policy activation + LIVE `E1-v2` execution + owner-reconciled three-arm reference scoring.
