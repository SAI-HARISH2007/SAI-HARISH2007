#!/usr/bin/env python3
"""Build the static, animated SVGs used by the profile README.

Writes assets/header.svg, assets/flow.svg and assets/card_*.svg.
Pure standard library. The contribution heatmap has its own script
(gen_heatmap.py) because it needs live data.
"""
import html
import math
import pathlib
import random
import textwrap

OUT = pathlib.Path(__file__).resolve().parent.parent / "assets"
OUT.mkdir(exist_ok=True)

MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,'DejaVu Sans Mono',monospace"
SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"

CYAN, VIOLET, MINT, RED = "#38bdf8", "#a78bfa", "#34d399", "#f87171"
BG, PANEL, LINE, MUTED, SOFT = "#070b14", "#0b1220", "#1e293b", "#64748b", "#94a3b8"


def esc(s):
    return html.escape(s, quote=True)


def fmt(x):
    return f"{x:.4f}".rstrip("0").rstrip(".")


# --------------------------------------------------------------------------
# header
# --------------------------------------------------------------------------
def build_header():
    W, H = 1200, 340
    T = 22.0  # seconds per typing cycle
    CW, FS = 8.4, 14  # monospace char width at 14px
    px, py = 60, 176  # terminal panel origin
    tx = px + 18  # text x inside panel
    line_y0, lh = py + 28, 21

    lines = [
        ("cmd", "whoami"),
        ("out", "sai-haresh-anand-s · Hyderabad, India"),
        ("cmd", "cat focus.txt"),
        ("out", "llm agents · verification gates · ai safety"),
        ("cmd", "cat results.txt"),
        ("out", "greenlight  83% → 100% root-cause accuracy · 0% unsafe actions"),
    ]

    # typing schedule
    t = 1.0
    events = []  # (time, line, chars)
    per_line = []  # list of [(time, chars)]
    for i, (kind, body) in enumerate(lines):
        n = len(body) + (2 if kind == "cmd" else 0)
        speed = 0.065 if kind == "cmd" else 0.014
        steps = [(t, 0)]
        events.append((t, i, 0))
        for k in range(1, n + 1):
            steps.append((t + k * speed, k))
            events.append((t + k * speed, i, k))
        per_line.append(steps)
        t += n * speed + (0.4 if kind == "cmd" else 0.55)
    reset_t = T - 1.4
    assert t < reset_t, t

    def key_times(times):
        return ";".join(fmt(x / T) for x in times)

    p = []
    a = p.append
    a(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Sai Haresh Anand S, builds LLM agents and the tests that keep them in check">')
    a("<defs>")
    a(f'<clipPath id="round"><rect width="{W}" height="{H}" rx="18"/></clipPath>')
    a(f'<linearGradient id="nameGrad" x1="0" x2="1"><stop offset="0" stop-color="#ffffff"/><stop offset="0.55" stop-color="#bae6fd"/><stop offset="1" stop-color="{VIOLET}"/></linearGradient>')
    a(f'<radialGradient id="glowR"><stop offset="0" stop-color="{CYAN}" stop-opacity="0.30"/><stop offset="1" stop-color="{CYAN}" stop-opacity="0"/></radialGradient>')
    a(f'<radialGradient id="glowV"><stop offset="0" stop-color="{VIOLET}" stop-opacity="0.26"/><stop offset="1" stop-color="{VIOLET}" stop-opacity="0"/></radialGradient>')
    a(f'<linearGradient id="sweep" x1="0" x2="1"><stop offset="0" stop-color="{CYAN}" stop-opacity="0"/><stop offset="0.5" stop-color="{CYAN}"/><stop offset="1" stop-color="{VIOLET}" stop-opacity="0"/></linearGradient>')
    a(f'<radialGradient id="fade" cx="0.82" cy="0.5" r="0.75"><stop offset="0" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0.05"/></radialGradient>')
    a('<mask id="gridMask"><rect width="100%" height="100%" fill="url(#fade)"/></mask>')
    a('<pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">'
      '<path d="M40 0H0V40" fill="none" stroke="#1e293b" stroke-width="1"/>'
      '<animateTransform attributeName="patternTransform" type="translate" from="0 0" to="40 40" dur="9s" repeatCount="indefinite"/></pattern>')
    a('<filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="4" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>')
    a("</defs>")

    a('<g clip-path="url(#round)">')
    a(f'<rect width="{W}" height="{H}" fill="{BG}"/>')
    a(f'<rect width="{W}" height="{H}" fill="url(#grid)" mask="url(#gridMask)" opacity="0.9"/>')
    a(f'<circle cx="1000" cy="170" r="400" fill="url(#glowR)"><animate attributeName="r" values="360;430;360" dur="9s" repeatCount="indefinite"/></circle>')
    a(f'<circle cx="120" cy="10" r="330" fill="url(#glowV)"><animate attributeName="opacity" values="0.7;1;0.7" dur="11s" repeatCount="indefinite"/></circle>')

    # drifting particles
    rnd = random.Random(11)
    for _ in range(26):
        cx, cy = rnd.uniform(20, W - 20), rnd.uniform(40, H - 20)
        r = rnd.uniform(0.9, 2.2)
        dur = rnd.uniform(6, 13)
        col = rnd.choice([CYAN, VIOLET, MINT, "#e2e8f0"])
        a(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="{col}">'
          f'<animate attributeName="cy" values="{cy:.1f};{cy - 38:.1f};{cy:.1f}" dur="{dur:.1f}s" repeatCount="indefinite"/>'
          f'<animate attributeName="opacity" values="0.15;0.85;0.15" dur="{dur * 0.7:.1f}s" repeatCount="indefinite"/></circle>')

    # window chrome
    for i, c in enumerate(("#ff5f57", "#febc2e", "#28c840")):
        a(f'<circle cx="{px + 4 + i * 20}" cy="40" r="6" fill="{c}" opacity="0.9"/>')
    a(f'<text x="{px + 74}" y="45" font-family="{MONO}" font-size="13" fill="{MUTED}">~/sai-haresh-anand-s</text>')

    # name + tagline
    a(f'<g><text x="{px}" y="116" font-family="{SANS}" font-size="58" font-weight="800" letter-spacing="-1.5" fill="url(#nameGrad)">Sai Haresh Anand S</text>'
      '<animate attributeName="opacity" from="0" to="1" dur="1s" fill="freeze"/>'
      '<animateTransform attributeName="transform" type="translate" from="0 16" to="0 0" dur="1s" fill="freeze"/></g>')
    a(f'<g><text x="{px}" y="154" font-family="{SANS}" font-size="22" fill="#cbd5e1">I build LLM agents, then wrap them in <tspan fill="{CYAN}" font-weight="600">code I can test</tspan>.</text>'
      '<animate attributeName="opacity" from="0" to="1" begin="0.35s" dur="1s" fill="freeze"/></g>')

    # terminal
    a(f'<rect x="{px}" y="{py}" width="640" height="{lh * len(lines) + 24}" rx="12" fill="{PANEL}" stroke="{LINE}"/>')
    for i, (kind, body) in enumerate(lines):
        y = line_y0 + i * lh
        n = len(body) + (2 if kind == "cmd" else 0)
        cid = f"c{i}"
        times = [s for s, _ in per_line[i]] + [reset_t]
        widths = [min(k * CW, n * CW) for _, k in per_line[i]] + [0]
        a(f'<clipPath id="{cid}"><rect x="{tx}" y="{y - 15}" height="21" width="0">'
          f'<animate attributeName="width" calcMode="discrete" repeatCount="indefinite" dur="{T}s" '
          f'keyTimes="0;{key_times(times)}" values="0;{";".join(fmt(w) for w in widths)}"/></rect></clipPath>')
        if kind == "cmd":
            a(f'<text x="{tx}" y="{y}" font-family="{MONO}" font-size="{FS}" textLength="{n * CW:.1f}" lengthAdjust="spacing" clip-path="url(#{cid})" xml:space="preserve">'
              f'<tspan fill="{MINT}">$ </tspan><tspan fill="#e2e8f0">{esc(body)}</tspan></text>')
        else:
            a(f'<text x="{tx}" y="{y}" font-family="{MONO}" font-size="{FS}" fill="{SOFT}" textLength="{n * CW:.1f}" lengthAdjust="spacing" clip-path="url(#{cid})" xml:space="preserve">{esc(body)}</text>')

    # cursor
    ev = [(0.0, 0, 0)] + events + [(reset_t, 0, 0)]
    kt = key_times([e[0] for e in ev])
    xs = ";".join(fmt(tx + e[2] * CW) for e in ev)
    ys = ";".join(fmt(line_y0 + e[1] * lh - 14) for e in ev)
    a(f'<rect width="8" height="17" fill="{CYAN}" x="{tx}" y="{line_y0 - 14}">'
      f'<animate attributeName="x" calcMode="discrete" repeatCount="indefinite" dur="{T}s" keyTimes="{kt}" values="{xs}"/>'
      f'<animate attributeName="y" calcMode="discrete" repeatCount="indefinite" dur="{T}s" keyTimes="{kt}" values="{ys}"/>'
      '<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.5;1" calcMode="discrete" dur="1.1s" repeatCount="indefinite"/></rect>')

    # right side: gate rings
    cx, cy = 990, 172
    def rot(inner, dur, rev=False):
        f, to = (360, 0) if rev else (0, 360)
        return (f'<g>{inner}<animateTransform attributeName="transform" type="rotate" '
                f'from="{f} {cx} {cy}" to="{to} {cx} {cy}" dur="{dur}s" repeatCount="indefinite"/></g>')

    a(rot(f'<circle cx="{cx}" cy="{cy}" r="132" fill="none" stroke="{CYAN}" stroke-opacity="0.38" stroke-width="1.5" stroke-dasharray="3 13"/>'
          f'<circle cx="{cx + 132}" cy="{cy}" r="5.5" fill="{CYAN}" filter="url(#glow)"/>'
          f'<circle cx="{cx + 132 * math.cos(2.3):.1f}" cy="{cy + 132 * math.sin(2.3):.1f}" r="4" fill="{VIOLET}" filter="url(#glow)"/>'
          f'<circle cx="{cx + 132 * math.cos(4.3):.1f}" cy="{cy + 132 * math.sin(4.3):.1f}" r="3.2" fill="{MINT}" filter="url(#glow)"/>', 46))
    a(rot(f'<circle cx="{cx}" cy="{cy}" r="100" fill="none" stroke="{VIOLET}" stroke-opacity="0.5" stroke-width="2" stroke-dasharray="46 14 6 14"/>'
          f'<circle cx="{cx + 100 * math.cos(1.0):.1f}" cy="{cy + 100 * math.sin(1.0):.1f}" r="4.2" fill="{VIOLET}" filter="url(#glow)"/>', 30, True))
    a(rot(f'<circle cx="{cx}" cy="{cy}" r="72" fill="none" stroke="{MINT}" stroke-opacity="0.4" stroke-width="1.2" stroke-dasharray="1 7"/>', 20))
    for d in (0, 1.8):
        a(f'<circle cx="{cx}" cy="{cy}" r="34" fill="none" stroke="{MINT}" stroke-width="2">'
          f'<animate attributeName="r" values="34;112" dur="3.6s" begin="{d}s" repeatCount="indefinite"/>'
          f'<animate attributeName="stroke-opacity" values="0.6;0" dur="3.6s" begin="{d}s" repeatCount="indefinite"/></circle>')
    a(f'<rect x="-27" y="-27" width="54" height="54" rx="11" transform="translate({cx} {cy}) rotate(45)" fill="{PANEL}" stroke="{MINT}" stroke-width="2.2" filter="url(#glow)"/>')
    a(f'<path d="M{cx - 13} {cy + 1} L{cx - 3} {cy + 11} L{cx + 14} {cy - 10}" fill="none" stroke="{MINT}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="46" stroke-dashoffset="46">'
      '<animate attributeName="stroke-dashoffset" values="46;0;0;46" keyTimes="0;0.25;0.85;1" dur="4.5s" repeatCount="indefinite"/></path>')
    for txt, x, y, anc in (("probe", cx, 28, "middle"), ("verify", cx + 150, cy + 4, "start"), ("approve", cx, 322, "middle")):
        a(f'<text x="{x}" y="{y}" text-anchor="{anc}" font-family="{MONO}" font-size="12" fill="{MUTED}" opacity="0.8">{txt}</text>')

    # bottom sweep
    a(f'<rect x="0" y="{H - 3}" width="{W}" height="3" fill="{LINE}" opacity="0.6"/>')
    a(f'<rect y="{H - 3}" width="320" height="3" fill="url(#sweep)"><animateTransform attributeName="transform" type="translate" from="-320 0" to="{W}" dur="5.5s" repeatCount="indefinite"/></rect>')
    a("</g>")
    a(f'<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="18" fill="none" stroke="{LINE}"/>')
    a("</svg>")
    (OUT / "header.svg").write_text("\n".join(p), encoding="utf-8")


# --------------------------------------------------------------------------
# flow: one greenlight run
# --------------------------------------------------------------------------
def build_flow():
    W, H, T = 1200, 310, 16.0
    xs = [130, 360, 590, 820, 1050]
    y = 168  # node row
    yr = y - 60  # rail the packet travels on
    labels = [("ALERT", "a page fires"), ("INVESTIGATE", "tools, logs, configs"), ("VERIFY GATE", "probe, or no verdict"),
              ("HUMAN OK", "a person approves"), ("REMEDIATE", "only after approval")]
    x0, x1 = xs[0], xs[-1]
    span = x1 - x0

    def kt(*v):
        return ";".join(fmt(i) for i in v)

    # packet timeline: (time fraction, position along the line)
    tl = [(0, 0), (0.07, .25), (0.13, .25), (0.22, .5), (0.28, .5), (0.36, .30), (0.44, .30),
          (0.52, .5), (0.56, .5), (0.62, .5), (0.66, .5), (0.74, .75), (0.80, .75), (0.88, 1), (0.94, 1), (1, 1)]

    p = []
    a = p.append
    a(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="One greenlight run: alert, investigate, verify gate rejects until a probe runs, human approval, remediation">')
    a("<defs>")
    a('<filter id="glow" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>')
    a(f'<linearGradient id="trail" x1="0" x2="1"><stop offset="0" stop-color="{CYAN}"/><stop offset="1" stop-color="{VIOLET}"/></linearGradient>')
    a("</defs>")
    a(f'<rect width="{W}" height="{H}" rx="18" fill="{PANEL}" stroke="{LINE}"/>')
    a(f'<text x="34" y="42" font-family="{MONO}" font-size="13" fill="{MUTED}">one run of greenlight, simplified</text>')
    a(f'<text x="{W - 34}" y="42" text-anchor="end" font-family="{MONO}" font-size="13" fill="{MUTED}">the gate is plain code, not a prompt</text>')

    # rail
    a(f'<path d="M{x0} {yr} H{x1}" stroke="{LINE}" stroke-width="4" stroke-linecap="round"/>')
    for x in xs:
        a(f'<path d="M{x} {yr} V{y - 38}" stroke="{LINE}" stroke-width="3"/><circle cx="{x}" cy="{yr}" r="5" fill="{PANEL}" stroke="{LINE}" stroke-width="2"/>')
    a(f'<path d="M{x0} {yr} H{x1}" stroke="url(#trail)" stroke-width="2" stroke-dasharray="6 14" stroke-linecap="round" opacity="0.7">'
      '<animate attributeName="stroke-dashoffset" from="20" to="0" dur="1.2s" repeatCount="indefinite"/></path>')

    # nodes
    for i, (x, (name, sub)) in enumerate(zip(xs, labels)):
        stroke_attr = f'stroke="{LINE}"'
        extra = ""
        if i == 2:
            stroke_attr = f'stroke="{CYAN}" stroke-width="2.5" filter="url(#glow)"'
            extra = (f'<animate attributeName="stroke" calcMode="discrete" dur="{T}s" repeatCount="indefinite" '
                     f'keyTimes="{kt(0, .22, .31, .55, .70)}" values="{CYAN};{RED};{CYAN};{MINT};{CYAN}"/>')
        a(f'<rect x="{x - 78}" y="{y - 38}" width="156" height="76" rx="16" fill="#0f1b2d" {stroke_attr}>{extra}</rect>')
        a(f'<text x="{x}" y="{y - 4}" text-anchor="middle" font-family="{MONO}" font-size="15" font-weight="700" fill="#e2e8f0" letter-spacing="1">{esc(name)}</text>')
        a(f'<text x="{x}" y="{y + 18}" text-anchor="middle" font-family="{SANS}" font-size="12.5" fill="{MUTED}">{esc(sub)}</text>')

    # packet
    kp = ";".join(fmt(v) for _, v in tl)
    kk = ";".join(fmt(k) for k, _ in tl)
    a(f'<circle r="10" fill="{CYAN}" filter="url(#glow)">'
      f'<animateMotion dur="{T}s" repeatCount="indefinite" calcMode="linear" keyPoints="{kp}" keyTimes="{kk}" path="M{x0} {yr} H{x1}"/>'
      f'<animate attributeName="fill" calcMode="discrete" dur="{T}s" repeatCount="indefinite" keyTimes="{kt(0, .23, .31, .58, .70)}" values="{CYAN};{RED};{CYAN};{MINT};{CYAN}"/>'
      f'<animate attributeName="opacity" dur="{T}s" repeatCount="indefinite" keyTimes="{kt(0, .93, 1)}" values="1;1;0"/></circle>')

    def note(txt, x, yy, color, t0, t1, size=14):
        a(f'<text x="{x}" y="{yy}" text-anchor="middle" font-family="{MONO}" font-size="{size}" font-weight="600" fill="{color}" opacity="0">{esc(txt)}'
          f'<animate attributeName="opacity" calcMode="discrete" dur="{T}s" repeatCount="indefinite" keyTimes="{kt(0, t0, t1)}" values="0;1;0"/></text>')

    note("REJECTED · no probe has run yet", xs[2], yr - 22, RED, .22, .33)
    note("run_probe(http)", xs[1], y + 66, MINT, .36, .50)
    note("VERIFIED · a probe confirmed the cause", xs[2], yr - 22, MINT, .58, .72)
    note("approved", xs[3], y + 66, MINT, .74, .82)
    note("executed", xs[4], y + 66, MINT, .88, .96)

    a(f'<text x="{W / 2}" y="{H - 40}" text-anchor="middle" font-family="{SANS}" font-size="17" fill="#cbd5e1">'
      f'Root-cause accuracy <tspan fill="{MINT}" font-weight="700">83% → 100%</tspan> on 12 seeded incidents · '
      f'<tspan fill="{MINT}" font-weight="700">0%</tspan> unsafe actions</text>')
    a(f'<text x="{W / 2}" y="{H - 16}" text-anchor="middle" font-family="{MONO}" font-size="12" fill="{MUTED}">same model as the baseline; every number reproduces with no API calls</text>')
    a("</svg>")
    (OUT / "flow.svg").write_text("\n".join(p), encoding="utf-8")


# --------------------------------------------------------------------------
# project cards
# --------------------------------------------------------------------------
CARDS = [
    dict(key="greenlight", accent=CYAN, tag="01 · INCIDENT AGENT", title="greenlight",
         desc="Investigates production incidents. It can't conclude until a live probe confirms the cause, and no fix runs without human approval.",
         stat="83% → 100% root cause on 12 incidents", chips=["Python", "Agents", "Evals"]),
    dict(key="provenance", accent=VIOLET, tag="02 · AGENT MEMORY", title="provenance",
         desc="Gives greenlight long-term memory. A recalled memory is a claim, so a matching verdict is re-verified by a probe in the current incident.",
         stat="6 incidents · 3 variants · failures documented", chips=["Hindsight", "Docker", "Python"]),
    dict(key="safestep", accent=MINT, tag="03 · APP + SELF AUDIT", title="SafeStep",
         desc="Scores route safety from landmarks, lighting and crowds, with SOS alerts and live trip sharing. Team of 3, and I led it.",
         stat="My own audit: 81% of prompt injections worked", chips=["Next.js", "Gemini", "Firebase"]),
    dict(key="quantbot", accent="#fbbf24", tag="04 · QUANT RESEARCH", title="QuantBot",
         desc="Backtests and paper trades with the same strategy code. The kill switch lives on a control plane the strategies can't override.",
         stat="83 tests · strict mypy · paper trading only", chips=["Python", "FastAPI", "pandas"]),
    dict(key="activation-shield", accent="#f472b6", tag="05 · INTERPRETABILITY · IN PROGRESS", title="activation-shield",
         desc="Finds a deception direction in a fine-tuned GPT-2 and suppresses it with a forward hook, without changing any weights.",
         stat="Detection near perfect, suppression is the hard part", chips=["PyTorch", "Transformers"]),
    dict(key="reclaim", accent="#fb923c", tag="06 · PAYMENTS AGENT", title="Reclaim",
         desc="Recovers failed payments. 114 Razorpay failure reasons resolve through an auditable rule table, and an LLM only sees the ambiguous ones.",
         stat="Rules where correctness is knowable", chips=["Python", "FastAPI", "Razorpay"]),
]


def build_cards():
    W, H = 560, 224
    for n, c in enumerate(CARDS):
        acc = c["accent"]
        p = []
        a = p.append
        a(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{esc(c["title"])}: {esc(c["desc"])}">')
        a("<defs>")
        a(f'<linearGradient id="g{n}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{acc}" stop-opacity="0.16"/><stop offset="1" stop-color="{acc}" stop-opacity="0"/></linearGradient>')
        a('<filter id="glow" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>')
        a("</defs>")
        a(f'<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="16" fill="{PANEL}" stroke="{LINE}"/>')
        a(f'<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="16" fill="url(#g{n})"/>')
        a(f'<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="16" fill="none" stroke="{acc}" stroke-width="2.2" pathLength="100" '
          f'stroke-dasharray="16 84" stroke-linecap="round" filter="url(#glow)">'
          f'<animate attributeName="stroke-dashoffset" from="0" to="-100" dur="{6 + (n % 3)}s" begin="-{n * 1.3:.1f}s" repeatCount="indefinite"/></rect>')
        a(f'<circle cx="30" cy="34" r="4" fill="{acc}"><animate attributeName="opacity" values="1;0.25;1" dur="2.4s" repeatCount="indefinite"/></circle>')
        a(f'<text x="44" y="38" font-family="{MONO}" font-size="12.5" letter-spacing="1.2" fill="{acc}">{esc(c["tag"])}</text>')
        a(f'<text x="28" y="76" font-family="{SANS}" font-size="29" font-weight="800" letter-spacing="-0.5" fill="#f1f5f9">{esc(c["title"])}</text>')
        for i, ln in enumerate(textwrap.wrap(c["desc"], 68)[:3]):
            a(f'<text x="28" y="{104 + i * 21}" font-family="{SANS}" font-size="15.5" fill="{SOFT}">{esc(ln)}</text>')
        sw = len(c["stat"]) * 7.6 + 28
        a(f'<rect x="28" y="{H - 66}" width="{sw:.0f}" height="28" rx="14" fill="{acc}" fill-opacity="0.12" stroke="{acc}" stroke-opacity="0.45"/>')
        a(f'<text x="{28 + 14}" y="{H - 47}" font-family="{MONO}" font-size="13" fill="{acc}">{esc(c["stat"])}</text>')
        x = 28
        for ch in c["chips"]:
            w = len(ch) * 7.4 + 22
            a(f'<rect x="{x}" y="{H - 32}" width="{w:.0f}" height="22" rx="6" fill="#0f1b2d" stroke="{LINE}"/>')
            a(f'<text x="{x + w / 2:.0f}" y="{H - 17}" text-anchor="middle" font-family="{MONO}" font-size="12" fill="{MUTED}">{esc(ch)}</text>')
            x += w + 8
        a("</svg>")
        (OUT / f"card_{c['key']}.svg").write_text("\n".join(p), encoding="utf-8")


if __name__ == "__main__":
    build_header()
    build_flow()
    build_cards()
    print("wrote", ", ".join(sorted(f.name for f in OUT.glob("*.svg"))))
