"""
build.py — Convert local README.md files to HTML at the correct historic URL paths.

Historic URLs: /YEAR/MM/DD/slug/
Local source:  YEAR/slug/README.md

Run:
    pip install markdown
    python build.py
"""

import re
import shutil
from pathlib import Path
from urllib.parse import urlparse

try:
    import markdown as mdlib
except ImportError:
    raise SystemExit("Missing dependency. Run: pip install markdown")

ROOT = Path(__file__).resolve().parent

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

PAGE_TEMPLATE = """\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} — JarenHavell.com</title>
  <link rel="icon" href="{root_rel}favicon.ico" type="image/x-icon">
  <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      background-color: #fff;
      color: #222;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
      font-size: 16px;
      line-height: 1.6;
    }}
    header {{
      background: #28a745;
      padding: 2.5rem 2rem 2rem;
      text-align: center;
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 1rem;
    }}
    header h1 {{ font-size: 2.2rem; font-weight: 800; }}
    header h1 a {{ color: #fff; text-decoration: none; }}
    nav {{ display: flex; gap: 1.5rem; }}
    nav a {{
      color: rgba(255,255,255,0.85);
      text-decoration: none;
      font-size: 0.95rem;
      letter-spacing: 0.5px;
      text-transform: uppercase;
      padding: 0.25rem 0.75rem;
      border-radius: 4px;
    }}
    nav a:hover {{ background: rgba(255,255,255,0.2); color: #fff; }}
    main {{
      max-width: 780px;
      margin: 0 auto;
      padding: 2.5rem 1.5rem;
    }}
    main h1 {{ font-size: 1.8rem; font-weight: 700; margin-bottom: 0.25rem; }}
    main h2 {{ font-size: 1.3rem; font-weight: 700; margin: 1.5rem 0 0.5rem; }}
    main h3 {{ font-size: 1.1rem; font-weight: 600; margin: 1.25rem 0 0.4rem; }}
    main p {{ margin-bottom: 1rem; color: #333; }}
    main em {{ color: #666; }}
    main a {{ color: #135e96; }}
    main ul, main ol {{ padding-left: 1.5rem; margin-bottom: 1rem; }}
    main li {{ margin: 0.25rem 0; }}
    main pre {{
      background: #f4f4f4;
      border: 1px solid #ddd;
      border-radius: 4px;
      padding: 1rem;
      overflow-x: auto;
      margin-bottom: 1rem;
      font-size: 0.9rem;
    }}
    main code {{
      background: #f4f4f4;
      padding: 0.15em 0.35em;
      border-radius: 3px;
      font-size: 0.9em;
    }}
    main pre code {{ background: none; padding: 0; }}
    main img {{ max-width: 100%; height: auto; margin: 1rem 0; border-radius: 4px; }}
    main blockquote {{
      border-left: 4px solid #ddd;
      padding-left: 1rem;
      color: #555;
      margin-bottom: 1rem;
    }}
    footer {{
      border-top: 1px solid #ddd;
      padding: 1.25rem 2rem;
      font-size: 0.85rem;
      color: #666;
      text-align: center;
    }}
  </style>
</head>
<body>
  <header>
    <h1><a href="{root_rel}index2.html">JarenHavell.com</a></h1>
    <nav>
      <a href="{root_rel}index2.html">Blog</a>
      <a href="{root_rel}about.md">About Me</a>
    </nav>
  </header>
  <main>
{content}
  </main>
  <footer>
    <p>Copyright Jaren Havell. You wouldn't download a car.</p>
  </footer>
</body>
</html>
"""


def build():
    built = 0
    skipped = 0

    for url in POST_URLS:
        parts = [p for p in urlparse(url).path.split("/") if p]
        if len(parts) < 4:
            print(f"! unexpected URL format: {url}")
            continue
        year, month, day, slug = parts[0], parts[1], parts[2], parts[3]

        src_md = ROOT / year / slug / "README.md"
        if not src_md.exists():
            print(f"! missing source: {src_md.relative_to(ROOT)}")
            skipped += 1
            continue

        out_dir = ROOT / year / month / day / slug
        out_dir.mkdir(parents=True, exist_ok=True)

        # Copy images so relative paths in the markdown still work
        src_images = ROOT / year / slug / "images"
        if src_images.exists():
            dst_images = out_dir / "images"
            if dst_images.exists():
                shutil.rmtree(dst_images)
            shutil.copytree(src_images, dst_images)

        md_text = src_md.read_text(encoding="utf-8")
        html_body = mdlib.markdown(md_text, extensions=["fenced_code", "tables"])

        title_match = re.search(r"^#\s+(.+)$", md_text, re.MULTILINE)
        title = title_match.group(1).strip() if title_match else slug

        depth = len(out_dir.relative_to(ROOT).parts)
        root_rel = "../" * depth

        html = PAGE_TEMPLATE.format(
            title=title,
            root_rel=root_rel,
            content=html_body,
        )
        (out_dir / "index.html").write_text(html, encoding="utf-8")
        print(f"  built: {out_dir.relative_to(ROOT)}/index.html")
        built += 1

    print(f"\nDone. {built} built, {skipped} skipped.")


if __name__ == "__main__":
    build()
