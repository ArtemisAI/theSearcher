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
=======
 # INSTRUCTIONS – Setting up & running theSearcher

 ## Prerequisites
 * Python 3.10+
 * pip / venv or Poetry
 * Google Cloud account with **Custom Search JSON API** enabled
 * A Programmable Search Engine (CSE) with Image Search turned ON
 * Git + Docker (optional for container run)

 ## 1 Clone & bootstrap
 ```bash
 git clone https://github.com/<org>/theSearcher.git
 cd theSearcher
 python -m venv .venv && source .venv/bin/activate
 pip install -r requirements.txt
 cp .env.example .env            # fill in the two secrets
 ```

 ## 2 Obtain credentials
 1. Enable Custom Search API in Google Cloud console
 2. Create an API key
 3. Create a Programmable Search Engine at https://programmablesearchengine.google.com/ (enable Image Search)
 4. Note your Search Engine ID (cx)
 5. Update `.env` with your `GOOGLE_API_KEY` and `GOOGLE_CSE_ID`

 ## 3 Dry-run
 ```bash
 python src/theSearcher.py --dry-run <path_to_image_library>
 ```

 ## 4 Live run
 ```bash
 python src/theSearcher.py <path_to_image_library>
 ```

 ## 5 Docker usage
 ```bash
 docker build -t thesearcher .
 docker run --rm \
   -v "$PWD/logs":/app/logs \
   -v "$HOME/Images":/data \
   -e GOOGLE_API_KEY -e GOOGLE_CSE_ID \
   thesearcher /data
 ```

 ## 6 Continuous integration
 CI configuration will include linting, tests, and Docker build on push.

 ## 7 Troubleshooting
 | Symptom                  | Likely Cause        | Remedy                         |
 | ------------------------ | ------------------- | ------------------------------ |
 | API authentication error | Invalid API key     | Verify `GOOGLE_API_KEY` in .env|
 | No results found         | Ambiguous query     | Refine folder names to include author or keywords
 | Certificate / SSL error  | Missing CA certificates (Alpine) | Rebuild image with `apk add ca-certificates`
