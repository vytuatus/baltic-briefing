#!/usr/bin/env python3
"""Build the public Baltic threat briefing page (index.html) from data/*.json.

Usage: python3 build.py   (run from the repository root)
Reads data/editions.json, indicators.json, stories.json, claims.json,
counts.json and links.json, and writes a self-contained index.html
(no scripts, no external files) for GitHub Pages.
"""
import json
import os
from datetime import date as Date
from html import escape

ROOT = os.path.dirname(os.path.abspath(__file__))
POINTS = {"quiet": 0, "watch": 1, "elevated": 2, "high": 3}
AREAS = ["Military", "Hybrid", "Political", "Logistics and medical"]
AREA_COLORS = ["#2f6fdf", "#d9534f", "#8a63d2", "#1f9d74"]
QUALITY = {"confirmed": "Supported", "likely": "Supported", "contested": "Open", "disputed": "Open",
           "unconfirmed": "Open", "misleading": "Rejected", "unsupported": "Rejected", "false": "Rejected"}
QCOLORS = {"Supported": "var(--ok)", "Open": "var(--warn)", "Rejected": "var(--bad)"}
QLABELS = {"Supported": "Confirmed or likely", "Open": "Contested, disputed or unconfirmed",
           "Rejected": "Misleading, unsupported or false"}


def load(name):
    path = os.path.join(ROOT, "data", name + ".json")
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    return data if isinstance(data, list) else data.get("rows", [])


def e(x):
    return escape("" if x is None else str(x))


def level(s):
    v = str(s or "").strip().lower()
    return {"low": "quiet", "quiet": "quiet", "moderate": "watch", "watch": "watch",
            "elevated": "elevated", "high": "high", "severe": "high"}.get(v, "watch")


def slug(s):
    return "".join(c if c.isalpha() else "-" for c in str(s or "").lower()).strip("-")


def fmt_long(d):
    y, m, dd = map(int, d.split("-"))
    return Date(y, m, dd).strftime("%A %-d %B %Y")


def fmt_short(d):
    y, m, dd = map(int, d.split("-"))
    return Date(y, m, dd).strftime("%b %-d")


def by_order(rows):
    return sorted(rows, key=lambda r: float(r.get("order", 0) or 0))


def score_chart(indicators, dates):
    W, H = 760, 250
    m = dict(top=12, right=190, bottom=26, left=34)
    series = {a: [] for a in AREAS}
    ymax = 3
    for d in dates:
        day = [r for r in indicators if r["date"] == d]
        for a in AREAS:
            rows = [r for r in day if r.get("group") == a]
            s = sum(POINTS.get(str(r.get("status", "")).lower(), 0) for r in rows)
            series[a].append((d, s, len(rows) * 3))
            ymax = max(ymax, len(rows) * 3)
    n = len(dates)
    iw = W - m["left"] - m["right"]

    def x(i):
        return m["left"] + (iw / 2 if n == 1 else iw * i / (n - 1))

    def y(v):
        return m["top"] + (H - m["top"] - m["bottom"]) * (1 - v / ymax)

    out = [f'<svg viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="Threat score by area over time">']
    for t in range(0, ymax + 1, 3):
        out.append(f'<line x1="{m["left"]}" x2="{W - m["right"]}" y1="{y(t):.1f}" y2="{y(t):.1f}" class="grid"/>')
        out.append(f'<text x="{m["left"] - 8}" y="{y(t):.1f}" dy="0.32em" text-anchor="end">{t}</text>')
    step = max(1, -(-n // 8))
    for i, d in enumerate(dates):
        if i % step == 0 or i == n - 1:
            out.append(f'<text x="{x(i):.1f}" y="{H - 6}" text-anchor="middle">{e(fmt_short(d))}</text>')
    ends = []
    for k, a in enumerate(AREAS):
        pts = series[a]
        col = AREA_COLORS[k]
        if n > 1:
            path = " ".join(f'{"M" if i == 0 else "L"}{x(i):.1f},{y(s):.1f}' for i, (_, s, _) in enumerate(pts))
            out.append(f'<path d="{path}" fill="none" stroke="{col}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>')
        r = 2 if n > 20 else 3.5
        for i, (d, s, mx) in enumerate(pts):
            out.append(f'<circle cx="{x(i):.1f}" cy="{y(s):.1f}" r="{r}" fill="{col}"><title>{e(fmt_short(d))} · {e(a)}: {s} of {mx}</title></circle>')
        ends.append([y(pts[-1][1]), f"{a} {pts[-1][1]}", col])
    ends.sort()
    for i in range(1, len(ends)):
        if ends[i][0] - ends[i - 1][0] < 14:
            ends[i][0] = ends[i - 1][0] + 14
    over = ends[-1][0] - (H - m["bottom"]) if ends else 0
    for en in ends:
        yy = en[0] - max(0, over)
        out.append(f'<text x="{x(n - 1) + 10:.1f}" y="{yy:.1f}" dy="0.32em" class="endlab" style="fill:{en[2]}">{e(en[1])}</text>')
    out.append("</svg>")
    return "".join(out)


def mini_bars(points, ymax):
    W, H = 240, 28
    n = max(1, len(points))
    band = W / n
    bw = min(16, band * 0.8)
    out = [f'<svg viewBox="0 0 {W} {H}" width="100%" height="{H}" preserveAspectRatio="none" aria-hidden="true">',
           f'<line x1="0" x2="{W}" y1="{H - 0.5}" y2="{H - 0.5}" class="grid"/>']
    for i, (d, v, note) in enumerate(points):
        h = max(2, (H - 3) * v / ymax) if ymax else 2
        col = "var(--accent)" if v > 0 else "var(--muted-bar)"
        out.append(f'<rect x="{i * band + (band - bw) / 2:.1f}" y="{H - 1 - h:.1f}" width="{bw:.1f}" height="{h:.1f}" rx="2" fill="{col}">'
                   f'<title>{e(fmt_short(d))}: {v} new. {e(note)}</title></rect>')
    out.append("</svg>")
    return "".join(out)


def quality_chart(claims, dates):
    W, H = 420, 170
    m = dict(top=8, right=4, bottom=22, left=26)
    rows = []
    for d in dates:
        c = {"Supported": 0, "Open": 0, "Rejected": 0}
        for r in claims:
            if r["date"] == d:
                c[QUALITY.get(str(r.get("verdict", "")).lower(), "Open")] += 1
        rows.append((d, c))
    ymax = max([1] + [sum(c.values()) for _, c in rows])
    n = len(rows)
    iw = W - m["left"] - m["right"]
    band = iw / max(1, n)
    bw = min(32, band * 0.7)

    def y(v):
        return m["top"] + (H - m["top"] - m["bottom"]) * (1 - v / ymax)

    out = [f'<svg viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="Claims by verdict per day">']
    tstep = max(1, -(-ymax // 4))
    for t in range(0, ymax + 1, tstep):
        out.append(f'<line x1="{m["left"]}" x2="{W - m["right"]}" y1="{y(t):.1f}" y2="{y(t):.1f}" class="grid"/>')
        out.append(f'<text x="{m["left"] - 6}" y="{y(t):.1f}" dy="0.32em" text-anchor="end">{t}</text>')
    lstep = max(1, -(-n // 6))
    for i, (d, c) in enumerate(rows):
        x0 = m["left"] + i * band + (band - bw) / 2
        base = 0
        for cat in ["Supported", "Open", "Rejected"]:
            v = c[cat]
            if v:
                out.append(f'<rect x="{x0:.1f}" y="{y(base + v):.1f}" width="{bw:.1f}" height="{y(base) - y(base + v):.1f}" fill="{QCOLORS[cat]}">'
                           f'<title>{e(fmt_short(d))} · {QLABELS[cat]}: {v}</title></rect>')
            base += v
        if i % lstep == 0 or i == n - 1:
            out.append(f'<text x="{x0 + bw / 2:.1f}" y="{H - 6}" text-anchor="middle">{e(fmt_short(d))}</text>')
    out.append("</svg>")
    return "".join(out)


def main():
    editions = load("editions")
    indicators = load("indicators")
    stories = load("stories")
    claims = load("claims")
    counts = load("counts")
    links = load("links")
    if not editions:
        raise SystemExit("data/editions.json is empty")
    last = max(r["date"] for r in editions)
    ed = [r for r in editions if r["date"] == last][0]
    latest = lambda rows: by_order([r for r in rows if r.get("date") == max((q["date"] for q in rows), default="")])
    ind_today, claims_today, stories_today = latest(indicators), latest(claims), latest(stories)
    links_last = max((r["date"] for r in links), default="")
    links_today = sorted([r for r in links if r["date"] == links_last], key=lambda r: (r.get("topic", ""), r.get("title", "")))

    ind_dates = sorted({r["date"] for r in indicators})[-60:]
    totals = []
    for d in ind_dates:
        day = [r for r in indicators if r["date"] == d]
        totals.append((d, sum(POINTS.get(str(r.get("status", "")).lower(), 0) for r in day), len(day) * 3))
    score, smax = (totals[-1][1], totals[-1][2]) if totals else (0, 0)
    change = totals[-1][1] - totals[-2][1] if len(totals) > 1 else None

    P = []
    a = P.append
    a("""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Baltic threat briefing</title>
<meta name="description" content="Daily fact-based briefing on Russia, NATO and the Baltic states, with warning indicators, a claim tracker and trends.">
<style>
:root{--bg:#f7f6f2;--panel:#ffffff;--fg:#1c1c1a;--muted:#6b6a64;--line:#e3e1da;--ok:#2e8b57;--warn:#c27c0e;--bad:#c9372c;--accent:#2f6fdf;--muted-bar:#cfcdc5;--grid:#ebe9e2}
@media (prefers-color-scheme:dark){:root{--bg:#1a1a18;--panel:#232321;--fg:#ecebe6;--muted:#a3a29b;--line:#3a3935;--ok:#5cc28a;--warn:#e3a640;--bad:#ef6a5e;--accent:#6b9cf5;--muted-bar:#4a4944;--grid:#33322e}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.55 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
.wrap{max-width:72rem;margin:0 auto;padding:24px 16px 64px}
h1{font-family:Georgia,"Times New Roman",serif;font-weight:400;font-size:clamp(2rem,5vw,2.8rem);line-height:1.15;margin:.3rem 0 .6rem}
h2{font-size:1.15rem;font-weight:600;margin:0 0 .25rem}h3{font-size:1rem;font-weight:600;margin:0}
.kicker{margin:0;font-size:.78rem;color:var(--muted);text-transform:uppercase;letter-spacing:.06em}
.lede{font-size:1.12rem;max-width:52rem;margin:0}.head{padding-bottom:1.5rem;border-bottom:1px solid var(--line);margin-bottom:1.5rem}
.sub{margin:0 0 1rem;color:var(--muted);font-size:.85rem;max-width:52rem}.card .sub{margin:.15rem 0 .6rem}
section{margin-top:2.6rem}.grid{display:grid;gap:16px;grid-template-columns:repeat(auto-fit,minmax(min(100%,18rem),1fr))}
.card{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:20px}.span{grid-column:1/-1}
.big{font-family:Georgia,serif;font-size:2.4rem;line-height:1.1;margin:0 0 .5rem}.of{font:1rem system-ui,sans-serif;color:var(--muted)}
.lv-quiet{color:var(--ok)}.lv-elevated{color:var(--warn)}.lv-high{color:var(--bad)}
.bottom{max-width:60rem;line-height:1.7;margin:0}
.scroll{overflow-x:auto;border:1px solid var(--line);border-radius:10px;background:var(--panel)}
table{width:100%;min-width:58rem;border-collapse:collapse;font-size:.85rem}th{text-align:left;font-weight:600;color:var(--muted);padding:10px 14px;border-bottom:1px solid var(--line);white-space:nowrap}
td{padding:10px 14px;border-bottom:1px solid var(--line);vertical-align:top}tr:last-child td{border-bottom:0}
td.strong{font-weight:600;font-size:.95rem;min-width:11rem}td.wide{min-width:18rem}td.muted{color:var(--muted);min-width:9rem}
.pill{display:inline-flex;align-items:center;gap:6px;white-space:nowrap;font-weight:600}.dot{width:.55rem;height:.55rem;border-radius:50%;display:inline-block;flex:none}
.s-quiet{background:var(--ok)}.s-watch{background:var(--muted)}.s-elevated{background:var(--warn)}.s-high{background:var(--bad)}
.t-rising,.t-new{color:var(--bad)}.t-easing{color:var(--ok)}
.verdict{display:inline-block;padding:1px 8px;border-radius:999px;border:1px solid var(--line);white-space:nowrap;font-weight:600}
.v-contested,.v-disputed,.v-unconfirmed{color:var(--warn)}.v-misleading,.v-unsupported,.v-false{color:var(--bad)}.v-likely,.v-confirmed{color:var(--ok)}
.stories{display:grid;gap:16px;grid-template-columns:repeat(auto-fit,minmax(min(100%,22rem),1fr))}
.story{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:20px;display:flex;flex-direction:column;gap:.6rem}
.story p{margin:0;font-size:.88rem}.tag{display:inline-block;padding:1px 8px;border-radius:999px;background:var(--bg);border:1px solid var(--line);font-size:.8rem}
.corr{color:var(--muted);font-size:.8rem}.take{border-left:2px solid var(--warn);padding-left:10px}
svg text{font-size:11px;fill:var(--muted);font-family:system-ui,sans-serif}svg .endlab{font-size:12px;font-weight:600}svg .grid{stroke:var(--grid);stroke-width:1}
.crow{display:grid;grid-template-columns:minmax(8rem,11rem) 1fr 2rem;gap:10px;align-items:center;font-size:.85rem;margin-bottom:8px}.cval{text-align:right;font-weight:600}
.legend{display:flex;flex-wrap:wrap;gap:14px;font-size:.8rem;color:var(--muted);margin-top:.6rem}.legend span{display:inline-flex;align-items:center;gap:6px}
.hist{overflow-x:auto}.hist table{min-width:0;width:auto}.hist td,.hist th{padding:3px;border:0;font-size:.78rem}.hist th{font-weight:400;text-align:center}
.hist td.lab{padding-right:12px;white-space:nowrap}.cell{display:block;width:2.4rem;height:1.3rem;border-radius:3px;background:var(--grid)}
.cell.s-quiet,.cell.s-watch{opacity:.6}
.links{list-style:none;margin:0;padding:0;display:grid;gap:12px;grid-template-columns:repeat(auto-fit,minmax(min(100%,22rem),1fr));font-size:.85rem}
.links a{color:var(--fg)}.ltopic{display:block;color:var(--muted)}.method li,.method p{font-size:.85rem}.method ul{padding-left:1.1rem;margin:.4rem 0 0}
footer{margin-top:3rem;color:var(--muted);font-size:.8rem}
</style></head><body><div class="wrap">""")
    a(f'<header class="head"><p class="kicker">Daily briefing · Russia, NATO and the Baltic states · {e(fmt_long(last))}</p>'
      f'<h1>Baltic threat briefing</h1><p class="lede">{e(ed.get("headline"))}</p></header>')
    a('<div class="grid">')
    a(f'<div class="card"><h3>Conventional attack risk</h3><p class="sub">Near term, judged from public indicators</p>'
      f'<p class="big lv-{level(ed.get("conventional"))}">{e(ed.get("conventional"))}</p><p style="margin:0">{e(ed.get("conventional_note"))}</p></div>')
    a(f'<div class="card"><h3>Hybrid activity</h3><p class="sub">Sabotage, jamming, drones and border pressure</p>'
      f'<p class="big lv-{level(ed.get("hybrid"))}">{e(ed.get("hybrid"))}</p><p style="margin:0">{e(ed.get("hybrid_note"))}</p></div>')
    a(f'<div class="card"><h3>What changed since yesterday</h3><p class="sub">New, rising or easing items only</p><p style="margin:0">{e(ed.get("changed"))}</p></div>')
    a("</div>")
    a(f'<section><h2>Critical assessment</h2><p class="sub">What the evidence supports, and where the coverage runs ahead of it.</p><p class="bottom">{e(ed.get("bottom_line"))}</p></section>')

    a('<section><h2>Warning indicators</h2><p class="sub">The physical and political signs that would come before an attack, rated from public reporting. When a sign is not reported, that does not prove it is absent.</p>'
      '<div class="scroll"><table><thead><tr><th>Indicator</th><th>Area</th><th>Status</th><th>Trend</th><th>What is being reported</th><th>Evidence behind it</th></tr></thead><tbody>')
    for r in ind_today:
        a(f'<tr><td class="strong">{e(r.get("indicator"))}</td><td class="muted">{e(r.get("group"))}</td>'
          f'<td><span class="pill"><i class="dot s-{level(r.get("status"))}"></i>{e(r.get("status"))}</span></td>'
          f'<td class="t-{slug(r.get("trend"))}">{e(r.get("trend"))}</td><td class="wide">{e(r.get("note"))}</td><td class="muted">{e(r.get("evidence"))}</td></tr>')
    a("</tbody></table></div></section>")

    a('<section><h2>Claim tracker</h2><p class="sub">Claims circulating today, who makes them, what backs them, and where sources contradict each other.</p>'
      '<div class="scroll"><table><thead><tr><th>Claim</th><th>Who says so</th><th>Evidence</th><th>What contradicts it</th><th>Verdict</th><th>Why</th></tr></thead><tbody>')
    for r in claims_today:
        a(f'<tr><td class="strong">{e(r.get("claim"))}</td><td class="muted">{e(r.get("claimed_by"))}</td><td class="muted">{e(r.get("evidence"))}</td>'
          f'<td class="wide">{e(r.get("conflict"))}</td><td><span class="verdict v-{slug(r.get("verdict"))}">{e(r.get("verdict"))}</span></td><td class="wide">{e(r.get("verdict_note"))}</td></tr>')
    a("</tbody></table></div></section>")

    a('<section><h2>Key reporting</h2><p class="sub">The stories that matter today, each with the type of evidence behind it and a critical take.</p><div class="stories">')
    for r in stories_today:
        a(f'<article class="story"><h3>{e(r.get("title"))}</h3><p><span class="tag">{e(r.get("evidence"))}</span> <span class="corr">{e(r.get("corroboration"))}</span></p>'
          f'<p>{e(r.get("summary"))}</p><p class="take"><b>Critical take.</b> {e(r.get("analysis"))}</p></article>')
    a("</div></section>")

    # Trends
    a('<section><h2>Trends over time</h2><p class="sub">These charts fill in as daily editions accumulate. They measure what gets reported, so a jump can mean more coverage rather than more activity.</p><div class="grid">')
    chg = ("First edition, so the lines start from today." if change is None
           else f'Change since the previous edition: <b class="{"lv-high" if change > 0 else "lv-quiet" if change < 0 else ""}">{"+" if change > 0 else ""}{change}</b>')
    a(f'<div class="card span"><h3>Threat score</h3><p class="sub">Indicator points per area: Quiet 0, Watch 1, Elevated 2, High 3. A rising logistics and medical line would be the most telling signal.</p>'
      f'<p class="big">{score}<span class="of"> of {smax}</span></p><p class="sub">{chg}</p>{score_chart(indicators, ind_dates) if ind_dates else ""}</div>')
    c_dates = sorted({r["date"] for r in counts})[-30:]
    a('<div class="card"><h3>Incidents reported per day</h3><p class="sub">New items first reported since the previous edition, last 30 days.</p>')
    if c_dates:
        ymax = max([1] + [int(r.get("value", 0) or 0) for r in counts if r["date"] in c_dates])
        for mrow in by_order([r for r in counts if r["date"] == c_dates[-1]]):
            pts = []
            for d in c_dates:
                hit = [r for r in counts if r["date"] == d and r.get("metric") == mrow.get("metric")]
                if hit:
                    pts.append((d, int(hit[0].get("value", 0) or 0), hit[0].get("note", "")))
            a(f'<div class="crow"><span>{e(mrow.get("metric"))}</span><span>{mini_bars(pts, ymax)}</span><span class="cval">{int(mrow.get("value", 0) or 0)}</span></div>')
    a("</div>")
    q_dates = sorted({r["date"] for r in claims})[-30:]
    a('<div class="card"><h3>Claim quality</h3><p class="sub">Claims checked each day by verdict. More open or rejected claims means a noisier information space.</p>')
    if q_dates:
        a(quality_chart(claims, q_dates))
    a('<div class="legend">' + "".join(f'<span><i class="dot" style="background:{QCOLORS[k]}"></i>{QLABELS[k]}</span>' for k in QLABELS) + "</div></div>")
    a("</div></section>")

    # History grid
    h_dates = sorted({r["date"] for r in indicators})[-21:]
    a('<section><h2>Indicator history</h2><p class="sub">Status of each indicator by day, so a slow build-up shows as a change in colour across the row.</p><div class="card hist"><table><thead><tr><th></th>')
    a("".join(f"<th>{e(fmt_short(d))}</th>" for d in h_dates) + "</tr></thead><tbody>")
    lookup = {(r["date"], r.get("indicator")): r for r in indicators}
    for ind in ind_today:
        a(f'<tr><td class="lab">{e(ind.get("indicator"))}</td>')
        for d in h_dates:
            r = lookup.get((d, ind.get("indicator")))
            cls = f" s-{level(r.get('status'))}" if r else ""
            tip = f'<title>{e(fmt_short(d))}: {e(r.get("status"))} · {e(r.get("trend"))}</title>' if r else ""
            a(f'<td><span class="cell{cls}" title="{e(fmt_short(d)) + ": " + e(r.get("status")) if r else ""}"></span></td>')
        a("</tr>")
    a('</tbody></table><div class="legend"><span><i class="dot s-quiet"></i>Quiet</span><span><i class="dot s-watch"></i>Watch</span>'
      '<span><i class="dot s-elevated"></i>Elevated</span><span><i class="dot s-high"></i>High</span></div></div></section>')

    # Sources
    persp = {}
    for r in links_today:
        persp[r.get("perspective")] = persp.get(r.get("perspective"), 0) + 1
    a(f'<section><h2>Sources</h2><p class="sub">Today\'s edition draws on {len(links_today)} sources from {len(persp)} perspectives: '
      + ", ".join(f"{e(k)} {v}" for k, v in sorted(persp.items(), key=lambda kv: -kv[1]))
      + '. Repeats of one wire story count once in the analysis, not many times.</p><ul class="links">')
    for r in links_today:
        url = str(r.get("url", ""))
        href = f' href="{e(url)}"' if url.startswith("https://") else ""
        a(f'<li><span class="ltopic">{e(r.get("topic"))} · {e(r.get("perspective"))}</span><a{href} target="_blank" rel="noopener noreferrer">{e(r.get("title"))}</a> — {e(r.get("outlet"))}</li>')
    a("</ul></section>")

    a("""<section class="method"><h2>How this briefing works</h2><div class="grid">
<div class="card"><h3>Source priority</h3><ul>
<li><b>Official and intelligence:</b> Baltic, Nordic, German, UK and US services, NATO and defence ministries.</li>
<li><b>Quality journalism:</b> Baltic broadcasters, Ukrainian outlets, Reuters, AP and major international papers.</li>
<li><b>Analysts and open-source investigators:</b> ISW, RUSI, satellite-imagery analysts and incident trackers.</li>
<li><b>The Russian side:</b> independent Russian outlets, plus state media to see the Kremlin's narrative.</li>
<li><b>Commentators and influencers:</b> included, always labelled as commentary rather than evidence.</li></ul></div>
<div class="card"><h3>Evidence labels</h3><ul>
<li><b>Official statement:</b> on the record, attributable.</li><li><b>Imagery or documents:</b> something you can inspect.</li>
<li><b>Anonymous sources:</b> credible outlet, not verifiable.</li><li><b>Unverified claim:</b> a single or partisan source.</li></ul>
<p>Many outlets repeating one wire report is one source, not many.</p></div>
<div class="card"><h3>Limits</h3><p>Built from the public web only: no dark-web, classified or paywalled material. Intelligence claims are reported as stated, not independently verified. Troop and logistics movements are only visible when someone publishes them, so a quiet indicator means nothing has been reported, not that nothing is happening. Not a substitute for official warnings from your government.</p></div>
</div></section>""")
    a(f'<footer>Compiled daily with Claude from public sources. Edition of {e(fmt_long(last))}. Previous editions are kept in this site\'s data files.</footer>')
    a("</div></body></html>")
    with open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8") as f:
        f.write("".join(P))
    print(f"Built index.html for {last}")


if __name__ == "__main__":
    main()
