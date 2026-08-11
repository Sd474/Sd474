import math, datetime

BG, GRID_F, GRID_C = "#050d1a", "#123456", "#1b4f80"
LINE, DIM, HOT, TXT = "#7dd3fc", "#4a7ba7", "#22d3ee", "#a8cbe8"
W, H = 1400, 700
F = "Fira Code,DejaVu Sans Mono,Consolas,monospace"

def t(x, y, s, size=11, fill=TXT, anchor="start", ls=1.2, op=1, weight=400):
    s = str(s).replace("&","&amp;").replace("<","&lt;")
    return (f'<text x="{x}" y="{y}" font-family="{F}" font-size="{size}" fill="{fill}" '
            f'text-anchor="{anchor}" letter-spacing="{ls}" opacity="{op}" font-weight="{weight}">{s}</text>')

def dim_h(x1, x2, y, label, up=6):
    """Horizontal dimension line with end ticks."""
    return (f'<g stroke="{DIM}" stroke-width="0.8">'
            f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}"/>'
            f'<line x1="{x1}" y1="{y-4}" x2="{x1}" y2="{y+4}"/>'
            f'<line x1="{x2}" y1="{y-4}" x2="{x2}" y2="{y+4}"/></g>'
            + t((x1+x2)/2, y-up, label, 9.5, DIM, "middle", 1.6))

def leader(x1, y1, x2, y2, label, anchor="start"):
    """Callout leader with a dot at the target."""
    return (f'<g stroke="{DIM}" stroke-width="0.8" fill="none">'
            f'<path d="M {x1} {y1} L {x2} {y2} l {18 if anchor=="start" else -18} 0"/></g>'
            f'<circle cx="{x1}" cy="{y1}" r="2.2" fill="{HOT}"/>'
            + t(x2 + (23 if anchor=="start" else -23), y2+3.4, label, 9.5, TXT, anchor, 1.4))

def build(d):
    g = []
    # ---- grid ----
    fine = "".join(f'<line x1="{x}" y1="0" x2="{x}" y2="{H}"/>' for x in range(0, W, 20)) + \
           "".join(f'<line x1="0" y1="{y}" x2="{W}" y2="{y}"/>' for y in range(0, H, 20))
    coarse = "".join(f'<line x1="{x}" y1="0" x2="{x}" y2="{H}"/>' for x in range(0, W, 100)) + \
             "".join(f'<line x1="0" y1="{y}" x2="{W}" y2="{y}"/>' for y in range(0, H, 100))
    g.append(f'<g stroke="{GRID_F}" stroke-width="0.45" opacity="0.5">{fine}</g>')
    g.append(f'<g stroke="{GRID_C}" stroke-width="0.7" opacity="0.5">{coarse}</g>')
    # ---- frame ----
    g.append(f'<rect x="18" y="18" width="{W-36}" height="{H-36}" fill="none" stroke="{LINE}" stroke-width="1.3" opacity="0.75"/>')
    g.append(f'<rect x="26" y="26" width="{W-52}" height="{H-52}" fill="none" stroke="{LINE}" stroke-width="0.5" opacity="0.4"/>')
    for cx, cy in ((18,18),(W-18,18),(18,H-18),(W-18,H-18)):
        sx = 1 if cx < W/2 else -1; sy = 1 if cy < H/2 else -1
        g.append(f'<path d="M {cx} {cy+sy*34} L {cx} {cy} L {cx+sx*34} {cy}" stroke="{HOT}" stroke-width="2" fill="none"/>')

    # ---- header strip ----
    g.append(t(46, 62, "SOUMIK  DEY", 30, LINE, ls=7, weight=700))
    g.append(t(48, 84, "MACHINE LEARNING ENGINEERING  /  DATA SYSTEMS", 10, DIM, ls=3.4))
    g.append(f'<line x1="46" y1="96" x2="640" y2="96" stroke="{LINE}" stroke-width="0.9" opacity="0.6"/>')
    g.append(t(W-46, 62, "FIG. 01 — SYSTEM OVERVIEW", 11, DIM, "end", 2.6))
    g.append(t(W-46, 82, f"GENERATED {datetime.date.today().isoformat()}", 9.5, DIM, "end", 2))

    # ---- main figure: pipeline schematic ----
    stages = [("IN","INGEST",180),("TF","TRANSFORM",420),("FE","FEATURE",660),("ML","MODEL",900),("SV","SERVE",1140)]
    ay = 250
    for i,(code,name,x) in enumerate(stages):
        g.append(f'<rect x="{x-62}" y="{ay-42}" width="124" height="84" fill="none" stroke="{LINE}" stroke-width="1.2"/>')
        g.append(f'<rect x="{x-56}" y="{ay-36}" width="112" height="72" fill="{HOT}" opacity="0.05"/>')
        g.append(f'<line x1="{x-62}" y1="{ay-20}" x2="{x+62}" y2="{ay-20}" stroke="{LINE}" stroke-width="0.7" opacity="0.6"/>')
        g.append(t(x, ay-27, code, 9.5, DIM, "middle", 2.4))
        g.append(t(x, ay+6, name, 12.5, LINE, "middle", 2.2, weight=600))
        g.append(t(x, ay+26, f"[{i+1:02d}]", 9, DIM, "middle", 1.8))
        if i < len(stages)-1:
            nx = stages[i+1][2]
            g.append(f'<line x1="{x+62}" y1="{ay}" x2="{nx-62}" y2="{ay}" stroke="{LINE}" stroke-width="1" opacity="0.7"/>')
            g.append(f'<path d="M {nx-72} {ay-4.5} L {nx-62} {ay} L {nx-72} {ay+4.5} Z" fill="{LINE}" opacity="0.8"/>')
            g.append(f'<circle r="3.4" fill="{HOT}"><animateMotion path="M {x+62} {ay} L {nx-62} {ay}" '
                     f'dur="2.6s" begin="{i*0.5}s" repeatCount="indefinite"/>'
                     f'<animate attributeName="opacity" values="0;1;1;0" dur="2.6s" begin="{i*0.5}s" repeatCount="indefinite"/></circle>')
    g.append(dim_h(118, 1202, 178, f"FULL PIPELINE — {d['repos']} REPOSITORIES"))
    g.append(leader(180, 208, 150, 148, "SOURCE", "start"))
    g.append(leader(900, 292, 940, 350, "INFERENCE", "start"))

    # ---- contribution punch strip ----
    sy = 400
    g.append(t(46, sy-14, "SECT. A—A   CONTRIBUTION RECORD, TRAILING 52 WEEKS", 10, DIM, ls=2.6))
    cw, ch, gap = 22, 8, 1.8
    weeks = [d['counts'][i:i+7] for i in range(0, len(d['counts']), 7)]
    mx = max(d['counts']) or 1
    for wi, wk in enumerate(weeks[:53]):
        for di, c in enumerate(wk):
            x = 46 + wi*(cw*0.395)
            y = sy + di*(ch+gap)
            o = 0.08 + 0.86*(c/mx)**0.6 if c else 0.06
            g.append(f'<rect x="{x:.1f}" y="{y}" width="8.2" height="{ch}" fill="{HOT if c else DIM}" opacity="{o:.3f}"/>')
    g.append(f'<line x1="46" y1="{sy+70}" x2="{46+53*cw*0.395:.0f}" y2="{sy+70}" stroke="{DIM}" stroke-width="0.7"/>')
    g.append(dim_h(46, 46+53*cw*0.395, sy+88, f"{d['total']} CONTRIBUTIONS / {d['active']} ACTIVE DAYS"))

    # ---- materials table (languages) ----
    tx, ty = 600, sy-14
    g.append(t(tx, ty, "BILL OF MATERIALS", 10, DIM, ls=2.6))
    g.append(f'<line x1="{tx}" y1="{ty+8}" x2="{tx+380}" y2="{ty+8}" stroke="{LINE}" stroke-width="0.8" opacity="0.6"/>')
    for i,(name, col, pct) in enumerate(d['langs'][:5]):
        y = ty + 30 + i*24
        g.append(t(tx, y, f"{i+1:02d}", 9.5, DIM, ls=1.4))
        g.append(t(tx+30, y, name.upper()[:18], 10.5, TXT, ls=1.6))
        bw = 138*pct/100
        g.append(f'<rect x="{tx+190}" y="{y-8}" width="138" height="9" fill="none" stroke="{DIM}" stroke-width="0.6"/>')
        g.append(f'<rect x="{tx+190}" y="{y-8}" width="0" height="9" fill="{col}" opacity="0.85">'
                 f'<animate attributeName="width" values="0;{bw:.1f}" dur="1.1s" begin="{0.4+i*0.16}s" fill="freeze"/></rect>')
        g.append(t(tx+380, y, f"{pct:.1f}%", 9.5, DIM, "end", 1.2))

    # ---- stat callouts ----
    px, py = 1000, sy-14
    g.append(t(px, py, "OPERATING DATA", 10, DIM, ls=2.6))
    g.append(f'<line x1="{px}" y1="{py+8}" x2="{px+336}" y2="{py+8}" stroke="{LINE}" stroke-width="0.8" opacity="0.6"/>')
    rows = [("COMMITS", d['commits']), ("PULL REQUESTS", d['prs']), ("ISSUES", d['issues']),
            ("LONGEST STREAK", f"{d['best']} d"), ("PEAK DAY", f"{d['busiest']} c"), ("ACTIVE SINCE", d['since'])]
    for i,(k,v) in enumerate(rows):
        y = py + 30 + i*24
        g.append(t(px, y, k, 10, DIM, ls=1.6))
        g.append(f'<line x1="{px+150}" y1="{y-3}" x2="{px+272}" y2="{y-3}" stroke="{DIM}" stroke-width="0.5" stroke-dasharray="2 3" opacity="0.6"/>')
        g.append(t(px+336, y, v, 11.5, HOT, "end", 1.4, weight=600))

    # ---- title block ----
    bx, by, bw2, bh = W-486, H-104, 440, 78
    g.append(f'<rect x="{bx}" y="{by}" width="{bw2}" height="{bh}" fill="none" stroke="{LINE}" stroke-width="1.1"/>')
    for fx in (bx+150, bx+272, bx+352):
        g.append(f'<line x1="{fx}" y1="{by}" x2="{fx}" y2="{by+bh}" stroke="{LINE}" stroke-width="0.6" opacity="0.7"/>')
    g.append(f'<line x1="{bx}" y1="{by+40}" x2="{bx+bw2}" y2="{by+40}" stroke="{LINE}" stroke-width="0.6" opacity="0.7"/>')
    cells = [(bx+10, by+16, "DRAWN BY", "S. DEY"), (bx+160, by+16, "DWG NO.", "SD-474"),
             (bx+282, by+16, "REV", "02"), (bx+362, by+16, "SHEET", "1/1"),
             (bx+10, by+56, "TITLE", "PROFILE OVERVIEW"), (bx+282, by+56, "SCALE", "1:1"),
             (bx+362, by+56, "UNITS", "COMMITS")]
    for cx, cy, k, v in cells:
        g.append(t(cx, cy-6, k, 7.5, DIM, ls=1.4))
        g.append(t(cx, cy+8, v, 10.5, LINE, ls=1.4, weight=600))
    g.append(t(46, H-46, "BRING ME YOUR WEIRD DISTRIBUTIONS", 10, DIM, ls=4.2))

    grain = ('<filter id="grain" x="0" y="0" width="100%" height="100%">'
             '<feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="3" stitchTiles="stitch"/>'
             '<feColorMatrix type="saturate" values="0"/></filter>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Blueprint schematic of GitHub activity">
<defs>{grain}</defs>
<rect width="{W}" height="{H}" fill="{BG}"/>
{"".join(g)}
<rect width="{W}" height="{H}" filter="url(#grain)" opacity="0.055" style="mix-blend-mode:overlay" pointer-events="none"/>
</svg>'''
