 # Business Requirements – theSearcher

 | Version | Author       | Date       |
 | ------- | ------------ | ---------- |
 | 1.0     | <Your Name>  | 2025-06-02 |

 ## 1 Purpose
 theSearcher scans folders of images, detects missing images or metadata, and fetches and downloads relevant images using the Google Custom Search API.

 ## 2 Success Criteria
 | ID    | Metric                             | Target                                    |
 | ----- | ---------------------------------- | ----------------------------------------- |
 | SC-1  | Detection accuracy                 | ≥ 98% of missing-image folders flagged     |
 | SC-2  | Download relevance                 | ≥ 95% of downloaded images match query    |
 | SC-3  | Throughput                         | 500 folders processed in <10 min on 1vCPU |
 | SC-4  | Cost per 1000 requests             | ≤ $5 (within free tier limits)            |

 ## 3 Scope
 **Included:**
 * Local filesystem scanning
 * Google Custom Search JSON API integration
 * Image download and storage in target folder
 * CLI interface, Docker container, unit + integration tests

 **Excluded:**
 * Embedding images into file metadata
 * GUI front-end

 ## 4 Stakeholders
 | Role          | Name / Team    | Responsibility                  |
 | ------------- | -------------- | ------------------------------- |
 | Product Owner | …              | Define acceptance criteria      |
 | Tech Lead     | …              | Architecture & code reviews     |
 | DevOps        | …              | Build pipeline & container      |
 | QA            | …              | Test plan & audit success criteria |

 ## 5 Assumptions & Risks
 * Google API quotas and pricing may change; plan fallback or billing.
 * Image relevance relies on folder naming accuracy.