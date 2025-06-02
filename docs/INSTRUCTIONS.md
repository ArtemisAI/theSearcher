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