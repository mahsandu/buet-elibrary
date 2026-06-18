#!/usr/bin/env python3
"""
BUET Library E-Resource Proxy Server
────────────────────────────────────
A lightweight Flask-based HTTP proxy for off-campus e-resource access.
This is an alternative / complement to the Nginx proxy, providing
more sophisticated HTML URL rewriting via BeautifulSoup.

Usage (standalone):
    python proxy_server.py

Usage (with Docker / Gunicorn):
    gunicorn -w 2 -b 0.0.0.0:5001 proxy_server:app

Architecture:
    User Browser → Proxy Server → Target Database → Proxy Server → User Browser
                  (rewrites URLs in HTML)
"""
import json
import os
import re
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup
from flask import Flask, Response, request, abort, session
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("PROXY_SECRET_KEY", "buet-library-change-me-in-production")

# ── Configuration ───────────────────────────────────────────────────────────
PROXY_BASE_URL = os.getenv("PROXY_BASE_URL", "http://proxy.buet.ac.bd:8080")

# Database registry (maps proxy path → target URL)
DATABASES = {
    "ieee": {
        "name": "IEEE Xplore",
        "base_url": "https://ieeexplore.ieee.org",
        "description": "IEEE journals, conferences, and standards",
    },
    "elsevier": {
        "name": "Elsevier ScienceDirect",
        "base_url": "https://www.sciencedirect.com",
        "description": "Elsevier journals and books",
    },
    "jstor": {
        "name": "JSTOR",
        "base_url": "https://www.jstor.org",
        "description": "JSTOR academic journals and books",
    },
    "springer": {
        "name": "SpringerLink",
        "base_url": "https://link.springer.com",
        "description": "Springer journals and books",
    },
    "wiley": {
        "name": "Wiley Online Library",
        "base_url": "https://onlinelibrary.wiley.com",
        "description": "Wiley journals and books",
    },
    "acm": {
        "name": "ACM Digital Library",
        "base_url": "https://dl.acm.org",
        "description": "ACM journals and conference proceedings",
    },
}

# ── Helpers ───────────────────────────────────────────────────────────────────

def rewrite_url(url: str, db_key: str, db_config: dict) -> str:
    """Rewrite an absolute URL to go through the proxy."""
    if not url:
        return url

    parsed = urlparse(url)

    # Skip javascript: and mailto: links
    if parsed.scheme in ("javascript", "mailto", "tel"):
        return url

    # Skip data URIs
    if parsed.scheme == "data":
        return url

    # If it's already a relative path, make it proxy-relative
    if not parsed.netloc:
        return f"/{db_key}{url}"

    # Check if the URL belongs to the target database domain
    base_parsed = urlparse(db_config["base_url"])
    if parsed.netloc == base_parsed.netloc or parsed.netloc.endswith(base_parsed.netloc):
        # Rewrite to proxy path
        new_path = parsed.path
        if parsed.query:
            new_path += f"?{parsed.query}"
        if parsed.fragment:
            new_path += f"#{parsed.fragment}"
        return f"/{db_key}{new_path}"

    # External links: leave as-is (but convert to https if possible)
    return url


def rewrite_html(content: bytes, db_key: str, db_config: dict) -> bytes:
    """Parse HTML and rewrite all URLs to go through the proxy."""
    try:
        text = content.decode("utf-8", errors="replace")
    except UnicodeDecodeError:
        return content

    soup = BeautifulSoup(text, "html.parser")

    # Rewrite <a href="...">
    for tag in soup.find_all("a", href=True):
        tag["href"] = rewrite_url(tag["href"], db_key, db_config)

    # Rewrite <link href="...">
    for tag in soup.find_all("link", href=True):
        tag["href"] = rewrite_url(tag["href"], db_key, db_config)

    # Rewrite <script src="...">
    for tag in soup.find_all("script", src=True):
        tag["src"] = rewrite_url(tag["src"], db_key, db_config)

    # Rewrite <img src="...">
    for tag in soup.find_all("img", src=True):
        tag["src"] = rewrite_url(tag["src"], db_key, db_config)

    # Rewrite <form action="...">
    for tag in soup.find_all("form", action=True):
        tag["action"] = rewrite_url(tag["action"], db_key, db_config)

    # Rewrite inline styles with url(...)
    for tag in soup.find_all(style=True):
        tag["style"] = re.sub(
            r'url\([\'"]?([^\'")]+)[\'"]?\)',
            lambda m: f'url({rewrite_url(m.group(1), db_key, db_config)})',
            tag["style"]
        )

    # Rewrite CSS text in <style> tags
    for style_tag in soup.find_all("style"):
        if style_tag.string:
            css = style_tag.string
            css = re.sub(
                r'url\([\'"]?([^\'")]+)[\'"]?\)',
                lambda m: f'url({rewrite_url(m.group(1), db_key, db_config)})',
                css
            )
            style_tag.string = css

    # Rewrite any data-* attributes that might contain URLs
    for tag in soup.find_all():
        for attr in list(tag.attrs):
            if attr.startswith("data-") and isinstance(tag.attrs[attr], str):
                if tag.attrs[attr].startswith("http"):
                    tag.attrs[attr] = rewrite_url(tag.attrs[attr], db_key, db_config)

    return str(soup).encode("utf-8")


def forward_request(db_key: str, path: str) -> Response:
    """Forward the request to the target database and rewrite the response."""
    db_config = DATABASES.get(db_key)
    if not db_config:
        abort(404, description=f"Database '{db_key}' not found. Available: {', '.join(DATABASES.keys())}")

    target_url = f"{db_config['base_url']}/{path}"

    # Prepare headers (forward most, except host)
    headers = {}
    for k, v in request.headers:
        k_lower = k.lower()
        if k_lower not in ("host", "content-length", "transfer-encoding", "connection", "accept-encoding"):
            headers[k] = v

    headers["X-Real-IP"] = request.remote_addr
    headers["X-Forwarded-For"] = request.headers.get("X-Forwarded-For", request.remote_addr)
    headers["X-Forwarded-Proto"] = request.scheme

    # Forward cookies (rewrite domain)
    cookies = {}
    for cookie_name, cookie_value in request.cookies.items():
        cookies[cookie_name] = cookie_value

    try:
        upstream = requests.request(
            method=request.method,
            url=target_url,
            headers=headers,
            data=request.get_data(),
            cookies=cookies,
            params=request.args,
            allow_redirects=False,
            timeout=30,
            stream=True,
        )
    except requests.RequestException as e:
        return Response(f"Proxy error: {e}", status=502)

    # Handle redirects from upstream
    if upstream.status_code in (301, 302, 303, 307, 308):
        location = upstream.headers.get("Location", "")
        rewritten_location = rewrite_url(location, db_key, db_config)
        return Response(
            status=upstream.status_code,
            headers={"Location": rewritten_location},
        )

    # Build response
    content_type = upstream.headers.get("Content-Type", "")
    is_html = "text/html" in content_type

    if is_html:
        content = rewrite_html(upstream.content, db_key, db_config)
    else:
        content = upstream.content

    response_headers = {}
    for k, v in upstream.headers.items():
        k_lower = k.lower()
        if k_lower not in ("content-encoding", "content-length", "transfer-encoding", "connection"):
            response_headers[k] = v

    # Set correct content length for rewritten content
    response_headers["Content-Length"] = str(len(content))

    # Add security headers
    response_headers["X-Frame-Options"] = "SAMEORIGIN"
    response_headers["X-Content-Type-Options"] = "nosniff"
    response_headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

    return Response(
        content,
        status=upstream.status_code,
        headers=response_headers,
    )


# ── Routes ───────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    """Landing page listing available databases."""
    lines = [
        "BUET Library E-Resource Proxy (Python)",
        "═══════════════════════════════════════════════════════",
        "",
        "Available Databases:",
    ]
    for key, db in DATABASES.items():
        lines.append(f"  /{key}/      - {db['name']} ({db['description']})")
    lines.append("")
    lines.append("Usage: https://proxy.buet.ac.bd:8080/ieee/")
    lines.append("═══════════════════════════════════════════════════════")
    return "\n".join(lines), 200, {"Content-Type": "text/plain"}


@app.route("/health")
def health():
    """Health check endpoint."""
    return json.dumps({"status": "ok", "databases": len(DATABASES)}), 200, {"Content-Type": "application/json"}


@app.route("/<db_key>/", defaults={"path": ""})
@app.route("/<db_key>/<path:path>")
def proxy(db_key, path):
    """Main proxy route."""
    return forward_request(db_key, path)


# ── Entry Point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=False)
