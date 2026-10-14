#!/usr/bin/env python3
"""Merge the Obsidian notes in content/ into a single PDF.

Order comes from content/index.md: every top-level `- [[Note]]` bullet is a
chapter, every `#### Heading` above it is a part. index.md itself is the
first page.

Usage: build_pdf.py [--content content] [--out Wireless-Security.pdf]
                    [--work build/pdf]
Pipeline: notes -> one HTML page (pandoc, KaTeX for formulas) -> PDF
(headless Chrome). No LaTeX needed.

Requires pandoc, Chrome/Chromium and a KaTeX install (`npm install katex`;
set KATEX_DIR to node_modules/katex/dist if it isn't found automatically).
mermaid-cli (`mmdc`) is optional (without it, mermaid blocks stay as code).
"""

import argparse
import html
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
FENCE = re.compile(r"^\s*(```|~~~)")
WIKILINK = re.compile(r"(!?)\[\[([^\]]+?)\]\]")
BLOCK_ID = re.compile(r"\s+\^[A-Za-z0-9-]+\s*$")
CALLOUT = re.compile(r"^(\s*>\s*)\[!(\w+)\][+-]?[ \t]*(.*?)\s*$")
HEADING = re.compile(r"^(#{1,6})\s+(.*)$")
IMAGE_EXT = {".png", ".jpg", ".jpeg", ".gif", ".pdf"}
# Rendered width (px) that corresponds to a full text line.
FULL_WIDTH_PX = 700


def warn(msg):
    print(f"::warning::{msg}" if os.environ.get("GITHUB_ACTIONS") else f"warning: {msg}")


def slug(name):
    return "note-" + re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def find_katex():
    candidates = [os.environ.get("KATEX_DIR", ""), "node_modules/katex/dist"]
    if npm := shutil.which("npm"):
        root = subprocess.run([npm, "root", "-g"], capture_output=True, text=True).stdout.strip()
        candidates.append(f"{root}/katex/dist")
    for c in candidates:
        if c and (Path(c) / "katex.min.js").exists():
            return Path(c).resolve()
    sys.exit("KaTeX not found: run `npm install katex` or set KATEX_DIR")


def find_chrome():
    for name in (os.environ.get("CHROME", ""), "google-chrome", "chromium", "chromium-browser"):
        if name and (path := shutil.which(name)):
            return path
    sys.exit("Chrome/Chromium not found (set CHROME)")


def split_frontmatter(text):
    m = re.match(r"\A---\n(.*?\n)---\n", text, re.S)
    if not m:
        return {}, text
    meta = {}
    for line in m.group(1).splitlines():
        k, _, v = line.partition(":")
        meta[k.strip()] = v.strip().strip("\"'")
    return meta, text[m.end():]


def parse_index(body, notes):
    """Return [(part_title, [note_stem, ...]), ...] in index order."""
    parts, in_index = [], False
    for line in body.splitlines():
        if re.match(r"^#{2,3}\s+Index\s*$", line):
            in_index = True
        elif in_index and (m := re.match(r"^####\s+(.*?)\s*$", line)):
            parts.append((m.group(1), []))
        elif in_index and parts and (m := re.match(r"^[-*]\s+\[\[([^\]|#]+)", line)):
            stem = m.group(1).strip()
            if stem in notes:
                parts[-1][1].append(stem)
            else:
                warn(f"index.md links to unknown note: {stem}")
    return parts


class Builder:
    def __init__(self, content, work):
        self.content, self.work = content, work
        self.files = {}  # stem -> path
        for p in content.rglob("*"):
            if p.is_file() and not p.name.startswith("."):
                key = p.stem if p.suffix == ".md" else p.name
                if key in self.files and p.suffix == ".md":
                    sys.exit(f"duplicate note name: {key}")
                self.files.setdefault(key, p)
        self.notes = {k: v for k, v in self.files.items() if v.suffix == ".md"}
        self.images = {}  # original name -> sanitized name in work dir
        self.mermaid_count = 0
        self.mmdc = shutil.which("mmdc")
        (work / "img").mkdir(parents=True, exist_ok=True)
        (work / "mermaid").mkdir(parents=True, exist_ok=True)

    def image(self, name):
        if name in self.images:
            return self.images[name]
        src = self.files.get(name)
        if src is None or src.suffix.lower() not in IMAGE_EXT:
            warn(f"image not found or unsupported: {name}")
            return None
        dest = f"img/{len(self.images):04d}{src.suffix.lower()}"
        shutil.copy(src, self.work / dest)
        self.images[name] = dest
        return dest

    def wikilink(self, m):
        embed, inner = m.group(1), m.group(2)
        target, *rest = re.split(r"\s*\\?\|\s*", inner)
        name, _, heading = target.partition("#")
        name = name.strip()
        if embed:
            if Path(name).suffix.lower() in IMAGE_EXT:
                dest = self.image(name)
                if not dest:
                    return ""
                width = ""
                for r in rest:
                    if r.strip().isdigit():
                        pct = max(5, min(100, round(int(r) / FULL_WIDTH_PX * 100)))
                        width = f"{{width={pct}%}}"
                return f"![]({dest}){width}"
            return name  # transcluded note: just name it
        label = rest[-1] if rest else (heading.strip() or name)
        if name in self.notes:
            return f"[{label}](#{slug(name)})"
        return label

    def mermaid(self, code):
        self.mermaid_count += 1
        n = self.mermaid_count
        src, out = self.work / "mermaid" / f"{n}.mmd", self.work / "mermaid" / f"{n}.png"
        fallback = "```\n" + code + "\n```"
        if not self.mmdc:
            warn("mmdc not found, mermaid diagram kept as code")
            return fallback
        src.write_text(code)
        cmd = [self.mmdc, "-i", str(src), "-o", str(out), "-s", "3", "-b", "white"]
        if cfg := os.environ.get("PUPPETEER_CONFIG"):
            cmd += ["-p", cfg]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode or not out.exists():
            warn(f"mermaid diagram {n} failed to render: {res.stderr.strip()[:300]}")
            return fallback
        return f"![](mermaid/{n}.png){{width=70%}}"

    def convert(self, text):
        """Obsidian markdown -> pandoc markdown."""
        out, lines, i = [], text.splitlines(), 0
        in_math = False
        # Shift headings so the shallowest one becomes level 2 (chapter is level 1).
        levels, fenced = [], False
        for line in lines:
            if FENCE.match(line):
                fenced = not fenced
            elif not fenced and (h := HEADING.match(line)):
                levels.append(len(h.group(1)))
        shift = 2 - min(levels) if levels else 0

        while i < len(lines):
            line = lines[i]
            if m := re.match(r"^\s*```mermaid\s*$", line):
                j = i + 1
                while j < len(lines) and not re.match(r"^\s*```\s*$", lines[j]):
                    j += 1
                out += ["", self.mermaid("\n".join(lines[i + 1:j])), ""]
                i = j + 1
                continue
            if FENCE.match(line):
                j = i + 1
                while j < len(lines) and not FENCE.match(lines[j]):
                    j += 1
                out += lines[i:j + 1]
                i = j + 1
                continue

            if line.count("$$") % 2:
                in_math = not in_math
            elif not in_math:
                line = BLOCK_ID.sub("", line)
                if re.fullmatch(r"\^[A-Za-z0-9-]+", line.strip()):
                    line = ""

            if h := HEADING.match(line):
                line = "#" * max(1, min(6, len(h.group(1)) + shift)) + " " + h.group(2)
            if c := CALLOUT.match(line):
                prefix, kind, title = c.groups()
                line = f"{prefix}**{title or kind.capitalize()}**\n{prefix.rstrip()}"
            if not in_math:
                line = WIKILINK.sub(self.wikilink, line)
            out.append(line)
            i += 1
        return "\n".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--content", default="content", type=Path)
    ap.add_argument("--out", default="Wireless-Security.pdf", type=Path)
    ap.add_argument("--work", default="build/pdf", type=Path)
    args = ap.parse_args()

    content, work = args.content.resolve(), args.work.resolve()
    shutil.rmtree(work, ignore_errors=True)
    b = Builder(content, work)

    meta, index_body = split_frontmatter((content / "index.md").read_text())
    title = meta.get("title", "Wireless Security")
    parts = parse_index(index_body, b.notes)
    if not parts:
        sys.exit("no parts/notes found in index.md")

    doc = [f"# {title} {{.unnumbered}}\n", b.convert(index_body)]
    used = {"index"}
    for part, stems in parts:
        doc.append(f'\n<h1 class="part">{html.escape(part)}</h1>\n')
        for stem in stems:
            used.add(stem)
            _, body = split_frontmatter(b.notes[stem].read_text())
            doc.append(f"\n# {stem} {{#{slug(stem)}}}\n\n{b.convert(body)}\n")
    for stem in sorted(set(b.notes) - used):
        warn(f"note not listed in index.md, skipped: {stem}")

    book = work / "book.md"
    book.write_text("\n".join(doc))

    katex = find_katex()
    page = work / "book.html"
    subprocess.run([
        "pandoc", str(book), "-o", str(page), "--standalone",
        "-f", "markdown+lists_without_preceding_blankline-citations-implicit_header_references",
        "--number-sections", "--resource-path", str(work),
        "--highlight-style=tango",
        "--katex=" + katex.as_uri() + "/",
        "-c", str(HERE / "pdf.css"),
        "-M", f"title={title}", "-M", "lang=en",
    ], check=True)

    cmd = [
        find_chrome(), "--headless", "--no-sandbox", "--disable-gpu",
        "--no-pdf-header-footer", "--virtual-time-budget=60000",
        f"--print-to-pdf={args.out.resolve()}", page.as_uri(),
    ]
    print("+", " ".join(cmd))
    subprocess.run(cmd, check=True)
    print(f"Wrote {args.out} ({args.out.stat().st_size / 1e6:.1f} MB)")


if __name__ == "__main__":
    main()
