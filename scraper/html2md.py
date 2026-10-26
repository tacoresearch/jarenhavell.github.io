"""
html2md.py: Convert a hand-written HTML post back into the Markdown archive layout.

Posts written directly in HTML (like 2026/10/25/velofix.html) never had a
README.md. This produces one in the same layout scrape.py uses:

    YEAR/MM/DD/name.html  ->  YEAR/name/README.md
                              YEAR/name/images/  (copied from next to the HTML)

The date comes from the YEAR/MM/DD folders. Jaren/Claw speaker blocks become
**Jaren:** paragraphs and **Claw:** blockquotes.

Run:
    pip install -r scraper/requirements.txt
    python scraper/html2md.py 2026/10/25/velofix.html [more.html ...]
"""

import html as htmllib
import shutil
import sys
from datetime import date
from pathlib import Path

from bs4 import BeautifulSoup
from markdownify import MarkdownConverter

OUT = Path(__file__).resolve().parent.parent


def md_convert(soup_fragment):
    return MarkdownConverter(heading_style="ATX", bullets="-").convert_soup(soup_fragment).strip()


def date_from_path(rel):
    year, month, day = (int(p) for p in rel.parts[:3])
    d = date(year, month, day)
    return f"{d:%B} {d.day}, {d.year}"


def process_html(html_path):
    html_path = Path(html_path).resolve()
    rel = html_path.relative_to(OUT)
    if len(rel.parts) != 4:
        print(f"! expected YEAR/MM/DD/name.html, got: {rel}")
        return None
    year = rel.parts[0]
    slug = html_path.stem
    date_text = date_from_path(rel)

    soup = BeautifulSoup(html_path.read_text(encoding="utf-8"), "html.parser")
    main = soup.find("main")
    title = main.find("h1").get_text(strip=True)

    # Drop page chrome: the title (goes in the front matter) and the theme toggle.
    main.find("h1").extract()
    for el in main.select(".topbar, script, style"):
        el.extract()

    # Speaker labels: <span class="who">Jaren:</span> -> **Jaren:**
    for who in main.select(".who"):
        who.name = "strong"
    # Claw's passages are coloured on the site; in Markdown, a blockquote sets them apart.
    for block in main.select(".line.claw"):
        block.name = "blockquote"

    # Captions and the post footer read as italic notes.
    for el in main.select("figcaption, footer"):
        el.wrap(soup.new_tag("em"))
        el.name = "p"

    out_dir = OUT / year / slug
    img_dir = out_dir / "images"
    copied, missing = 0, []
    for img in main.find_all("img"):
        src = img.get("src", "")
        local = html_path.parent / src
        if src.startswith(("http:", "https:", "/")) or not local.is_file():
            missing.append(src)
            continue
        img_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(local, img_dir / local.name)
        img["src"] = f"images/{local.name}"
        copied += 1

    body_md = htmllib.unescape(md_convert(main))
    front = f"# {title}\n\n*{date_text}*\n\n"
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "README.md").write_text(front + body_md + "\n", encoding="utf-8")

    print(f"[{year}] {slug}  (images: {copied})")
    for src in missing:
        print(f"  ! image not found next to the HTML, left as-is: {src}")
    return {"year": year, "slug": slug, "title": title, "date_text": date_text,
            "path": f"{year}/{slug}/README.md"}


def main():
    if len(sys.argv) < 2:
        raise SystemExit("Usage: python scraper/html2md.py YEAR/MM/DD/name.html [...]")
    for path in sys.argv[1:]:
        process_html(path)


if __name__ == "__main__":
    main()
