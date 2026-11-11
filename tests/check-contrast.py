#!/usr/bin/env python3
"""WCAG 2.x contrast checker for the Comunica+ category palette.

Parses every --cat-* / --cat-*-ink declaration from index.html, resolves the
effective pair per visual style (:root default, plus body[data-style="adulto"]
overrides on background, with ink falling back to :root) and asserts each pair
reaches 4.5:1 (WCAG 2.2 SC 1.4.3, AA, normal text).

Usage:
    python3 tests/check-contrast.py index.html

Exit codes: 0 = every pair passes, 1 = at least one pair fails.
"""
import re
import sys

VAR_RE = re.compile(r"--cat-([a-z]+)(?:-(ink))?:\s*(#[0-9A-Fa-f]{6})")
ADULTO_MARKER = 'body[data-style="adulto"]{'


def luminance(hex_color):
    r, g, b = (int(hex_color[i:i + 2], 16) / 255 for i in (1, 3, 5))

    def lin(c):
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

    return 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b)


def contrast(a, b):
    la, lb = luminance(a), luminance(b)
    return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)


def parse_block(text, target_bg, target_ink):
    for cat, is_ink, value in VAR_RE.findall(text):
        (target_ink if is_ink else target_bg)[cat] = value


def parse(path):
    with open(path, encoding="utf-8") as fh:
        src = fh.read()
    if ADULTO_MARKER not in src:
        sys.exit(f"marker {ADULTO_MARKER!r} not found in {path} — ABORT")
    before, rest = src.split(ADULTO_MARKER, 1)
    adulto_block = rest.split("}", 1)[0]
    default_bg, default_ink, adulto_bg, adulto_ink = {}, {}, {}, {}
    parse_block(before, default_bg, default_ink)
    parse_block(adulto_block, adulto_bg, adulto_ink)
    return default_bg, default_ink, adulto_bg, adulto_ink


def main():
    if len(sys.argv) != 2:
        sys.exit(f"usage: {sys.argv[0]} <path-to-index.html>")
    default_bg, default_ink, adulto_bg, adulto_ink = parse(sys.argv[1])
    failures = []
    print(f"{'style':8} {'category':12} {'bg':9} {'ink':9} {'ratio':>6}  verdict")
    for style, bgs, inks in (
        ("default", default_bg, default_ink),
        ("adulto", {**default_bg, **adulto_bg}, {**default_ink, **adulto_ink}),
    ):
        for cat in sorted(bgs):
            bg, ink = bgs[cat], inks.get(cat)
            if not ink:
                print(f"{style:8} {cat:12} {bg:9} {'MISSING':9} {'-':>6}  FAIL")
                failures.append((style, cat, "missing ink"))
                continue
            ratio = contrast(bg, ink)
            ok = ratio >= 4.5
            print(f"{style:8} {cat:12} {bg:9} {ink:9} {ratio:6.2f}  {'PASS' if ok else 'FAIL'}")
            if not ok:
                failures.append((style, cat, f"{ratio:.2f}"))
    print(f"\n{len(failures)} pair(s) below AA 4.5:1")
    for style, cat, detail in failures:
        print(f"  - [{style}] {cat}: {detail}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
