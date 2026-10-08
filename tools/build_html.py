"""
Course maintenance: build course.html, the whole course as ONE page you can
open in any browser, offline. Needs pandoc (https://pandoc.org) and plain Python 3:

    python tools/build_html.py

Links between course pages become jumps inside the page; links to exercise
files keep working as long as course.html stays in the course folder.
"""
import re
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGES = (["README.md"]
         + sorted(str(p.relative_to(ROOT)).replace("\\", "/")
                  for p in (ROOT / "modules").glob("*/README.md"))
         + ["AI_PLAYBOOK.md", "CHEATSHEET.md", "GLOSSARY.md", "BOOK_MAP.md", "data/README.md",
            "modules/10-directing-ai/exercises/ex10_2_rewrite_briefs.md",
            "modules/10-directing-ai/exercises/ex10_3_ai_session_log.md",
            "modules/12-capstone/exercises/capstone_brief.md"])

CSS = """
body{max-width:52rem;margin:2rem auto;padding:0 1rem;font:16px/1.6 system-ui,Segoe UI,sans-serif;color:#222;background:#fdfcf9}
h1{border-top:3px solid #b8b2a5;padding-top:1.5rem;margin-top:3rem}
code{background:#f1ede4;padding:.1em .3em;border-radius:3px;font-size:.92em}
pre{background:#f6f3ec;padding:.8rem;overflow-x:auto;border-left:3px solid #b8b2a5}
pre code{background:none;padding:0}
table{border-collapse:collapse;margin:1rem 0;font-size:.95em}
td,th{border:1px solid #ddd6c8;padding:.35rem .6rem;vertical-align:top}
th{background:#f1ede4}
blockquote{border-left:4px solid #8fb0c7;margin:1rem 0;padding:.2rem 1rem;background:#eef3f6}
details{background:#f6f3ec;padding:.5rem 1rem;margin:1rem 0}
nav#TOC{background:#f6f3ec;padding:1rem 2rem;font-size:.95em}
"""


def file_id(path):
    return "page-" + re.sub(r"[^a-z0-9]+", "-", path.lower()).strip("-")


def rewrite_links(text, page):
    here = (ROOT / page).parent

    def fix(match):
        label, target = match.group(1), match.group(2)
        if target.startswith(("http", "mailto", "#")):
            return match.group(0)
        path, _, anchor = target.partition("#")
        resolved = (here / path).resolve()
        rel = str(resolved.relative_to(ROOT)).replace("\\", "/") if path else page
        if rel in PAGES:
            return f"[{label}](#{anchor or file_id(rel)})"
        return f"[{label}]({rel}{'#' + anchor if anchor else ''})"

    return re.sub(r"\[([^\]]*)\]\(([^)\s]+)\)", fix, text)


parts = []
for page in PAGES:
    text = (ROOT / page).read_text(encoding="utf-8")
    parts.append(f'\n\n<div id="{file_id(page)}"></div>\n\n' + rewrite_links(text, page))

with tempfile.TemporaryDirectory() as tmp:
    src = Path(tmp) / "course.md"
    src.write_text("\n".join(parts), encoding="utf-8")
    css = Path(tmp) / "style.css"
    css.write_text(CSS, encoding="utf-8")
    subprocess.run(["pandoc", str(src), "-f", "gfm", "-t", "html5", "--standalone",
                    "--toc", "--toc-depth=1", "--embed-resources", "--css", str(css),
                    "--metadata", "title=Python for QGIS in the Age of AI",
                    "-o", str(ROOT / "course.html")], check=True)
print("wrote", ROOT / "course.html")
