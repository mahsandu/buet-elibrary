#!/usr/bin/env python3
import os
import sys
from datetime import datetime, timezone

from sickle import Sickle
from elasticsearch import helpers

import utils

DSPACE_ENDPOINT = "http://lib.buet.ac.bd:8080/oai/request"
INDEX_NAME = "buet_unified_catalog"
WATERMARK_FILE = "last_harvest_dspace.txt"


def get_last_harvest():
    if os.path.exists(WATERMARK_FILE):
        with open(WATERMARK_FILE, "r") as f:
            return f.read().strip()
    return None


def set_last_harvest(date_str):
    with open(WATERMARK_FILE, "w") as f:
        f.write(date_str)


def extract_handle_id(identifier):
    if not identifier:
        return None
    if "/" in identifier:
        return identifier.strip().split("/")[-1]
    return identifier.strip()


def build_record(record):
    identifier = record.header.identifier
    handle_id = extract_handle_id(identifier)
    if not handle_id:
        utils.log_message("warning", f"Skipping record with no handle_id: {identifier}")
        return None

    metadata = record.metadata
    title = metadata.get("title", [""])[0] if metadata.get("title") else ""
    creator = metadata.get("creator", [""])[0] if metadata.get("creator") else ""
    publish_date = metadata.get("date", [""])[0] if metadata.get("date") else ""
    subjects = metadata.get("subject", []) if metadata.get("subject") else []

    doc = {
        "_index": INDEX_NAME,
        "_id": f"dspace_{handle_id}",
        "id": f"dspace_{handle_id}",
        "title": title,
        "creator": creator,
        "publish_date": publish_date,
        "subjects": subjects,
        "source_system": "dspace",
        "format_type": "Digital Thesis/Article",
        "target_uri": f"http://lib.buet.ac.bd:8080/handle/{handle_id}",
        "fingerprint": utils.compute_fingerprint(title, creator, publish_date),
        "date_indexed": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
    }
    return doc


def run_harvest(from_date=None, until_date=None):
    utils.log_message("info", "Starting DSpace harvest")
    sickle = Sickle(DSPACE_ENDPOINT)

    params = {"metadataPrefix": "oai_dc"}
    if from_date:
        params["from_"] = from_date
    if until_date:
        params["until"] = until_date

    try:
        records = sickle.ListRecords(**params)
    except Exception as e:
        utils.log_message("error", f"Failed to initiate DSpace harvest: {e}")
        return

    es = utils.get_es_client()
    docs = []
    count = 0
    failed = 0

    for record in records:
        try:
            doc = build_record(record)
            if doc:
                docs.append(doc)
                count += 1
            if len(docs) >= 100:
                helpers.bulk(es, docs)
                utils.log_message("info", f"Indexed {len(docs)} DSpace records")
                docs = []
        except Exception as e:
            utils.log_message("warning", f"Error processing DSpace record: {e}")
            failed += 1
            continue

    if docs:
        try:
            helpers.bulk(es, docs)
            utils.log_message("info", f"Indexed final {len(docs)} DSpace records")
        except Exception as e:
            utils.log_message("error", f"DSpace bulk indexing failed: {e}")
            failed += len(docs)

    now = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    set_last_harvest(now)
    utils.log_message("info", f"DSpace harvest complete: {count} indexed, {failed} failed")


def main():
    last = get_last_harvest()
    from_date = last
    until_date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    utils.log_message("info", f"Incremental DSpace harvest from {from_date} to {until_date}")
    run_harvest(from_date=from_date, until_date=until_date)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        utils.log_message("info", "DSpace harvest interrupted by user")
        sys.exit(0)
    except Exception as e:
        utils.log_message("error", f"DSpace harvest failed: {e}")
        sys.exit(1)
