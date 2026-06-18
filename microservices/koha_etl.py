#!/usr/bin/env python3
import os
import sys
from datetime import datetime, timezone

from sickle import Sickle
from elasticsearch import helpers

import utils

KOHA_ENDPOINT = "https://lib.buet.ac.bd/cgi-bin/koha/oai.pl"
INDEX_NAME = "buet_unified_catalog"
WATERMARK_FILE = "last_harvest_koha.txt"


def get_last_harvest():
    if os.path.exists(WATERMARK_FILE):
        with open(WATERMARK_FILE, "r") as f:
            return f.read().strip()
    return None


def set_last_harvest(date_str):
    with open(WATERMARK_FILE, "w") as f:
        f.write(date_str)


def find_marc_fields(record_xml, tag, code=None):
    results = []
    for elem in record_xml.iter():
        tag_name = elem.tag
        if tag_name.startswith("{"):
            tag_name = tag_name.split("}")[-1]
        if tag_name == "datafield" and elem.get("tag") == tag:
            if code is None:
                if elem.text:
                    results.append(elem.text)
            else:
                for sub in elem:
                    sub_tag = sub.tag
                    if sub_tag.startswith("{"):
                        sub_tag = sub_tag.split("}")[-1]
                    if sub_tag == "subfield" and sub.get("code") == code and sub.text:
                        results.append(sub.text)
        elif tag_name == "controlfield" and elem.get("tag") == tag and code is None:
            if elem.text:
                results.append(elem.text)
    return results


def build_record(record):
    xml = record.xml
    biblionumbers = find_marc_fields(xml, "001")
    biblionumber = biblionumbers[0].strip() if biblionumbers else ""
    if not biblionumber:
        utils.log_message("warning", "Skipping record with no biblionumber")
        return None

    titles = find_marc_fields(xml, "245", "a")
    title = titles[0] if titles else ""

    creators = find_marc_fields(xml, "100", "a")
    creator = creators[0] if creators else ""

    isbns = find_marc_fields(xml, "020", "a")
    isbn = isbns[0] if isbns else ""

    dates_260 = find_marc_fields(xml, "260", "c")
    dates_264 = find_marc_fields(xml, "264", "c")
    publish_date = dates_260[0] if dates_260 else (dates_264[0] if dates_264 else "")

    subjects = find_marc_fields(xml, "650", "a")

    doc = {
        "_index": INDEX_NAME,
        "_id": f"koha_{biblionumber}",
        "id": f"koha_{biblionumber}",
        "title": title,
        "creator": creator,
        "isbn": isbn,
        "publish_date": publish_date,
        "subjects": subjects,
        "source_system": "koha",
        "format_type": "Physical Book",
        "target_uri": f"https://lib.buet.ac.bd/cgi-bin/koha/opac-detail.pl?biblionumber={biblionumber}",
        "fingerprint": utils.compute_fingerprint(title, creator, publish_date),
        "date_indexed": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
    }
    return doc


def run_harvest(from_date=None, until_date=None):
    utils.log_message("info", "Starting Koha harvest")
    sickle = Sickle(KOHA_ENDPOINT, verify=False)

    params = {"metadataPrefix": "marcxml"}
    if from_date:
        params["from_"] = from_date
    if until_date:
        params["until"] = until_date

    try:
        records = sickle.ListRecords(**params)
    except Exception as e:
        utils.log_message("error", f"Failed to initiate Koha harvest: {e}")
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
                utils.log_message("info", f"Indexed {len(docs)} Koha records")
                docs = []
        except Exception as e:
            utils.log_message("warning", f"Error processing Koha record: {e}")
            failed += 1
            continue

    if docs:
        try:
            helpers.bulk(es, docs)
            utils.log_message("info", f"Indexed final {len(docs)} Koha records")
        except Exception as e:
            utils.log_message("error", f"Koha bulk indexing failed: {e}")
            failed += len(docs)

    now = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    set_last_harvest(now)
    utils.log_message("info", f"Koha harvest complete: {count} indexed, {failed} failed")


def main():
    last = get_last_harvest()
    from_date = last
    until_date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    utils.log_message("info", f"Incremental Koha harvest from {from_date} to {until_date}")
    run_harvest(from_date=from_date, until_date=until_date)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        utils.log_message("info", "Koha harvest interrupted by user")
        sys.exit(0)
    except Exception as e:
        utils.log_message("error", f"Koha harvest failed: {e}")
        sys.exit(1)
