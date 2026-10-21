# Current Verified Results & Qualification Status

This document reports **only verified engineering and experimental evidence** from the qualified baseline (`ac4ade796e56377882b8069d0fb7a14809e8180b`, scientific source hash `5aa87228b07ead1c4ecde48e7330e62771a86dbed7ac0fc4097f50152d306f5b`, integration hash `0155dc81df270dc5b6413ce6587aa52ed69e3cb7f415cd5146bf1188431ac927`), as recorded in `docs/experiments/KOA_FINAL_ENGINEERING_AND_RESEARCH_CLOSURE.md` and `qualification/reports/koa_final_closure/`.

> [!IMPORTANT]
> **Scientific Honesty Statement:** Engineering qualification and native `MOCK` execution demonstrate that the integrated benchmark connector, local MedCPT retrieval, obligation planner, `A0`/`A1`/`G` PRE verification, corrective retrieval, member-bound Staged POST `v4`, grounded revision, `PolicyGuard`, and `RunStore` execute end-to-end without contract drift. **They do not establish clinical accuracy, medical safety, or empirical superiority of `DV-OGEC-RAG` (`A1`) over `GENERIC` (`G`) or `A0`.**

---

## 1. Executive Summary of Verified Baseline Status

| Qualification Dimension | Verified Status / Result | Evidence Receipt / Provenance Identifier |
| :--- | :--- | :--- |
| **Qualified Git Baseline (`Agentic-RAG-KOA`)** | `ac4ade796e56377882b8069d0fb7a14809e8180b` | Scientific source SHA-256: `5aa87228b07ead1c4ecde48e7330e62771a86dbed7ac0fc4097f50152d306f5b` |
| **Active Prospective Protocol (`E1-v2`)** | `e1-v2.refined-full-primary.v2` | Protocol lock SHA-256: `98ad86c861986f3794d9b5818cafe44d396967340faf3631d6fb06d91006e5a3` |
| **Native `MOCK` Pilot Campaign (`pilot3`)** | **9 / 9 cells completed** (`PASS`) | Run `20261020T124525034329Z-c18d0afc7ed84f2d` (`closure-pilot-final.receipt.json`, `52.015s`, exit `0`) |
| **Native `MOCK` Full Campaign (`full`)** | **144 / 144 cells completed** (`PASS`) | Run `20261020T124618087083Z-031bcc4e5ec34fed` (`closure-parent-final.receipt.json`, `416.140s`, exit `0`) |
| **Critical Current-Source Test Selection** | **129 / 129 `PASS`** (`0` fail, `0` error, `0` skip) | `closure-critical-final.tests.json` (exit `0`, zero source drift) |
| **Historical Version Boundary Tests** | **41 / 41 `PASS`** & **23 / 23 `PASS`** | `test_qualification_admission_v2` (41/41) & `test_runtime_qualification_manifest` (23/23) |
| **Financial-Scope Isolation Integration** | **3 / 3 `PASS`** | `closure-financial-scope-final.receipt.json` (fictional ledgers; real approvals remain inactive) |
| **Provider Static Compatibility Matrix** | **14 / 14 probe schemas `QUALIFIED_OFFLINE`** | `provider-compatibility-final.json` (OpenAI SDK `3.15.0`, fictional client) |
| **CLI Replay & Export Verification** | **9 / 9 CLI actions `PASS`** | `verified-demo-final/demo.json` (JSON/CSV/Markdown exports verified) |
| **Reconciled Offline Regression Inventory** | **`PARTIAL`: 103 / 109 modules completed** (`1,400 PASS`, `21 SKIP`, `0 FAIL/ERROR`, `6 RESOURCE_BLOCKED`) | `regression-reconciled.json` (composite of initial 102/109 run + sequential resource-admitted retry) |
| **Actual `E1-v2` Real-Provider Execution** | **`NOT_EXECUTED`** (`0` real API calls) | Requires credentials, financial policy activation, and explicit LIVE spending authorization |
| **Independent Clinical-Quality Evaluation** | **`NOT_EVALUABLE`** (`0 / 16` eligible items) | `SCORING_BLOCKED_BY_OWNER_REFERENCE` (trusted owner evaluation registry is empty) |

---

## 2. Native `MOCK` Campaign Results (`pilot3` and `full`)

Both the 9-cell engineering pilot (`pilot3`) and the 144-cell full parent campaign (`full`) were executed on the declared Windows host using the **real native MedCPT + FAISS retrieval substrate (`koa-frozen-medcpt-v1`)** and the **real compiled `DV-OGEC-RAG` controller and `Staged POST v4` validators**, paired with the deterministic offline fake SDK (`qualification/e1_v2_mock.py`).

### 2.1 Execution Telemetry

| Metric / Property | Native `MOCK` Pilot (`pilot3`) | Native `MOCK` Full Campaign (`full`) |
| :--- | :--- | :--- |
| **Run Identifier** | `20261020T124525034329Z-c18d0afc7ed84f2d` | `20261020T124618087083Z-031bcc4e5ec34fed` |
| **Plan Hash (SHA-256)** | `8a0c52f6e7c5bd6cbc02e85e5e15952b4be8934a949d120e0f2810caa43ba364` | `f11bd863d697dce57987e4f040ab7e632ad894189731e921c9b751a1c3b4cca1` |
| **DEV Questions $\times$ Replicates $\times$ Arms** | $3 \times 1 \times 3 = \mathbf{9\text{ cells}}$ | $16 \times 3 \times 3 = \mathbf{144\text{ cells}}$ |
| **Shared Preparations (`Planner` + $E_0$)** | $3$ | $48$ |
| **Terminal Cells Completed** | **9 / 9** (`0` missing, `0` failed) | **144 / 144** (`0` missing, `0` failed) |
| **Fictional SDK Requests Accounted** | **107** (includes 14 extended qualification calls) | **1,137** |
| **Real Provider API Requests / Real Cost** | **0 calls / USD 0.00** | **0 calls / USD 0.00** |
| **Native Wall-Clock Elapsed Time** | `52.015 s` | `416.140 s` |
| **Process Exit / Source Drift** | `0x0` / `False` | `0x0` / `False` |

### 2.2 Scripted Controller Observations in `MOCK` Mode

In `MOCK` mode, the deterministic fake SDK (`qualification/e1_v2_mock.py`) supplies scripted responses designed to exercise all controller branches—including initial `READY`, initial `INSUFFICIENT` triggering `CORRECTIVE_RETRIEVAL` ($\le 1$) and `PRE` recheck, and `NEEDS_REVISION` triggering `REVISION_CYCLE` ($\le 1$) and second `POST`. Because the fake SDK is symmetric across arms, **each arm exhibits identical controller counts by construction**:

| `MOCK` Campaign & Arm | Per-Arm Cells | Initial PRE `READY` | Final PRE `READY` | Corrective Retrieval Used | Grounded Revision Used | `COMPLETED_ANSWER` (`ACCEPT`) | `COMPLETED_ABSTAIN` (`ABSTAIN`) | Technical Failure (`FAILED_*`) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **`pilot3` — Each of `A0`, `A1`, `G`** | 3 | 2 | 3 | 1 | 1 | 3 | 0 | 0 |
| **`full` — Each of `A0`, `A1`, `G`** | 48 | 45 | 48 | 3 | 3 | 48 | 0 | 0 |

> [!CAUTION]
> **Interpretation of `MOCK` Observations:** The identical numbers across `A0`, `A1`, and `G` in Table 2.2 reflect **deterministic branch-coverage scripting**, not empirical parity or medical accuracy. In accordance with the `E1-v2` protocol, `research/e1_v2.py` sets all comparative point estimates and bootstrap confidence intervals to `null` when `execution_kind == "MOCK"`.

---

## 3. Scientific Outcome Eligibility Matrix

The table below reports the exact evaluation status of every scientific endpoint across the authorized `KOA-GuidelineBench rc0.2.0` scope at the Engineering Closure baseline:

| Scientific Endpoint / Research Question | Eligible `E1-v2` Items (Authorized Scope) | Official Status | Exact Missing Prerequisite / Contract |
| :--- | :---: | :--- | :--- |
| **`A1` vs. `G` Primary Clinical Decision Quality** | **0 / 16** | `NOT_EVALUABLE` | Independent clinical reference labels and prospective qualified three-arm scorer |
| **`A1` vs. `A0` Question-Visibility Quality Effect** | **0 / 16** | `NOT_EVALUABLE` | Independent clinical reference labels and prospective qualified three-arm scorer |
| **$E_0$ / $E_1$ PRE Sufficiency & False Abstention (FAR)** | **0 / 16** | `NOT_EVALUABLE` | Independently adjudicated evidence-snapshot sufficiency (Task B displayed-bundle labels cannot transfer) |
| **Corrective Evidence Recovery Success** | **0 / 16** | `NOT_EVALUABLE` | Independently mapped missing/recoverable target evidence IDs |
| **Grounded Answer Correctness & Atomic Claim Support** | **0 / 16** | `NOT_EVALUABLE` | Reference answer/claim truth and qualified scoring authority |
| **Owner Corpus-Action Endpoint (Task C)** | 8 historical found-action records | `BLOCKED` | Current owner-approved `EvaluationContext`, mapping, scorer/adapter, and projection receipt (not clinical answer correctness) |
| **Task B Displayed-Bundle Sufficiency** | 5 pairs (9 distinct bundles, 4 intents) | `SEPARATE_CONTRACT` | Separate displayed-bundle task contract; never evaluated as `E1-v2` $E_0$/$E_1$ gold |
| **Verified EN–VI Cross-Lingual Consistency** | Unknown qualified pair count | `NOT_QUALIFIED` | Independent semantic-equivalence attestation unavailable |

---

## 4. Offline Regression Suite Breakdown

The complete offline test inventory comprises **109 test modules** (`tests/test_*.py`), executed under strict single-process isolation (`tests/run_koa_system_offline.py --isolated-modules`) with network sockets disabled, single-threaded native math libraries, and a 20,155-file write-protection guard:

1. **Initial Full-Inventory Pass (`regression-isolated-1792500819658442800/summary.json`):**
   - **102 modules `PASS`**, **7 modules `RESOURCE_BLOCKED`** (the Windows commit-memory admission guard observed $< 3\text{ GiB}$ available commit memory and declined to launch those 7 heavy native-model modules rather than risking OS paging crashes).
   - **1,399 tests started:** **1,378 `PASS`**, **21 `SKIP`**, **0 assertion failures**, **0 errors**, **0 native process crashes**, and **0 file drift**.
2. **Sequential Resource-Admitted Retry (`regression-reconciled.json`):**
   - When host commit headroom recovered, `test_e1_infrastructure` completed **22 / 22 `PASS`** (including the 96-cell native lifecycle test).
   - The remaining 6 modules stopped at the pre-test commit-memory admission gate without starting tests.
   - **Reconciled Composite Inventory:** **103 / 109 modules completed**, **1,421 tests started**, **1,400 `PASS`**, **21 explicit `SKIP`**, **0 `FAIL`**, **0 `ERROR`**, and **6 `RESOURCE_BLOCKED`**.
   - **6 Remaining `RESOURCE_BLOCKED` Modules** (require $\ge 3\text{ GiB}$ free Windows commit memory to run full module discovery):
     - `test_e1_recovery`
     - `test_e1_rolling_accounting`
     - `test_e1_v2`
     - `test_e1_v2_release`
     - `test_i5_real_construction`
     - `test_koa_system`
     *(Note: Targeted critical classes from these modules were independently verified in the 129/129 critical test receipt `closure-critical-final.tests.json`, and `test_koa_system` previously passed 22/22 in isolated module qualification.)*
3. **21 Explicit `SKIP` Cases (`skip-boundary-final.json`):**
   - **14 cases:** Require public prediction JSON-Schema validation via an optional `jsonschema` package not installed in the frozen offline `.venv`.
   - **6 cases:** Invoke owner deep validation requiring a permitted external owner configuration.
   - **1 case:** Owner-emitter test outside the authorized release-only runtime boundary.

---

## 5. Historical Exploratory `LIVE` Context (Pre-`E1-v2` Baseline)

Prior to the prospective `E1-v2` (`v4`) three-arm design, three historical exploratory `LIVE` runs were recorded under the earlier two-arm `E1` protocol (`FULL` vs. `GENERIC` on `v1`/`v3`, recorded in `docs/experiments/KOA_SYSTEM_HANDOFF.md`):

| Historical `LIVE` Run ID | Runtime Contract | Attempted / Planned Cells | Valid Terminal Cells | `ACCEPT` | `ABSTAIN` | Technical / Output Failures | Physical Requests | Settled Conservative Cost (USD) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `20261018T132457910134Z-0d28f3a552a549c0` | Original `E1` | 96 / 96 | 79 | 0 | 79 | 17 (POST output failures) | 287 | `0.5534230` |
| `20261018T155317026868Z-ff5d3673fdad4002` | `v3` | 5 / 96 (6th halted) | 3 | 0 | 3 | 2 persisted + 1 halted | 50 | `0.7648155` |
| `20261018T172729644801Z-f1d774719c05423a` | `e1.compact-grounded-staged-post.v3` | 94 / 96 (2 budget-stopped) | 87 | 3 (`FULL`: 3, `G`: 0) | 84 (`FULL`: 41, `G`: 43) | 6 model-output + 1 budget | 332 | `1.9030532` |

Forensic analysis of these historical two-arm runs (`docs/experiments/M5_ROOT_CAUSE_AND_RESEARCH_DECISIONS.md` and `M6_QUESTION_GROUNDED_SEMANTIC_CONTRAST.md`) motivated two strictly scoped design refinements that are tested prospectively in `E1-v2`:
1. Introducing question visibility in `A1` (`e1-v2.pre.question-plan-evidence.v1`) while retaining `A0` (`Plan + E0` only) as an explicit ablation control; and
2. Upgrading the POST wire to `e1.member-bound-staged-post.v4` to eliminate wire-level pair/alias truncation without relaxing semantic acceptance guards.

Historical `v3` observations are never merged into `E1-v2` (`v4`) analyses or treated as reference truth.
