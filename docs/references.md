# References & Verified Bibliography

All references listed below correspond to real, verifiable scholarly publications or official clinical practice guidelines referenced in the `KOA-GuidelineBench` (`rc0.2.0`) source registry and the `DV-OGEC-RAG` methodological design.

---

## 1. Clinical Practice Guidelines in `KOA-GuidelineBench` (`rc0.2.0`)

1. **ACSQHC (2024)** — Australian Commission on Safety and Quality in Health Care. *Osteoarthritis of the Knee Clinical Care Standard (2024)*. Sydney: ACSQHC; 2024.  
   - **Benchmark `source_id`:** `acsqhc_koa_2024` (`CURRENT`, English, 32 evidence units)  
   - **Official URI:** <https://www.safetyandquality.gov.au/resources/osteoarthritis-knee-clinical-care-standard-2024>

2. **BYT Vietnam (2014)** — Bộ Y tế (Ministry of Health, Vietnam). *Hướng dẫn chẩn đoán và điều trị các bệnh cơ xương khớp* (Ban hành kèm theo Quyết định số 361/QĐ-BYT ngày 25/01/2014). Hà Nội: Bộ Y tế; 2014.  
   - **Benchmark `source_id`:** `byt_cxuongkhop_2014` (`HISTORICAL`, Vietnamese, 39 evidence units)  
   - **Official URI:** <https://kcb.vn/van-ban/huong-dan-chan-doan-va-dieu-tri-cac-benh-co-xuong-khop.html>

3. **EULAR (2023 / published 2024)** — Moseng T, Vliet Vlieland TPM, Battista S, Beckwee D, Boyadzhieva V, Conaghan PG, et al. EULAR recommendations for the non-pharmacological core management of hip and knee osteoarthritis: 2023 update. *Annals of the Rheumatic Diseases*. 2024;83(6):730–740.  
   - **Benchmark `source_id`:** `eular_koa_2023` (`CURRENT`, English, 24 evidence units)  
   - **DOI:** [10.1136/ard-2023-225041](https://doi.org/10.1136/ard-2023-225041)

4. **NICE NG226 (2022)** — National Institute for Health and Care Excellence. *Osteoarthritis in over 16s: diagnosis and management* (NICE Guideline NG226). London: NICE; published 19 October 2022.  
   - **Benchmark `source_id`:** `nice_ng226_2022` (`CURRENT`, English, 84 evidence units)  
   - **Official URI:** <https://www.nice.org.uk/guidance/ng226/>

5. **VA/DoD (2026)** — U.S. Department of Veterans Affairs and Department of Defense. *VA/DoD Clinical Practice Guideline for the Non-Surgical Management of Hip & Knee Osteoarthritis*. Washington, DC: Department of Veterans Affairs / Department of Defense; 2026.  
   - **Benchmark `source_id`:** `va_dod_oa_2026` (`CURRENT`, English, 97 evidence units)  
   - **Official URI:** <https://www.healthquality.va.gov/HEALTHQUALITY/guidelines/CD/OA/index.asp>

---

## 2. Retrieval-Augmented Generation, Self-Reflection & Atomic Verification

6. **RAG (Foundational Architecture)** — Lewis P, Perez E, Piktus A, Petroni F, Karpukhin V, Goyal N, et al. Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks. In: *Advances in Neural Information Processing Systems (NeurIPS)*, Vol. 33, pp. 9459–9474; 2020.  
   - **arXiv:** [2005.11401](https://arxiv.org/abs/2005.11401)

7. **Self-RAG (Reflective Retrieval & Critique)** — Asai A, Wu Z, Wang Y, Sil A, Hajishirzi H. Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection. In: *Twelfth International Conference on Learning Representations (ICLR)*; 2024.  
   - **arXiv:** [2310.11511](https://arxiv.org/abs/2310.11511)

8. **CRAG (Corrective Retrieval-Augmented Generation)** — Yan S-Q, Gu J-C, Zhu Y, Ling Z-H. Corrective Retrieval Augmented Generation. *arXiv preprint*; 2024.  
   - **arXiv:** [2401.15884](https://arxiv.org/abs/2401.15884)

9. **FActScore (Atomic Claim Decomposition & Verification)** — Min S, Krishna K, Lyu X, Lewis M, Yih W-t, Koh PW, Iyyer M, Zettlemoyer L, Hajishirzi H. FActScore: Fine-grained Atomic Evaluation of Factual Precision in Long Form Text Generation. In: *Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing (EMNLP)*, pp. 12076–12100; 2023.  
   - **DOI:** [10.18653/v1/2023.emnlp-main.741](https://doi.org/10.18653/v1/2023.emnlp-main.741) · **arXiv:** [2305.14251](https://arxiv.org/abs/2305.14251)

10. **Selective Question Answering & Abstention** — Kamath A, Jia R, Liang P. Selective Question Answering under Domain Shift. In: *Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics (ACL)*, pp. 5684–5696; 2020.  
    - **DOI:** [10.18653/v1/2020.acl-main.503](https://doi.org/10.18653/v1/2020.acl-main.503) · **arXiv:** [2006.09462](https://arxiv.org/abs/2006.09462)

---

## 3. Biomedical Information Retrieval, Vector Indexing & Medical QA Benchmarks

11. **MedCPT (Biomedical Contrastive Pre-trained Transformers)** — Jin Q, Kim W, Chen Q, Comeau DC, Yeganova L, Wilbur WJ, Lu Z. MedCPT: Contrastive Pre-trained Transformers with large-scale PubMed search logs for zero-shot biomedical information retrieval. *Bioinformatics*. 2023;39(11):btad651.  
    - **DOI:** [10.1093/bioinformatics/btad651](https://doi.org/10.1093/bioinformatics/btad651) · **arXiv:** [2307.00589](https://arxiv.org/abs/2307.00589)

12. **FAISS (Exact & Approximate Similarity Search)** — Johnson J, Douze M, Jégou H. Billion-Scale Similarity Search with GPUs. *IEEE Transactions on Big Data*. 2021;7(3):535–547.  
    - **DOI:** [10.1109/TBDATA.2019.2921572](https://doi.org/10.1109/TBDATA.2019.2921572) · **arXiv:** [1702.08734](https://arxiv.org/abs/1702.08734)

13. **MIRAGE (Medical RAG Benchmark)** — Xiong G, Jin Q, Lu Z, Zhang A. Benchmarking Retrieval-Augmented Generation for Medicine. In: *Findings of the Association for Computational Linguistics: ACL 2024*, pp. 6233–6251; 2024.  
    - **DOI:** [10.18653/v1/2024.findings-acl.372](https://doi.org/10.18653/v1/2024.findings-acl.372) · **arXiv:** [2402.13178](https://arxiv.org/abs/2402.13178)

14. **Osteoarthritis Benchmark (`DocOA` External Adapter Reference)** — OpenMedLab. *Osteoarthritis-Benchmark* (`GIQA` / `MOQA` subsets, pinned commit `ed05e1e2aa61db86db30d7eb3ff6fe32498f33f0`).  
    - **Repository:** <https://github.com/openmedlab/Osteoarthritis-Benchmark>
