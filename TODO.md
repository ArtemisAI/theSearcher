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
=======
 # TODO – theSearcher

 > Move tasks rightwards (Backlog → In-Progress → Review → Done).
 > Keep each item atomic (≤ 1 day of work).

 ## Backlog
 - [ ] Create project skeleton (docs, logs, .gitignore, .dockerignore, .env.example)
 - [ ] Setup Python project structure (src/, tests/)
 - [ ] Configure environment variables and secrets handling
 - [ ] Implement basic image search and download feature
 - [ ] Setup logging and error handling
 ## In-Progress
 - [ ] None yet

 ## Review
 - [ ] None yet

 ## Done
 - [x] Add README.md stub

- [ ] Define project structure (directories, main files) - (Covered by initial setup)
- [ ] Implement folder iteration logic
- [ ] Implement image existence check in folders
- [ ] Research and select Google API for image search
- [ ] Implement Google Image Search functionality
- [ ] Implement image download and save functionality
- [ ] Implement logging for progress and errors
- [ ] Implement comprehensive error handling
- [ ] Write unit tests for folder iteration
- [ ] Write unit tests for image existence check
- [ ] Write unit tests for Google Image Search (mocking API calls)
- [ ] Write unit tests for image download
- [ ] Create `.env.example` with placeholder for API key
- [ ] Write script for user to input folder path
- [ ] Write main script execution flow
- [ ] Refine code and add comments
- [ ] Final testing and debugging