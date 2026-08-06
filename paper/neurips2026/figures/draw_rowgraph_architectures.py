#!/usr/bin/env python3
"""Generate paper-style architecture diagrams for RowGraph-Base and RelGraph.

The diagrams are intentionally drawn from primitives instead of relying on a
diagramming package, so the SVG and high-resolution PNG remain reproducible in
the repository's lightweight environment.
"""

from __future__ import annotations

import html
import math
from dataclasses import dataclass, field
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


W, H = 2300, 1150
SCALE = 2
OUT = Path(__file__).resolve().parent

NAVY = "#17263F"
TEXT = "#34445F"
MUTED = "#68758A"
LIGHT = "#F7F9FC"
BORDER = "#D8E0EA"
BLUE = "#3974B9"
BLUE_BG = "#EEF5FC"
TEAL = "#159487"
TEAL_BG = "#EAF7F4"
PURPLE = "#7854B3"
PURPLE_BG = "#F5F0FA"
ORANGE = "#E38428"
ORANGE_BG = "#FFF5E7"
GREEN = "#32956D"
GREEN_BG = "#EAF7F0"
RED = "#C95E51"
RED_BG = "#FFF0ED"
WHITE = "#FFFFFF"


def _font_path(bold: bool = False, italic: bool = False) -> str:
    base = Path("/usr/share/fonts/truetype/dejavu")
    name = "DejaVuSans"
    if bold and italic:
        name += "-BoldOblique"
    elif bold:
        name += "-Bold"
    elif italic:
        name += "-Oblique"
    return str(base / f"{name}.ttf")


@dataclass
class Shape:
    kind: str
    args: tuple
    kw: dict = field(default_factory=dict)


class Canvas:
    def __init__(self, title: str):
        self.title = title
        self.shapes: list[Shape] = []

    def rect(self, x, y, w, h, *, fill=WHITE, stroke=BORDER, sw=2, r=18):
        self.shapes.append(Shape("rect", (x, y, w, h), dict(fill=fill, stroke=stroke, sw=sw, r=r)))

    def circle(self, x, y, r, *, fill=WHITE, stroke=BLUE, sw=3):
        self.shapes.append(Shape("circle", (x, y, r), dict(fill=fill, stroke=stroke, sw=sw)))

    def diamond(self, x, y, rx, ry, *, fill=WHITE, stroke=PURPLE, sw=3):
        self.shapes.append(Shape("diamond", (x, y, rx, ry), dict(fill=fill, stroke=stroke, sw=sw)))

    def line(self, pts, *, color=MUTED, sw=3, arrow=True, dash=None):
        self.shapes.append(Shape("line", (tuple(pts),), dict(color=color, sw=sw, arrow=arrow, dash=dash)))

    def text(self, x, y, s, *, size=22, color=TEXT, bold=False, italic=False,
             anchor="middle"):
        self.shapes.append(Shape("text", (x, y, s), dict(size=size, color=color, bold=bold,
                                                          italic=italic, anchor=anchor)))

    def save(self, stem: str):
        self._save_svg(OUT / f"{stem}.svg")
        self._save_png(OUT / f"{stem}.png")

    def _save_svg(self, path: Path):
        marker_colors = sorted({s.kw["color"] for s in self.shapes if s.kind == "line" and s.kw["arrow"]})
        marker_ids = {c: f"arr{i}" for i, c in enumerate(marker_colors)}
        out = [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
            "<defs>",
            '<filter id="shadow" x="-20%" y="-20%" width="140%" height="140%">'
            '<feDropShadow dx="0" dy="3" stdDeviation="5" flood-color="#17263F" flood-opacity="0.10"/>'
            "</filter>",
        ]
        for color, mid in marker_ids.items():
            out.append(
                f'<marker id="{mid}" viewBox="0 0 10 10" refX="8" refY="5" '
                'markerWidth="8" markerHeight="8" orient="auto-start-reverse">'
                f'<path d="M0,0 L10,5 L0,10 Z" fill="{color}"/></marker>'
            )
        out += ["</defs>", f'<rect width="{W}" height="{H}" fill="{WHITE}"/>']
        for s in self.shapes:
            if s.kind == "rect":
                x, y, w, h = s.args
                k = s.kw
                out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{k["r"]}" '
                           f'fill="{k["fill"]}" stroke="{k["stroke"]}" stroke-width="{k["sw"]}"/>')
            elif s.kind == "circle":
                x, y, r = s.args
                k = s.kw
                out.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{k["fill"]}" '
                           f'stroke="{k["stroke"]}" stroke-width="{k["sw"]}"/>')
            elif s.kind == "diamond":
                x, y, rx, ry = s.args
                k = s.kw
                pts = f"{x},{y-ry} {x+rx},{y} {x},{y+ry} {x-rx},{y}"
                out.append(f'<polygon points="{pts}" fill="{k["fill"]}" stroke="{k["stroke"]}" '
                           f'stroke-width="{k["sw"]}"/>')
            elif s.kind == "line":
                pts, = s.args
                k = s.kw
                p = " ".join(f"{x},{y}" for x, y in pts)
                dash = f' stroke-dasharray="{k["dash"]}"' if k["dash"] else ""
                marker = f' marker-end="url(#{marker_ids[k["color"]]})"' if k["arrow"] else ""
                out.append(f'<polyline points="{p}" fill="none" stroke="{k["color"]}" '
                           f'stroke-width="{k["sw"]}" stroke-linecap="round" '
                           f'stroke-linejoin="round"{dash}{marker}/>' )
            elif s.kind == "text":
                x, y, value = s.args
                k = s.kw
                weight = "700" if k["bold"] else "400"
                style = "italic" if k["italic"] else "normal"
                anchor = {"left": "start", "right": "end"}.get(k["anchor"], "middle")
                out.append(f'<text x="{x}" y="{y}" text-anchor="{anchor}" '
                           f'font-family="DejaVu Sans, Arial, sans-serif" font-size="{k["size"]}" '
                           f'font-weight="{weight}" font-style="{style}" fill="{k["color"]}">'
                           f'{html.escape(value)}</text>')
        out.append("</svg>")
        path.write_text("\n".join(out), encoding="utf-8")

    def _save_png(self, path: Path):
        im = Image.new("RGB", (W * SCALE, H * SCALE), WHITE)
        d = ImageDraw.Draw(im)
        font_cache = {}

        def font(size, bold=False, italic=False):
            key = (size, bold, italic)
            if key not in font_cache:
                font_cache[key] = ImageFont.truetype(_font_path(bold, italic), size * SCALE)
            return font_cache[key]

        def xy(v):
            return tuple(int(round(z * SCALE)) for z in v)

        for s in self.shapes:
            if s.kind == "rect":
                x, y, w, h = s.args
                k = s.kw
                d.rounded_rectangle(xy((x, y, x + w, y + h)), radius=k["r"] * SCALE,
                                    fill=k["fill"], outline=k["stroke"], width=k["sw"] * SCALE)
            elif s.kind == "circle":
                x, y, r = s.args
                k = s.kw
                d.ellipse(xy((x-r, y-r, x+r, y+r)), fill=k["fill"], outline=k["stroke"],
                          width=k["sw"] * SCALE)
            elif s.kind == "diamond":
                x, y, rx, ry = s.args
                k = s.kw
                d.polygon([xy((x, y-ry)), xy((x+rx, y)), xy((x, y+ry)), xy((x-rx, y))],
                          fill=k["fill"], outline=k["stroke"], width=k["sw"] * SCALE)
            elif s.kind == "line":
                pts, = s.args
                k = s.kw
                pix = [xy(p) for p in pts]
                if k["dash"]:
                    self._draw_dashed(d, pix, k["color"], k["sw"] * SCALE)
                else:
                    d.line(pix, fill=k["color"], width=k["sw"] * SCALE, joint="curve")
                if k["arrow"] and len(pix) >= 2:
                    self._draw_arrowhead(d, pix[-2], pix[-1], k["color"], 12 * SCALE)
            elif s.kind == "text":
                x, y, value = s.args
                k = s.kw
                f = font(k["size"], k["bold"], k["italic"])
                anchor = {"left": "lm", "right": "rm"}.get(k["anchor"], "mm")
                d.text(xy((x, y)), value, font=f, fill=k["color"], anchor=anchor)
        im.save(path, dpi=(300, 300), optimize=True)
        im.save(path.with_suffix(".pdf"), "PDF", resolution=300.0)

    @staticmethod
    def _draw_arrowhead(draw, p0, p1, color, size):
        dx, dy = p1[0] - p0[0], p1[1] - p0[1]
        length = max(math.hypot(dx, dy), 1)
        ux, uy = dx / length, dy / length
        px, py = -uy, ux
        base = (p1[0] - ux * size, p1[1] - uy * size)
        pts = [p1, (base[0] + px * size * 0.48, base[1] + py * size * 0.48),
               (base[0] - px * size * 0.48, base[1] - py * size * 0.48)]
        draw.polygon(pts, fill=color)

    @staticmethod
    def _draw_dashed(draw, pts, color, width):
        for a, b in zip(pts, pts[1:]):
            dx, dy = b[0]-a[0], b[1]-a[1]
            length = max(math.hypot(dx, dy), 1)
            ux, uy = dx/length, dy/length
            pos = 0.0
            while pos < length:
                end = min(pos + 18, length)
                draw.line([(a[0]+ux*pos, a[1]+uy*pos), (a[0]+ux*end, a[1]+uy*end)],
                          fill=color, width=width)
                pos += 30


def heading(c: Canvas, label: str, title: str, x: int, y: int):
    c.circle(x, y-7, 20, fill=NAVY, stroke=NAVY, sw=1)
    c.text(x, y-6, label, size=18, color=WHITE, bold=True)
    c.text(x+34, y, title, size=23, color=NAVY, bold=True, anchor="left")


def badge(c: Canvas, x, y, w, text, *, fill=NAVY, color=WHITE):
    c.rect(x, y, w, 36, fill=fill, stroke=fill, sw=1, r=18)
    c.text(x+w/2, y+19, text, size=17, color=color, bold=True)


def node(c: Canvas, x, y, label, *, seed=False, small=False):
    r = 38 if small else 46
    c.circle(x, y, r, fill=ORANGE_BG if seed else WHITE,
             stroke=ORANGE if seed else BLUE, sw=5 if seed else 4)
    c.text(x, y+1, label, size=23 if not small else 19, color=NAVY,
           bold=seed, italic=not seed)


def candidate(c: Canvas, x, y, label, sublabel):
    c.diamond(x, y, 46, 40, fill=PURPLE_BG, stroke=PURPLE, sw=4)
    c.text(x, y-1, label, size=21, color=NAVY, italic=True)
    if sublabel:
        c.text(x, y+58, sublabel, size=15, color=MUTED)


def mini_table(c: Canvas, x, y, w, h, title, *, seed=False, rows=2):
    c.rect(x, y, w, h, fill=WHITE, stroke=ORANGE if seed else "#8494AA", sw=3, r=10)
    c.rect(x, y, w, 38, fill=ORANGE_BG if seed else "#EAF0F7",
           stroke=ORANGE if seed else "#8494AA", sw=2, r=10)
    c.text(x+w/2, y+21, title, size=18, color=NAVY, bold=True)
    top = y + 52
    for rr in range(rows):
        cy = top + rr*38
        for cc in range(3):
            fill = RED_BG if seed and rr == 0 and cc == 2 else LIGHT
            stroke = RED if seed and rr == 0 and cc == 2 else BORDER
            c.rect(x+12+cc*(w-30)/3, cy, (w-42)/3, 27, fill=fill, stroke=stroke, sw=1, r=4)
    if seed:
        c.text(x+w-27, top+15, "?", size=20, color=RED, bold=True)


def type_cells(c: Canvas, x, y):
    specs = [("num", BLUE_BG, BLUE), ("text", PURPLE_BG, PURPLE),
             ("time", TEAL_BG, TEAL), ("bool", ORANGE_BG, ORANGE)]
    for i, (lab, fill, stroke) in enumerate(specs):
        c.rect(x+i*70, y, 60, 42, fill=fill, stroke=stroke, sw=2, r=9)
        c.text(x+i*70+30, y+22, lab, size=15, color=TEXT)


def draw_init_panel(c: Canvas, x0: int, width: int):
    heading(c, "b", "Row initialization", x0+24, 92)
    c.text(x0+width/2, 142, "column name  +  typed value", size=18, color=MUTED)
    type_cells(c, x0+30, 166)
    for xx in (x0+60, x0+130, x0+200, x0+270):
        c.line([(xx, 210), (x0+width/2, 255)], color="#8B98AA", sw=2, arrow=True)
    c.circle(x0+width/2-46, 286, 38, fill=WHITE, stroke=BLUE, sw=3)
    c.circle(x0+width/2+46, 286, 38, fill=WHITE, stroke=BLUE, sw=3)
    c.text(x0+width/2-46, 287, "mean", size=17, italic=True)
    c.text(x0+width/2+46, 287, "max", size=17, italic=True)
    c.line([(x0+width/2-20, 316), (x0+width/2, 342)], color=MUTED, sw=3)
    c.line([(x0+width/2+20, 316), (x0+width/2, 342)], color=MUTED, sw=3)
    c.rect(x0+54, 344, width-108, 48, fill="#EAF0F7", stroke="#8292A8", sw=2, r=22)
    c.text(x0+width/2, 369, "Linear(mean || max)", size=17, color=NAVY, bold=True)
    c.line([(x0+width/2, 393), (x0+width/2, 442)], color=MUTED, sw=3)
    c.text(x0+40, 425, "relative time", size=15, color=PURPLE, anchor="left")
    c.line([(x0+118, 430), (x0+width/2-44, 456)], color=PURPLE, sw=2)
    c.text(x0+width-38, 425, "seed marker", size=15, color=ORANGE, anchor="right")
    c.line([(x0+width-92, 430), (x0+width/2+38, 455)], color=ORANGE, sw=2)
    node(c, x0+width/2, 482, "h_r^0", small=True)
    c.text(x0+width/2, 548, "one vector per retained row", size=16, color=MUTED)
    c.text(x0+width/2, 610, "Classification candidates", size=20, color=NAVY, bold=True)
    c.circle(x0+84, 657, 21, fill=WHITE, stroke="#8292A8", sw=2)
    c.circle(x0+width-84, 657, 21, fill=WHITE, stroke="#8292A8", sw=2)
    c.text(x0+84, 658, "0", size=18, italic=True)
    c.text(x0+width-84, 658, "1", size=18, italic=True)
    c.line([(x0+84, 679), (x0+84, 720)], color=MUTED, sw=2)
    c.line([(x0+width-84, 679), (x0+width-84, 720)], color=MUTED, sw=2)
    candidate(c, x0+84, 755, "c_0", "")
    candidate(c, x0+width-84, 755, "c_1", "")
    c.text(x0+84, 812, "False", size=15, color=MUTED)
    c.text(x0+width-84, 812, "True", size=15, color=MUTED)


def draw_context_panel(c: Canvas, x0: int, width: int):
    heading(c, "a", "Sampled context", x0+24, 92)
    c.rect(x0+12, 130, width-24, 716, fill=LIGHT, stroke="#9BB1CD", sw=2, r=26)
    # Position tables relative to the panel edges so narrower variants never
    # let Task or Races protrude beyond the sampled-context boundary.
    driver_x = x0 + 30
    task_x = x0 + width - 172
    results_x = x0 + 32
    races_x = x0 + width - 162
    mini_table(c, driver_x, 180, 145, 140, "Drivers", rows=2)
    mini_table(c, task_x, 155, 155, 178, "Task", seed=True, rows=3)
    mini_table(c, results_x, 430, 150, 150, "Results", rows=2)
    mini_table(c, races_x, 443, 145, 140, "Races", rows=2)
    c.line([(task_x, 230), (driver_x+146, 238)], color=BLUE, sw=4)
    c.line([(driver_x+145, 289), (results_x+75, 430)], color=TEAL, sw=4)
    c.line([(results_x+150, 500), (races_x, 500)], color=BLUE, sw=4)
    c.text(task_x+77, 355, "seed row", size=17, color=ORANGE, bold=True)
    c.text(task_x+77, 381, "target masked", size=15, color=RED)
    badge(c, x0+50, 760, width-100, "bounded hybrid sampling", fill=NAVY)
    c.text(x0+width/2, 823, "≤ S_max sampled non-padding cells", size=16, color=MUTED)


def draw_row_graph(c: Canvas, x0: int, y0: int, w: int, h: int, *, conditioned=False):
    c.rect(x0, y0, w, h, fill=BLUE_BG, stroke="#A8BED8", sw=2, r=26)
    c.text(x0+28, y0+39, "Candidate-augmented row graph", size=22, color=NAVY,
           bold=True, anchor="left")
    badge(c, x0+w-108, y0+18, 82, "L = 6", fill=BLUE)

    sx, sy = x0+105, y0+222
    node(c, sx, sy, "r*", seed=True)
    node(c, x0+290, y0+132, "r_1", small=True)
    node(c, x0+290, y0+310, "r_2", small=True)
    node(c, x0+470, y0+152, "r_3", small=True)
    node(c, x0+470, y0+308, "r_4", small=True)

    # f2p and p2f pairs
    for a, b in [((sx+40, sy-20), (x0+250, y0+148)),
                 ((sx+43, sy+23), (x0+250, y0+294)),
                 ((x0+330, y0+135), (x0+431, y0+151)),
                 ((x0+330, y0+303), (x0+431, y0+306))]:
        c.line([a, b], color=BLUE, sw=4)
        # offset reverse edge for visual separation
        c.line([(b[0], b[1]+12), (a[0], a[1]+12)], color=TEAL, sw=3)

    candidate(c, x0+w-82, y0+150, "c_0", "False")
    candidate(c, x0+w-82, y0+310, "c_1", "True")
    c.line([(x0+510, y0+308), (x0+w-128, y0+310)], color=GREEN, sw=4, dash="8 6")
    c.text(x0+w-200, y0+275, "observed label", size=15, color=GREEN)

    if conditioned:
        # Every retained FK pair receives the condition selected by chi(e).
        # Forward and reverse copies of the same FK share this condition.
        for px, py in [(x0+200, y0+150), (x0+205, y0+296),
                       (x0+385, y0+135), (x0+385, y0+306)]:
            c.rect(px-35, py-18, 70, 34, fill=ORANGE_BG, stroke=ORANGE, sw=2, r=15)
            c.text(px, py, "δₑ", size=15, color="#A75A18", bold=True)
    else:
        c.rect(x0+w-280, y0+h-69, 250, 40, fill=WHITE, stroke="#9EADBF", sw=2, r=18)
        c.text(x0+w-155, y0+h-48, "FK condition  δ_e = 0", size=17, color=MUTED, bold=True)

    c.text(x0+32, y0+h-42, "f2p", size=15, color=BLUE, anchor="left")
    c.line([(x0+80, y0+h-48), (x0+125, y0+h-48)], color=BLUE, sw=4)
    c.text(x0+145, y0+h-42, "p2f", size=15, color=TEAL, anchor="left")
    c.line([(x0+190, y0+h-48), (x0+235, y0+h-48)], color=TEAL, sw=3)

    if conditioned:
        c.rect(x0+w-430, y0+h-70, 400, 42, fill=WHITE, stroke=ORANGE, sw=2, r=18)
        c.text(x0+w-230, y0+h-48,
               "mₑ = αₑ ReLU(Wτ hsrc + bτ + δₑ)", size=16, color=NAVY, bold=True)


def draw_readout(c: Canvas, x0: int, y0: int, w: int):
    heading(c, "d", "Candidate readout", x0+24, y0)
    node(c, x0+90, y0+173, "h_seed", seed=True, small=True)
    candidate(c, x0+88, y0+315, "h_c0", "")
    candidate(c, x0+88, y0+440, "h_c1", "")
    c.circle(x0+210, y0+310, 28, fill=WHITE, stroke="#8494AA", sw=3)
    c.circle(x0+210, y0+435, 28, fill=WHITE, stroke="#8494AA", sw=3)
    c.text(x0+210, y0+311, "||", size=21, bold=True)
    c.text(x0+210, y0+436, "||", size=21, bold=True)
    c.line([(x0+125, y0+177), (x0+190, y0+291)], color=MUTED, sw=3)
    c.line([(x0+125, y0+177), (x0+190, y0+416)], color=MUTED, sw=3)
    c.line([(x0+133, y0+315), (x0+181, y0+310)], color=PURPLE, sw=3)
    c.line([(x0+133, y0+440), (x0+181, y0+435)], color=PURPLE, sw=3)
    c.rect(x0+260, y0+270, 115, 205, fill="#E9EEF6", stroke="#62738D", sw=3, r=24)
    c.text(x0+317, y0+340, "shared", size=17, color=MUTED)
    c.text(x0+317, y0+378, "MLP", size=28, color=NAVY, bold=True)
    c.line([(x0+238, y0+310), (x0+260, y0+310)], color=MUTED, sw=3)
    c.line([(x0+238, y0+435), (x0+260, y0+435)], color=MUTED, sw=3)
    c.line([(x0+375, y0+315), (x0+420, y0+315)], color=PURPLE, sw=3)
    c.line([(x0+375, y0+435), (x0+420, y0+435)], color=PURPLE, sw=3)
    c.text(x0+434, y0+316, "s₀", size=21, color=NAVY, italic=True, anchor="left")
    c.text(x0+434, y0+436, "s₁", size=21, color=NAVY, italic=True, anchor="left")
    c.rect(x0+36, y0+560, w-72, 78, fill=NAVY, stroke=NAVY, sw=1, r=28)
    c.text(x0+w/2, y0+600, "classification:  logit = s₁ − s₀", size=18,
           color=WHITE, bold=True)


def draw_base():
    c = Canvas("RowGraph-Base")
    c.text(42, 35, "ROWGRAPH–BASE", size=30, color=NAVY, bold=True, anchor="left")
    c.text(1748, 35, "typed row-level message passing", size=19, color=MUTED, anchor="right")
    c.line([(420, 70), (420, 1040)], color=BORDER, sw=2, arrow=False, dash="6 9")
    c.line([(780, 70), (780, 1040)], color=BORDER, sw=2, arrow=False, dash="6 9")
    c.line([(1520, 70), (1520, 1040)], color=BORDER, sw=2, arrow=False, dash="6 9")
    draw_context_panel(c, 20, 380)
    draw_init_panel(c, 440, 320)
    heading(c, "c", "Typed row propagation", 820, 92)
    draw_row_graph(c, 810, 140, 680, 680, conditioned=False)
    c.rect(850, 850, 600, 100, fill=WHITE, stroke="#A8BED8", sw=2, r=20)
    c.text(1150, 885, "mₑ = αₑ ReLU(Wτ hsrc + bτ)", size=19,
           color=NAVY, bold=True)
    c.text(1150, 922, "No auxiliary relation graph; δₑ is identically zero", size=16,
           color=MUTED)
    draw_readout(c, 1550, 92, 700)
    c.save("rowgraph_base_architecture")


def relation_node(c: Canvas, x, y, label, rho, *, query=False):
    c.rect(x-90, y-34, 180, 68, fill=WHITE, stroke=ORANGE if query else PURPLE,
           sw=4 if query else 3, r=20)
    c.text(x, y-9, label, size=15, color=NAVY, bold=True)
    c.text(x, y+18, rho, size=17, color=PURPLE, italic=True)
    if query:
        c.circle(x-76, y-22, 8, fill=ORANGE, stroke=ORANGE, sw=1)


def draw_relation_graph(c: Canvas, x0, y0, w, h):
    c.rect(x0, y0, w, h, fill=PURPLE_BG, stroke="#C9B8DD", sw=2, r=26)
    c.text(x0+25, y0+38, "Auxiliary relation graph", size=22, color=NAVY,
           bold=True, anchor="left")
    badge(c, x0+w-105, y0+18, 78, "P = 2", fill=PURPLE)
    relation_node(c, x0+125, y0+130, "Task → Drivers", "ρ_q", query=True)
    relation_node(c, x0+360, y0+102, "Results → Drivers", "ρ_2")
    relation_node(c, x0+565, y0+165, "Results → Races", "ρ_3")
    relation_node(c, x0+345, y0+242, "Races → Circuits", "ρ_4")
    # Same-tail and same-head matches are symmetric predicates.  Because the
    # implementation enumerates ordered relation-node pairs, each produces
    # two directed edges carrying the same type.
    c.line([(x0+215, y0+112), (x0+270, y0+98)], color=PURPLE, sw=3)
    c.line([(x0+270, y0+120), (x0+215, y0+134)], color=PURPLE, sw=3)
    c.text(x0+243, y0+83, "t2t", size=14, color=PURPLE)
    c.line([(x0+450, y0+96), (x0+480, y0+143)], color=PURPLE, sw=3)
    c.line([(x0+480, y0+177), (x0+447, y0+128)], color=PURPLE, sw=3)
    c.text(x0+477, y0+112, "h2h", size=14, color=PURPLE)
    c.line([(x0+500, y0+183), (x0+420, y0+224)], color=PURPLE, sw=3)
    c.text(x0+478, y0+219, "t2h", size=14, color=PURPLE)
    c.line([(x0+430, y0+235), (x0+485, y0+250), (x0+535, y0+196)],
           color=PURPLE, sw=3)
    c.text(x0+500, y0+263, "h2t", size=14, color=PURPLE)
    c.text(x0+25, y0+h-25, "relation nodes = unique (child table, parent table) pairs",
           size=15, color=MUTED, anchor="left")


def draw_relgraph():
    c = Canvas("RelGraph")
    c.text(42, 35, "RELGRAPH", size=30, color=NAVY, bold=True, anchor="left")
    c.text(1748, 35, "query-conditioned FK message passing", size=19,
           color=MUTED, anchor="right")
    c.line([(400, 70), (400, 1060)], color=BORDER, sw=2, arrow=False, dash="6 9")
    c.line([(740, 70), (740, 1060)], color=BORDER, sw=2, arrow=False, dash="6 9")
    c.line([(1660, 70), (1660, 1060)], color=BORDER, sw=2, arrow=False, dash="6 9")

    draw_context_panel(c, 15, 365)
    draw_init_panel(c, 420, 300)

    heading(c, "c", "Relation-conditioned propagation", 780, 92)
    draw_relation_graph(c, 770, 130, 860, 340)
    c.rect(1080, 482, 240, 44, fill=ORANGE_BG, stroke=ORANGE, sw=2, r=19)
    c.text(1200, 505, "δₑ = Affine(z[χ(e)])", size=18, color="#A75A18", bold=True)
    # Each FK pair selects its relation state through chi(e); the arrow points
    # to the graph as a whole, while per-pair badges make the mapping explicit.
    c.line([(1200, 470), (1200, 482)], color=ORANGE, sw=3, dash="8 6")
    draw_row_graph(c, 770, 545, 860, 545, conditioned=True)
    c.line([(1200, 526), (1200, 545)], color=ORANGE, sw=3, dash="8 6")
    c.text(1355, 536, "map by χ(e) to every FK pair", size=14,
           color="#A75A18", anchor="left")

    draw_readout(c, 1690, 92, 580)
    c.save("relgraph_architecture")


if __name__ == "__main__":
    draw_base()
    draw_relgraph()
    print("Generated RowGraph-Base and RelGraph architecture diagrams.")
