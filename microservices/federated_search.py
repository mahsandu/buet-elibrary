#!/usr/bin/env python3
"""
Federated Search Gateway for BUET E-Library
────────────────────────────────────────────
Queries multiple external databases in parallel and returns merged results.

Usage (standalone):
    python federated_search.py

Usage (with Docker / Gunicorn):
    gunicorn -w 2 -b 0.0.0.0:5002 federated_search:app

Supported APIs (free tier):
    - Crossref:    https://api.crossref.org/works  (no API key)
    - OpenAlex:    https://api.openalex.org/works  (no API key)
    - CORE:        https://api.core.ac.uk/v3/search/works  (free API key)
    - IEEE Xplore: https://ieeexplore.ieee.org/gateway/inspec/api  (requires key)
    - Elsevier:    https://api.elsevier.com/content/search/scopus  (requires key)

To enable IEEE / Elsevier, add API keys to the DATABASES dict below or
set environment variables: IEEE_API_KEY, ELSEVIER_API_KEY, CORE_API_KEY.
"""

import asyncio
import json
import os
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from typing import Dict, List, Optional

import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# ── Configuration ────────────────────────────────────────────────────────

# Database API configurations (add credentials in production)
DATABASES = {
    "ieee": {
        "name": "IEEE Xplore",
        "base_url": "https://ieeexplore.ieee.org/gateway/inspec/api",
        "enabled": False,  # Requires API key
        "api_key": os.getenv("IEEE_API_KEY"),
    },
    "elsevier": {
        "name": "Elsevier ScienceDirect",
        "base_url": "https://api.elsevier.com/content/search/scopus",
        "enabled": False,  # Requires API key
        "api_key": os.getenv("ELSEVIER_API_KEY"),
    },
    "crossref": {
        "name": "Crossref (Open Access)",
        "base_url": "https://api.crossref.org/works",
        "enabled": True,  # Free, no API key required
        "api_key": None,
    },
    "core": {
        "name": "CORE Aggregator",
        "base_url": "https://api.core.ac.uk/v3/search/works",
        "enabled": bool(os.getenv("CORE_API_KEY")),  # Free key required
        "api_key": os.getenv("CORE_API_KEY"),
    },
    "openalex": {
        "name": "OpenAlex",
        "base_url": "https://api.openalex.org/works",
        "enabled": True,  # Completely free
        "api_key": None,
    },
    "bangladesh_ir": {
        "name": "Bangladesh Institutional Repositories",
        "base_url": None,  # OAI-PMH endpoints listed below
        "enabled": True,
        "oai_endpoints": [
            "http://dspace.buet.ac.bd:8080/oai/request",  # BUET DSpace
            # Add other Bangladesh IRs here
        ],
    },
}


# ── Search Functions ───────────────────────────────────────────────────

def search_crossref(query: str, max_results: int = 10) -> List[Dict]:
    """Search Crossref (open access, no API key required)."""
    try:
        params = {
            "query": query,
            "rows": max_results,
            "sort": "relevance",
            "filter": "has-abstract:true",
        }
        resp = requests.get(
            DATABASES["crossref"]["base_url"],
            params=params,
            timeout=10,
        )
        resp.raise_for_status()
        data = resp.json()

        results = []
        for item in data.get("message", {}).get("items", []):
            results.append({
                "source": "crossref",
                "title": item.get("title", [""])[0] if item.get("title") else "",
                "creator": ", ".join(
                    a.get("given", "") + " " + a.get("family", "")
                    for a in item.get("author", [])
                )[:200],
                "publish_date": str(item.get("published-print", {}).get("date-parts", [[""]])[0][0]) or "",
                "subjects": item.get("subject", []),
                "format_type": "Journal Article",
                "target_uri": item.get("URL", ""),
                "doi": item.get("DOI", ""),
                "publisher": item.get("publisher", ""),
                "abstract": item.get("abstract", "")[:500],
                "score": 1.0,  # Crossref doesn't provide scores
                "open_access": item.get("is-referenced-by-count", 0) > 0,
            })
        return results
    except Exception as e:
        return [{"source": "crossref", "error": str(e)}]


def search_openalex(query: str, max_results: int = 10) -> List[Dict]:
    """Search OpenAlex (completely free, no API key)."""
    try:
        params = {
            "search": query,
            "per-page": max_results,
            "sort": "cited_by_count:desc",
        }
        resp = requests.get(
            DATABASES["openalex"]["base_url"],
            params=params,
            timeout=10,
        )
        resp.raise_for_status()
        data = resp.json()

        results = []
        for item in data.get("results", []):
            authors = []
            for auth in item.get("authorships", [])[:3]:
                name = auth.get("author", {}).get("display_name", "")
                if name:
                    authors.append(name)

            results.append({
                "source": "openalex",
                "title": item.get("display_name", ""),
                "creator": ", ".join(authors),
                "publish_date": item.get("publication_year", ""),
                "subjects": [
                    c.get("display_name", "")
                    for c in item.get("concepts", [])[:3]
                ],
                "format_type": "Journal Article",
                "target_uri": item.get("open_access", {}).get("oa_url", "") or item.get("id", ""),
                "doi": item.get("doi", ""),
                "publisher": item.get("host_venue", {}).get("display_name", ""),
                "abstract": item.get("abstract_inverted_index", {}) and "Abstract available" or "",
                "score": item.get("cited_by_count", 0) / 100.0,  # Normalize
                "open_access": item.get("open_access", {}).get("is_oa", False),
            })
        return results
    except Exception as e:
        return [{"source": "openalex", "error": str(e)}]


def search_core(query: str, max_results: int = 10, api_key: Optional[str] = None) -> List[Dict]:
    """Search CORE (requires free API key for production)."""
    if not api_key:
        return [{"source": "core", "error": "API key required. Get one at https://core.ac.uk/services/api"}]

    try:
        headers = {"Authorization": f"Bearer {api_key}"}
        params = {"query": query, "limit": max_results}
        resp = requests.get(
            DATABASES["core"]["base_url"],
            headers=headers,
            params=params,
            timeout=10,
        )
        resp.raise_for_status()
        data = resp.json()

        results = []
        for item in data.get("results", []):
            results.append({
                "source": "core",
                "title": item.get("title", ""),
                "creator": item.get("authors", [{}])[0].get("name", "") if item.get("authors") else "",
                "publish_date": item.get("publishedDate", "")[:4],
                "subjects": item.get("fieldOfStudy", []),
                "format_type": "Journal Article",
                "target_uri": item.get("links", [{}])[0].get("url", "") if item.get("links") else "",
                "doi": item.get("doi", ""),
                "publisher": item.get("publisher", ""),
                "abstract": item.get("abstract", "")[:500],
                "score": item.get("score", 0) / 100.0,
                "open_access": True,  # CORE is open access
            })
        return results
    except Exception as e:
        return [{"source": "core", "error": str(e)}]


# ── Unified Search Function ────────────────────────────────────────────

def federated_search(query: str, max_results: int = 10, sources: Optional[List[str]] = None) -> Dict:
    """
    Execute federated search across multiple databases in parallel.
    
    Args:
        query: Search query string
        max_results: Maximum results per source
        sources: List of source names to query (None = all enabled)
    
    Returns:
        Dict with merged results, source metadata, and timing info
    """
    start_time = datetime.now(timezone.utc)

    # Determine which sources to query
    if sources is None:
        sources = [k for k, v in DATABASES.items() if v.get("enabled")]

    # Execute searches in parallel using ThreadPool
    results_by_source = {}
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {}

        if "crossref" in sources:
            futures["crossref"] = executor.submit(search_crossref, query, max_results)
        if "openalex" in sources:
            futures["openalex"] = executor.submit(search_openalex, query, max_results)
        if "core" in sources:
            futures["core"] = executor.submit(search_core, query, max_results, DATABASES["core"].get("api_key"))

        for source_name, future in futures.items():
            try:
                results_by_source[source_name] = future.result(timeout=15)
            except Exception as e:
                results_by_source[source_name] = [{"source": source_name, "error": str(e)}]

    # Merge and rank results
    all_results = []
    source_counts = {}
    source_errors = {}

    for source_name, results in results_by_source.items():
        source_counts[source_name] = 0
        for r in results:
            if "error" in r:
                source_errors[source_name] = r["error"]
            else:
                all_results.append(r)
                source_counts[source_name] += 1

    # Sort by relevance score (descending)
    all_results.sort(key=lambda x: x.get("score", 0), reverse=True)

    # Deduplicate by DOI
    seen_dois = set()
    deduplicated = []
    for r in all_results:
        doi = r.get("doi", "").lower()
        if doi and doi in seen_dois:
            continue
        if doi:
            seen_dois.add(doi)
        deduplicated.append(r)

    elapsed = (datetime.now(timezone.utc) - start_time).total_seconds()

    return {
        "query": query,
        "total_results": len(deduplicated),
        "results": deduplicated[:max_results * len(sources)],
        "source_counts": source_counts,
        "source_errors": source_errors,
        "elapsed_seconds": elapsed,
        "sources_queried": list(sources),
        "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
    }


# ── Flask Routes ───────────────────────────────────────────────────────

@app.route("/health")
def health():
    return jsonify({"status": "ok", "mode": "federated_search"})


@app.route("/api/federated/search")
def search():
    """
    Federated search endpoint.
    
    Query params:
        q: Search query (required)
        limit: Max results per source (default: 10)
        sources: Comma-separated source names (default: all enabled)
    
    Example:
        GET /api/federated/search?q=machine+learning&limit=5&sources=crossref,openalex
    """
    query = request.args.get("q", "").strip()
    if not query:
        return jsonify({"error": "Query parameter 'q' is required"}), 400

    try:
        limit = int(request.args.get("limit", 10))
    except ValueError:
        limit = 10

    sources = request.args.get("sources")
    if sources:
        sources = [s.strip() for s in sources.split(",")]
    else:
        sources = None

    results = federated_search(query, max_results=limit, sources=sources)
    return jsonify(results)


@app.route("/api/federated/sources")
def list_sources():
    """List available federated search sources and their status."""
    return jsonify({
        "sources": {
            k: {
                "name": v["name"],
                "enabled": v["enabled"],
                "requires_api_key": v.get("api_key") is not None,
            }
            for k, v in DATABASES.items()
        }
    })


# ── Entry Point ────────────────────────────────────────────────────────

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=False)
