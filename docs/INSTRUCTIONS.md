# INSTRUCTIONS – Setting up & running theSearcher

## Prerequisites
* Python 3.10+
* pip / venv or Poetry
* Google Cloud account with **Custom Search JSON API** enabled
* A Programmable Search Engine (CSE) with Image Search turned ON
* Git + Docker (optional for container run)

## 1  Clone & bootstrap

```bash
git clone https://github.com/<org>/theSearcher.git
cd theSearcher
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env            # fill in the two secrets
```

## 2 Obtain credentials
Go to https://console.cloud.google.com/apis/library/customsearch.googleapis.com

Enable API → Create credentials → API key.

Go to https://programmablesearchengine.google.com/ → Add
Sites to search: * (search across the web)
Search engine ID (cx) will look like 1234567890abcdef:g3hij4klm.

Edit .env:

```env
GOOGLE_API_KEY=AIza...abc
GOOGLE_CSE_ID=1234567890abcdef:g3hij4klm
```

## 3 Dry-run on a sample library
```bash
python src/theSearcher.py --input <your_image_query> --dry-run
```
Expected output: log indicating a search query would be made (no network calls).

## 4 Live run
```bash
python src/theSearcher.py --input <your_image_query>
```
First run performs actual search and download (watch quota consumption in logs).

## 5 Docker usage
```bash
docker build -t thesearcher .
docker run --rm -e GOOGLE_API_KEY -e GOOGLE_CSE_ID thesearcher --input <your_image_query>
```

## 6 Continuous integration
Push to GitHub; CI workflow (.github/workflows/ci.yml) will:

Lint (ruff / black).

Run unit tests.

Build Docker image.

Publish thesearcher:<commit> to GHCR (requires secrets).

## 7 Troubleshooting
| Symptom | Likely Cause | Remedy |
|---|---|---|
| 403 Daily Limit Exceeded | Out of free quota | Wait 24 h or enable billing |
| Irrelevant images downloaded | Ambiguous search query |
| SSL handshake error on Alpine | CA certs missing | Re-build image (apk add ca-certificates) |
