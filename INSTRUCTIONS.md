0 Repository layout
arduino
Copy
Edit
audiobook-cover-fetcher/
├── docs/
│   ├── BUSINESS_REQUIREMENTS.md
│   ├── ARCHITECTURE.md
│   └── INSTRUCTIONS.md      ← step-by-step setup & usage
├── TODO.md                  ← living kanban – move items across columns
├── src/
│   ├── scan_audio_library.py
│   └── __init__.py
├── tests/
│   ├── unit/
│   └── integration/
├── .env.example
├── Dockerfile
└── .github/
    └── workflows/ci.yml
1 BUSINESS_REQUIREMENTS.md (place in docs/)
markdown
Copy
Edit
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

2 ARCHITECTURE.md (place in docs/)
markdown
Copy
Edit
# Architecture Overview

![diagram](docs/cover_fetcher_flow.svg)  <!-- optional, generate later -->

## 1  Components
1. **Scanner** (`scan_audio_library.py`) – walks the directory tree, detects folders that lack an image file.
2. **Fetcher** (google-images-search wrapper) – calls Google Custom Search, downloads the first XLARGE JPEG.
3. **Config Layer** – `.env` or ENV vars for API key, CSE ID, concurrency.
4. **Logging & Metrics** – Python `logging`, Prometheus textfile export (future).
5. **Container** – Alpine-based Docker image, entry-point is the scanner CLI.

## 2  Data Flow
[Filesystem] → (Scanner) → need_cover? ──► (Fetcher) ─► [Google API]
▲ └──► download.jpg
└────────────── logs / metrics ────────────────────────────────┘

markdown
Copy
Edit

## 3  Error Handling
* Network or quota errors raise `GoogleImagesSearchError` → exponential back-off, then skip.
* If no audio file detected → folder logged at WARNING level, skipped.

## 4  Extensibility
* Provider interface in `providers/__init__.py`; add `SerpAPIProvider` later.
* Plug-in system for audio-tag embedding (`plugins/tagger_mutagen.py`).

3 INSTRUCTIONS.md (place in docs/)
markdown
Copy
Edit
# INSTRUCTIONS – Setting up & running the Audiobook Cover Fetcher

## Prerequisites
* Python 3.10+
* pip / venv or Poetry
* Google Cloud account with **Custom Search JSON API** enabled
* A Programmable Search Engine (CSE) with Image Search turned ON
* Git + Docker (optional for container run)

## 1  Clone & bootstrap

```bash
git clone https://github.com/<org>/audiobook-cover-fetcher.git
cd audiobook-cover-fetcher
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env            # fill in the two secrets
2 Obtain credentials
Go to https://console.cloud.google.com/apis/library/customsearch.googleapis.com

Enable API → Create credentials → API key.

Go to https://programmablesearchengine.google.com/ → Add
Sites to search: * (search across the web)
Search engine ID (cx) will look like 1234567890abcdef:g3hij4klm.

Edit .env:

env
Copy
Edit
GOOGLE_API_KEY=AIza...abc
GOOGLE_CSE_ID=1234567890abcdef:g3hij4klm
3 Dry-run on a sample library
bash
Copy
Edit
python src/scan_audio_library.py ~/Media/Audiobooks --dry-run
Expected output: list of folders that would receive art (no network calls).

4 Live run
bash
Copy
Edit
python src/scan_audio_library.py ~/Media/Audiobooks
First run downloads actual images (watch quota consumption in logs).

5 Docker usage
bash
Copy
Edit
docker build -t cover-fetcher .
docker run --rm -v "$HOME/Media/Audiobooks:/library" \
           -e GOOGLE_API_KEY -e GOOGLE_CSE_ID \
           cover-fetcher /library
6 Continuous integration
Push to GitHub; CI workflow (.github/workflows/ci.yml) will:

Lint (ruff / black).

Run unit tests.

Build Docker image.

Publish cover-fetcher:<commit> to GHCR (requires secrets).

7 Troubleshooting
Symptom	Likely Cause	Remedy
403 Daily Limit Exceeded	Out of free quota	Wait 24 h or enable billing
Random photos not covers	Ambiguous title	Include author in filename (1984 - George Orwell.m4b)
SSL handshake error on Alpine	CA certs missing	Re-build image (apk add ca-certificates)

yaml
Copy
Edit

---

## 4  TODO.md  (root level – single source of truth for work items)

```markdown
# TODO – Audiobook Cover Fetcher

> Move tasks rightwards (Backlog → In-Progress → Review → Done).  
> Keep each item atomic (≤ 1 day of work).

## Backlog
- [ ] Design `Provider` abstract class to allow SerpAPI fallback.
- [ ] Write `.github/ISSUE_TEMPLATE/bug_report.md`.
- [ ] Add Prometheus metrics export (scan duration, success / failure counts).
- [ ] Generate architecture diagram (`docs/cover_fetcher_flow.svg`) via Mermaid.

## In-Progress
- [ ] **#12** Implement `--dry-run` CLI flag (Eve).

## Review
- [ ] **#7** Dockerfile multi-stage build (Bob).

## Done
- [x] Initialise repo, commit PoC script. (Alice)
- [x] Set up GitHub Actions CI. (DevOps)

5 Next steps for the team
Stage	Time-box	Deliverable
0 Kick-off & environment	½ day	Repo skeleton, docs committed
1 Prototype	2 days	scan_audio_library.py working on local sample
2 Robustness	3 days	Error handling, logging, back-off, unit tests
3 Packaging	1 day	Docker image, .env.example, README update
4 CI/CD	1 day	Linting, tests, image push on tag
5 Audit & hand-off	½ day	Manual QA run on 1 k folder library, metrics report

You now have all core project artefacts ready for the team:

Business requirements (why & what).

Architecture (how).

Instructions (setup & operations).

TODO kanban (work management).

Copy them into your repo and iterate – the skeleton covers everything the devs and DevOps will need to know to finish the job in orderly stages.
