# Research Report Outline — KOA Agentic-RAG System

**Working Title:** *KOA Agentic-RAG System: Evidence-Grounded Agentic Retrieval-Augmented Generation and Benchmark Governance for Knee Osteoarthritis Clinical Guidelines*  
**Authors:** Phạm Hồng Đăng Khoa, Nguyễn Hoàng Khang  
**Target Document Type:** Full Academic Technical Report / Thesis Manuscript Blueprint

> [!NOTE]
> **Scientific Honesty Guardrail:** Section 8 (*Results and Discussion*) intentionally preserves explicit `NOT_EXECUTED` (for real-provider `E1-v2` runs) and `NOT_EVALUABLE` (for reference-scored clinical quality endpoints) markers. Do not populate comparative quality tables until an authorized live run and independent owner reference reconciliation are completed.

---

## 1. Abstract
- **Context & Problem:** Clinical question answering over knee osteoarthritis (KOA) practice guidelines requires multi-obligation evidence sufficiency, adherence to source authority constraints, and verifiable claim grounding rather than unconstrained top-$k$ passage synthesis.
- **Contributions:**
  1. **`KOA-GuidelineBench` (`rc0.2.0`):** A multi-authority clinical guideline benchmark ecosystem (5 guideline sources, 276 native evidence units, 170 semantic intents) featuring strict three-layer exposure governance (`RUNTIME_VISIBLE`, `EVALUATOR_ONLY`, `REVIEWER_AUDIT_ONLY`) and distinct contracts for displayed-bundle sufficiency (Task B: 5 DEV pairs, 9 unique bundles, 4 intents) and corpus recovery/gating (Task C: 16 DEV cases).
  2. **`DV-OGEC-RAG`:** An obligation-guided, dual-verification agentic RAG architecture integrating question-only obligation planning, pre-generation sufficiency verification (`PRE`), bounded corrective retrieval ($\le 1$), atomic claim decomposition, member-bound staged post-generation verification (`POST v4`), bounded grounded revision ($\le 1$), and a deterministic `PolicyGuard`.
- **Experimental Design & Status:** Prospective three-arm block-randomized protocol (`e1-v2.refined-full-primary.v2`: `A0`, `A1`, `G` across 48 shared preparations / 144 cells). Reports complete offline engineering qualification (`9/9` pilot, `144/144` full native `MOCK`, `129/129` critical tests, `103/109` regression modules) while explicitly distinguishing engineering readiness from pending real-provider execution (`NOT_EXECUTED`) and owner-held clinical quality scoring (`NOT_EVALUABLE`).

---

## 2. Introduction
- **2.1 Clinical Motivation:** High prevalence of knee osteoarthritis; complexity of harmonizing multi-component non-pharmacological and pharmacological guidance across international and national authorities (ACSQHC, BYT, EULAR, NICE, VA/DoD).
- **2.2 Failure Modes of Standard Medical RAG:**
  - Partial obligation coverage in initial retrieval ($E_0$);
  - Source-scope contamination (e.g., mixing historical and current guidelines without attribution);
  - Composite claim hallucination or omission of clinical qualifiers during generation;
  - Over-reliance on uncalibrated LLM self-reflection without deterministic action/provenance guards.
- **2.3 Research Questions (`RQ1`–`RQ3`):**
  - `RQ1` (Primary): Refined obligation-guided PRE (`A1`) vs. matched generic PRE (`G`) policy bundles.
  - `RQ2` (Mechanistic Ablation): Question-visible FULL PRE (`A1`) vs. plan-only FULL PRE (`A0`).
  - `RQ3` (Supporting): Plan-only FULL PRE (`A0`) vs. matched generic PRE (`G`) on the common `v4` runtime.
- **2.4 Summary of Contributions & Scope Boundaries:** Clear demarcation between benchmark governance, agentic runtime engineering, and clinical evaluation boundaries.
- *Embedded Figure:* [Diagram 01 — Overall Research Framework](../assets/diagrams/01-research-framework.svg).

---

## 3. Related Work
- **3.1 Retrieval-Augmented Generation in Biomedicine:** Foundational RAG (Lewis et al., 2020), biomedical dense retrieval with PubMed click logs (MedCPT; Jin et al., 2023), exact vector indexing (FAISS; Johnson et al., 2021), and medical RAG benchmarking (MIRAGE; Xiong et al., 2024).
- **3.2 Reflective and Corrective RAG Architectures:** Self-RAG (Asai et al., 2024) and Corrective RAG (Yan et al., 2024); contrast between unconstrained reflection tokens and typed obligation-state verification with deterministic guards.
- **3.3 Atomic Fact Verification & Selective Prediction:** Fine-grained claim verification (FActScore; Min et al., 2023) and selective abstention under uncertainty (Kamath et al., 2020); extension to member-bound claim–evidence pair verification (`Staged POST v4`) and obligation completeness checking.

---

## 4. `KOA-GuidelineBench` (`rc0.2.0`): Construction, Provenance & Governance
- **4.1 Guideline Corpus & Provenance Architecture:**
  - Breakdown of the 5 authorities: ACSQHC 2024 (32 units), BYT Vietnam 2014 (39 units, `HISTORICAL`), EULAR 2023 (24 units), NICE NG226 2022 (84 units), VA/DoD 2026 (97 units) $\rightarrow$ **276 `EvidenceUnit` records** and **170 `SemanticIntent` records**.
  - Cryptographic document SHA-256 digests, PDF page start/end locators, heading paths, and native quotation selectors.
- **4.2 Task Definitions & Statistical Units:**
  - **Task B (`koa_evidence_sufficiency`):** 5 DEV pairs across 9 unique displayed bundles and 4 semantic intents. Why displayed-bundle labels cannot transfer to open-retrieval $E_0$/$E_1$ snapshots.
  - **Task C (`koa_recovery_evidence_gating`):** 16 English DEV cases with locked source scopes. Why $16 + 5$ is never reported as "21 independent clinical questions."
- **4.3 Exposure Adjudication (`BA1-D1` / `BA1-D2`):**
  - Method-neutral obligation derivation ($\text{Canonical MO} \neq \text{Predicted MO}$).
  - Three-layer partitioning: `RUNTIME_VISIBLE` (`runtime/`), `EVALUATOR_ONLY` (`evaluator/`), and `REVIEWER_AUDIT_ONLY` (`audit_provenance/`).
- **4.4 External Benchmark Smoke Adapter (`DocOA`):** Structural validation on `GIQA` (337 rows) and `MOQA` (145 rows) under rule `docoa.explicit-knee-target.v1`, and why scientific RAG comparison remains `NOT_QUALIFIED` without a matched passage corpus.
- *Embedded Figure:* [Diagram 04 — Benchmark vs. Runtime vs. Independent Evaluation](../assets/diagrams/04-benchmark-evaluation-boundary.svg).

---

## 5. Proposed `DV-OGEC-RAG` Method Architecture
- **5.1 Formal Runtime Objects & Closed Typed Contracts:** `RuntimeQuestion`, `MaterialObligation`, `Plan`, `AuthorityBinding`, `EvidenceMemory`, `PreVerificationObservation`, `GenericPreState`, `AnswerObservation`, `AtomicClaim`, `StagedPostObservation`.
- **5.2 Question-Only Obligation Planning & Pre-Scoring Source Filtering:**
  - Predicting material obligations without gold leakage; freezing `plan_identity`.
  - Local MedCPT query/article encoding and FAISS `IndexFlatIP` (`top_k = 8`, `reranker = NONE`) with source-scope filtering *prior* to inner-product scoring.
- **5.3 Dual Verification Lifecycle:**
  - **Stage I — Pre-Generation Verification (`PRE`) & Bounded Corrective Retrieval ($\le 1$):** Deterministic all-obligation readiness reducer (including planner-"optional" obligations); obligation-targeted vs. generic-gap query synthesis; merged memory ($E_0 \cup E_1$) and mandatory PRE recheck; `PRE_EVIDENCE_GATE`.
  - **Stage II — Candidate Generation, Atomic Decomposition & Member-Bound Staged POST (`v4`):** Three-pass POST verification (`pair` $\rightarrow$ `diagnosis` $\rightarrow$ `remedies`) with code-owned identity aliases; bounded grounded revision ($\le 1$) using existing `EvidenceMemory` only; `POST_EVIDENCE_GATE`.
- **5.4 Deterministic Control Plane (`ValidActionSet` $\rightarrow$ `DeterministicRulesPolicy` $\rightarrow$ `PolicyGuard`):**
  - Why `PolicyGuard` is a deterministic verifier rather than an autonomous LLM; separation of `COMPLETED_ANSWER` (`ACCEPT`), `COMPLETED_ABSTAIN` (`ABSTAIN`), and `FAILED_*` (technical failure).
- *Embedded Figures:* [Diagram 02 — DV-OGEC-RAG Agentic Architecture](../assets/diagrams/02-agentic-rag-architecture.svg) and [Diagram 03 — Controller State Machine](../assets/diagrams/03-controller-state-machine.svg).

---

## 6. Experimental Setup (`E1-v2` Protocol)
- **6.1 Prospective Protocol Lock (`e1-v2.refined-full-primary.v2`):** Lineage from historical `E1` (`v3`) and predecessor `v1`; cryptographic lock pinning (`98ad86c8...`).
- **6.2 Three-Arm Design (`A0`, `A1`, `G`):** Input contracts, shared downstream `v4` substrate, and causal interpretation caveats for `A1` vs. `G` versus the clean mechanistic ablation `A1` vs. `A0`.
- **6.3 Blocked Shared Preparation & Counterbalancing:** 16 Task C DEV questions $\times$ 3 replicates = 48 shared `(Plan, E0)` preparations $\times$ 3 arms = 144 cells; 6 rotating permutations (8 blocks per permutation).
- **6.4 Metric Hierarchy & Statistical Plan:**
  - Tier 1 (`reference_scored`), Tier 2 (`controller_observed`), Tier 3 (`diagnostic`), Tier 4 (`technical`).
  - Question-cluster bootstrap rule ($20,000$ resamples, seed `401`) restricted to complete `LIVE` gates.
- *Embedded Figure:* [Diagram 05 — E1-v2 Experimental Arms](../assets/diagrams/05-experimental-arms.svg).

---

## 7. Engineering Implementation & Offline Qualification
- **7.1 Native Runtime, `RunStore` Durability & Pre-Dispatch Accounting:** Append-only `INTENT`/`USAGE` ledger, dual run/global ceilings, and fail-closed torn-write handling.
- **7.2 Offline Qualification Evidence:**
  - Critical current-source test selection: **129 / 129 `PASS`**.
  - Native `MOCK` Pilot (`pilot3`): **9 / 9 cells completed** (`107` fictional requests, `52.015 s`).
  - Native `MOCK` Full Campaign (`full`): **144 / 144 cells completed** (`1,137` fictional requests, `416.140 s`).
  - Provider static matrix: **14 / 14 schemas `QUALIFIED_OFFLINE`**.
  - Isolated 109-module regression suite: **`PARTIAL` (103 / 109 modules completed; 1,400 `PASS`, 21 `SKIP`, 6 `RESOURCE_BLOCKED` under Windows 3 GiB commit guard)**.

---

## 8. Results and Discussion
- **8.1 Verified `MOCK` Controller Trajectory Verification:** Summary of scripted branch execution across `A0`, `A1`, and `G` (demonstrating correction and revision loops without claiming empirical comparison).
- **8.2 Historical Two-Arm `LIVE` Context (`v1`/`v3` Failure Taxonomy):** Summary of the 96-cell historical runs (`0d28f3a5...`, `f1d77471...`) that motivated `A1` question visibility and `v4` member-bound POST.
- **8.3 Reserved Placeholders for Prospective `E1-v2` `LIVE` Execution (`NOT_EXECUTED`) & Independent Quality Scoring (`NOT_EVALUABLE`):**
  - Behavioral contrasts $\hat{\Delta}_{\text{ready}}(A_1, G)$, $\hat{\Delta}_{\text{ready}}(A_1, A_0)$, $\hat{\Delta}_{\text{ready}}(A_0, G)$: **`PENDING_LIVE_EXECUTION`**.
  - Reference-scored clinical quality (FAR, answer correctness, grounded support, completeness): **`NOT_EVALUABLE` (`0/16` in public scope; `SCORING_BLOCKED_BY_OWNER_REFERENCE`)**.

---

## 9. Limitations and Threats to Validity
- **9.1 Scientific & Statistical Limitations:** Small DEV sample ($N = 16$ questions; 4 semantic intents in Task B), DEV-tuned design history, bundled policy differences between `A1` and `G`, all-obligation gating strictness, and unresolved model alias (`gpt-5.6-luna`).
- **9.2 Engineering & Operational Blockers:** 6 native regression modules awaiting host commit-memory headroom ($\ge 3\text{ GiB}$); inactive independent financial policy; unexecuted real-provider probes; absence of owner scoring context in public delivery; unverified third-party guideline redistribution rights.

---

## 10. Conclusion and Future Work
- **10.1 Summary of Architectural & Methodological Achievements:** End-to-end typed agentic RAG framework with cryptographically audited benchmark boundaries and deterministic action control.
- **10.2 Sequenced Roadmap to Full Scientific Closure:**
  1. Complete remaining 6 native module qualifications on a high-memory host;
  2. Obtain financial policy activation, credential verification, and explicit authorization for the 9-cell `pilot3` and 144-cell `full` `LIVE` runs;
  3. Reconcile predictions with the benchmark owner's sealed `EvaluationContext` under a prospective three-arm scoring annex;
  4. Extend to held-out `TEST` evaluation and optional `Jev` selective policy comparison once authorized.
