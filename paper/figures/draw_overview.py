#!/usr/bin/env python3
"""Rebuild the architecture overview (architecture.svg / architecture.pdf).

Requires CairoSVG: python -m pip install cairosvg
Run: python paper/figures/draw_overview.py [preview.png]
All geometry and typography are in SVG; the PDF contains vector artwork.
"""
from html import escape
from pathlib import Path
import math
import sys

W, H = 2240, 960
OUT = Path(__file__).resolve().parent
INK = '#24364B'
MUTED = '#617083'
BORDER = '#B8C5D2'
BLUE = '#426D98'
TEAL = '#3D867A'
RUST = '#B87348'
RED = '#B65A61'
BLUE_BG = '#F1F5FA'
TEAL_BG = '#F0F7F5'
RED_BG = '#FCF1F2'
RUST_BG = '#FBF5EE'
KEY_BG = '#ECEFF3'
parts = []


def rect(x, y, w, h, fill='white', stroke=BORDER, radius=8, sw=1.6, dash=False):
    dashed = ' stroke-dasharray="6 4"' if dash else ''
    parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{dashed}/>')


def text(x, y, value, size=23, color=INK, weight=400, anchor='middle', raw=False, italic=False, keep_space=False):
    style = ' font-style="italic"' if italic else ''
    style += ' xml:space="preserve"' if keep_space else ''
    parts.append(f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="DejaVu Sans, sans-serif" font-size="{size}" font-weight="{weight}" fill="{color}"{style}>{value if raw else escape(value)}</text>')


def text_width(s, size, italic=False, bold=False):
    """Advance width as rendered by Cairo, which CairoSVG uses for export."""
    import cairocffi as cairo
    ctx = cairo.Context(cairo.ImageSurface(cairo.FORMAT_ARGB32, 1, 1))
    ctx.select_font_face('DejaVu Sans',
                         cairo.FONT_SLANT_ITALIC if italic else cairo.FONT_SLANT_NORMAL,
                         cairo.FONT_WEIGHT_BOLD if bold else cairo.FONT_WEIGHT_NORMAL)
    ctx.set_font_size(size)
    return ctx.text_extents(s)[4]


def mtext(x, y, segs, size=22, color=INK, weight=400, anchor='middle'):
    """Inline math from (string, kind) segments, one <text> per segment.

    kind: 'rm' upright, 'it' italic, 'sub'/'isub' upright/italic subscript,
    'sup' superscript. Segments are placed explicitly because Cairo does not
    honour text-anchor across shifted tspans.
    """
    small = size*0.68
    shift = {'sub': 0.28, 'isub': 0.28, 'ssub': 0.28, 'sup': -0.42}
    items = []
    for s, kind in segs:
        fs = small if kind in shift else size
        italic = kind in ('it', 'isub')
        w = text_width(s, fs, italic, weight >= 600)
        items.append((s, fs, italic, y + shift.get(kind, 0)*size, w, kind == 'ssub'))
    # 'ssub' is a subscript stacked under the preceding superscript.
    total, prev = 0, 0
    for *_, w, stacked in items:
        total = max(total, prev + w) if stacked else total + w
        prev = total - w if not stacked else prev
    cur = x - total/2 if anchor == 'middle' else x
    prev_start, end = cur, cur
    for s, fs, italic, yy, w, stacked in items:
        start = prev_start if stacked else end
        text(round(start, 1), round(yy, 1), s, round(fs, 1), color, weight, 'start', italic=italic, keep_space=True)
        prev_start, end = start, max(end, start + w)


def line(points, color=INK, sw=2, arrow=False, dash=False):
    coords = ' '.join(f'{x},{y}' for x, y in points)
    marker = f' marker-end="url(#{color[1:]})"' if arrow else ''
    dashed = ' stroke-dasharray="8 6"' if dash else ''
    parts.append(f'<polyline points="{coords}" fill="none" stroke="{color}" stroke-width="{sw}" stroke-linejoin="round" stroke-linecap="round"{marker}{dashed}/>')


def circle(x, y, r, fill='white', stroke=BLUE, sw=2):
    parts.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')


def panel(x, y, w, h, title, fill, color, size=32):
    rect(x, y, w, h, fill, BORDER, 14, 1.8)
    line([(x+22, y+61), (x+w-22, y+61)], color, 1.3)
    text(x+w/2, y+42, title, size, INK, 700)


def table(x, y, widths, headers, rows, colors=None, size=22, keys=(), row_colors=None):
    """Header plus value rows; columns in `keys` are key columns (drawn grey)."""
    h = 41 + 43*len(rows)
    rect(x, y, sum(widths), h, 'white', BORDER, 3)
    offset = x
    for i, (w, head) in enumerate(zip(widths, headers)):
        key = i in keys
        fill = KEY_BG if key else (colors or [BLUE_BG]*len(widths))[i]
        rect(offset+1, y+1, w-2, 39, fill, 'none', 0)
        if key:
            rect(offset+1, y+42, w-2, h-43, '#F7F8FA', 'none', 0)
        if i:
            line([(offset, y), (offset, y+h)], BORDER, 1.2)
        text(offset+w/2, y+27, head, size, MUTED if key else INK, 500, italic=key)
        for r, vals in enumerate(rows):
            val = vals[i]
            color = MUTED if key or val == '[masked]' else (row_colors or [INK]*len(rows))[r]
            text(offset+w/2, y+67+43*r, val, size, color, italic=key)
        offset += w
    for r in range(len(rows)):
        line([(x, y+41+43*r), (x+sum(widths), y+41+43*r)], BORDER, 1.2)


def grid_icon(x, y, size=48, race=False):
    color = INK if race else BLUE
    rect(x-size/2, y-size/2, size, size, 'white', color, 5, 2.3)
    step = (size-8)/4
    for r in range(4):
        for c in range(4):
            if race and (r+c) % 2 == 0:
                rect(x-size/2+4+c*step, y-size/2+4+r*step, step, step, color, 'none', 0)
    if not race:
        for i in range(1, 4):
            line([(x-size/2+i*size/4, y-size/2+2), (x-size/2+i*size/4, y+size/2-2)], color, 1.3)
            line([(x-size/2+2, y-size/2+i*size/4), (x+size/2-2, y-size/2+i*size/4)], color, 1.3)


def driver_icon(x, y, size=57):
    circle(x, y, size/2, '#FFF8EB', BLUE, 2.3)
    circle(x, y-8, size*.12, '#BC9652', 'none')
    parts.append(f'<path d="M {x-size*.23},{y+size*.22} Q {x-size*.23},{y-size*.01} {x},{y-size*.01} Q {x+size*.23},{y-size*.01} {x+size*.23},{y+size*.22} Z" fill="#BC9652"/>')


def schema_table(x, y, w, name, fields, task=False):
    color = RED if task else BLUE
    text(x+w/2, y-21, name, 24, color, 700)
    rect(x, y, w, 181, 'white', color, 4, 1.8)
    rect(x+1, y+1, w-2, 42, RED_BG if task else '#E7EEF6', 'none', 3)
    line([(x, y+43), (x+w, y+43)], color, 1)
    for i, value in enumerate(fields):
        text(x+w/2, y+29+i*42, value, 22, color if task else INK, 500 if i == 0 else 400)


def pair(a, b, ra, rb):
    """a is the child, b is the parent; preserve the FK direction."""
    dx, dy = b[0]-a[0], b[1]-a[1]
    d = math.hypot(dx, dy)
    ux, uy = dx/d, dy/d
    nx, ny = -uy*6, ux*6
    start = (a[0]+ux*ra, a[1]+uy*ra)
    end = (b[0]-ux*rb, b[1]-uy*rb)
    line([(start[0]+nx, start[1]+ny), (end[0]+nx, end[1]+ny)], INK, 2.4, True)
    line([(end[0]-nx, end[1]-ny), (start[0]-nx, start[1]-ny)], TEAL, 2.4, True)


def task_node(x, y, second, query=False):
    rect(x-50, y-29, 100, 58, RED_BG if query else 'white', RED, 5, 2.2)
    text(x, y-4, 'Task', 21, RED, 600)
    text(x, y+20, second, 17, RED if query else MUTED, 600 if query else 400)


def build():
    parts.clear()
    parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc">')
    parts.append('<title id="title">ReGRow architecture overview</title><desc id="desc">Context sampling feeds relation encoding and row initialization. The relation graph conditions bidirectional foreign-key messages in the row graph; earlier task rows send label edges to class nodes, and a shared MLP scores the query row against each class node.</desc><defs>')
    for color in [INK, BLUE, TEAL, RUST, RED]:
        parts.append(f'<marker id="{color[1:]}" viewBox="0 0 10 8" refX="9" refY="4" markerWidth="8" markerHeight="6.4" orient="auto-start-reverse"><path d="M0 0 L10 4 L0 8 Z" fill="{color}"/></marker>')
    parts.append('</defs>')
    rect(0, 0, W, H, 'white', 'none', 0)

    panel(20, 20, 660, 920, 'Context Sampling', '#F7F9FC', BLUE)
    panel(725, 20, 660, 440, 'Relation Encoding', TEAL_BG, TEAL)
    panel(1430, 20, 595, 440, 'RelationGraph', TEAL_BG, TEAL)
    panel(725, 520, 510, 420, 'Row Initialization', BLUE_BG, BLUE)
    panel(1270, 520, 715, 420, 'RowGraph', BLUE_BG, BLUE)
    panel(2015, 520, 205, 420, 'Prediction', '#F7F8FA', BLUE, 25)

    # Context: sampled schema, then the retained rows.
    rect(40, 104, 620, 370, 'white', BORDER, 9)
    text(350, 143, 'Sampled schema and context', 26, INK, 600)
    schema_table(59, 252, 111, 'Races', ['RaceId', 'Year', 'Name'])
    schema_table(210, 252, 132, 'Results', ['DriverId', 'RaceId', 'Rank', 'Laps'])
    schema_table(382, 252, 118, 'Drivers', ['DriverId', 'Dob', 'Code'])
    schema_table(540, 252, 104, 'Task', ['Time', 'DriverId', 'Label'], True)
    grid_icon(114, 187, 34, True)
    grid_icon(276, 187, 34)
    driver_icon(441, 187, 38)
    rect(577, 169, 30, 35, RED_BG, RED, 3)
    for yy in [180, 188, 196]:
        line([(583, yy), (601, yy)], RED, 1.5)
    line([(208, 326), (173, 326)], INK, 2.2, True)
    line([(344, 326), (379, 326)], INK, 2.2, True)
    line([(538, 326), (503, 326)], INK, 2.2, True)
    text(350, 459, 'FK references: child → parent', 21, MUTED)
    line([(350, 475), (350, 507)], INK, 2.6, True)
    rect(40, 512, 620, 406, 'white', BORDER, 9)
    text(350, 551, 'Sampled retained rows', 26, INK, 600)
    # Two earlier task rows with visible labels, then the query row.
    table(60, 570, [124, 182, 268], ['DriverId', 'date', 'did_not_finish'],
          [['1', '1999-11-28', '0'], ['1', '2000-01-30', '1'], ['1', '2000-02-27', '[masked]']],
          [RED_BG]*3, 22, keys=(0,), row_colors=[INK, INK, RED])
    table(60, 752, [124, 182, 50, 218], ['DriverId', 'DriverRef', '…', 'Nationality'],
          [['1', 'heidfeld', '…', 'Germany']], size=22, keys=(0,))
    rect(66, 857, 22, 18, KEY_BG, BORDER, 2, 1.2)
    text(98, 872, 'key column: becomes an FK edge, not a cell', 19, MUTED, anchor='start', italic=True)
    text(350, 905, '⋮', 30, MUTED)

    # Relation interaction patterns. The chain is an illustrative schema pattern.
    patterns = [
        (113, 'Shared child', BLUE, BLUE_BG, 'Results → Drivers', 'Results → Races', 'same FK-holding table'),
        (226, 'Shared parent', TEAL, TEAL_BG, 'Results → Drivers', 'Task → Drivers', 'same referenced table'),
        (339, 'Directed chain', RUST, RUST_BG, 'Results → Races', 'Races → Circuits', 'one relation continues into another'),
    ]
    for yy, title, color, fill, left, right, note in patterns:
        rect(746, yy, 618, 99, 'white', BORDER, 7)
        rect(758, yy+16, 185, 66, fill, 'none', 5)
        text(850.5, yy+56, title, 22, color, 600)
        text(1052, yy+37, left, 21, INK, 500)
        text(1255, yy+37, right, 21, INK, 500)
        text(1151, yy+76, note, 20, MUTED)

    # Relation graph: three relations and their interactions.
    rect(1568, 112, 310, 61, 'white', BLUE, 5, 2)
    text(1723, 150, 'Results → Drivers', 25, INK, 600)
    rect(1451, 338, 264, 63, 'white', BLUE, 5, 2)
    text(1583, 377, 'Results → Races', 23, INK, 600)
    rect(1766, 338, 237, 63, RED_BG, RED, 5, 2)
    text(1884.5, 377, 'Task → Drivers', 23, RED, 600)
    line([(1684, 179), (1581, 330)], BLUE, 2.6, True)
    line([(1600, 330), (1703, 179)], BLUE, 2.6, True)
    line([(1754, 179), (1860, 330)], TEAL, 2.6, True)
    line([(1879, 330), (1773, 179)], TEAL, 2.6, True)
    rect(1445, 232, 176, 38, TEAL_BG, 'none', 0)
    text(1533, 258, 'Shared child', 22, BLUE, 500)
    rect(1824, 232, 191, 38, TEAL_BG, 'none', 0)
    text(1919.5, 258, 'Shared parent', 22, TEAL, 500)
    text(1884, 430, 'query relation', 19, RED)

    # Row initialization (Eqs. cell and rowencoding) for one Drivers row:
    # non-key cells -> cell vectors -> mean||max pooling -> + time + query marker.
    text(915, 609, 'one Drivers row, non-key cells only', 19, MUTED, italic=True)
    table(745, 622, [150, 50, 160], ['DriverRef', '…', 'Nationality'],
          [['heidfeld', '…', 'Germany']], [TEAL_BG, '#F1F0F7', RUST_BG], 20)
    for cx in (820, 1025):
        line([(cx, 708), (cx, 730)], INK, 2, True)
        rect(cx-30, 733, 60, 34, 'white', BLUE, 6, 1.8)
        mtext(cx, 758, [('x', 'it'), ('n', 'isub')], 22)
    text(870, 757, '…', 22, MUTED)
    text(1068, 746, 'column name', 17, MUTED, anchor='start')
    text(1068, 767, '+ value', 17, MUTED, anchor='start')
    for x0, x1 in [(820, 880), (870, 912), (1025, 944)]:
        line([(x0, 769), (x1, 789)], INK, 2, True)
    rect(800, 792, 225, 46, 'white', BLUE, 9, 2)
    mtext(912.5, 822, [('W', 'it'), ('row', 'sub'), ('[ mean ‖ max ]', 'rm')], 20, INK, 600)
    line([(1027, 815), (1060, 815)], INK, 2.3, True)
    circle(1078, 815, 16, 'white', INK, 2)
    text(1078, 823, '+', 24, INK, 600)
    line([(1095, 815), (1130, 815)], INK, 2.3, True)
    circle(1172, 815, 39, 'white', BLUE, 2.2)
    text(1157, 826, '<tspan font-style="italic">h</tspan>', 33, INK, raw=True)
    text(1172, 836, '<tspan font-style="italic">r</tspan>', 20, INK, raw=True)
    text(1192, 805, '(0)', 18, INK)
    rect(950, 866, 110, 38, 'white', BLUE, 7, 1.8)
    mtext(1005, 892, [('ψ(Δ', 'rm'), ('r', 'isub'), (')', 'rm')], 20)
    rect(1086, 866, 112, 38, RED_BG, RED, 7, 1.8)
    mtext(1142, 892, [('e', 'rm'), ('⋆', 'sup'), ('row', 'ssub')], 20, RED, 600)
    line([(1030, 864), (1067, 829)], INK, 2, True)
    line([(1120, 864), (1089, 830)], INK, 2, True)
    text(1005, 927, 'relative time', 17, MUTED)
    text(1142, 927, 'query row only', 17, MUTED)

    # Row graph: database rows on the left, task rows and class nodes on the right.
    race1, race2 = (1335, 655), (1335, 805)
    res1, res2 = (1470, 655), (1470, 805)
    driver = (1615, 730)
    query, hist0, hist1 = (1770, 640), (1770, 735), (1770, 830)
    cls0, cls1 = (1925, 735), (1925, 830)
    pair(res1, race1, 33, 33)
    pair(res2, race2, 33, 33)
    pair(res1, driver, 33, 40)
    pair(res2, driver, 33, 40)
    pair(query, driver, 52, 40)
    pair(hist0, driver, 52, 40)
    pair(hist1, driver, 52, 40)
    line([(1822, 735), (1893, 735)], RUST, 2.6, True)
    line([(1822, 830), (1893, 830)], RUST, 2.6, True)
    for pos in [race1, race2]:
        grid_icon(*pos, 50, True)
    for pos in [res1, res2]:
        grid_icon(*pos, 50)
    driver_icon(*driver, 72)
    text(1335, 615, 'Races', 20, MUTED)
    text(1470, 615, 'Results', 20, MUTED)
    text(1615, 682, 'Drivers', 20, MUTED)
    task_node(*query, 'query', True)
    task_node(*hist0, 'label 0')
    task_node(*hist1, 'label 1')
    for (cx, cy), j in [(cls0, '0'), (cls1, '1')]:
        circle(cx, cy, 29, RUST_BG, RUST, 2.3)
        mtext(cx-2, cy+9, [('c', 'it'), (j, 'sub')], 26)
    text(1915, 690, 'class nodes', 18, RUST, 600)
    line([(1290, 909), (1331, 909)], INK, 2.4, True)
    text(1341, 916, 'f → p', 20, INK, anchor='start')
    line([(1430, 909), (1471, 909)], TEAL, 2.4, True)
    text(1481, 916, 'p → f', 20, TEAL, anchor='start')
    line([(1570, 909), (1611, 909)], RUST, 2.4, True)
    text(1621, 916, 'label', 20, RUST, anchor='start')

    # Main flow arrows, kept outside the panels.
    line([(681, 305), (722, 305)], INK, 3, True)
    line([(681, 748), (722, 748)], INK, 3, True)
    line([(1386, 249), (1427, 249)], INK, 3, True)
    line([(1236, 815), (1267, 815)], INK, 3, True)
    line([(1726, 461), (1726, 517)], TEAL, 3, True, True)
    rect(1461, 475, 530, 29, 'white', 'none', 0)
    text(1726, 497, 'relation-conditioned FK messages', 24, TEAL, 500)
    line([(1986, 735), (2012, 735)], INK, 3, True)

    # Prediction (Eq. readout): one shared MLP scores the query against each class node.
    for yy, j in [(598, '0'), (642, '1')]:
        rect(2030, yy, 175, 38, 'white', BORDER, 6, 1.6)
        mtext(2117.5, yy+26, [('[', 'rm'), ('h', 'it'), ('q', 'isub'), (' ‖ ', 'rm'), ('h', 'it'),
                             ('c' + '₀₁'[int(j)], 'isub'), (']', 'rm')], 20)
    line([(2117, 682), (2117, 704)], INK, 2.5, True)
    rect(2040, 707, 155, 48, 'white', BLUE, 7, 2)
    text(2117.5, 738, 'shared MLP', 20, INK, 600)
    line([(2117, 757), (2117, 781)], INK, 2.5, True)
    mtext(2130, 776, [('s', 'it'), ('0', 'sub'), (', ', 'rm'), ('s', 'it'), ('1', 'sub')], 18, MUTED, anchor='start')
    rect(2035, 784, 165, 42, 'white', BLUE, 7, 2)
    mtext(2117.5, 812, [('σ(', 'rm'), ('s', 'it'), ('1', 'sub'), (' − ', 'rm'), ('s', 'it'), ('0', 'sub'), (')', 'rm')], 20)
    line([(2117, 828), (2117, 852)], INK, 2.5, True)
    circle(2117, 885, 30, 'white', BLUE, 2)
    text(2117, 896, 'ŷ', 34, INK)
    parts.append('</svg>')
    return '\n'.join(parts)


if __name__ == '__main__':
    import cairosvg

    svg = build()
    # Preserve the previous assets once.
    for ext in ('svg', 'pdf'):
        old, backup = OUT / f'architecture.{ext}', OUT / f'architecture_previous.{ext}'
        if old.exists() and not backup.exists():
            backup.write_bytes(old.read_bytes())
    (OUT / 'architecture.svg').write_text(svg, encoding='utf-8')
    cairosvg.svg2pdf(bytestring=svg.encode(), write_to=str(OUT / 'architecture.pdf'))
    if len(sys.argv) > 1:
        cairosvg.svg2png(bytestring=svg.encode(), write_to=sys.argv[1], scale=2)
    print('Exported architecture.svg and architecture.pdf')
