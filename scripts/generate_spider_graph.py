#!/usr/bin/env python3
"""Generate a Spider-Verse themed contribution graph SVG.

Usage:
  GITHUB_TOKEN=... GITHUB_USER=Hassan-Ali-17 python scripts/generate_spider_graph.py
  python scripts/generate_spider_graph.py --demo      # fake data, for testing
Output: assets/spider-contrib.svg
"""
import json, os, random, sys, urllib.request

OUT = "assets/spider-contrib.svg"
CELL, GAP = 11, 4
STEP = CELL + GAP
PAD_L, PAD_T = 24, 34

QUERY = """query($login:String!){user(login:$login){contributionsCollection{
contributionCalendar{totalContributions weeks{contributionDays{contributionCount date}}}}}}"""


def fetch(user, token):
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {"login": user}}).encode(),
        headers={"Authorization": f"bearer {token}", "Content-Type": "application/json"},
    )
    data = json.load(urllib.request.urlopen(req))
    cal = data["data"]["user"]["contributionsCollection"]["contributionCalendar"]
    weeks = [[d["contributionCount"] for d in w["contributionDays"]] for w in cal["weeks"]]
    return weeks, cal["totalContributions"]


def demo():
    random.seed(4)
    weeks = [[random.choice([0, 0, 0, 1, 2, 4, 7, 12]) for _ in range(7)] for _ in range(53)]
    return weeks, sum(map(sum, weeks))


def level(n, mx):
    if n == 0: return 0
    r = n / mx
    return 1 if r < .25 else 2 if r < .5 else 3 if r < .8 else 4


COLORS = ["#14080b", "#4a0d14", "#8f1220", "#e01a2b", "#00eaff"]  # 4 = peak days glow cyan


def build(weeks, total):
    mx = max(max(w) for w in weeks) or 1
    W = PAD_L * 2 + len(weeks) * STEP
    H = PAD_T + 7 * STEP + 52
    cells, i = [], 0
    for x, w in enumerate(weeks):
        for y, n in enumerate(w):
            lv = level(n, mx)
            cx, cy = PAD_L + x * STEP, PAD_T + y * STEP
            anim = ""
            if lv >= 3:
                d = round(random.uniform(0, 3), 2)
                anim = (f'<animate attributeName="opacity" values="1;.45;1" dur="2.6s" '
                        f'begin="{d}s" repeatCount="indefinite"/>')
            cells.append(f'<rect x="{cx}" y="{cy}" width="{CELL}" height="{CELL}" rx="2" '
                         f'fill="{COLORS[lv]}">{anim}</rect>')
            i += 1

    # web thread: zigzag through the grid, the spider crawls along it
    pts = []
    for x in range(len(weeks)):
        cx = PAD_L + x * STEP + CELL / 2
        ys = [PAD_T + CELL / 2, PAD_T + 6 * STEP + CELL / 2]
        if x % 2: ys.reverse()
        pts += [(cx, ys[0]), (cx, ys[1])]
    path = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    dur = max(30, len(weeks) * 0.9)

    spider = """
<g id="sp">
  <g fill="#ff1e1e">
    <path d="M0,-4 L7,-12 L12,-18 M2,-2 L12,-5 L19,-10 M2,2 L12,5 L19,10 M0,4 L7,12 L12,18
             M0,-4 L-7,-12 L-12,-18 M-2,-2 L-12,-5 L-19,-10 M-2,2 L-12,5 L-19,10 M0,4 L-7,12 L-12,18"
          fill="none" stroke="#ff1e1e" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>
    <ellipse cx="0" cy="5" rx="5" ry="7.5"/><ellipse cx="0" cy="-5" rx="3.6" ry="4.4"/>
  </g>
</g>"""
    spider_anim = (f'<g><use href="#sp" transform="scale(.62)"/>'
                   f'<animateMotion dur="{dur}s" repeatCount="indefinite" path="{path}"/></g>')

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Spider-Verse contribution graph: {total} contributions in the last year">
<defs>{spider}
<pattern id="scan" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="1.4" fill="#000" opacity=".25"/></pattern></defs>
<rect width="{W}" height="{H}" rx="14" fill="#05050a"/>
<text x="{PAD_L}" y="22" font-family="Courier New,monospace" font-size="13" font-weight="700" fill="#00eaff" letter-spacing="2">&gt; web.crawl(contributions) // {total} in the last year</text>
<path d="{path}" fill="none" stroke="#00eaff" stroke-opacity=".18" stroke-width="1" stroke-dasharray="2 4"/>
{''.join(cells)}
{spider_anim}
<g font-family="Courier New,monospace" font-size="10" fill="#8a8a99">
<text x="{PAD_L}" y="{H-18}">less</text>
{''.join(f'<rect x="{PAD_L+30+k*16}" y="{H-27}" width="11" height="11" rx="2" fill="{c}"/>' for k, c in enumerate(COLORS))}
<text x="{PAD_L+30+5*16+4}" y="{H-18}">more</text></g>
<rect width="{W}" height="{H}" rx="14" fill="url(#scan)" pointer-events="none"/>
</svg>"""


def main():
    if "--demo" in sys.argv:
        weeks, total = demo()
    else:
        weeks, total = fetch(os.environ["GITHUB_USER"], os.environ["GITHUB_TOKEN"])
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, "w", encoding="utf-8").write(build(weeks, total))
    print("wrote", OUT)


if __name__ == "__main__":
    main()
