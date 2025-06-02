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

## 3  Error Handling
* Network or quota errors raise `GoogleImagesSearchError` → exponential back-off, then skip.
* If no audio file detected → folder logged at WARNING level, skipped.

## 4  Extensibility
* Provider interface in `providers/__init__.py`; add `SerpAPIProvider` later.
* Plug-in system for audio-tag embedding (`plugins/tagger_mutagen.py`).
