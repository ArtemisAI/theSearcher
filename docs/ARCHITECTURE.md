 # Architecture Overview – theSearcher

 ## 1 Components
 1. **Scanner** – walks the directory tree and detects missing images in folders.
 2. **Fetcher** – integrates with Google Custom Search API to retrieve relevant images.
 3. **Config Layer** – environment variables (`.env`) for API keys, search engine ID, logging levels.
 4. **Logging & Metrics** – Python `logging` for audit and debugging.
 5. **Container** – Docker image with entry-point CLI.

 ## 2 Data Flow
 ```text
 [Filesystem] → (Scanner) → missing? ──► (Fetcher) ─► [Google API]
 ▲        │                              ▼
 └────────┴─────────── download.jpg     logs/metrics ────▶ [File/Monitoring]
 ```

 ## 3 Error Handling
 * Network or quota errors: retry with back-off, then skip.
 * No images found: log warning and continue.

 ## 4 Extensibility
 * Provider interface for alternate search APIs.
 * Plugin system for image post-processing.