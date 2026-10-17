#!/usr/bin/env python3
"""Generates glitching section headers + multiverse (Earth-N) project cards as SVGs."""
import os
from xml.sax.saxutils import escape

FONT = "'Courier New', Consolas, Menlo, monospace"

# ---------------------------------------------------------------- headers
HEADERS = [
    ("who",        "> who.am_i()"),
    ("stack",      "> tech.stack[]"),
    ("skills",     "> spider_sense.scan(skills)"),
    ("featured",   "> git log --featured"),
    ("stats",      "> github.stats --realtime"),
    ("experience", "> cat ./experience.log"),
]

def header(text, k):
    t = escape(text)
    d = round(0.35 * k, 2)  # stagger so headers don't glitch in sync
    return f"""<svg viewBox="0 0 800 60" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{t}">
<defs>
  <linearGradient id="bar" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ff1e1e"/><stop offset="1" stop-color="#00eaff"/></linearGradient>
  <linearGradient id="ul" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#ff1e1e"/><stop offset=".5" stop-color="#000"/><stop offset="1" stop-color="#00eaff"/></linearGradient>
  <clipPath id="sl"><rect x="0" y="22" width="800" height="12"/></clipPath>
  <pattern id="sc" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="1.3" fill="#000" opacity=".3"/></pattern>
</defs>
<style>
  text{{font:700 28px {FONT};letter-spacing:1px}}
  .c{{animation:c 3.4s steps(1,end) {d}s infinite}}
  .r{{animation:r 3.4s steps(1,end) {d}s infinite}}
  .m{{animation:m 3.4s steps(1,end) {d}s infinite}}
  .s{{opacity:0;animation:s 3.4s steps(1,end) {d}s infinite}}
  @keyframes c{{0%,60%,100%{{transform:translate(-2px,0)}}62%{{transform:translate(-9px,2px)}}64%{{transform:translate(5px,-1px)}}66%{{transform:translate(-2px,0)}}88%{{transform:translate(-12px,0)}}90%{{transform:translate(-2px,0)}}}}
  @keyframes r{{0%,60%,100%{{transform:translate(2px,0)}}62%{{transform:translate(9px,-2px)}}64%{{transform:translate(-5px,1px)}}66%{{transform:translate(2px,0)}}88%{{transform:translate(12px,0)}}90%{{transform:translate(2px,0)}}}}
  @keyframes m{{0%,59%,100%{{opacity:1}}60%{{opacity:.35}}61%{{opacity:1}}87%{{opacity:.4}}89%{{opacity:1}}}}
  @keyframes s{{0%,62%,100%{{opacity:0;transform:translateX(0)}}63%{{opacity:1;transform:translateX(26px)}}65%{{opacity:1;transform:translateX(-18px)}}67%{{opacity:0}}88%{{opacity:1;transform:translateX(-22px)}}90%{{opacity:0}}}}
</style>
<rect width="800" height="60" rx="10" fill="#05050a"/>
<rect x="10" y="10" width="6" height="34" rx="2" fill="url(#bar)"/>
<text class="c" x="30" y="38" fill="#00eaff" opacity=".85">{t}</text>
<text class="r" x="30" y="38" fill="#ff1e1e" opacity=".85">{t}</text>
<text class="m" x="30" y="38" fill="#ffffff">{t}</text>
<g clip-path="url(#sl)"><text class="s" x="30" y="38" fill="#ff1e1e">{t}</text></g>
<rect x="0" y="52" width="800" height="3" fill="url(#ul)"/>
<rect x="-120" y="52" width="120" height="3" fill="#fff" opacity=".9">
  <animate attributeName="x" values="-120;800" dur="2.6s" repeatCount="indefinite"/>
  <animate attributeName="opacity" values=".9;.5;.9" dur=".6s" repeatCount="indefinite"/>
</rect>
<rect width="800" height="60" rx="10" fill="url(#sc)"/>
</svg>"""

# ---------------------------------------------------------------- cards
EARTHS = [
    # n, name, tagline, tags, accent
    (1, "Hassan-Verse 3D Portfolio", "Step into the rift: a 3D desk you can explore.",   ["Three.js", "React", "Vercel"],            "#ff1e1e"),
    (2, "Cost-Based Query Optimizer", "Selinger DP join ordering, built from scratch.",   ["C++", "Algorithms", "Systems"],          "#00eaff"),
    (3, "FairGig  //  Softec 2026",   "Gig workers' earnings, tracked and verified.",     ["TypeScript", "Microservices", "Top 5"],  "#b14bff"),
    (4, "Fleet Crisis Command",       "Live fleet tracking with an AI crisis advisor.",   ["Next.js", "Flask", "Socket.IO"],         "#4d7cff"),
    (5, "VORTEX OS",                  "A hand-built Linux shell on the road to a distro.",["Python", "Linux", "Shell"],              "#39ff88"),
    (6, "TaskFlow Pro",               "One workspace for every team's tasks, with AI.",   ["Python", "Flask", "AI"],                 "#ffd400"),
    (7, "Zaiqa On Wheels",            "Food and groceries, ordered and delivered.",       ["Flask", "SQLite", "Full-stack"],         "#ff7a1a"),
    (8, "Rental Car App",             "Zero STL. Fully from scratch.",                    ["C++", "File I/O", "Low-level"],          "#ff4fa3"),
    (9, "Scrabble (C++ & SFML)",      "A full digital Scrabble on a 15x15 board.",        ["C++", "SFML", "OOP"],                    "#9aa4ff"),
]

def card(n, name, tag, tags, col):
    d = round(0.45 * n, 2)
    chips, x = [], 28
    for t in tags:
        w = 16 + 8.2 * len(t)
        chips.append(f'<rect x="{x}" y="138" width="{w:.0f}" height="24" rx="12" fill="none" stroke="{col}" stroke-opacity=".8"/>'
                     f'<text x="{x + w/2:.0f}" y="154" text-anchor="middle" class="chip">{escape(t)}</text>')
        x += w + 10
    return f"""<svg viewBox="0 0 560 190" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Earth-{n}: {escape(name)}. {escape(tag)}">
<defs>
  <clipPath id="sl"><rect x="0" y="16" width="560" height="9"/></clipPath>
  <pattern id="sc" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="1.3" fill="#000" opacity=".28"/></pattern>
  <linearGradient id="fade" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{col}" stop-opacity=".16"/><stop offset=".6" stop-color="{col}" stop-opacity="0"/></linearGradient>
</defs>
<style>
  .lab{{font:700 15px {FONT};letter-spacing:5px}}
  .nm{{font:700 22px {FONT};fill:#fff}}
  .tg{{font:14px {FONT};fill:#c4c4d0}}
  .chip{{font:700 11px {FONT};fill:{col};letter-spacing:.5px}}
  .dim{{font:700 11px {FONT};fill:{col};opacity:.7;letter-spacing:3px}}
  .lc{{animation:lc 3.6s steps(1,end) {d}s infinite}}
  .lr{{animation:lr 3.6s steps(1,end) {d}s infinite}}
  .ls{{opacity:0;animation:ls 3.6s steps(1,end) {d}s infinite}}
  .bd{{animation:bd 3.6s steps(1,end) {d}s infinite}}
  @keyframes lc{{0%,60%,100%{{transform:translate(-1.5px,0)}}62%{{transform:translate(-8px,1px)}}64%{{transform:translate(4px,0)}}66%{{transform:translate(-1.5px,0)}}}}
  @keyframes lr{{0%,60%,100%{{transform:translate(1.5px,0)}}62%{{transform:translate(8px,-1px)}}64%{{transform:translate(-4px,0)}}66%{{transform:translate(1.5px,0)}}}}
  @keyframes ls{{0%,62%,100%{{opacity:0;transform:translateX(0)}}63%{{opacity:1;transform:translateX(22px)}}65%{{opacity:1;transform:translateX(-16px)}}67%{{opacity:0}}}}
  @keyframes bd{{0%,60%,100%{{stroke-opacity:.9}}61%{{stroke-opacity:.2}}62%{{stroke-opacity:.9}}86%{{stroke-opacity:.3}}87%{{stroke-opacity:.9}}}}
</style>
<rect width="560" height="190" rx="14" fill="#05050a"/>
<rect width="560" height="190" rx="14" fill="url(#fade)"/>
<rect class="bd" x="1.5" y="1.5" width="557" height="187" rx="13" fill="none" stroke="{col}" stroke-width="2"/>
<rect x="0" y="22" width="7" height="146" fill="{col}"/>
<text class="lab lc" x="28" y="36" fill="#00eaff" opacity=".8">EARTH-{n}</text>
<text class="lab lr" x="28" y="36" fill="{col}" opacity=".9">EARTH-{n}</text>
<text class="lab" x="28" y="36" fill="#fff" opacity=".9">EARTH-{n}</text>
<g clip-path="url(#sl)"><text class="lab ls" x="28" y="36" fill="{col}">EARTH-{n}</text></g>
<text class="dim" x="532" y="36" text-anchor="end">DIM-{n:02d}</text>
<text class="nm" x="28" y="82">{escape(name)}</text>
<text class="tg" x="28" y="112">{escape(tag)}</text>
{''.join(chips)}
<rect x="-90" y="184" width="90" height="3" fill="{col}" opacity=".9"><animate attributeName="x" values="-90;560" dur="3.2s" begin="{d}s" repeatCount="indefinite"/></rect>
<rect width="560" height="190" rx="14" fill="url(#sc)"/>
</svg>"""

if __name__ == "__main__":
    os.makedirs("assets/headers", exist_ok=True)
    os.makedirs("assets/earths", exist_ok=True)
    for k, (slug, text) in enumerate(HEADERS):
        open(f"assets/headers/{slug}.svg", "w", encoding="utf-8").write(header(text, k))
    for e in EARTHS:
        open(f"assets/earths/earth-{e[0]}.svg", "w", encoding="utf-8").write(card(*e))
    print("done")
