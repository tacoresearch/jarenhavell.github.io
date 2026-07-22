import base64
import re
import time
import html as htmllib
from pathlib import Path
from urllib.parse import urlparse, unquote

import requests
from bs4 import BeautifulSoup
from markdownify import MarkdownConverter

BASE = "https://jarenhavell.com"
OUT = Path(__file__).resolve().parent.parent
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; jarenhavell-archiver/1.0)"}

POST_URLS = [
    "https://jarenhavell.com/2015/12/29/light-up-musical-christmas-card/",
    "https://jarenhavell.com/2011/04/27/server-room-environmental-monitoring-light-and-temperature/",
    "https://jarenhavell.com/2016/04/26/remote-assistance-msra-exe/",
    "https://jarenhavell.com/2018/01/23/sccm-site-reset/",
    "https://jarenhavell.com/2018/02/17/hey-linux-what-wireless-card-do-i-have/",
    "https://jarenhavell.com/2018/12/19/spi-fast-display-library-is-good-kedei-3-5-is-garbage/",
    "https://jarenhavell.com/2018/12/26/cloning-a-debian-system/",
    "https://jarenhavell.com/2018/09/18/combine-pdf-files/",
    "https://jarenhavell.com/2018/05/04/dd-writing-an-img-or-iso-to-a-disk/",
    "https://jarenhavell.com/2018/02/04/install-sudo-on-debian/",
    "https://jarenhavell.com/2018/02/07/install-chrome-on-debian/",
    "https://jarenhavell.com/2018/02/22/screenfetch-and-neofetch/",
    "https://jarenhavell.com/2019/01/01/1-year-with-linux/",
    "https://jarenhavell.com/2018/09/14/copy-a-file-over-ssh-using-scp/",
    "https://jarenhavell.com/2019/04/09/customromkindlefire7-2019/",
    "https://jarenhavell.com/2019/12/29/installing-retropi-and-pi-hole-using-a-linux-computer/",
    "https://jarenhavell.com/2020/01/01/kindle-fire-7-9th-gen-xyz-2019-mustang-unbrick-downgrade-unlock-root/",
    "https://jarenhavell.com/2019/03/11/windows-password-reset-tool/",
    "https://jarenhavell.com/2025/08/10/expand-raidz-pool-by-adding-a-disk-zfs-expansion-in-proxmox-9/",
]

ABOUT_URL = "https://jarenhavell.com/about/"


class Converter(MarkdownConverter):
    def convert_iframe(self, el, text, **kwargs):
        src = el.get("src", "")
        m = re.search(r"(?:embed/|watch\?v=)([\w-]+)", src)
        if m:
            return f"\n\n[Video: https://www.youtube.com/watch?v={m.group(1)}]\n\n"
        return f"\n\n[Embedded content: {src}]\n\n" if src else ""


def md_convert(soup_fragment):
    return Converter(heading_style="ATX", bullets="-").convert_soup(soup_fragment).strip()


def slug_from_url(url):
    parts = [p for p in urlparse(url).path.split("/") if p]
    return parts[-1] if parts else "index"


def fetch(url):
    r = requests.get(url, headers=HEADERS, timeout=30)
    r.raise_for_status()
    return r.text


def download_image(img_url, dest_dir, seen, counter):
    if img_url in seen:
        return seen[img_url]

    if img_url.startswith("data:"):
        m = re.match(r"data:image/([\w+.-]+);base64,(.*)", img_url, re.S)
        if not m:
            print(f"  ! unsupported data URI image")
            return None
        ext = m.group(1).split("+")[0]
        ext = {"jpeg": "jpg"}.get(ext, ext)
        counter[0] += 1
        name = f"embedded-{counter[0]}.{ext}"
        dest = dest_dir / name
        try:
            dest.write_bytes(base64.b64decode(m.group(2)))
            seen[img_url] = dest.name
            return dest.name
        except Exception as e:
            print(f"  ! failed to decode embedded image: {e}")
            return None

    parsed = urlparse(img_url)
    name = unquote(Path(parsed.path).name) or "image"
    name = re.sub(r'[<>:"/\\|?*]', "_", name)
    if not Path(name).suffix:
        name += ".jpg"
    dest = dest_dir / name
    i = 1
    while dest.exists() and img_url not in seen:
        dest = dest_dir / f"{Path(name).stem}-{i}{Path(name).suffix}"
        i += 1
    try:
        r = requests.get(img_url, headers=HEADERS, timeout=30)
        r.raise_for_status()
        dest.write_bytes(r.content)
        seen[img_url] = dest.name
        return dest.name
    except Exception as e:
        print(f"  ! failed to download image {img_url}: {e}")
        return None


def process_post(url):
    html_text = fetch(url)
    soup = BeautifulSoup(html_text, "html.parser")
    article = soup.find("article")
    title = article.find("h2").get_text(strip=True)
    time_el = article.find("time")
    date_text = time_el.get_text(strip=True) if time_el else ""

    parts = [p for p in urlparse(url).path.split("/") if p]
    year = parts[0]
    slug = slug_from_url(url)

    year_dir = OUT / year
    img_dir = year_dir / slug / "images"

    # The real content is everything in <article> after the <h2> and <time>.
    for tag in [article.find("h2"), article.find("time")]:
        if tag:
            tag.extract()

    seen_images = {}
    embedded_counter = [0]
    blob_count = 0
    for img in article.find_all("img"):
        src = img.get("src", "")
        if src.startswith("blob:"):
            blob_count += 1
            img.replace_with(soup.new_string(f"[image unavailable in source: {img.get('alt') or 'blob URL never uploaded'}]"))
            continue
        img_dir.mkdir(parents=True, exist_ok=True)
        local_name = download_image(src, img_dir, seen_images, embedded_counter)
        if local_name:
            img["src"] = f"images/{local_name}"
            if img.get("srcset"):
                del img["srcset"]
        time.sleep(0.1)

    body_md = md_convert(article)
    body_md = htmllib.unescape(body_md)

    front = f"# {title}\n\n*{date_text}*\n\n"
    out_dir = year_dir / slug
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "README.md").write_text(front + body_md + "\n", encoding="utf-8")

    print(f"[{year}] {slug}  (images: {len(seen_images)}, blob-broken: {blob_count})")
    return {
        "year": year,
        "slug": slug,
        "title": title,
        "date_text": date_text,
        "path": f"{year}/{slug}/README.md",
        "blob_broken": blob_count,
    }


def process_about():
    html_text = fetch(ABOUT_URL)
    soup = BeautifulSoup(html_text, "html.parser")
    article = soup.find("article")
    title = article.find("h2").get_text(strip=True)
    article.find("h2").extract()
    body_md = md_convert(article)
    body_md = htmllib.unescape(body_md)
    (OUT / "about.md").write_text(f"# {title}\n\n" + body_md + "\n", encoding="utf-8")
    print("about.md written")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    posts = []
    for url in POST_URLS:
        try:
            posts.append(process_post(url))
        except Exception as e:
            print(f"! error processing {url}: {e}")
        time.sleep(0.2)

    process_about()

    from datetime import datetime
    def parse_date(d):
        try:
            return datetime.strptime(d, "%B %d, %Y")
        except Exception:
            return datetime.min
    posts.sort(key=lambda p: parse_date(p["date_text"]), reverse=True)

    years = sorted({p["year"] for p in posts}, reverse=True)
    lines = ["# JarenHavell.com Archive", "", "Local Markdown archive of jarenhavell.com, organized by year.", "", "See also: [About](about.md)", ""]
    for year in years:
        lines.append(f"## {year}")
        lines.append("")
        for p in posts:
            if p["year"] == year:
                note = "  *(some images unavailable — broken blob: links in source)*" if p["blob_broken"] else ""
                lines.append(f"- [{p['title']}]({p['path']}) — {p['date_text']}{note}")
        lines.append("")

    (OUT / "README.md").write_text("\n".join(lines), encoding="utf-8")
    print("README.md written")


if __name__ == "__main__":
    main()
