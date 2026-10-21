# Implementation & Engineering Architecture

This document maps the high-level software modules of the private research runtime (`KwanFam26022005/Agentic-RAG-KOA`, qualified commit `ac4ade796e56377882b8069d0fb7a14809e8180b`, scientific source hash `5aa87228b07ead1c4ecde48e7330e62771a86dbed7ac0fc4097f50152d306f5b`, integration hash `0155dc81df270dc5b6413ce6587aa52ed69e3cb7f415cd5146bf1188431ac927`), explaining how the theoretical contracts of `DV-OGEC-RAG` and `KOA-GuidelineBench` are realized in code.

---

## 1. High-Level Module Mapping

The private research codebase is partitioned into four top-level packages with strict dependency direction (`benchmarks/` and `dv_ogec_rag/` never import `research/` or owner evaluator internals):

| Package / Directory | Core Modules | Engineering Responsibility |
| :--- | :--- | :--- |
| **`dv_ogec_rag/`** *(Core Method Runtime)* | `contracts.py`, `control.py`, `variants.py`, `runner_workflow.py`, `runner.py` | Closed typed dataclasses (`RuntimeQuestion`, `Plan`, `MaterialObligation`, `EvidenceMemory`, `AtomicClaim`); `ValidActionSet`, `DeterministicRulesPolicy`, `PolicyGuard`, `Controller`; variant definitions (`METHOD_FULL_DVOGEC`, `MATCHED_GENERIC_PRESTATE`); workflow compiler (`compile_workflow`) and one-shot `ComposedRuntime`. |
| **`dv_ogec_rag/`** *(Retrieval & Verification Adapters)* | `koa_medcpt.py`, `koa_retrieval.py`, `pre_wire.py`, `generic_prestate.py`, `post_decision.py`, `scoped_pairs.py`, `staged_post.py`, `member_post.py`, `real_construction.py`, `llm.py` | Offline pinned MedCPT encoders and FAISS `IndexFlatIP` (`top_k = 8`, pre-scoring source filter); `A0`/`A1` obligation PRE wire and `G` generic pre-state wire; `e1.member-bound-staged-post.v4` (`pair`, `diagnosis`, `remedies` passes); OpenAI Responses transport adapter with strict JSON schema validation. |
| **`dv_ogec_rag/`** *(Campaign & Accounting Engine)* | `paired_campaign.py`, `provider_accounting.py`, `campaign_durability.py`, `evaluator_boundary.py` | Blocked shared-preparation execution (`prepare_shared_block`), matched substrate verification (`validate_matched_configs`), per-role call ceilings (`role_maxima`), and append-only `RunBudget` journal. |
| **`benchmarks/`** *(Benchmark Connectors)* | `contracts.py`, `catalog.py`, `dev_e1.py`, `koa_rc02.json`, `docoa.py`, `docoa.json` | Closed public DEV allowlist for `KOA-GuidelineBench rc0.2.0`; cryptographic verification of release, runtime, split, and corpus hashes; construction of `GoldFreeRuntimeInput` / `DevSample`; structural smoke adapter for external `DocOA`. |
| **`research/`** *(Experiment CLI & Read-Only Evaluation)* | `__main__.py`, `e1_engine.py`, `e1_runtime.py`, `e1_v2.py`, `persistence.py`, `accounting.py`, `financial_scopes.py`, `provider_qualification.py`, `evaluation.py`, `owner_scoring.py`, `failure_taxonomy.py` | Unified CLI (`python -m research`), `E1-v2` plan compiler (`full` 144-cell and `pilot3` 9-cell profiles), nonclinical provider qualification phase, append-only `RunStore`, failure localization, and read-only owner evaluation reconciliation. |
| **`qualification/` & `tests/`** *(Verification Harness)* | `qualification/e1_v2_mock.py`, `tests/e1_fake_sdk.py`, `tests/run_koa_system_offline.py` | Deterministic native MOCK client exercising all `A0`/`A1`/`G` branches (including correction and revision), Windows commit-memory admission guards (`--min-commit-mib 3072`), and 109-module isolated regression suite. |

---

## 2. Native Execution and Shared Preparation Engine

When `research/e1_engine.py` executes an `E1-v2` campaign (`--mock` or `--execute`), it runs the **actual native pipeline**—not a simplified script or mock state machine:

1. **Asset & Protocol Lock Preflight (`e1_v2.validate` & `validate_assets`):**
   - Verifies that `docs/experiments/E1_V2_SCIENTIFIC_PROTOCOL.md` matches the raw SHA-256 pinned in `experiments/e1_pre_v2/protocol.lock.json` (`98ad86c861986f3794d9b5818cafe44d396967340faf3631d6fb06d91006e5a3`), and that the experiment configuration pins the exact lock hash (`5ce81a22cf4cbb828f9d20a1698934fa8add4697076d13b4dfd2a989754ed5cd`).
   - Verifies the local MedCPT encoder snapshots and the 276-vector FAISS `IndexFlatIP` artifact hashes (`902dcb37c7d038dc556c1854428dd9033d31c6f3cdee1510b2971fa70edc0acb`).
2. **Nonclinical Provider Qualification Phase (`research/provider_qualification.py`):**
   - Before initializing the retrieval models or dispatching benchmark cells, an optional 9-call (`representative`) or 14-call (`extended`) nonclinical probe invokes the native `Planner`, `A0 PRE`, `A1 PRE`, `G PRE`, `Generator`, `Decomposer`, and member-bound `POST` (`pair`, `diagnosis`, `remedies`) adapters—plus `A1` recheck, grounded revision, and second `POST` in `extended` mode—to verify transport and closed-schema adherence under the same campaign budget cap.
3. **Shared Block Preparation (`prepare_shared_block`):**
   - For each of the 48 `(question_id, replicate)` blocks (or 3 blocks in `pilot3`), invokes the `Planner` once and executes local MedCPT `INITIAL_RETRIEVAL` once.
   - Freezes `Plan` and $E_0$ and records their digests before any arm cell runs.
4. **Counterbalanced Arm Execution (`execute_cell`):**
   - Dispatches `A0`, `A1`, and `G` according to the block's assigned permutation (`execution_order`).
   - Each arm runs inside a fresh one-shot `ComposedRuntime` instance with its respective PRE contract and corrective query builder, followed by the shared downstream `v4` pipeline and `PolicyGuard`.

---

## 3. Immutable `RunStore` and Append-Only Persistence

All campaign outputs are persisted through `research/persistence.py` and `dv_ogec_rag/campaign_durability.py` under `experiments/<family>/runs/<run-id>/`:

- **`manifest.json`:** Written once before cell dispatch. Pins `run_id`, `execution_mode` (`MOCK` vs. `LIVE`), Git `HEAD`, `source_hash` (`build_source_identity`), `integration_hash`, `protocol_lock_sha256`, `config_sha256`, `plan_hash`, and role/provider identities.
- **Append-Only Cell & Trajectory Records:** Each completed or failed arm cell is flushed immediately with `fsync`. If a process is interrupted mid-campaign, already persisted terminal rows remain intact while the run summary stays `RUNNING` / `PARTIAL`; no unsealed run is silently rewritten as `COMPLETED` or automatically resumed.
- **Cryptographic Verification (`research verify --run <RUN_ID>`):** Recomputes trajectory digests, checks cell completeness against the planned inventory, verifies that `MOCK` runs are never marked eligible for scientific scoring, and flags any divergence between `traces/progress.jsonl` and `summary.json`.

---

## 4. Pre-Dispatch Financial Accounting and Fault Safety

Because multi-stage agentic verification with batched POST passes can issue up to 34 physical LLM requests per cell in the worst case, the runtime enforces **strict pre-dispatch financial accounting** (`dv_ogec_rag/provider_accounting.py` and `research/financial_scopes.py`):

1. **Single Operator Cap (`--max-cost-usd`):** Every LLM call—including nonclinical provider qualification probes—must reserve its conservative worst-case cost in the `RunBudget` journal *before* the HTTP request is sent (`INTENT` record) and settle actual token usage upon completion (`USAGE` record).
2. **Dual Ceiling Enforcement:** Admission checks each request against both the per-run cap and the applicable financial scope (`legacy-shared` preserves the historical `USD 5.00` aggregate cap, `USD 4.491997350` recorded exposure, and `USD 1.05` quarantined unknown-usage liability `#87`; `independent-campaign` requires a separate explicit policy activation and remains inactive by default).
3. **Fail-Closed Journal Durability:** Failed, short, or partial journal appends restore the writer's last confirmed in-memory state, mark storage uncertain, and permanently block further dispatch from that writer without truncating existing journal bytes.

---

## 5. Verification CLI Surface

The research engine exposes a deterministic, JSON-capable CLI (`python -m research`) verified in the Engineering Closure (`verified-demo-final/demo.json`):

```powershell
# 1. Validate KOA-GuidelineBench rc0.2.0 public DEV contract & hashes
python -X utf8 -B -m research benchmark validate --benchmark koa-guidelinebench --json

# 2. Inspect benchmark cardinalities and exposure boundaries
python -X utf8 -B -m research benchmark inspect --benchmark koa-guidelinebench --json

# 3. Validate E1-v2 protocol lock, config pins, and retrieval assets
python -X utf8 -B -m research experiment e1_pre_v2 --validate --json

# 4. Compile deterministic execution plan (pilot3 or full)
python -X utf8 -B -m research experiment e1_pre_v2 --plan --plan-profile pilot3 --provider-qualification extended --json

# 5. Perform read-only preflight / dry-run (zero dispatch, zero ledger writes)
python -X utf8 -B -m research experiment e1_pre_v2 --dry-run --plan-profile pilot3 --provider-qualification extended --max-cost-usd 5 --json

# 6. Verify persisted run integrity and evaluate read-only outputs
python -X utf8 -B -m research verify --run <RUN_ID> --json
python -X utf8 -B -m research evaluate e1_pre_v2 --run <RUN_ID> --json
python -X utf8 -B -m research report e1_pre_v2 --run <RUN_ID> --output <NEW_EXPORT_DIR> --json
```
