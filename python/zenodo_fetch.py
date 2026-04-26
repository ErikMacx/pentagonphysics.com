#!/usr/bin/env python3
"""
Fetch all Pentagon Physics papers from Zenodo.
No API key needed for public records.

Usage:
    python3 zenodo_fetch.py              # prints to terminal
    python3 zenodo_fetch.py --csv        # also saves zenodo_papers.csv
    python3 zenodo_fetch.py --json       # also saves zenodo_papers.json
"""

import urllib.request
import urllib.parse
import json
import csv
import sys
from datetime import datetime

AUTHOR_QUERY = 'creators.orcid:"0009-0009-6175-4408"'
ACCESS_TOKEN = "5dlvcHabPR0Pecuk2h1uCl1h3pjyPj9ZtrE6HcJXi3aRUmMU0gFyPvvmqbSW"
BASE_URL = "https://zenodo.org/api/records"
PAGE_SIZE = 100  # max per page


def fetch_all_records():
    """Fetch all records, handling pagination."""
    all_records = []
    page = 1

    while True:
        params = (
            f"q={urllib.parse.quote(AUTHOR_QUERY)}"
            f"&size={PAGE_SIZE}"
            f"&page={page}"
            f"&sort=mostrecent"
        )
        url = f"{BASE_URL}?{params}"
        print(f"Fetching page {page}... ", end="", flush=True)

        req = urllib.request.Request(url)
        req.add_header("Accept", "application/json")
        req.add_header("Authorization", f"Bearer {ACCESS_TOKEN}")

        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode())

        hits = data.get("hits", {}).get("hits", [])
        total = data.get("hits", {}).get("total", 0)
        all_records.extend(hits)
        print(f"got {len(hits)} records (total: {total})")

        if len(all_records) >= total or len(hits) == 0:
            break
        page += 1

    return all_records


def extract_info(record):
    """Extract key fields from a Zenodo record."""
    meta = record.get("metadata", {})
    return {
        "zenodo_id": record.get("id", ""),
        "doi": record.get("doi", ""),
        "title": meta.get("title", ""),
        "publication_date": meta.get("publication_date", ""),
        "authors": "; ".join(
            c.get("name", "") for c in meta.get("creators", [])
        ),
        "description": meta.get("description", "")[:300],  # first 300 chars
        "keywords": "; ".join(meta.get("keywords", [])),
        "version": meta.get("version", ""),
        "resource_type": meta.get("resource_type", {}).get("title", ""),
        "license": meta.get("license", {}).get("id", ""),
        "url": f"https://zenodo.org/records/{record.get('id', '')}",
        "files": "; ".join(
            f.get("key", "") for f in record.get("files", [])
        ),
    }


def main():
    print(f"=== Zenodo Paper Fetcher ===")
    print(f"Searching for: {AUTHOR_QUERY}\n")

    records = fetch_all_records()
    papers = [extract_info(r) for r in records]

    # Print summary
    print(f"\n{'='*70}")
    print(f"Found {len(papers)} records\n")

    for i, p in enumerate(papers, 1):
        print(f"{i:3d}. {p['title']}")
        print(f"     DOI:  {p['doi']}")
        print(f"     Date: {p['publication_date']}")
        print(f"     URL:  {p['url']}")
        if p['keywords']:
            print(f"     Tags: {p['keywords']}")
        print()

    # Optional exports
    if "--csv" in sys.argv:
        outfile = "zenodo_papers.csv"
        fields = list(papers[0].keys()) if papers else []
        with open(outfile, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()
            writer.writerows(papers)
        print(f"Saved to {outfile}")

    if "--json" in sys.argv:
        outfile = "zenodo_papers.json"
        with open(outfile, "w", encoding="utf-8") as f:
            json.dump(papers, f, indent=2, ensure_ascii=False)
        print(f"Saved to {outfile}")

    if "--csv" not in sys.argv and "--json" not in sys.argv:
        print("Tip: run with --csv or --json to save output to a file.")


if __name__ == "__main__":
    main()
