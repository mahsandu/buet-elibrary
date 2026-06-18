#!/usr/bin/env python3
"""
Elasticsearch Index Setup Script for BUET E-Library V4
Creates the buet_unified_catalog index with the proper mapping.
"""

import argparse
import json
import os
import sys

from elasticsearch import Elasticsearch

# ---------------------------------------------------------------------------
# Colors for terminal output
# ---------------------------------------------------------------------------
class Colors:
    OK = '\033[92m'
    WARN = '\033[93m'
    ERR = '\033[91m'
    INFO = '\033[96m'
    RESET = '\033[0m'


def c(color, text):
    return f"{color}{text}{Colors.RESET}"


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
ES_HOST = os.environ.get("ELASTICSEARCH_HOST", "http://elasticsearch:9200")
INDEX_NAME = "buet_unified_catalog"
ALIAS_NAME = "buet_search"
SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "schema.json")

# Index settings (single-node dev / small prod)
INDEX_SETTINGS = {
    "number_of_shards": 1,
    "number_of_replicas": 0,
    "refresh_interval": "1s",
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def load_schema() -> dict:
    if not os.path.exists(SCHEMA_PATH):
        print(c(Colors.ERR, f"Schema file not found: {SCHEMA_PATH}"))
        sys.exit(1)
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def ask_yes_no(question: str) -> bool:
    while True:
        choice = input(f"{question} [y/N]: ").strip().lower()
        if choice in ("y", "yes"):
            return True
        if choice in ("n", "no", ""):
            return False


def ensure_index_deleted(es: Elasticsearch, force: bool) -> bool:
    if not es.indices.exists(index=INDEX_NAME):
        return True

    print(c(Colors.WARN, f"Index '{INDEX_NAME}' already exists."))
    if not force and not ask_yes_no("Delete and recreate?"):
        print(c(Colors.INFO, "Aborted. Existing index left untouched."))
        return False

    print(c(Colors.INFO, f"Deleting existing index '{INDEX_NAME}' ..."))
    es.indices.delete(index=INDEX_NAME)
    print(c(Colors.OK, f"Index '{INDEX_NAME}' deleted."))
    return True


def create_index(es: Elasticsearch, schema: dict) -> None:
    body = {
        "settings": {
            **schema.get("settings", {}),
            **INDEX_SETTINGS,
        },
        "mappings": schema.get("mappings", {}),
    }
    # Override refresh_interval with the desired normal-operation value
    body["settings"]["refresh_interval"] = INDEX_SETTINGS["refresh_interval"]

    print(c(Colors.INFO, f"Creating index '{INDEX_NAME}' ..."))
    es.indices.create(index=INDEX_NAME, body=body)
    print(c(Colors.OK, f"Index '{INDEX_NAME}' created successfully."))


def create_alias(es: Elasticsearch) -> None:
    if es.indices.exists_alias(name=ALIAS_NAME):
        print(c(Colors.WARN, f"Alias '{ALIAS_NAME}' already exists."))
        return

    print(c(Colors.INFO, f"Creating alias '{ALIAS_NAME}' -> '{INDEX_NAME}' ..."))
    es.indices.put_alias(index=INDEX_NAME, name=ALIAS_NAME)
    print(c(Colors.OK, f"Alias '{ALIAS_NAME}' created."))


def verify_index(es: Elasticsearch) -> None:
    print(c(Colors.INFO, "Verifying index ..."))
    info = es.indices.get(index=INDEX_NAME)
    mapping = es.indices.get_mapping(index=INDEX_NAME)
    print(json.dumps(mapping[INDEX_NAME], indent=2, ensure_ascii=False))
    print(c(Colors.OK, "Verification complete."))


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> int:
    parser = argparse.ArgumentParser(
        description="Set up the BUET E-Library Elasticsearch index."
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Delete existing index without prompting.",
    )
    parser.add_argument(
        "--no-alias",
        action="store_true",
        help="Skip creating the 'buet_search' alias.",
    )
    parser.add_argument(
        "--host",
        default=ES_HOST,
        help=f"Elasticsearch host URL (default: {ES_HOST}).",
    )
    args = parser.parse_args()

    print(c(Colors.INFO, f"Connecting to Elasticsearch at {args.host} ..."))
    try:
        es = Elasticsearch([args.host])
        if not es.ping():
            raise ConnectionError("Elasticsearch ping failed.")
    except Exception as exc:
        print(c(Colors.ERR, f"Failed to connect to Elasticsearch: {exc}"))
        return 1

    print(c(Colors.OK, "Elasticsearch connection established."))

    schema = load_schema()

    if not ensure_index_deleted(es, args.force):
        return 0

    try:
        create_index(es, schema)
    except Exception as exc:
        print(c(Colors.ERR, f"Failed to create index: {exc}"))
        return 1

    if not args.no_alias:
        try:
            create_alias(es)
        except Exception as exc:
            print(c(Colors.WARN, f"Alias creation failed: {exc}"))

    try:
        verify_index(es)
    except Exception as exc:
        print(c(Colors.WARN, f"Verification failed: {exc}"))

    print(c(Colors.OK, "\nSetup complete."))
    return 0


if __name__ == "__main__":
    sys.exit(main())
