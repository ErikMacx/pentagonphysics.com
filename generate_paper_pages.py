#!/usr/bin/env python3
"""
Generate Google Scholar-optimized HTML pages for Pentagon Physics papers.
Reads from zenodo_catalogue.csv and creates individual paper pages with proper metadata.
"""

import csv
import re
from datetime import datetime
from pathlib import Path

# HTML template with Google Scholar meta tags
PAPER_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    
    <!-- Google Scholar Required Meta Tags -->
    <meta name="citation_title" content="{title}">
    <meta name="citation_author" content="McLean, Eric">
    <meta name="citation_publication_date" content="{pub_date}">
    
    <!-- Google Scholar Recommended Meta Tags -->
    <meta name="citation_pdf_url" content="{pdf_url}">
    <meta name="citation_doi" content="{doi}">
    <meta name="citation_journal_title" content="Zenodo">
    
    <!-- Standard Meta Tags -->
    <meta name="description" content="{title} - Pentagon Physics paper by Eric McLean">
    <meta name="author" content="Eric McLean">
    
    <title>{title} - Pentagon Physics</title>
    
    <!-- Link to main site CSS -->
    <link rel="stylesheet" href="../style.css">
</head>
<body>
    <header>
        <nav>
            <a href="../index.html">Home</a>
            <a href="../papers.html">All Papers</a>
            <a href="../tools.html">Tools</a>
        </nav>
    </header>
    
    <main class="paper-page">
        <article>
            <h1>{title}</h1>
            
            <div class="paper-metadata">
                <p><strong>Author:</strong> Eric McLean, Independent Researcher, Cyprus</p>
                <p><strong>Published:</strong> {pub_date_display}</p>
                <p><strong>DOI:</strong> <a href="https://doi.org/{doi}">{doi}</a></p>
                <p><strong>Zenodo Record:</strong> <a href="{zenodo_url}">{zenodo_id}</a></p>
            </div>
            
            <!-- Abstract section - REQUIRED to be visible for Google Scholar -->
            <section class="abstract">
                <h2>Abstract</h2>
                <p><em>Full abstract available in the PDF. This paper is part of the Pentagon Physics programme, 
                deriving fundamental constants and Standard Model parameters from the single axiom σ = 1/(1+σ).</em></p>
            </section>
            
            <section class="download">
                <h2>Download</h2>
                <a href="{pdf_url}" class="download-button">Download PDF from Zenodo</a>
                <p class="file-info">Open access under Creative Commons license</p>
            </section>
            
            <section class="citation">
                <h2>How to Cite</h2>
                <pre>McLean, E. ({year}). {title}. Zenodo. https://doi.org/{doi}</pre>
            </section>
            
            <section class="related">
                <h2>Related Papers</h2>
                <p><a href="../papers.html">View all Pentagon Physics papers</a></p>
            </section>
        </article>
    </main>
    
    <footer>
        <p>&copy; 2024-2026 Eric McLean. Licensed under CC BY 4.0.</p>
    </footer>
</body>
</html>
"""

def slugify(text):
    """Convert title to URL-friendly slug."""
    # Remove special characters, convert to lowercase
    slug = re.sub(r'[^\w\s-]', '', text.lower())
    # Replace spaces with hyphens
    slug = re.sub(r'[-\s]+', '-', slug)
    # Limit length
    return slug[:80]

def format_date(date_str):
    """Convert YYYY-MM-DD to YYYY/MM/DD format for Google Scholar."""
    try:
        dt = datetime.strptime(date_str, '%Y-%m-%d')
        return dt.strftime('%Y/%m/%d')
    except:
        return date_str.replace('-', '/')

def extract_zenodo_id(doi):
    """Extract Zenodo record ID from DOI."""
    # DOI format: 10.5281/zenodo.19420169
    return doi.split('.')[-1]

def generate_paper_page(title, doi, created_date, output_dir):
    """Generate a single paper HTML page."""
    
    # Create slug for filename
    slug = slugify(title)
    filename = f"{slug}.html"
    
    # Extract info
    zenodo_id = extract_zenodo_id(doi)
    zenodo_url = f"https://zenodo.org/records/{zenodo_id}"
    pdf_url = f"https://zenodo.org/records/{zenodo_id}/files/{slug}.pdf"
    
    # Format dates
    pub_date = format_date(created_date)
    pub_date_display = datetime.strptime(created_date, '%Y-%m-%d').strftime('%B %d, %Y')
    year = created_date[:4]
    
    # Fill template
    html = PAPER_TEMPLATE.format(
        title=title,
        doi=doi,
        pub_date=pub_date,
        pub_date_display=pub_date_display,
        pdf_url=pdf_url,
        zenodo_url=zenodo_url,
        zenodo_id=zenodo_id,
        year=year
    )
    
    # Write file
    output_path = output_dir / filename
    output_path.write_text(html, encoding='utf-8')
    
    return {
        'filename': filename,
        'title': title,
        'date': pub_date_display,
        'url': f"papers/{filename}"
    }

def generate_papers_index(papers, output_dir):
    """Generate the main papers listing page."""
    
    html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Publications - Pentagon Physics</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <header>
        <nav>
            <a href="index.html">Home</a>
            <a href="papers.html" class="active">All Papers</a>
            <a href="tools.html">Tools</a>
        </nav>
    </header>
    
    <main>
        <h1>Pentagon Physics Publications</h1>
        <p class="intro">{count} papers deriving all Standard Model parameters from the axiom σ = 1/(1+σ)</p>
        
        <div class="papers-list">
"""
    
    # Sort by date (newest first)
    papers_sorted = sorted(papers, key=lambda p: p['date'], reverse=True)
    
    for paper in papers_sorted:
        html += f"""            <article class="paper-item">
                <h2><a href="{paper['url']}">{paper['title']}</a></h2>
                <p class="paper-meta">{paper['date']}</p>
            </article>
"""
    
    html += """        </div>
    </main>
    
    <footer>
        <p>&copy; 2024-2026 Eric McLean. Licensed under CC BY 4.0.</p>
    </footer>
</body>
</html>
"""
    
    output_path = output_dir / 'papers.html'
    output_path.write_text(html.format(count=len(papers)), encoding='utf-8')

def generate_sitemap(papers, output_dir):
    """Generate XML sitemap for Google."""
    
    xml = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url>
        <loc>https://pentagonphysics.com/</loc>
        <lastmod>{today}</lastmod>
        <priority>1.0</priority>
    </url>
    <url>
        <loc>https://pentagonphysics.com/papers.html</loc>
        <lastmod>{today}</lastmod>
        <priority>0.9</priority>
    </url>
""".format(today=datetime.now().strftime('%Y-%m-%d'))
    
    for paper in papers:
        xml += f"""    <url>
        <loc>https://pentagonphysics.com/{paper['url']}</loc>
        <lastmod>{datetime.now().strftime('%Y-%m-%d')}</lastmod>
        <priority>0.8</priority>
    </url>
"""
    
    xml += "</urlset>\n"
    
    output_path = output_dir / 'sitemap.xml'
    output_path.write_text(xml, encoding='utf-8')

def generate_robots_txt(output_dir):
    """Generate robots.txt to allow Google Scholar crawling."""
    
    txt = """User-agent: *
Allow: /

User-agent: Googlebot
Allow: /

User-agent: Googlebot-Scholar
Allow: /

Sitemap: https://pentagonphysics.com/sitemap.xml
"""
    
    output_path = output_dir / 'robots.txt'
    output_path.write_text(txt, encoding='utf-8')

def main():
    """Main generation function."""
    
    # Setup paths
    script_dir = Path(__file__).parent
    csv_path = script_dir / 'zenodo_catalogue.csv'
    output_base = script_dir / 'pentagonphysics_site'
    papers_dir = output_base / 'papers'
    
    # Create directories
    output_base.mkdir(exist_ok=True)
    papers_dir.mkdir(exist_ok=True)
    
    # Read catalogue
    papers = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Skip if not done
            if row['State'] != 'done':
                continue
                
            print(f"Generating page for: {row['Title']}")
            
            paper_info = generate_paper_page(
                title=row['Title'],
                doi=row['DOI'],
                created_date=row['Created'],
                output_dir=papers_dir
            )
            papers.append(paper_info)
    
    # Generate index page
    print(f"\nGenerating papers index...")
    generate_papers_index(papers, output_base)
    
    # Generate sitemap
    print(f"Generating sitemap.xml...")
    generate_sitemap(papers, output_base)
    
    # Generate robots.txt
    print(f"Generating robots.txt...")
    generate_robots_txt(output_base)
    
    print(f"\n✓ Generated {len(papers)} paper pages")
    print(f"✓ Generated papers.html index")
    print(f"✓ Generated sitemap.xml")
    print(f"✓ Generated robots.txt")
    print(f"\nOutput directory: {output_base}")
    print(f"\nNext steps:")
    print(f"1. Copy contents to your GitHub Pages repo")
    print(f"2. Submit sitemap.xml to Google Search Console")
    print(f"3. Wait 6-12 weeks for Google Scholar indexing")

if __name__ == '__main__':
    main()
