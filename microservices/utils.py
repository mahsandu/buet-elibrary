#!/usr/bin/env python3
import os
import json
import hashlib
import re
import time
import socket
from datetime import datetime, timezone

import requests
from bs4 import BeautifulSoup
from elasticsearch import Elasticsearch
from redis import Redis
from dotenv import load_dotenv


def get_es_client():
    return Elasticsearch([os.getenv("ES_HOST", "http://elasticsearch:9200")])


def get_redis_client():
    return Redis(
        host=os.getenv("REDIS_HOST", "redis"),
        port=int(os.getenv("REDIS_PORT", "6379")),
        decode_responses=True,
    )


def normalize_text(text):
    if not text:
        return ""
    text = text.strip().lower()
    text = re.sub(r"[^\w\s]", "", text)
    return text


def compute_fingerprint(title, creator, publish_date):
    normalized = f"{normalize_text(title)}{normalize_text(creator)}{normalize_text(publish_date)}"
    return hashlib.md5(normalized.encode("utf-8")).hexdigest()


def load_env():
    load_dotenv()
    return {
        "ES_HOST": os.getenv("ES_HOST", "http://elasticsearch:9200"),
        "REDIS_HOST": os.getenv("REDIS_HOST", "redis"),
        "REDIS_PORT": int(os.getenv("REDIS_PORT", "6379")),
        "MODE": os.getenv("MODE", "api"),
    }


def log_message(level, message):
    print(
        json.dumps(
            {
                "level": level,
                "message": message,
                "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            }
        )
    )


def safe_request(url, headers=None, verify=False, timeout=10):
    for attempt in range(3):
        try:
            response = requests.get(url, headers=headers, verify=verify, timeout=timeout)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            log_message("warning", f"Request attempt {attempt + 1} failed for {url}: {e}")
            if attempt < 2:
                time.sleep(2 ** attempt)
            else:
                raise


def scrape_koha_status(biblionumber):
    url = f"https://lib.buet.ac.bd/cgi-bin/koha/opac-detail.pl?biblionumber={biblionumber}"
    headers = {"User-Agent": "BUET-Discovery-Node"}
    resp = safe_request(url, headers=headers, verify=False, timeout=5)
    soup = BeautifulSoup(resp.text, "html.parser")

    status = "unknown"
    location = None
    call_number = None
    barcode = None
    due_date = None

    items_table = soup.find("table", {"id": "items"}) or soup.find(
        "table", class_=lambda x: x and "items" in x.split()
    )

    if items_table:
        tbody = items_table.find("tbody")
        rows = tbody.find_all("tr") if tbody else items_table.find_all("tr")
        for row in rows:
            if row.find("th"):
                continue
            cells = row.find_all("td")
            if len(cells) >= 2:
                for cell in cells:
                    cell_text = cell.get_text(strip=True)
                    if cell_text.lower() in [
                        "available",
                        "checked out",
                        "on hold",
                        "reference only",
                        "not for loan",
                    ]:
                        status = cell_text
                    elif cell_text.isdigit() and len(cell_text) >= 8:
                        barcode = cell_text
                    elif any(
                        cell_text.startswith(p)
                        for p in [
                            "QA", "TK", "T", "HB", "HF", "PE", "QC", "QD",
                            "PR", "PS", "PZ", "E", "A", "B", "C", "D", "F",
                            "G", "H", "J", "K", "L", "M", "N", "P", "R",
                            "S", "U", "V", "Z",
                        ]
                    ):
                        call_number = cell_text
                    elif any(
                        k in cell_text.lower()
                        for k in ["library", "floor", "hall", "section", "reading", "stack"]
                    ):
                        location = cell_text
                    elif ("due" in cell_text.lower() or "-" in cell_text) and any(
                        c.isdigit() for c in cell_text
                    ):
                        due_date = cell_text

    if status == "unknown":
        for elem in soup.find_all(["span", "div", "td"]):
            text = elem.get_text(strip=True)
            if text.lower() in [
                "available",
                "checked out",
                "on hold",
                "reference only",
                "not for loan",
            ]:
                status = text
                break

    return {
        "status": status,
        "location": location,
        "call_number": call_number,
        "barcode": barcode,
        "due_date": due_date,
    }
