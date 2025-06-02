# Business Requirements – Audiobook Cover Fetcher

| Version | Author | Date        |
| ------- | ------ | ----------- |
| 1.0     | <Your Name> | 2025-06-01 |

## 1  Purpose
Our audiobook collection is organised by *one folder per title*, but roughly 40 % of the folders have no cover art.
Missing artwork confuses end-users, mobile apps and DLNA servers, and reduces catalogue appeal.
The goal is to **detect unillustrated titles and pull a high-resolution cover into each folder automatically**.

## 2  Success Criteria
| ID | Metric | Target |
| -- | ------ | ------ |
| SC-1 | Detection accuracy | ≥ 98 % of missing-art folders are flagged |
| SC-2 | Cover relevance | ≥ 95 % of downloaded images visually match the title (manual audit) |
| SC-3 | Throughput | 500 folders processed in < 10 min on a 1-vCPU VM |
| SC-4 | Costs | ≤ $5 / 1000 look-ups (stays within Google free tier for routine workloads) |
| SC-5 | Compliance | Uses only officially supported APIs; no scraping |

## 3  Scope
✅ Included
* Local file-system scan (Linux, macOS, Windows).
* Google Programmable Search Engine (Custom Search JSON API).
* Image download and storage as `cover.jpg` in the target folder.
* CLI, Docker image, unit + integration tests, GitHub Actions CI pipeline.

❌ Excluded
* Embedding artwork into audio file tags (could be a phase-2 epic).
* GUI front-end.
* Multi-tenant cloud deployment.

## 4  Stakeholders
| Role               | Name / Team       | Responsibility                  |
| ------------------ | ----------------- | ------------------------------ |
| Product Owner      | …                 | Define acceptance criteria      |
| Tech Lead          | …                 | Architecture & code reviews     |
| DevOps             | …                 | Build pipeline & container      |
| QA                 | …                 | Test plan & audit SC-1/SC-2      |

## 5  Assumptions & Risks
* Google may change pricing or quota; mitigate via SerpAPI fallback.
* Some titles share names – disambiguation relies on filenames including author or series.
* Free tier (100 req/day) is enough for daily incremental runs; initial backfill may need a temporary paid burst.
