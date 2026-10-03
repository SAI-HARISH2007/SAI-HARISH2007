#!/usr/bin/env python3
"""Render the last 12 months of GitHub activity as an animated SVG heatmap.

Reads real data from the GitHub GraphQL API (GH_TOKEN / GITHUB_TOKEN, or the
gh CLI when run locally) and writes assets/heatmap.svg. If the fetch fails or
returns nothing, it exits non-zero and leaves the existing file alone.
"""
import datetime as dt
import html
import json
import os
import pathlib
import subprocess
import sys
import urllib.request

LOGIN = os.environ.get("GH_LOGIN", "SAI-HARISH2007")
OUT = pathlib.Path(__file__).resolve().parent.parent / "assets" / "heatmap.svg"

MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,'DejaVu Sans Mono',monospace"
SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"
PANEL, LINE, MUTED = "#0b1220", "#1e293b", "#64748b"
RAMP = ["#131c2e", "#134e6b", "#0891b2", "#22d3ee", "#a7f3d0"]
LEVELS = {"NONE": 0, "FIRST_QUARTILE": 1, "SECOND_QUARTILE": 2, "THIRD_QUARTILE": 3, "FOURTH_QUARTILE": 4}

QUERY = """query($login:String!){user(login:$login){contributionsCollection{contributionCalendar{
totalContributions weeks{contributionDays{date contributionCount contributionLevel}}}}}}"""


def token():
    t = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if t:
        return t
    return subprocess.run(["gh", "auth", "token"], capture_output=True, text=True, check=True).stdout.strip()


def fetch():
    body = json.dumps({"query": QUERY, "variables": {"login": LOGIN}}).encode()
    req = urllib.request.Request("https://api.github.com/graphql", data=body,
                                 headers={"Authorization": f"bearer {token()}", "Content-Type": "application/json"})
    last = None
    for _ in range(4):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                data = json.load(r)
            cal = data["data"]["user"]["contributionsCollection"]["contributionCalendar"]
            return cal
        except Exception as e:  # network flakiness on WSL, rate limits
            last = e
    raise SystemExit(f"fetch failed: {last}")


def stats(days):
    counts = [d["count"] for d in days]
    active = sum(1 for c in counts if c)
    best = cur = 0
    for c in counts:
        cur = cur + 1 if c else 0
        best = max(best, cur)
    return active, best, max(counts)


def render(cal):
    weeks = cal["weeks"]
    days = []
    grid = []
    for w, wk in enumerate(weeks):
        for d in wk["contributionDays"]:
            wd = dt.date.fromisoformat(d["date"]).isoweekday() % 7  # Sunday = 0
            item = dict(w=w, d=wd, date=d["date"], count=d["contributionCount"], lvl=LEVELS[d["contributionLevel"]])
            grid.append(item)
            days.append(item)
    total = cal["totalContributions"]
    active, best, busiest = stats(days)

    C, G = 13, 3
    P = C + G
    left, top = 52, 64
    ncols = len(weeks)
    W = left + ncols * P + 24
    H = top + 7 * P + 70

    out = []
    a = out.append
    a(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="GitHub contributions in the last 12 months: {total}">')
    a("<defs>")
    a('<filter id="bloom" x="-80%" y="-80%" width="260%" height="260%"><feGaussianBlur stdDeviation="3.2"/></filter>')
    a(f'<linearGradient id="bar" x1="0" x2="1"><stop offset="0" stop-color="#22d3ee" stop-opacity="0"/><stop offset="0.5" stop-color="#22d3ee"/><stop offset="1" stop-color="#a78bfa" stop-opacity="0"/></linearGradient>')
    a("</defs>")
    a(f'<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="18" fill="{PANEL}" stroke="{LINE}"/>')
    a(f'<text x="28" y="36" font-family="{MONO}" font-size="13" letter-spacing="1" fill="#22d3ee">ACTIVITY</text>')
    a(f'<text x="108" y="36" font-family="{MONO}" font-size="13" fill="{MUTED}">last 12 months, live from GitHub</text>')
    a(f'<text x="{W - 28}" y="37" text-anchor="end" font-family="{SANS}" font-size="22" font-weight="800" fill="#f1f5f9">{total}'
      f'<tspan font-size="13" font-weight="400" fill="#94a3b8" font-family="{MONO}"> contributions</tspan></text>')
    a(f'<rect x="28" y="46" width="{W - 56}" height="1" fill="{LINE}"/>')
    a(f'<rect x="28" y="45.5" width="260" height="2" fill="url(#bar)"><animateTransform attributeName="transform" type="translate" from="-260 0" to="{W}" dur="6s" repeatCount="indefinite"/></rect>')

    # month labels
    seen = None
    for wk_i, wk in enumerate(weeks):
        first = dt.date.fromisoformat(wk["contributionDays"][0]["date"])
        if first.month != seen and first.day <= 7:
            seen = first.month
            if wk_i < ncols - 2:
                a(f'<text x="{left + wk_i * P}" y="{top - 8}" font-family="{MONO}" font-size="11" fill="{MUTED}">{first.strftime("%b").lower()}</text>')
    for row, name in ((1, "mon"), (3, "wed"), (5, "fri")):
        a(f'<text x="28" y="{top + row * P + 11}" font-family="{MONO}" font-size="10" fill="{MUTED}">{name}</text>')

    # cells: pop-in, then a light wave sweeps across, hot cells glow
    for g in grid:
        x, y = left + g["w"] * P, top + g["d"] * P
        pop = 0.2 + g["w"] * 0.03 + g["d"] * 0.012
        a(f'<rect x="{x}" y="{y}" width="{C}" height="{C}" rx="3.5" fill="{RAMP[g["lvl"]]}" opacity="0">'
          f'<animate attributeName="opacity" from="0" to="1" begin="{pop:.2f}s" dur="0.35s" fill="freeze"/>'
          f'<title>{g["count"]} on {g["date"]}</title></rect>')
    for g in grid:
        if g["lvl"] >= 3:
            x, y = left + g["w"] * P, top + g["d"] * P
            ph = (g["w"] * 0.37 + g["d"] * 0.11) % 3.2
            a(f'<rect x="{x - 1}" y="{y - 1}" width="{C + 2}" height="{C + 2}" rx="5" fill="{RAMP[g["lvl"]]}" filter="url(#bloom)" opacity="0.5">'
              f'<animate attributeName="opacity" values="0.25;0.9;0.25" dur="3.2s" begin="-{ph:.2f}s" repeatCount="indefinite"/></rect>')
    wave_dur = 9.0
    for g in grid:
        x, y = left + g["w"] * P, top + g["d"] * P
        begin = 1.8 + g["w"] * 0.085 + g["d"] * 0.015
        if g["lvl"]:
            col, peak = "#ffffff", 0.7
        else:
            col, peak = "#22d3ee", 0.16
        a(f'<rect x="{x}" y="{y}" width="{C}" height="{C}" rx="3.5" fill="{col}" opacity="0" pointer-events="none">'
          f'<animate attributeName="opacity" values="0;{peak};0;0" keyTimes="0;0.05;0.16;1" dur="{wave_dur}s" begin="{begin:.2f}s" repeatCount="indefinite"/></rect>')

    # today marker
    last = grid[-1]
    cx, cy = left + last["w"] * P + C / 2, top + last["d"] * P + C / 2
    a(f'<circle cx="{cx}" cy="{cy}" r="8" fill="none" stroke="#34d399" stroke-width="1.6">'
      '<animate attributeName="r" values="7;17" dur="2.4s" repeatCount="indefinite"/>'
      '<animate attributeName="stroke-opacity" values="0.9;0" dur="2.4s" repeatCount="indefinite"/></circle>')
    a(f'<rect x="{cx - C / 2 - 1.5}" y="{cy - C / 2 - 1.5}" width="{C + 3}" height="{C + 3}" rx="4.5" fill="none" stroke="#34d399" stroke-width="1.5"/>')

    # footer: stats + legend
    fy = top + 7 * P + 30
    a(f'<text x="28" y="{fy + 4}" font-family="{MONO}" font-size="12" fill="#94a3b8">'
      f'<tspan fill="#22d3ee">{active}</tspan> active days   '
      f'<tspan fill="#22d3ee">{best}</tspan> day best streak   '
      f'<tspan fill="#22d3ee">{busiest}</tspan> in the busiest day</text>')
    lx = W - 28 - (5 * (C + 4)) - 62
    a(f'<text x="{lx}" y="{fy + 4}" text-anchor="end" font-family="{MONO}" font-size="11" fill="{MUTED}">less</text>')
    for i, col in enumerate(RAMP):
        a(f'<rect x="{lx + 10 + i * (C + 4)}" y="{fy - 7}" width="{C}" height="{C}" rx="3.5" fill="{col}"/>')
    a(f'<text x="{lx + 16 + 5 * (C + 4)}" y="{fy + 4}" font-family="{MONO}" font-size="11" fill="{MUTED}">more</text>')
    a(f'<text x="28" y="{H - 14}" font-family="{MONO}" font-size="10.5" fill="#475569">generated by scripts/gen_heatmap.py from the GitHub API, refreshed daily by a workflow</text>')
    a("</svg>")
    return "\n".join(out), total


if __name__ == "__main__":
    cal = fetch()
    svg, total = render(cal)
    if total <= 0:
        sys.exit("no contributions returned, leaving the existing heatmap in place")
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(svg, encoding="utf-8")
    print(f"wrote {OUT} ({total} contributions)")
