#!/usr/bin/env python3
"""
Pentagon Physics Outreach Mailer v2
====================================
Reads the contact spreadsheet, maps each contact to the correct email template,
attaches both papers to every email, deduplicates by email, and sends via SMTP.

USAGE:
  1. Preview mode (see all emails, send nothing):
       python3 pentagon_outreach.py

  2. Send mode (actually sends):
       python3 pentagon_outreach.py --send

SETUP:
  - Place this script in a folder with:
      Pentagon_Physics_Outreach_Contacts.xlsx
      α⁻¹ IS THE UNIVERSAL CONVERSION RATE OF Λ, G, H₀ Final McLean.pdf
      Nuclear_Mass_Is_Derived_v10 (3).pdf
  - pip install openpyxl  (if not already installed)
  - Update SMTP_PASSWORD below with your email password
"""

import smtplib
import time
import sys
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# ──────────────────────────────────────────────
# CONFIGURATION — UPDATE THESE
# ──────────────────────────────────────────────
SMTP_SERVER = "mail.privateemail.com"
SMTP_PORT = 465          # Namecheap Private Email SSL
USE_SSL = True
SMTP_USER = "eric@tcel.com"
SMTP_PASSWORD = "Streamdeck@1959"

FROM_NAME = "Eric McLean"
FROM_EMAIL = "eric@tcel.com"

DELAY_SECONDS = 30       # gap between sends to avoid spam filters
SPREADSHEET = "Pentagon_Physics_Outreach_Contacts.xlsx"

# Both papers — attached to every email
PDF_ALPHA = "\u03b1\u207b\u00b9 IS THE UNIVERSAL CONVERSION RATE OF \u039b, G, H\u2080 Final McLean.pdf"
PDF_MASS = "Nuclear_Mass_Is_Derived_v10 (3).pdf"
ATTACHMENTS = [PDF_ALPHA, PDF_MASS]

WEBSITE = "www.pentagonphysics.com"

SIGNATURE = f"""\
Eric McLean (Mac)
TCEL | eric@tcel.com
+357 9992 0089
ORCID: 0009-0009-6175-4408
{WEBSITE}"""

SIGNATURE_SHORT = f"""\
Eric McLean (Mac)
TCEL | eric@tcel.com
+357 9992 0089
{WEBSITE}"""

# ──────────────────────────────────────────────
# EMAIL TEMPLATES
# ──────────────────────────────────────────────

def get_physicist_email(name):
    salutation = f"Dear {name}," if name else "Dear Professor,"
    return {
        "subject": "Three cosmological measurements recover \u03b1\u207b\u00b9 as their common slope",
        "body": f"""{salutation}

Three of the most precisely measured constants in physics \u2014 \u039b, G, and H\u2080 \u2014 fall on a single straight line when plotted against coordinates derived from the self-referential equation \u03c3 = 1/(1+\u03c3). The slope of that line is 137.036. No electromagnetic input is used.

The horizontal axis is algebraic: the partition identity \u03c6\u207b\u00b9 + \u03c6\u207b\u00b2 = 1 produces four bridge ratios \u2014 one for each structurally distinct way to traverse a two-part budget. These are fixed by algebra alone. The vertical axis is observational: how many orders of magnitude below the Planck scale each constant sits. Plot four points. They fall on a straight line. The slope is \u03b1\u207b\u00b9.

This overdetermines the fine structure constant: it is now recoverable from cosmology alone, with no electrons, no atoms, no QED. The Dirac large numbers, the vacuum catastrophe, and the Hubble tension all resolve as consequences of the same geometry.

The second attached paper derives the total nuclear mass of every element from hydrogen to uranium using the eigenvalue spectrum of the 600-cell adjacency matrix. Zero free parameters. RMS error 0.11% across the periodic table. Iron-56 sits at the fixed point: 30 neutrons matching the 30 bonding modes of the spectrum exactly.

Both results are part of a programme that has derived all 26 Standard Model parameters from the single axiom \u03c3 = 1/(1+\u03c3). Eighty papers, all open-access. The full programme is at {WEBSITE}.

I would welcome your critical assessment.

{SIGNATURE}"""
    }


def get_journal_editor_email(name):
    salutation = f"Dear {name}," if name else "Dear Editors,"
    return {
        "subject": "Two independent results from one equation \u2014 zero free parameters",
        "body": f"""{salutation}

I wish to bring to your attention two results that may be suitable for your journal.

The first: three of the most precisely measured constants in physics \u2014 the cosmological constant, the gravitational constant, and the Hubble rate \u2014 fall on a single straight line when plotted against coordinates derived from one equation. The slope is 137.036 \u2014 the fine structure constant, recovered with no electromagnetic input whatsoever.

The second: the total nuclear mass of every element from hydrogen to uranium, derived from the eigenvalue spectrum of the 600-cell adjacency matrix. Zero free parameters. RMS error 0.11% across 118 elements.

If these derivations are correct, five implications follow immediately:

1. The fine structure constant is overdetermined \u2014 recoverable from cosmology alone, no atoms required.
2. The Dirac large numbers are resolved as intervals on a straight line with slope \u03b1\u207b\u00b9.
3. The nuclear binding energy curve is the fixed-point iteration of \u03c3 = 1/(1+\u03c3) drawn across 118 elements.
4. The 3/2 ratio between nuclear and proton coupling \u2014 never derived in ninety years of nuclear physics \u2014 emerges as an algebraic identity of the 600-cell spectrum.
5. The Hubble tension is diagnosed: Pentagon Physics predicts H\u2080 = 71.7 km/s/Mpc from pure geometry.

Both papers are attached. I would be glad to prepare a formal submission if you consider either within scope. The full programme (80 papers) is at {WEBSITE}.

{SIGNATURE}"""
    }


def get_popular_scientist_email(name):
    salutation = f"Dear {name}," if name else "Dear Professor,"
    return {
        "subject": "One equation, 26 constants, zero parameters",
        "body": f"""{salutation}

What if the 26 free parameters of the Standard Model are not free at all?

A result published today shows that three of the most precisely measured constants in physics \u2014 the cosmological constant, the gravitational constant, and the Hubble rate \u2014 fall on a single straight line. The slope of that line is 137.036 \u2014 the fine structure constant, recovered with no electromagnetic input.

The same equation \u2014 \u03c3 = 1/(1+\u03c3) \u2014 derives the total nuclear mass of every element from hydrogen to uranium at 0.11% accuracy with zero free parameters. Iron-56 sits at the fixed point because its neutron count (30) matches the bonding modes of the 600-cell exactly. Stars die when the equation converges.

Both papers are attached. Eighty papers are published, all open-access. The full programme is at {WEBSITE}.

I know this reads like a bold claim. The kill conditions are published. The arithmetic is open. I would very much welcome your assessment.

{SIGNATURE}"""
    }


def get_newspaper_email(name):
    salutation = f"Dear {name}," if name else "Dear Editor,"
    return {
        "subject": "Embargoed result \u2014 three cosmological measurements recover the fine structure constant",
        "body": f"""{salutation}

I'd like to offer you early sight of a result published today. Three of the most precisely measured constants in physics \u2014 the cosmological constant, the gravitational constant, and the Hubble rate \u2014 fall on a single straight line when plotted against coordinates derived from one equation. The slope of that line is 137.036 \u2014 the fine structure constant, measured independently by atomic physics to eleven significant figures. No electromagnetic input is used.

If this holds, it means the most important number in atomic physics can be recovered from cosmology alone \u2014 no atoms required. The Hubble tension, the Dirac large numbers, and the vacuum catastrophe all dissolve as consequences of the same geometry.

The second attached paper derives the mass of every element in the periodic table from the same equation. Zero free parameters. 0.11% accuracy across 118 elements.

The results are part of a programme called Pentagon Physics \u2014 80 published papers deriving all 26 Standard Model parameters from a single self-referential equation with zero free parameters. The full programme is at {WEBSITE}.

I am a Scottish independent researcher. The papers include explicit kill conditions \u2014 specific measurements that would destroy the framework. I would welcome scrutiny.

{SIGNATURE}"""
    }


def get_media_email(name):
    salutation = f"Dear {name}," if name else "Dear Editor,"
    return {
        "subject": "Science scoop \u2014 independent physicist derives the constants of nature from one equation",
        "body": f"""{salutation}

An independent researcher has shown that three unrelated measurements of the universe \u2014 the cosmological constant, the gravitational constant, and the Hubble rate \u2014 fall on a single straight line. The slope is 137.036: the fine structure constant. No electromagnetic input. No fitting.

The same equation derives the mass of every element in the periodic table at 0.11% accuracy with zero free parameters.

Eighty published papers. Ten pre-registered kill conditions. None have been violated.

The equation is five characters long: \u03c3 = 1/(1+\u03c3).

Both papers are attached. The full programme is at {WEBSITE}.

I believe this is a story. I'd welcome a conversation if you'd like to explore it.

{SIGNATURE_SHORT}"""
    }


def get_publisher_email(name):
    salutation = f"Dear {name}," if name else "Dear Publisher,"
    return {
        "subject": "Two books from a programme that derives the constants of nature",
        "body": f"""{salutation}

I am writing to introduce a publishing project built on an extraordinary foundation: a research programme that has derived all 26 free parameters of the Standard Model of physics from a single equation with zero free parameters.

A result published today shows that three of the most precisely measured constants in physics \u2014 the cosmological constant, the gravitational constant, and the Hubble rate \u2014 fall on a single straight line. The slope is 137.036 \u2014 the fine structure constant. No electromagnetic input is used. The second attached paper derives the mass of every element in the periodic table from the same equation at 0.11% accuracy.

The programme is called Pentagon Physics. It spans 80 published papers, covers six physical scales from the proton to the cosmological constant, and achieves sub-percent accuracy throughout. Every derivation carries explicit falsification conditions. The full programme is at {WEBSITE}.

Two books emerge from this work:

Pentagon Physics \u2014 the physics story. One equation produces \u03b1, G, \u039b, the Higgs mass, the proton mass, the nuclear binding curve, neutrino masses, and the gauge group of the Standard Model. Stars die when the axiom converges. The multiverse is unnecessary. The measurement problem dissolves. This is the successor to "The Elegant Universe" and "The Road to Reality" \u2014 but with results, not speculation.

The Geometry of Becoming \u2014 the deeper story. Consciousness, emergence, and the relationship between self-referential mathematics and lived experience. This is the book for readers of Rovelli's "The Order of Time" and Hofstadter's "G\u00f6del, Escher, Bach."

The Standard Model has stood unchallenged for fifty years \u2014 not because it is complete, but because no alternative has produced results. This programme has. The first serious book to tell this story will define the conversation.

I would welcome the opportunity to discuss these projects with you.

{SIGNATURE}"""
    }


def get_agent_email(name):
    salutation = f"Dear {name}," if name else "Dear Agent,"
    return {
        "subject": "A paradigm shift in physics \u2014 two books, 80 papers, zero free parameters",
        "body": f"""{salutation}

I am seeking representation for two non-fiction books at the centre of what may be the most significant shift in fundamental physics since the Standard Model was completed fifty years ago.

The programme is called Pentagon Physics. It has derived all 26 free parameters of the Standard Model \u2014 every coupling constant, every particle mass, every mixing angle \u2014 from a single self-referential equation with zero free parameters. Not fitted. Not calibrated. Derived, from pure geometry.

A result published today demonstrates the scope: three of the most precisely measured constants in physics \u2014 the cosmological constant, the gravitational constant, and the Hubble rate \u2014 fall on a single straight line. The slope is 137.036, the fine structure constant, recovered with no electromagnetic input whatsoever. A second paper derives the mass of every element in the periodic table at 0.11% accuracy. Both are attached as proof of concept.

Eighty papers are published, each with a DOI on Zenodo. Every result carries explicit conditions under which it would be falsified. The full programme, including interactive explanations and the complete paper catalogue, is at {WEBSITE}.

Book One: Pentagon Physics. The physics story. An independent Scottish researcher, working outside the institutional system, identifies the geometry that produces the constants of nature. Stars die when the equation converges. The multiverse is unnecessary. The hierarchy problem, the vacuum catastrophe, the measurement problem \u2014 all dissolve. Comparable to Brian Greene's "The Elegant Universe" or Roger Penrose's "The Road to Reality," but built on derived results rather than speculation.

Book Two: The Geometry of Becoming. The consciousness and emergence story. Self-reference as the origin of pattern, awareness, and structure. For readers of Hofstadter, Rovelli, and Iain McGilchrist. Rooted in thirty-five years of research.

The physics world has not yet engaged with these results. The first serious book to do so will define the conversation.

I would welcome the opportunity to discuss these projects with you.

{SIGNATURE}"""
    }


# ──────────────────────────────────────────────
# PERSONAL OVERRIDES (by email address)
# ──────────────────────────────────────────────

def get_canongate_email(name):
    clean_name = str(name).split("(")[0].strip() if name else ""
    if "Byng" in str(name) or not clean_name:
        salutation = "Dear Jamie,"
    else:
        salutation = f"Dear {clean_name},"
    return {
        "subject": "A Scottish physicist, a Scottish equation, a Scottish publisher",
        "body": f"""{salutation}

I'm writing to you specifically because this book belongs at Canongate.

An independent Scottish researcher has derived all 26 free parameters of the Standard Model of physics from a single equation with zero free parameters. Every coupling constant, every particle mass, every mixing angle. The fine structure constant to seven significant figures. The mass of every element from hydrogen to uranium at 0.11% accuracy. The proton-electron mass ratio to 5 parts per billion. The cosmological constant to the correct order of magnitude. The Higgs mass within 0.17 standard deviations of measurement. Eighty papers published. Ten kill conditions that would destroy the framework. None have been violated.

The equation is \u03c3 = 1/(1+\u03c3). Five characters. One solution. The rest is geometry.

James Clerk Maxwell, Edinburgh-born, the greatest Scottish physicist who ever lived, wrote E=mc\u00b2 forty years before Einstein. He unified electricity and magnetism with four equations. This programme finishes what Maxwell started: unifying everything else, from the same geometric foundation, using the same field that Maxwell discovered.

Maxwell was Edinburgh. This work is Scottish. And the publisher who tells this story should be Scottish too.

Two books:

Pentagon Physics: the physics. How one equation derives the constants of nature. Stars die when the equation converges. The multiverse is unnecessary. The hierarchy problem, the vacuum catastrophe, the measurement problem, three generations, all dissolve. Not solved with new mechanisms. Dissolved, because they were artefacts of treating derived quantities as free parameters. This is the successor to "The Road to Reality," but with results, not speculation.

The Geometry of Becoming: consciousness, emergence, and the relationship between self-referential mathematics and lived experience. For readers of Iain McGilchrist, Carlo Rovelli, and Douglas Hofstadter. Rooted in thirty-five years of research.

The physics world has not yet engaged with these results. The first serious book to do so will define the conversation.

Both papers are attached. The full programme is at {WEBSITE}.

I'd welcome a conversation.

{SIGNATURE}"""
    }


# Map specific email addresses to personal templates
PERSONAL_OVERRIDES = {
    "submissions@canongate.co.uk": get_canongate_email,
    "simon.thorogood@canongate.co.uk": get_canongate_email,
}


# ──────────────────────────────────────────────
# CATEGORY MAPPING
# ──────────────────────────────────────────────

CATEGORY_MAP = {
    "Physicists": get_physicist_email,
    "Journal Editors": get_journal_editor_email,
    "Popular Scientists": get_popular_scientist_email,
    "Newspaper Science Editors": get_newspaper_email,
    "Popular Podcasts": get_media_email,
    "Journalists": get_media_email,
    "Science Blogs": get_media_email,
    "Science Book Publishers": get_publisher_email,
    "Book Publishers": get_publisher_email,
    "Literary Agents": get_agent_email,
}


# ──────────────────────────────────────────────
# SPREADSHEET PARSING
# ──────────────────────────────────────────────

def load_contacts(filepath):
    try:
        import openpyxl
    except ImportError:
        print("ERROR: openpyxl not installed. Run: pip install openpyxl")
        sys.exit(1)

    wb = openpyxl.load_workbook(filepath, read_only=True, data_only=True)
    ws = wb.active
    rows = list(ws.iter_rows(values_only=True))

    header_idx = None
    for i, row in enumerate(rows):
        if row and row[0] and str(row[0]).strip().lower() == "category":
            header_idx = i
            break

    if header_idx is None:
        print("ERROR: Could not find header row in spreadsheet.")
        sys.exit(1)

    contacts = []
    seen_emails = set()

    for row in rows[header_idx + 1:]:
        if not row or not row[0]:
            continue

        category = str(row[0]).strip() if row[0] else ""
        contact_person = str(row[2]).strip() if row[2] else ""
        email = str(row[4]).strip() if row[4] else ""
        affiliation = str(row[5]).strip() if row[5] else ""
        priority = str(row[6]).strip() if row[6] else ""

        if not email or email == "None" or "@" not in email:
            continue

        email_lower = email.lower()
        if email_lower in seen_emails:
            continue
        seen_emails.add(email_lower)

        display_name = contact_person if contact_person and contact_person != "None" else ""
        if display_name in ("Editors", "Editorial Office", "Science Desk",
                            "Various (Baez, Schreiber)", "Preskill / Caltech group",
                            "Various hosts"):
            display_name = ""

        contacts.append({
            "category": category,
            "contact_person": display_name,
            "email": email,
            "affiliation": affiliation,
            "priority": priority,
        })

    wb.close()
    return contacts


# ──────────────────────────────────────────────
# EMAIL SENDING
# ──────────────────────────────────────────────

def attach_pdf(msg, filepath):
    if not os.path.exists(filepath):
        print(f"  WARNING: Attachment not found: {filepath}")
        return
    with open(filepath, "rb") as f:
        part = MIMEBase("application", "pdf")
        part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f'attachment; filename="{os.path.basename(filepath)}"')
        msg.attach(part)


def send_email(contact, email_data, send_mode=False):
    msg = MIMEMultipart()
    msg["From"] = f"{FROM_NAME} <{FROM_EMAIL}>"
    msg["To"] = contact["email"]
    msg["Subject"] = email_data["subject"]
    msg.attach(MIMEText(email_data["body"], "plain", "utf-8"))
    for pdf in ATTACHMENTS:
        attach_pdf(msg, pdf)

    if send_mode:
        try:
            if USE_SSL:
                server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
            else:
                server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
                server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.send_message(msg)
            server.quit()
            return True
        except Exception as e:
            print(f"  SEND FAILED: {e}")
            return False
    return True


# ──────────────────────────────────────────────
# MAIN
# ──────────────────────────────────────────────

def main():
    send_mode = "--send" in sys.argv

    if send_mode:
        print("=" * 60)
        print("  SEND MODE \u2014 EMAILS WILL BE SENT")
        print("=" * 60)
        confirm = input("\nType YES to confirm: ")
        if confirm.strip() != "YES":
            print("Aborted.")
            sys.exit(0)
    else:
        print("=" * 60)
        print("  PREVIEW MODE \u2014 no emails will be sent")
        print("  Run with --send to actually send")
        print("=" * 60)

    if not os.path.exists(SPREADSHEET):
        print(f"\nERROR: Spreadsheet not found: {SPREADSHEET}")
        print("Place the spreadsheet in the same folder as this script.")
        sys.exit(1)

    for pdf in ATTACHMENTS:
        if not os.path.exists(pdf):
            print(f"\nWARNING: PDF not found: {pdf}")

    contacts = load_contacts(SPREADSHEET)
    print(f"\nLoaded {len(contacts)} unique contacts (deduplicated by email)\n")

    cat_counts = {}
    for c in contacts:
        cat = c["category"]
        cat_counts[cat] = cat_counts.get(cat, 0) + 1
    print("Category breakdown:")
    for cat, count in sorted(cat_counts.items()):
        template_fn = CATEGORY_MAP.get(cat)
        status = "MAPPED" if template_fn else "UNMAPPED"
        print(f"  {cat}: {count} contacts [{status}]")

    print(f"\nAttachments (to all):")
    for pdf in ATTACHMENTS:
        exists = "\u2713" if os.path.exists(pdf) else "\u2717 MISSING"
        print(f"  {exists}  {pdf}")

    sent = 0
    failed = 0
    skipped = 0

    print("\n" + "=" * 60)

    for i, contact in enumerate(contacts, 1):
        category = contact["category"]
        email_lower = contact["email"].lower()

        # Check for personal overrides first
        override_fn = PERSONAL_OVERRIDES.get(email_lower)
        if override_fn:
            template_fn = override_fn
            category = category + " [PERSONAL]"
        else:
            template_fn = CATEGORY_MAP.get(category)

        if not template_fn:
            print(f"\n[{i}/{len(contacts)}] SKIPPED \u2014 unknown category: {category}")
            print(f"  {contact['contact_person']} <{contact['email']}>")
            skipped += 1
            continue

        email_data = template_fn(contact["contact_person"])

        print(f"\n[{i}/{len(contacts)}] {category}")
        print(f"  To:      {contact['contact_person'] or '(generic)'} <{contact['email']}>")
        print(f"  Subject: {email_data['subject']}")

        if not send_mode:
            preview_lines = email_data["body"].strip().split("\n")[:3]
            for line in preview_lines:
                print(f"  | {line}")
            print(f"  | ... ({len(email_data['body'])} chars total)")
        else:
            success = send_email(contact, email_data, send_mode=True)
            if success:
                sent += 1
                print(f"  SENT OK")
                if i < len(contacts):
                    print(f"  Waiting {DELAY_SECONDS}s before next send...")
                    time.sleep(DELAY_SECONDS)
            else:
                failed += 1

    print("\n" + "=" * 60)
    print("SUMMARY")
    print(f"  Total contacts: {len(contacts)}")
    if send_mode:
        print(f"  Sent:    {sent}")
        print(f"  Failed:  {failed}")
    else:
        print(f"  Would send: {len(contacts) - skipped}")
        print(f"  Skipped:    {skipped}")
        print(f"\n  Run with --send to send all emails")
    print("=" * 60)


if __name__ == "__main__":
    main()
