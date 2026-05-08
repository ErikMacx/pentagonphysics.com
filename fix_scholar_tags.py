#!/usr/bin/env python3
"""Add missing Google Scholar meta tags to paper pages. Idempotent."""

import csv
import os
import re
import json
import urllib.request
import time

PAPERS_DIR = os.path.join(os.path.dirname(__file__), "papers")
CSV_PATH = os.path.join(os.path.dirname(__file__), "zenodo_catalogue.csv")

# Load CSV: DOI -> date
doi_to_date = {}
with open(CSV_PATH, newline="", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        doi = row["DOI"].strip()
        date = row["Created"].strip()
        doi_to_date[doi] = date

def get_pdf_url(record_id):
    """Fetch the PDF filename from Zenodo API."""
    url = f"https://zenodo.org/api/records/{record_id}"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read())
        for f in data.get("files", []):
            if f["key"].lower().endswith(".pdf"):
                # Use the download URL with proper encoding
                encoded_key = urllib.request.quote(f["key"], safe="")
                return f"https://zenodo.org/records/{record_id}/files/{encoded_key}"
        return None
    except Exception as e:
        print(f"  WARNING: API error for {record_id}: {e}")
        return None

updated = 0
skipped = 0

for fname in sorted(os.listdir(PAPERS_DIR)):
    if not fname.endswith(".html"):
        continue

    fpath = os.path.join(PAPERS_DIR, fname)
    with open(fpath, "r", encoding="utf-8") as f:
        html = f.read()

    # First, clean up any malformed tags from previous run
    # Fix broken citation_doi line (missing closing >)
    html = re.sub(
        r'(<meta\s+name="citation_doi"\s+content="[^"]+)"(\s*\n)',
        r'\1">\2',
        html
    )
    # Remove stray >> at end of citation_pdf_url lines
    html = re.sub(r'(citation_pdf_url[^>]*>)>', r'\1', html)
    # Remove any existing citation_publication_date and citation_pdf_url tags
    html = re.sub(r'<meta\s+name="citation_publication_date"[^>]*>\n?', '', html)
    html = re.sub(r'<meta\s+name="citation_pdf_url"[^>]*>\n?', '', html)

    # Extract DOI
    m = re.search(r'<meta\s+name="citation_doi"\s+content="([^"]+)"', html)
    if not m:
        print(f"SKIP {fname}: no citation_doi found")
        skipped += 1
        continue

    doi = m.group(1)
    record_id = doi.split(".")[-1]

    # Build new tags
    new_tags = []

    date = doi_to_date.get(doi)
    if date:
        new_tags.append(f'<meta name="citation_publication_date" content="{date}">')

    pdf_url = get_pdf_url(record_id)
    if pdf_url:
        new_tags.append(f'<meta name="citation_pdf_url" content="{pdf_url}">')
    else:
        print(f"WARN {fname}: no PDF found for record {record_id}")

    time.sleep(0.3)

    if new_tags:
        # Find the full citation_doi line and insert after it
        doi_line = re.search(r'<meta\s+name="citation_doi"\s+content="[^"]+">', html)
        if doi_line:
            insert_pos = doi_line.end()
            insertion = "\n" + "\n".join(new_tags)
            html = html[:insert_pos] + insertion + html[insert_pos:]

        with open(fpath, "w", encoding="utf-8") as f:
            f.write(html)
        updated += 1
        print(f"DONE {fname}: added {len(new_tags)} tag(s)")
    else:
        skipped += 1

print(f"\nFinished: {updated} updated, {skipped} skipped")
