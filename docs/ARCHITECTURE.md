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
=======
# Project Architecture

## Overview
The application will be a Python script designed to run locally. It will scan a user-specified directory of music albums, identify albums missing cover art, search for appropriate art using the Google Images API, and download it.

## Components
1.  **Main Script (`src/album_art_downloader.py`):**
    *   Handles command-line arguments (input folder path).
    *   Orchestrates the overall process.
    *   Initializes and uses other components.

2.  **Folder Scanner (`src/folder_utils.py`):**
    *   Responsible for iterating through subdirectories of the main music folder.
    *   Identifies potential album folders.

3.  **Image Checker (`src/image_utils.py`):**
    *   Checks if a recognized image file (e.g., `cover.jpg`, `folder.png`) already exists in an album folder.
    *   Supports common image extensions (JPEG, PNG).

4.  **Google Image Search Client (`src/google_image_client.py`):**
    *   Manages interaction with the Google Custom Search JSON API.
    *   Constructs search queries based on folder names (album titles).
    *   Retrieves search results.
    *   Requires an API key, which will be stored in a `.env` file.

5.  **Image Downloader (`src/image_utils.py`):**
    *   Handles downloading the selected image from a URL.
    *   Saves the image to the appropriate album folder with a standardized name.

6.  **Logging Module:**
    *   Standard Python `logging` module.
    *   Configured to log important events, errors, and progress.
    *   Output to console and potentially a log file.

7.  **Configuration (`.env`):**
    *   Stores sensitive information like the Google API Key.
    *   Loaded at runtime.

## Data Flow
1.  User runs the script, providing a path to their music library.
2.  The **Main Script** invokes the **Folder Scanner**.
3.  **Folder Scanner** identifies an album folder.
4.  **Main Script** invokes the **Image Checker** for that folder.
5.  If no image is found:
    a.  **Main Script** uses the folder name to instruct **Google Image Search Client** to find album art.
    b.  **Google Image Search Client** returns a list of potential image URLs.
    c.  **Main Script** (or a dedicated selection logic) picks the best URL.
    d.  **Main Script** instructs **Image Downloader** to fetch and save the image.
6.  Process repeats for all album folders.
7.  **Logging Module** records actions and errors throughout the process.

## Error Handling
-   API request failures (network issues, invalid API key).
-   Image download failures.
-   File system errors (permissions, disk space).
-   Invalid input folder path.

## Future Considerations
-   Asynchronous operations for API calls and downloads to improve performance for large libraries.
-   A more sophisticated image selection module (e.g., using image analysis or user preferences).
-   Plugin architecture for different image search providers or metadata sources.
