# Federated Search Guide for BUET E-Library

## What Is Federated Search?

**Federated Search** sends a query to multiple information sources simultaneously and aggregates the results in real time. Unlike the **unified index** (where metadata is pre-harvested into Elasticsearch), federated search queries each source live.

### Unified Index vs. Federated Search

| Aspect | Unified Index (Elasticsearch) | Federated Search |
|--------|------------------------------|------------------|
| **Data source** | Koha, DSpace (local systems) | External databases (IEEE, Elsevier, Crossref) |
| **Speed** | Milliseconds (pre-indexed) | 2–10 seconds (live API calls) |
| **Ranking** | Consistent, tunable relevance | Variable per source |
| **Faceting** | Full control over facets | Limited or source-dependent |
| **Freshness** | Delayed (harvest schedule) | Real-time |
| **Licensing** | No issues (local metadata) | Must respect API terms |
| **Coverage** | Institutional holdings only | Global scholarly content |

### BUET's Hybrid Strategy

For BUET, the optimal architecture is **hybrid**:

```
┌────────────────────────────────────────────────────────────┐
│                    User Search Box                           │
│         "machine learning in civil engineering"              │
└──────────────────────────┬─────────────────────────────────┘
                           │
          ┌────────────────┼────────────────┐
          │                │                │
          ▼                ▼                ▼
   ┌────────────┐  ┌────────────┐  ┌────────────────────┐
   │ Unified    │  │ Federated  │  │ Proxy (E-Resource) │
   │ Index      │  │ Search     │  │ (Off-Campus Access)│
   │ (ES)       │  │ Gateway    │  │                    │
   └────────────┘  └────────────┘  └────────────────────┘
   │ Koha       │  │ Crossref   │  │ IEEE Xplore        │
   │ DSpace     │  │ OpenAlex   │  │ Elsevier           │
   │            │  │ CORE       │  │ JSTOR              │
   │            │  │ (via API)  │  │ (via proxy)        │
   └────────────┘  └────────────┘  └────────────────────┘
          │                │                │
          └────────────────┼────────────────┘
                           ▼
              ┌────────────────────┐
              │   Drupal Results   │
              │   (Merged View)    │
              │  ┌──────────────┐  │
              │  │ Local: 45    │  │  ← From Elasticsearch
              │  │ Global: 128  │  │  ← From Federated Search
              │  └──────────────┘  │
              └────────────────────┘
```

---

## Implementation Approaches

### Approach 1: Parallel API Aggregation (Implemented)

**File:** `microservices/federated_search.py`

The Python gateway queries multiple APIs in parallel using `ThreadPoolExecutor`, merges results, deduplicates by DOI, and returns a unified JSON response.

**Supported APIs (Free Tier):**

| Source | API | Free Tier | API Key Required |
|--------|-----|-----------|----------------|
| **Crossref** | `https://api.crossref.org/works` | Unlimited | No |
| **OpenAlex** | `https://api.openalex.org/works` | Unlimited | No |
| **CORE** | `https://api.core.ac.uk/v3/search/works` | 10K req/month | Yes (free) |
| **IEEE Xplore** | `https://ieeexplore.ieee.org/gateway/inspec/api` | Limited | Yes |
| **Elsevier Scopus** | `https://api.elsevier.com/content/search/scopus` | Limited | Yes |

**How to enable IEEE / Elsevier:**

1. Register for API keys:
   - IEEE: https://developer.ieee.org/
   - Elsevier: https://dev.elsevier.com/

2. Add keys to `microservices/federated_search.py`:
   ```python
   DATABASES["ieee"]["api_key"] = "your-ieee-api-key"
   DATABASES["ieee"]["enabled"] = True
   DATABASES["elsevier"]["api_key"] = "your-elsevier-api-key"
   DATABASES["elsevier"]["enabled"] = True
   ```

**Usage:**

```bash
# Search all enabled sources
curl "http://localhost:5002/api/federated/search?q=machine+learning&limit=5"

# Search specific sources
curl "http://localhost:5002/api/federated/search?q=machine+learning&sources=crossref,openalex"

# List available sources
curl "http://localhost:5002/api/federated/sources"
```

**Response format:**

```json
{
  "query": "machine learning",
  "total_results": 23,
  "results": [
    {
      "source": "openalex",
      "title": "Machine Learning: A Practical Approach",
      "creator": "John Smith, Jane Doe",
      "publish_date": "2023",
      "subjects": ["Computer Science", "Artificial Intelligence"],
      "format_type": "Journal Article",
      "target_uri": "https://doi.org/10.1234/example",
      "doi": "10.1234/example",
      "publisher": "IEEE",
      "abstract": "This paper explores...",
      "score": 0.95,
      "open_access": true
    }
  ],
  "source_counts": {"crossref": 10, "openalex": 13},
  "source_errors": {},
  "elapsed_seconds": 2.4,
  "sources_queried": ["crossref", "openalex"],
  "timestamp": "2026-06-19T00:00:00Z"
}
```

---

### Approach 2: Z39.50 / SRU for Library Catalogs

**For:** Querying other Koha/DSpace instances, library union catalogs, or Bangladesh national bibliographic databases.

Z39.50 is a standard library protocol for searching remote catalogs. SRU (Search/Retrieve via URL) is its HTTP-based successor.

**Example: Querying a remote Koha via Z39.50:**

```python
# Requires: pip install pymarc
from pymarc import Record
from io import BytesIO
import socket

def z3950_search(host: str, port: int, database: str, query: str, max_results: int = 10):
    """
    Search a remote Z39.50 catalog.
    
    Args:
        host: Z39.50 server hostname
        port: Z39.50 port (usually 210)
        database: Database name on the server
        query: CQL or Prefix Query Format (PQF) query
        max_results: Maximum records to retrieve
    
    Returns:
        List of MARC records as dictionaries
    """
    try:
        from PyZ3950 import zoom
        conn = zoom.Connection(host, port)
        conn.databaseName = database
        conn.preferredRecordSyntax = 'USMARC'
        
        query_obj = zoom.Query('CCL', query)
        results = conn.search(query_obj)
        
        records = []
        for i, result in enumerate(results[:max_results]):
            raw = result.get_record()
            record = Record(data=raw)
            records.append({
                "title": record.title(),
                "creator": record.author(),
                "isbn": record.isbn(),
                "publisher": record.publisher(),
                "publish_date": record.pubyear(),
                "source": f"z3950:{host}",
            })
        
        conn.close()
        return records
    except ImportError:
        return [{"error": "PyZ3950 not installed. Run: pip install PyZ3950"}]
    except Exception as e:
        return [{"error": str(e)}]


# Example: Search Bangladesh National Library (if Z39.50 is available)
# results = z3950_search("bnl.gov.bd", 210, "biblios", "machine learning")
```

**Note:** PyZ3950 is a legacy library. For modern Python, consider `sickle` (OAI-PMH) or SRU over HTTP:

```python
# SRU (HTTP-based, no special library needed)
def sru_search(base_url: str, query: str, max_results: int = 10):
    """Search via SRU/CQL over HTTP."""
    import xml.etree.ElementTree as ET
    
    params = {
        "operation": "searchRetrieve",
        "query": query,
        "maximumRecords": max_results,
        "recordSchema": "marcxml",
    }
    resp = requests.get(base_url, params=params, timeout=15)
    resp.raise_for_status()
    
    root = ET.fromstring(resp.text)
    # Parse MARCXML records from SRU response
    records = []
    # ... parse logic ...
    return records
```

---

### Approach 3: JavaScript Meta-Search (Client-Side)

For a lightweight, no-backend approach, query multiple sources directly from the browser using JavaScript `fetch()` and merge results in the client.

**Pros:** No server infrastructure needed, real-time, leverages user's bandwidth  
**Cons:** CORS issues, API keys exposed, slower on mobile

**Example: `drupal/js/federated-search.js`**

```javascript
/**
 * Drupal behavior for federated meta-search
 * Queries multiple APIs in parallel and renders merged results
 */
(function (Drupal, once) {
  Drupal.behaviors.buetFederatedSearch = {
    attach: function (context, settings) {
      once('buet-federated-search', '#federated-search-results', context).forEach(function (container) {
        const query = container.dataset.query;
        if (!query) return;

        // Query sources in parallel
        const sources = [
          { name: 'crossref', url: `https://api.crossref.org/works?query=${encodeURIComponent(query)}&rows=5` },
          { name: 'openalex', url: `https://api.openalex.org/works?search=${encodeURIComponent(query)}&per-page=5` },
        ];

        Promise.allSettled(
          sources.map(src => 
            fetch(src.url)
              .then(r => r.json())
              .then(data => ({ source: src.name, data }))
              .catch(err => ({ source: src.name, error: err.message }))
          )
        ).then(results => {
          const merged = [];
          results.forEach(r => {
            if (r.status === 'fulfilled' && !r.value.error) {
              // Normalize results from each source
              if (r.value.source === 'crossref') {
                r.value.data.message.items.forEach(item => {
                  merged.push({
                    title: item.title[0],
                    authors: (item.author || []).map(a => `${a.given} ${a.family}`).join(', '),
                    year: item['published-print']?.['date-parts']?.[0]?.[0],
                    doi: item.DOI,
                    url: item.URL,
                    source: 'Crossref',
                  });
                });
              } else if (r.value.source === 'openalex') {
                r.value.data.results.forEach(item => {
                  merged.push({
                    title: item.display_name,
                    authors: (item.authorships || []).map(a => a.author.display_name).join(', '),
                    year: item.publication_year,
                    doi: item.doi,
                    url: item.open_access?.oa_url || item.id,
                    source: 'OpenAlex',
                  });
                });
              }
            }
          });

          // Render merged results
          container.innerHTML = merged.length 
            ? merged.map(r => `
              <div class="federated-result">
                <h4><a href="${r.url}" target="_blank">${r.title}</a></h4>
                <p class="authors">${r.authors}</p>
                <p class="meta">${r.year} | ${r.source} | DOI: ${r.doi}</p>
              </div>
            `).join('')
            : '<p>No federated results found.</p>';
        });
      });
    }
  };
})(Drupal, once);
```

---

### Approach 4: Proxy-Based Federated Search

**Use the existing proxy** (`proxy.buet.ac.bd:8080`) as a federated search backend.

When a user searches for "machine learning", the system can:
1. Query the **unified index** for local Koha/DSpace results
2. Open an **iframe or new tab** for each external database with the search term pre-filled
3. Or use the **proxy to fetch** database results and merge them

**Example: Pre-fill search across databases via proxy:**

```html
<!-- Drupal template: search results page -->
<div class="federated-links">
  <h3>Also search in:</h3>
  <ul>
    <li><a href="https://proxy.buet.ac.bd:8080/ieee/search/search.jsp?queryText=machine+learning" target="_blank">IEEE Xplore</a></li>
    <li><a href="https://proxy.buet.ac.bd:8080/elsevier/search?qs=machine+learning" target="_blank">Elsevier ScienceDirect</a></li>
    <li><a href="https://proxy.buet.ac.bd:8080/jstor/action/doBasicSearch?Query=machine+learning" target="_blank">JSTOR</a></li>
  </ul>
</div>
```

**Note:** Each database has its own search URL pattern. This approach is simple but doesn't merge results — it sends the user to each database individually.

---

## Integration with Drupal

### Option A: Custom Search API Datasource (Server-Side)

Create a custom Drupal Search API datasource that queries the federated search gateway:

```php
// drupal/custom_module/src/Plugin/search_api/datasource/FederatedDatasource.php
namespace Drupal\buet_elibrary\Plugin\search_api\datasource;

use Drupal\search_api\Datasource\DatasourcePluginBase;

/**
 * @SearchApiDatasource(
 *   id = "federated",
 *   label = @Translation("Federated Search"),
 *   description = @Translation("Queries external databases via federated search gateway."),
 * )
 */
class FederatedDatasource extends DatasourcePluginBase {
  
  public function loadMultiple(array $ids) {
    // Not applicable — federated search is live, not indexed
    return [];
  }
  
  public function getItemIds($page = NULL) {
    // Not applicable
    return [];
  }
}
```

**Better approach:** Don't use Search API for federated results. Use a **custom controller** that calls the federated gateway and renders results alongside Search API results.

### Option B: Custom Controller (Recommended)

```php
// drupal/custom_module/src/Controller/FederatedSearchController.php
namespace Drupal\buet_elibrary\Controller;

use Drupal\Core\Controller\ControllerBase;
use Symfony\Component\HttpFoundation\JsonResponse;
use Symfony\Component\HttpFoundation\Request;

class FederatedSearchController extends ControllerBase {
  
  public function search(Request $request) {
    $query = $request->query->get('q');
    if (empty($query)) {
      return new JsonResponse(['error' => 'Query required'], 400);
    }
    
    // Call the federated search microservice
    $client = \Drupal::httpClient();
    $response = $client->get('http://microservices:5002/api/federated/search', [
      'query' => ['q' => $query, 'limit' => 10],
      'timeout' => 15,
    ]);
    
    $data = json_decode($response->getBody(), TRUE);
    
    // Render as themed output
    return [
      '#theme' => 'federated_search_results',
      '#query' => $query,
      '#results' => $data['results'] ?? [],
      '#total' => $data['total_results'] ?? 0,
      '#sources' => $data['source_counts'] ?? [],
    ];
  }
}
```

### Option C: React/Vue Component (Decoupled)

For a modern frontend, build a React component that queries both Elasticsearch and the federated gateway in parallel:

```javascript
// React component: FederatedSearchResults.jsx
import React, { useState, useEffect } from 'react';

function FederatedSearchResults({ query }) {
  const [localResults, setLocalResults] = useState([]);
  const [federatedResults, setFederatedResults] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Query both sources in parallel
    Promise.all([
      fetch(`/api/search/unified?q=${encodeURIComponent(query)}`),
      fetch(`/api/federated/search?q=${encodeURIComponent(query)}`)
    ])
    .then(([localRes, fedRes]) => Promise.all([localRes.json(), fedRes.json()]))
    .then(([local, fed]) => {
      setLocalResults(local.results);
      setFederatedResults(fed.results);
      setLoading(false);
    });
  }, [query]);

  if (loading) return <div>Searching across databases...</div>;

  return (
    <div className="federated-search">
      <div className="local-results">
        <h3>BUET Library ({localResults.length} results)</h3>
        {localResults.map(r => (
          <div key={r.id} className="result">
            <a href={r.target_uri}>{r.title}</a>
            <p>{r.creator} | {r.format_type}</p>
          </div>
        ))}
      </div>
      
      <div className="federated-results">
        <h3>Global Scholarly Content ({federatedResults.length} results)</h3>
        {federatedResults.map((r, i) => (
          <div key={i} className="result">
            <a href={r.target_uri} target="_blank" rel="noopener">
              {r.title} <span className="external">↗</span>
            </a>
            <p>{r.creator} | {r.source} | {r.publish_date}</p>
            {r.open_access && <span className="oa-badge">Open Access</span>}
          </div>
        ))}
      </div>
    </div>
  );
}

export default FederatedSearchResults;
```

---

## Rank Fusion: Merging Results from Multiple Sources

When combining results from Elasticsearch (local) and federated APIs (global), you need a **rank fusion** strategy because each source uses different scoring.

### Simple Reciprocal Rank Fusion (RRF)

```python
def reciprocal_rank_fusion(results_lists, k=60):
    """
    Merge multiple ranked lists using Reciprocal Rank Fusion.
    
    Args:
        results_lists: Dict of {source_name: [ordered_results]}
        k: Constant (default 60, higher = more forgiving of low ranks)
    
    Returns:
        List of results sorted by fused score
    """
    scores = {}
    
    for source_name, results in results_lists.items():
        for rank, result in enumerate(results):
            doc_id = result.get("doi") or result.get("id") or result.get("title")
            if doc_id not in scores:
                scores[doc_id] = {"result": result, "score": 0}
            scores[doc_id]["score"] += 1.0 / (k + rank + 1)
    
    sorted_results = sorted(scores.values(), key=lambda x: x["score"], reverse=True)
    return [r["result"] for r in sorted_results]


# Usage:
merged = reciprocal_rank_fusion({
    "elasticsearch": local_results,   # From ES
    "crossref": crossref_results,      # From Crossref API
    "openalex": openalex_results,      # From OpenAlex API
})
```

### Weighted Fusion (BUET-Preferred)

Give higher weight to local (BUET) results because they are immediately accessible:

```python
def weighted_fusion(results_lists, weights):
    """
    Merge results with source-specific weights.
    
    Args:
        results_lists: Dict of {source_name: [ordered_results]}
        weights: Dict of {source_name: weight}
    
    Returns:
        List of results sorted by weighted score
    """
    scores = {}
    
    for source_name, results in results_lists.items():
        weight = weights.get(source_name, 1.0)
        for rank, result in enumerate(results):
            doc_id = result.get("doi") or result.get("id") or result.get("title")
            if doc_id not in scores:
                scores[doc_id] = {"result": result, "score": 0}
            # Weighted reciprocal rank
            scores[doc_id]["score"] += weight * (1.0 / (60 + rank + 1))
    
    sorted_results = sorted(scores.values(), key=lambda x: x["score"], reverse=True)
    return [r["result"] for r in sorted_results]


# BUET weights: prioritize local holdings
weights = {
    "elasticsearch": 2.0,   # Local results are 2x more important
    "crossref": 1.0,
    "openalex": 1.0,
    "core": 1.2,            # CORE is open access, slight boost
}
```

---

## Performance Considerations

### 1. Timeout Handling

External APIs can be slow. Set aggressive timeouts and return partial results:

```python
from concurrent.futures import ThreadPoolExecutor, as_completed

def search_with_timeout(query, sources, timeout=5):
    results = {}
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {executor.submit(search_fn, query): name for name, search_fn in sources.items()}
        
        for future in as_completed(futures, timeout=timeout):
            name = futures[future]
            try:
                results[name] = future.result(timeout=1)
            except Exception:
                results[name] = []  # Source failed, continue with others
    
    return results
```

### 2. Caching

Cache federated search results to reduce API calls:

```python
import hashlib
from functools import wraps

def cache_search_results(ttl=300):  # 5 minutes
    def decorator(fn):
        @wraps(fn)
        def wrapper(query, *args, **kwargs):
            cache_key = f"search:{hashlib.md5(query.encode()).hexdigest()}"
            
            # Check Redis cache
            cached = redis_client.get(cache_key)
            if cached:
                return json.loads(cached)
            
            # Execute and cache
            result = fn(query, *args, **kwargs)
            redis_client.setex(cache_key, ttl, json.dumps(result))
            return result
        return wrapper
    return decorator
```

### 3. Rate Limiting

Respect API rate limits:

```python
import time
from collections import defaultdict

class RateLimiter:
    def __init__(self, max_requests=10, window=1):
        self.max_requests = max_requests
        self.window = window
        self.requests = defaultdict(list)
    
    def can_request(self, source):
        now = time.time()
        # Remove old requests outside the window
        self.requests[source] = [t for t in self.requests[source] if now - t < self.window]
        
        if len(self.requests[source]) < self.max_requests:
            self.requests[source].append(now)
            return True
        return False
```

---

## CORS and Security

### For Client-Side JavaScript Approach

Most academic APIs **do not** send CORS headers. Options:

1. **Server-side proxy** (recommended): Route all API calls through the Drupal backend or Python gateway
2. **JSONP** (legacy, limited support)
3. **CORS proxy** (e.g., `https://cors-anywhere.herokuapp.com/` — not for production)

### For Server-Side Approach

No CORS issues. The Python gateway makes all API calls server-to-server.

**Security best practices:**
- Store API keys in environment variables, never in client-side code
- Validate and sanitize all query parameters
- Log API usage for rate limit monitoring
- Implement IP-based access control for the federated search endpoint

---

## Deployment

### Add to Docker Compose

Add the federated search service to `docker-compose.yml`:

```yaml
  federated:
    build:
      context: ./microservices
    container_name: elib_federated
    restart: unless-stopped
    depends_on:
      - redis
    networks:
      - elib_network
    environment:
      - REDIS_HOST=redis
      - REDIS_PORT=6379
      - IEEE_API_KEY=${IEEE_API_KEY:-}
      - ELSEVIER_API_KEY=${ELSEVIER_API_KEY:-}
      - CORE_API_KEY=${CORE_API_KEY:-}
    command: ["python", "federated_search.py"]
```

Add to `.env`:
```bash
# Federated Search API Keys (optional — free sources work without keys)
IEEE_API_KEY=
ELSEVIER_API_KEY=
CORE_API_KEY=your-free-core-api-key
```

---

## Roadmap

| Phase | Feature | Effort |
|-------|---------|--------|
| **V4.1** | Crossref + OpenAlex integration (free, no keys) | 1 day |
| **V4.2** | CORE integration (free API key) | 1 day |
| **V4.3** | IEEE Xplore API (requires institutional API key) | 2 days |
| **V4.4** | Elsevier Scopus API (requires institutional API key) | 2 days |
| **V4.5** | Z39.50/SRU for Bangladesh union catalogs | 3 days |
| **V4.6** | Rank fusion (RRF + weighted) in gateway | 1 day |
| **V4.7** | React/Vue decoupled frontend component | 3 days |
| **V4.8** | Caching layer (Redis) for API responses | 1 day |
| **V4.9** | Analytics: log and report which sources users query | 1 day |

---

## References

- [Crossref API Documentation](https://api.crossref.org/)
- [OpenAlex API](https://docs.openalex.org/)
- [CORE API v3](https://api.core.ac.uk/docs/v3/)
- [IEEE Xplore API](https://developer.ieee.org/)
- [Elsevier APIs](https://dev.elsevier.com/)
- [Z39.50 Protocol](https://www.loc.gov/z3950/agency/)
- [SRU/CQL Specification](https://www.loc.gov/standards/sru/)
- [Reciprocal Rank Fusion (Cormack, Clarke, et al.)](https://plg.uwaterloo.ca/~gvcormac/cormacksigir09-rrf.pdf)
