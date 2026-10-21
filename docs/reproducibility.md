# Reproducibility, Provenance & Public Release Boundary

This document defines what can be inspected and reproduced directly from this **public research documentation repository** (`KwanFam26022005/KOA-Agentic-RAG-System`), what resides in the **private qualified runtime repository** (`KwanFam26022005/Agentic-RAG-KOA`) and external benchmark review candidate (`KOA-GuidelineBench rc0.2.0`), and why specific assets are withheld under public-release security and copyright governance.

---

## 1. Two-Repository Separation Model

| Repository / Asset Location | Visibility | Scope & Contents |
| :--- | :---: | :--- |
| **`KwanFam26022005/KOA-Agentic-RAG-System`** *(This Repository)* | **PUBLIC** | Scientific documentation (`docs/`), verified Mermaid & SVG architecture diagrams (`assets/diagrams/`), academic report outline (`report/`), presentation storyboard (`slides/`), cryptographic provenance hashes, and sanitized aggregate results. |
| **`KwanFam26022005/Agentic-RAG-KOA`** *(Source Runtime Repository)* | **PRIVATE** | Python implementation (`dv_ogec_rag/`, `research/`, `benchmarks/`, `qualification/`, `tests/`), frozen experiment protocols/locks, qualification receipts (`qualification/reports/`), and Linux/RunPod provisioning runbooks. |
| **`KOA-GuidelineBench rc0.2.0`** *(External Benchmark Package)* | **INTERNAL REVIEW CANDIDATE** (`public_release = false`) | `runtime/` DEV/TEST inputs and 276 native guideline `EvidenceUnit` records; owner-separated `evaluator/` and `audit_provenance/` layers. |

---

## 2. Cryptographic Provenance Pinning

To allow independent auditors and collaborators with authorized access to verify exact artifact correspondence without exposing restricted text in a public repository, all key artifacts are pinned by their SHA-256 digests:

| Artifact Category | Identifier / Version | Pinned Digest (SHA-256 / Git SHA) |
| :--- | :--- | :--- |
| **Qualified Private Git Commit** | `Agentic-RAG-KOA` (`main`) | `ac4ade796e56377882b8069d0fb7a14809e8180b` |
| **Scientific Source Content Identity** | `build_source_identity` (`dv_ogec_rag/experiment.py`) | `5aa87228b07ead1c4ecde48e7330e62771a86dbed7ac0fc4097f50152d306f5b` |
| **Research Integration Identity** | `integration_identity` (`research/e1_runtime.py`) | `0155dc81df270dc5b6413ce6587aa52ed69e3cb7f415cd5146bf1188431ac927` |
| **Active `E1-v2` Protocol Lock** | `e1-v2.refined-full-primary.v2` (`protocol.lock.json`) | `98ad86c861986f3794d9b5818cafe44d396967340faf3631d6fb06d91006e5a3` |
| **Predecessor `E1-v2` v1 Protocol Lock** | `e1-v2.question-visibility.v1` | `85310854aaea4a1d2ca57095e5c63416b3da9813836ebddcf772e6544668575a` |
| **`E1-v2` Experiment Configuration** | `experiments/e1_pre_v2/config.json` | `5ce81a22cf4cbb828f9d20a1698934fa8add4697076d13b4dfd2a989754ed5cd` |
| **`E1-v2` Full Campaign Plan (144 cells)** | `full` profile (`16 x 3 x 3`) | `f11bd863d697dce57987e4f040ab7e632ad894189731e921c9b751a1c3b4cca1` |
| **`E1-v2` Pilot Campaign Plan (9 cells)** | `pilot3` profile (`3 x 1 x 3`) | `8a0c52f6e7c5bd6cbc02e85e5e15952b4be8934a949d120e0f2810caa43ba364` |
| **`KOA-GuidelineBench rc0.2.0` Release Manifest** | `REVIEW_RELEASE_MANIFEST.json` | `eda0e26c1832f41150b37da7780076f9ea04f55927765faaee3b4a2047e5985b` |
| **`KOA-GuidelineBench rc0.2.0` Runtime Manifest** | `runtime/BENCHMARK_MANIFEST.json` | `6538ef4413ebf4a3ee52cb06defd3420da7c7958cedcb017e9c8bf66505ecb47` |
| **Runtime Exposure Contract** | `runtime/RUNTIME_EXPOSURE_CONTRACT.json` | `4d9ee4cfa656b0ac5dbf13b5b22dccf37d69b6250c5b17c7e133e2237387caa4` |
| **Public Typed DEV Assignment (16 cases)** | `benchmarks/dev_e1.py` | `987f2bb21f0844ea1b9a041f686bec66296f60bc05883bd629c429ad5c1458f7` |
| **Native Guideline Corpus (276 units)** | `runtime/data/knowledge/evidence_units.jsonl` | `f9cdcccd5a0e97784ee59ceeb43292a6a8419c61ed6825180e37256e66e1de52` |
| **Frozen MedCPT FAISS Index Manifest** | `koa_rc02_medcpt_l2_v1/manifest.json` | `902dcb37c7d038dc556c1854428dd9033d31c6f3cdee1510b2971fa70edc0acb` |
| **NCBI MedCPT Article Encoder Revision** | `ncbi/MedCPT-Article-Encoder` (Hugging Face) | `d05a736da4bb84ee4057b7f7999485be6ed85465` |
| **NCBI MedCPT Query Encoder Revision** | `ncbi/MedCPT-Query-Encoder` (Hugging Face) | `d83a36cc6b8e3a5c5e9d9d6ba156808c1643dcbc` |

---

## 3. What Can vs. Cannot Be Reproduced from the Public Repository

### 3.1 Directly Verifiable from This Public Repository
1. **Architectural & Methodological Audit:** Complete inspection of the 5 system diagrams (`.mmd` and `.svg`), role contracts, controller state transitions, `PolicyGuard` preconditions, and the three-layer benchmark exposure matrix (`EXPOSURE_MATRIX.md` summary).
2. **Experimental Design & Protocol Verification:** Inspection of the 3-arm `E1-v2` block-randomized design (`A0`, `A1`, `G`), shared-preparation invariants, physical request ceilings, and statistical inference rules.
3. **Diagram Regeneration:** Any researcher with Node.js and `@mermaid-js/mermaid-cli` can regenerate all five SVG figures directly from `assets/diagrams/*.mmd`:
   ```bash
   npx @mermaid-js/mermaid-cli@11.17.0 -i assets/diagrams/02-agentic-rag-architecture.mmd -o assets/diagrams/02-agentic-rag-architecture.svg -b white -w 1600
   ```

### 3.2 Requires Authorized Access to the Private Runtime & Benchmark Assets
Executing `python -m research` commands (`benchmark validate`, `experiment e1_pre_v2 --mock`, `verify`, `evaluate`, or `tests/run_koa_system_offline.py`) requires:
1. **Private Source Checkout:** `KwanFam26022005/Agentic-RAG-KOA` at commit `ac4ade796e56377882b8069d0fb7a14809e8180b` (or handoff commit `3b81b843d6e95970069589b791c3c1ed675fe308`) with `source_hash` matching `5aa87228b07ead1c4ecde48e7330e62771a86dbed7ac0fc4097f50152d306f5b`.
2. **Python & Native Dependencies:** Python `3.11` (`3.11.9` used in Windows qualification), `torch==2.9.1`, `transformers`, `faiss-cpu`, `numpy`, and `openai==3.15.0` (fictional client in `MOCK` mode).
3. **Pinned MedCPT Snapshots (~837.12 MiB):** Publicly downloadable from Hugging Face at the exact revisions listed in Section 2, placed under `benchmarks/local/models/hf` with `HF_HUB_OFFLINE=1` and `TRANSFORMERS_OFFLINE=1`.
4. **Authorized `KOA-GuidelineBench rc0.2.0` `runtime/` Subset (~556 KB) & Frozen FAISS Index (~3.61 MiB):** Provisioned by the benchmark owner with verified SHA-256 hashes.
5. **Host Memory Headroom:** At least **3 GiB available commit memory** (`--min-commit-mib 3072`) and single-threaded native BLAS/OpenMP settings (`OPENBLAS_NUM_THREADS=1`, `OMP_NUM_THREADS=1`, `MKL_NUM_THREADS=1`, `TOKENIZERS_PARALLELISM=false`).

---

## 4. Protected Assets Excluded from Public Release

In compliance with public-release safety rules and copyright governance, the following asset classes are **strictly excluded** from this repository:

- **No Secrets or Credentials:** Zero `.env` files, API keys, tokens, SSH keys, or provider authentication headers.
- **No Licensed Clinical Guideline Text:** None of the 276 `EvidenceUnit` quotations, raw PDFs, or raw `RunStore` request/response payloads (which embed retrieved guideline text even in `MOCK` runs) are committed.
- **No Sealed Benchmark Gold or Evaluator Internals:** Zero `EVALUATOR_ONLY` or `REVIEWER_AUDIT_ONLY` files, canonical material obligations, accepted `EvidencePath` objects, or `TEST` split cases.
- **No Unlicensed Source Code or Binary Weights:** No private runtime `.py` modules, model `.safetensors`/`.bin` weights, `.faiss` indexes, or internal financial journals.
- **License Status:** No `LICENSE` file is included in this repository because redistribution rights for the underlying clinical guidelines and benchmark release remain `UNVERIFIED`, and source-code reuse licensing has not yet been granted. All rights remain reserved by the respective authors and guideline issuing bodies.
