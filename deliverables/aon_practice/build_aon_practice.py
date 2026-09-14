#!/usr/bin/env python3
"""Original Aon-style practice workbook: numerical, verbal, deductive (switch), inductive,
numeracy (digit) and information handling. All items and figures are authored here."""
import pymupdf as fitz, math

OUT = "/root/Documents/aon_practice/Aon_Style_Practice_Workbook.pdf"
PW = "Pro@2027!!"
OWNER = "Ali Almuhanna"
PW_, PH = 595, 842
M = 50
INK = (0.12, 0.13, 0.16); SUB = (0.40, 0.42, 0.46); LINE = (0.78, 0.80, 0.83)
NAVY = (0.10, 0.22, 0.40); TEAL = (0.05, 0.50, 0.50); ORANGE = (0.86, 0.50, 0.12); RED = (0.75, 0.22, 0.18)
LIGHT = (0.94, 0.95, 0.97)

doc = fitz.open()
page = None; y = 0; pageno = 0

def newpage(section=""):
    global page, y, pageno
    page = doc.new_page(width=PW_, height=PH); pageno += 1; y = M
    page.insert_text((M, PH - 28), f"Aon-style Practice Workbook  ·  {section}", fontname="helv", fontsize=7.5, color=SUB)
    page.insert_text((PW_ - M - 20, PH - 28), str(pageno), fontname="helv", fontsize=7.5, color=SUB)
    page.draw_line((M, PH - 36), (PW_ - M, PH - 36), color=LINE, width=0.5)

def need(h, section=""):
    if y + h > PH - 50: newpage(section)

def wrap(text, size, width, font="helv"):
    words = text.split(); lines = []; cur = ""
    for w in words:
        t = (cur + " " + w).strip()
        if fitz.get_text_length(t, fontname=font, fontsize=size) <= width: cur = t
        else: lines.append(cur); cur = w
    if cur: lines.append(cur)
    return lines

def para(text, size=9.5, color=INK, font="helv", width=None, indent=0, gap=4, section=""):
    global y
    width = width or (PW_ - 2 * M - indent)
    lines = wrap(text, size, width, font)
    need(len(lines) * (size + 3) + gap, section)
    for ln in lines:
        page.insert_text((M + indent, y + size), ln, fontname=font, fontsize=size, color=color); y += size + 3
    y += gap

def heading(text, size=15, color=NAVY, section=""):
    global y
    need(size + 14, section)
    page.insert_text((M, y + size), text, fontname="hebo", fontsize=size, color=color); y += size + 10

def sub(text, size=10.5):
    global y
    need(size + 10)
    page.insert_text((M, y + size), text, fontname="hebo", fontsize=size, color=INK); y += size + 6

def item(n, text, options=None, tfc=False, section=""):
    """Question with A-D options or T/F/CS boxes."""
    global y
    lines = wrap(text, 9.5, PW_ - 2 * M - 26)
    h = len(lines) * 12.5 + (len(options) * 12 if options else 0) + (14 if tfc else 0) + 8
    need(h, section)
    page.draw_rect(fitz.Rect(M, y + 1, M + 18, y + 13), color=None, fill=NAVY)
    page.insert_text((M + 3 if n < 10 else M + 1, y + 11), str(n), fontname="hebo", fontsize=8.5, color=(1, 1, 1))
    for ln in lines:
        page.insert_text((M + 26, y + 10), ln, fontname="helv", fontsize=9.5, color=INK); y += 12.5
    if options:
        for k, o in zip("ABCD", options):
            page.insert_text((M + 40, y + 9), f"{k}.  {o}", fontname="helv", fontsize=9.2, color=INK); y += 12
    if tfc:
        x = M + 40
        for lab in ("TRUE", "FALSE", "CANNOT SAY"):
            page.draw_rect(fitz.Rect(x, y + 1, x + 9, y + 10), color=SUB, width=0.7)
            page.insert_text((x + 13, y + 9), lab, fontname="helv", fontsize=8.5, color=SUB); x += 90
        y += 14
    y += 8

def table(headers, rows, colw, size=8.5, section=""):
    global y
    rh = size + 6; need(rh * (len(rows) + 1) + 8, section)
    x0 = M; tw = sum(colw)
    page.draw_rect(fitz.Rect(x0, y, x0 + tw, y + rh), color=None, fill=NAVY)
    x = x0
    for h, w in zip(headers, colw):
        page.insert_text((x + 4, y + size + 1), h, fontname="hebo", fontsize=size, color=(1, 1, 1)); x += w
    y += rh
    for i, r in enumerate(rows):
        if i % 2 == 0: page.draw_rect(fitz.Rect(x0, y, x0 + tw, y + rh), color=None, fill=LIGHT)
        x = x0
        for j, (c, w) in enumerate(zip(r, colw)):
            bold = str(c).startswith("*"); c = str(c).lstrip("*")
            page.insert_text((x + 4, y + size + 1), c, fontname="hebo" if bold else "helv", fontsize=size, color=INK); x += w
        y += rh
    page.draw_rect(fitz.Rect(x0, y - rh * (len(rows) + 1), x0 + tw, y), color=LINE, width=0.6)
    y += 8

# ------------------------------------------------------------------ figures
def bar_chart(title, cats, series, colors, ymax, ystep, unit, width=300, height=170):
    """Grouped bar chart drawn with vector primitives."""
    global y
    need(height + 58)
    x0 = M + 40; y0 = y + height + 30; pw = width; ph = height
    page.insert_text((M, y + 9), title, fontname="hebo", fontsize=9, color=INK)
    page.draw_line((x0, y0), (x0 + pw, y0), color=INK, width=0.8)
    page.draw_line((x0, y0), (x0, y0 - ph), color=INK, width=0.8)
    for v in range(0, ymax + 1, ystep):
        yy = y0 - ph * v / ymax
        page.draw_line((x0, yy), (x0 + pw, yy), color=LINE, width=0.4)
        page.insert_text((x0 - 26, yy + 3), f"{v}", fontname="helv", fontsize=7.5, color=SUB)
    page.insert_text((x0 - 36, y0 - ph - 8), unit, fontname="helv", fontsize=7, color=SUB)
    n = len(cats); gw = pw / n; bw = gw / (len(series) + 1)
    for i, c in enumerate(cats):
        gx = x0 + i * gw + bw / 2
        for s, (name, vals) in enumerate(series):
            v = vals[i]; bx = gx + s * bw; bh = ph * v / ymax
            page.draw_rect(fitz.Rect(bx, y0 - bh, bx + bw - 2, y0), color=None, fill=colors[s])
            page.insert_text((bx + 2, y0 - bh - 3), f"{v}", fontname="helv", fontsize=7, color=INK)
        page.insert_text((gx + 4, y0 + 11), c, fontname="helv", fontsize=8, color=INK)
    lx = x0 + pw + 12
    for s, (name, vals) in enumerate(series):
        page.draw_rect(fitz.Rect(lx, y + 34 + s * 14, lx + 9, y + 43 + s * 14), color=None, fill=colors[s])
        page.insert_text((lx + 13, y + 42 + s * 14), name, fontname="helv", fontsize=7.5, color=INK)
    y = y0 + 24

def bubble_chart(title, pts, xmax, ymax, xlab, ylab, width=300, height=180):
    global y
    need(height + 62)
    x0 = M + 46; y0 = y + height + 30; pw = width; ph = height
    page.insert_text((M, y + 9), title, fontname="hebo", fontsize=9, color=INK)
    page.draw_line((x0, y0), (x0 + pw, y0), color=INK, width=0.8)
    page.draw_line((x0, y0), (x0, y0 - ph), color=INK, width=0.8)
    for v in range(0, ymax + 1, 10):
        yy = y0 - ph * v / ymax
        page.draw_line((x0, yy), (x0 + pw, yy), color=LINE, width=0.4)
        page.insert_text((x0 - 28, yy + 3), f"{v}%", fontname="helv", fontsize=7.5, color=SUB)
    for v in [0, 1, 2, 3, 4]:
        xx = x0 + pw * v / xmax
        page.draw_line((xx, y0), (xx, y0 - ph), color=LINE, width=0.4)
        page.insert_text((xx - 8, y0 + 11), f"{v:.1f}%", fontname="helv", fontsize=7.5, color=SUB)
    page.insert_text((x0 + pw / 2 - 30, y0 + 24), xlab, fontname="helv", fontsize=8, color=INK)
    page.insert_text((x0 - 40, y0 - ph - 8), ylab, fontname="helv", fontsize=7.5, color=INK)
    for name, gx, gy, rev, col in pts:
        cx = x0 + pw * gx / xmax; cy = y0 - ph * gy / ymax; r = 6 + rev / 22
        page.draw_circle((cx, cy), r, color=None, fill=col)
        page.insert_text((cx + r + 4, cy + 3), f"{name} (EUR {rev}m)", fontname="helv", fontsize=7.5, color=INK)
    y = y0 + 34

def grid_panel(x, yy, size, filled, dots=None, arrow=None, squares=None, label=None):
    """3x3 grid panel. filled = set of (r,c). arrow = 'up/right/down/left'. dots=n, squares=(n,black)."""
    cell = size / 3
    page.draw_rect(fitz.Rect(x, yy, x + size, yy + size), color=SUB, width=0.7)
    if filled is not None:
        for i in range(1, 3):
            page.draw_line((x + i * cell, yy), (x + i * cell, yy + size), color=LINE, width=0.4)
            page.draw_line((x, yy + i * cell), (x + size, yy + i * cell), color=LINE, width=0.4)
        for r, c in filled:
            page.draw_rect(fitz.Rect(x + c * cell + 2, yy + r * cell + 2, x + (c + 1) * cell - 2, yy + (r + 1) * cell - 2), color=None, fill=NAVY)
    if dots is not None:
        for k in range(dots):
            cx = x + 10 + (k % 3) * (size - 20) / 2; cy = yy + 10 + (k // 3) * (size - 20) / 2
            page.draw_circle((cx, cy), 4, color=None, fill=TEAL)
    if arrow:
        cx, cy = x + size / 2, yy + size / 2; L = size * 0.32
        d = {"up": (0, -1), "down": (0, 1), "right": (1, 0), "left": (-1, 0)}[arrow]
        tip = (cx + d[0] * L, cy + d[1] * L); tail = (cx - d[0] * L, cy - d[1] * L)
        page.draw_line(tail, tip, color=ORANGE, width=2.2)
        px, py = -d[1], d[0]
        page.draw_polyline([tip, (tip[0] - d[0] * 9 + px * 6, tip[1] - d[1] * 9 + py * 6), (tip[0] - d[0] * 9 - px * 6, tip[1] - d[1] * 9 - py * 6), tip], color=None, fill=ORANGE)
    if squares:
        n, black = squares
        for k in range(n):
            cx = x + 8 + (k % 3) * (size - 16) / 2; cy = yy + 8 + (k // 3) * (size - 16) / 2
            page.draw_rect(fitz.Rect(cx, cy, cx + 8, cy + 8), color=INK, width=0.8, fill=INK if black else (1, 1, 1))
    if label:
        page.insert_text((x + size / 2 - 3, yy + size + 10), label, fontname="hebo", fontsize=8, color=INK)

def figure_series(panels, options, size=46):
    """panels: list of kwargs for grid_panel; options: list of (letter, kwargs)."""
    global y
    need(size * 2 + 50)
    x = M + 26
    page.insert_text((x, y + 8), "Series:", fontname="helv", fontsize=8, color=SUB); y += 12
    for i, p in enumerate(panels):
        grid_panel(x + i * (size + 14), y, size, **p)
    qx = x + len(panels) * (size + 14)
    page.draw_rect(fitz.Rect(qx, y, qx + size, yy := y + size), color=SUB, width=0.7, dashes="[3 3] 0")
    page.insert_text((qx + size / 2 - 4, y + size / 2 + 5), "?", fontname="hebo", fontsize=14, color=SUB)
    y += size + 8
    page.insert_text((x, y + 8), "Options:", fontname="helv", fontsize=8, color=SUB); y += 12
    for i, (letter, p) in enumerate(options):
        grid_panel(x + i * (size + 14), y, size, label=letter, **p)
    y += size + 22

def arrow_glyph(x, yc):
    page.draw_line((x, yc), (x + 11, yc), color=SUB, width=1.1)
    page.draw_polyline([(x + 11, yc), (x + 7, yc - 3), (x + 7, yc + 3), (x + 11, yc)], color=None, fill=SUB)

def switch_item(n, inp, out, options, steps=None):
    """switchChallenge-style: input digits -> output; choose operator (position map)."""
    global y
    need(60)
    page.draw_rect(fitz.Rect(M, y + 1, M + 18, y + 13), color=None, fill=NAVY)
    page.insert_text((M + 3 if n < 10 else M + 1, y + 11), str(n), fontname="hebo", fontsize=8.5, color=(1, 1, 1))
    x = M + 30
    def boxes(vals, x, col):
        for v in vals:
            page.draw_rect(fitz.Rect(x, y, x + 16, y + 16), color=col, width=1)
            page.insert_text((x + 4.5, y + 12), str(v), fontname="hebo", fontsize=10, color=col); x += 18
        return x
    x = boxes(inp, x, INK); arrow_glyph(x + 4, y + 8); x += 20
    if steps:
        for s in steps:
            page.draw_rect(fitz.Rect(x, y - 1, x + 36, y + 17), color=TEAL, width=1, fill=(0.92, 0.97, 0.97))
            page.insert_text((x + 5, y + 12), s, fontname="hebo", fontsize=9.5, color=TEAL); x += 40
            arrow_glyph(x + 2, y + 8); x += 18
    else:
        page.draw_rect(fitz.Rect(x, y - 1, x + 36, y + 17), color=TEAL, width=1, dashes="[3 3] 0")
        page.insert_text((x + 13, y + 12), "?", fontname="hebo", fontsize=10, color=TEAL); x += 40
        arrow_glyph(x + 2, y + 8); x += 18
    if out: boxes(out, x, NAVY)
    else:
        for _ in range(3):
            page.draw_rect(fitz.Rect(x, y, x + 16, y + 16), color=NAVY, width=1, dashes="[2 2] 0"); x += 18
    y += 24
    ox = M + 30
    for k, o in zip("ABCD", options):
        page.insert_text((ox, y + 9), f"{k}.  {o}", fontname="helv", fontsize=9.2, color=INK); ox += 110
    y += 22

# ================================================================== COVER
newpage("Cover")
page.draw_rect(fitz.Rect(0, 0, PW_, 250), color=None, fill=NAVY)
page.insert_text((M, 110), "Aon-style Assessment", fontname="hebo", fontsize=28, color=(1, 1, 1))
page.insert_text((M, 145), "Practice Workbook", fontname="hebo", fontsize=28, color=(1, 1, 1))
page.insert_text((M, 180), "Numerical · Verbal · Deductive (switch) · Inductive · Numeracy (digit) · Information handling",
                 fontname="helv", fontsize=9.5, color=(0.85, 0.88, 0.95))
page.insert_text((M, 205), "40 original practice items with figures, answer key and worked reasoning", fontname="helv", fontsize=9.5, color=(0.85, 0.88, 0.95))
y = 290
para(f"Prepared for: {OWNER}", 11, INK)
para("Purpose: timed practice in the item formats used by Aon-style online reasoning assessments. Every data sheet, chart, passage and item in this workbook is original practice material — none is taken from a live test.", 9.5, SUB)
y += 10
sub("How to use this workbook")
for t in ["Work each section against the clock shown in its header. The real tests are short and dense; pace matters more than perfection.",
          "For TRUE / FALSE / CANNOT SAY items, use only the data sheet or passage in front of you. Outside knowledge and assumptions make a statement CANNOT SAY, never TRUE.",
          "Attempt everything before opening the answer key (Section G). Then read the reasoning for every item you got wrong or guessed."]:
    para("•  " + t, 9.5, INK, indent=8)
y += 10
sub("Contents")
for t in ["A  Numerical reasoning — 2 data sheets, 12 items (recommended 10 min)",
          "B  Verbal reasoning — 1 passage, 6 items (5 min)",
          "C  Deductive reasoning, switch format — 6 items (4 min)",
          "D  Inductive reasoning, figure series — 4 items (4 min)",
          "E  Numeracy, digit format — 8 items (4 min)",
          "F  Information handling — 1 table, 4 items (4 min)",
          "G  Answer key with worked reasoning",
          "H  Strategy notes for each format"]:
    para(t, 9.5, INK, indent=8, gap=1)

# ================================================================== A NUMERICAL
newpage("A · Numerical reasoning")
heading("Section A — Numerical reasoning", section="A · Numerical")
para("Recommended time: 10 minutes for 12 items. Decide whether each statement is TRUE, FALSE or CANNOT SAY using only the data sheet above it.", 9.5, SUB)
sub("Data sheet 1 — Meridian Metals plc, income statement (EUR million)")
table(["", "FY1", "FY2", "FY3"],
      [["Revenue", "1,840", "1,960", "2,150"], ["Cost of sales", "1,210", "1,290", "1,420"],
       ["*Gross profit", "*630", "*670", "*730"], ["Operating expenses", "410", "445", "470"],
       ["*Operating profit", "*220", "*225", "*260"], ["Employees (year end)", "6,200", "6,450", "6,900"]],
      [190, 80, 80, 80])
table(["FY3 revenue by segment", "EUR million", "", ""],
      [["Construction", "860", "", ""], ["Automotive", "645", "", ""], ["Energy", "430", "", ""], ["Other", "215", "", ""]],
      [190, 80, 80, 80])
item(1, "Revenue grew by more than 15% between FY1 and FY3.", tfc=True)
item(2, "Gross margin (gross profit as a percentage of revenue) was higher in FY3 than in FY1.", tfc=True)
item(3, "Operating profit per employee in FY3 exceeded EUR 38,000.", tfc=True)
item(4, "The Automotive segment accounted for exactly 30% of FY3 revenue.", tfc=True)
item(5, "The Construction segment's revenue grew between FY2 and FY3.", tfc=True)
item(6, "Operating expenses rose by a smaller percentage from FY2 to FY3 than from FY1 to FY2.", tfc=True)

newpage("A · Numerical reasoning")
sub("Data sheet 2 — Client segments and workforce")
bubble_chart("Market share vs. market growth by client segment (bubble size = revenue)",
             [("Segment A", 1.0, 15, 120, RED), ("Segment B", 2.0, 30, 230, TEAL), ("Segment C", 3.5, 40, 410, ORANGE)],
             4, 50, "Market growth", "Market share")
bar_chart("Employees by region (thousands)", ["Europe", "Americas", "Asia"],
          [("FY2", [4.2, 2.9, 1.8]), ("FY3", [4.6, 3.1, 2.4])], [RED, ORANGE], 5, 1, "thousand")
item(7, "Segment C has both the highest market share and the highest market growth of the three segments.", tfc=True)
item(8, "Revenue from Segment B is more than twice the revenue from Segment A.", tfc=True)
item(9, "Total employees across the three regions increased by more than 12% from FY2 to FY3.", tfc=True)
item(10, "Asia had the largest absolute increase in employees between FY2 and FY3.", tfc=True)
item(11, "Segment A's market share will fall next year.", tfc=True)
item(12, "Segment A generates more revenue per percentage point of market share than Segment C.", tfc=True)

# ================================================================== B VERBAL
newpage("B · Verbal reasoning")
heading("Section B — Verbal reasoning", section="B · Verbal")
para("Recommended time: 5 minutes for 6 items. Judge each statement only on what the passage says. TRUE = follows logically from the passage; FALSE = contradicts it; CANNOT SAY = the passage gives no basis to decide.", 9.5, SUB)
page.draw_rect(fitz.Rect(M - 6, y - 4, PW_ - M + 6, y + 122), color=None, fill=LIGHT);
para("Northgate Logistics introduced a hybrid-working policy in March. Under the policy, office-based staff may work remotely for up to three days per week, provided their line manager has approved a fixed weekly schedule in advance. Warehouse and driving roles are excluded because they require physical presence. A review after six months found that 62% of eligible staff had adopted a hybrid schedule, and that average reported job satisfaction among adopters had risen by four points on the company's ten-point scale. The review did not measure productivity. Managers were instructed that requests could be refused only on operational grounds and that every refusal must be documented. The company has announced that the policy will be extended to its two Irish subsidiaries next year.", 9.5, INK, width=PW_ - 2 * M - 4)
y += 8
item(13, "Eligible staff may choose a different set of remote days each week.", tfc=True)
item(14, "Warehouse staff are excluded from the hybrid-working policy.", tfc=True)
item(15, "Hybrid working has increased productivity at Northgate Logistics.", tfc=True)
item(16, "More than half of eligible staff adopted a hybrid schedule.", tfc=True)
item(17, "A manager may refuse a hybrid-working request without recording the reason.", tfc=True)
item(18, "The policy currently applies to the company's Irish subsidiaries.", tfc=True)

# ================================================================== C DEDUCTIVE
newpage("C · Deductive reasoning (switch)")
heading("Section C — Deductive reasoning, switch format", section="C · Deductive")
para("Recommended time: 4 minutes for 6 items. An operator is a three-digit code that re-orders the input. The code reads left to right: the first digit says which INPUT position goes to OUTPUT position 1, the second digit which input position goes to output position 2, and so on. Example: operator 2 1 3 applied to 4 7 2 gives 7 4 2 (positions 1 and 2 swap, position 3 stays).", 9.5, SUB)
para("Items 19–22: which operator produced the output?  Items 23–24: apply the operators in order and choose the output.", 9.5, INK)
y += 4
switch_item(19, [4, 7, 2], [7, 4, 2], ["2 1 3", "3 2 1", "1 3 2", "3 1 2"])
switch_item(20, [5, 8, 1], [1, 5, 8], ["2 3 1", "3 1 2", "1 2 3", "2 1 3"])
switch_item(21, [9, 3, 6], [6, 3, 9], ["3 2 1", "2 1 3", "1 3 2", "2 3 1"])
switch_item(22, [2, 7, 5], [2, 5, 7], ["2 1 3", "3 2 1", "1 3 2", "3 1 2"])
switch_item(23, [1, 4, 8], None, ["8 4 1", "4 1 8", "1 8 4", "8 1 4"], steps=["2 3 1", "2 1 3"])
switch_item(24, [6, 2, 9], None, ["9 2 6", "2 6 9", "6 9 2", "2 9 6"], steps=["3 1 2", "3 2 1"])

# ================================================================== D INDUCTIVE
newpage("D · Inductive reasoning")
heading("Section D — Inductive reasoning, figure series", section="D · Inductive")
para("Recommended time: 4 minutes for 4 items. Work out the rule that links the panels in the series, then choose the option that correctly continues it.", 9.5, SUB)
sub("25.  Which panel comes next?")
figure_series([dict(filled={(0, 0)}), dict(filled={(0, 1)}), dict(filled={(0, 2)}), dict(filled={(1, 2)})],
              [("A", dict(filled={(2, 2)})), ("B", dict(filled={(2, 1)})), ("C", dict(filled={(1, 0)})), ("D", dict(filled={(0, 1)}))])
sub("26.  Which panel comes next?")
figure_series([dict(filled=None, dots=1), dict(filled=None, dots=3), dict(filled=None, dots=2), dict(filled=None, dots=4), dict(filled=None, dots=3)],
              [("A", dict(filled=None, dots=4)), ("B", dict(filled=None, dots=5)), ("C", dict(filled=None, dots=6)), ("D", dict(filled=None, dots=2))])
sub("27.  Which panel comes next?")
figure_series([dict(filled=None, arrow="up"), dict(filled=None, arrow="right"), dict(filled=None, arrow="down"), dict(filled=None, arrow="left")],
              [("A", dict(filled=None, arrow="up")), ("B", dict(filled=None, arrow="right")), ("C", dict(filled=None, arrow="down")), ("D", dict(filled=None, arrow="left"))])
sub("28.  Which panel comes next?")
figure_series([dict(filled=None, squares=(2, True)), dict(filled=None, squares=(3, False)), dict(filled=None, squares=(4, True))],
              [("A", dict(filled=None, squares=(5, True))), ("B", dict(filled=None, squares=(5, False))), ("C", dict(filled=None, squares=(4, False))), ("D", dict(filled=None, squares=(6, True)))])

# ================================================================== E NUMERACY
newpage("E · Numeracy (digit)")
heading("Section E — Numeracy, digit format", section="E · Numeracy")
para("Recommended time: 4 minutes for 8 items. Find the missing number or operator that makes each equation correct. No calculator.", 9.5, SUB)
item(29, "7  ?  3  =  21   — which operator replaces the question mark?", ["+", "−", "×", "÷"])
item(30, "48  ÷  ?  =  6", ["6", "8", "7", "9"])
item(31, "?  +  17  =  41", ["24", "26", "34", "23"])
item(32, "9  ×  6  −  ?  =  40", ["12", "14", "16", "24"])
item(33, "( 5  +  ? )  ×  3  =  36", ["6", "7", "8", "9"])
item(34, "100  −  4  ×  ?  =  64", ["9", "8", "12", "16"])
item(35, "?  ÷  4  +  5  =  12", ["24", "28", "32", "68"])
item(36, "2  ×  ?  +  3  ×  4  =  30", ["7", "8", "9", "11"])

# ================================================================== F INFO HANDLING
newpage("F · Information handling")
heading("Section F — Information handling", section="F · Information")
para("Recommended time: 4 minutes for 4 items. Answer using the shipment log below.", 9.5, SUB)
table(["Shipment", "Origin", "Destination", "Weight (kg)", "Service", "Cost (EUR )"],
      [["S101", "Madrid", "Berlin", "12", "Express", "84"], ["S102", "Lyon", "Madrid", "30", "Standard", "62"],
       ["S103", "Berlin", "Lyon", "8", "Express", "71"], ["S104", "Madrid", "Lyon", "22", "Standard", "48"],
       ["S105", "Lyon", "Berlin", "15", "Express", "93"], ["S106", "Berlin", "Madrid", "40", "Standard", "75"]],
      [70, 80, 90, 85, 85, 70])
item(37, "What is the total cost of all Express shipments?", ["EUR 233", "EUR 248", "EUR 256", "EUR 185"])
item(38, "Which is the heaviest Standard shipment?", ["S102", "S104", "S106", "S105"])
item(39, "What is the average weight of shipments originating in Madrid?", ["16 kg", "17 kg", "18 kg", "34 kg"])
item(40, "Which shipment has the lowest cost per kilogram?", ["S102", "S104", "S106", "S101"])

# ================================================================== G ANSWER KEY
newpage("G · Answer key")
heading("Section G — Answer key and worked reasoning", section="G · Answers")
para("Check every item, not just the ones you missed: the reasoning shows the fastest route, which is what the time limit rewards.", 9.5, SUB)
KEY = [
 ("A · Numerical", [
  (1, "TRUE", "2,150 ÷ 1,840 = 1.168 → growth of 16.8%, which is more than 15%."),
  (2, "FALSE", "FY1 margin 630 ÷ 1,840 = 34.2%; FY3 margin 730 ÷ 2,150 = 34.0%. FY3 is slightly lower."),
  (3, "FALSE", "EUR 260m ÷ 6,900 employees = EUR 37,681 per employee, below EUR 38,000."),
  (4, "TRUE", "645 ÷ 2,150 = 0.300 exactly, i.e. 30%."),
  (5, "CANNOT SAY", "The sheet gives segment revenue for FY3 only; there is no FY2 segment figure to compare."),
  (6, "TRUE", "FY1→FY2: 35 ÷ 410 = 8.5%. FY2→FY3: 25 ÷ 445 = 5.6%. The later rise is smaller."),
  (7, "TRUE", "Segment C sits furthest right (3.5% growth) and highest (40% share)."),
  (8, "FALSE", "Twice Segment A is 2 × EUR 120m = EUR 240m; Segment B is EUR 230m, which is less."),
  (9, "TRUE", "FY2 total 4.2 + 2.9 + 1.8 = 8.9k; FY3 total 4.6 + 3.1 + 2.4 = 10.1k; rise 1.2 ÷ 8.9 = 13.5%."),
  (10, "TRUE", "Increases: Europe +0.4k, Americas +0.2k, Asia +0.6k. Asia is largest."),
  (11, "CANNOT SAY", "The chart shows current share and current growth; it says nothing about next year."),
  (12, "FALSE", "A: 120 ÷ 15 = EUR 8.0m per point. C: 410 ÷ 40 = EUR 10.25m per point. C is higher.")]),
 ("B · Verbal", [
  (13, "FALSE", "The passage requires a fixed weekly schedule approved in advance, so days cannot vary week to week."),
  (14, "TRUE", "Warehouse and driving roles are explicitly excluded."),
  (15, "CANNOT SAY", "The review measured satisfaction but 'did not measure productivity'. No basis either way."),
  (16, "TRUE", "62% of eligible staff adopted a hybrid schedule; 62% is more than half."),
  (17, "FALSE", "Refusals are only allowed on operational grounds and 'every refusal must be documented'."),
  (18, "FALSE", "The policy 'will be extended' to the Irish subsidiaries next year, so it does not currently apply to them.")]),
 ("C · Deductive (switch)", [
  (19, "A", "Output 7 4 2 takes input position 2 first, then 1, then 3 → operator 2 1 3."),
  (20, "B", "Output 1 5 8 takes position 3, then 1, then 2 → operator 3 1 2."),
  (21, "A", "Output 6 3 9 is the full reversal → operator 3 2 1."),
  (22, "C", "Output 2 5 7 keeps position 1 and swaps 2 and 3 → operator 1 3 2."),
  (23, "A", "1 4 8 → (2 3 1) → 4 8 1 → (2 1 3) → 8 4 1."),
  (24, "B", "6 2 9 → (3 1 2) → 9 6 2 → (3 2 1) → 2 6 9.")]),
 ("D · Inductive", [
  (25, "A", "The filled cell moves one step clockwise around the outer ring: top-left, top-centre, top-right, middle-right → bottom-right."),
  (26, "B", "Dot counts run 1, 3, 2, 4, 3: alternately +2 then −1. After 3 comes 3 + 2 = 5."),
  (27, "A", "The arrow rotates 90° clockwise each panel: up, right, down, left → up again."),
  (28, "B", "The count rises by one each panel (2, 3, 4 → 5) while the fill alternates black, white, black → white. Five white squares.")]),
 ("E · Numeracy (digit)", [
  (29, "C", "7 × 3 = 21."), (30, "B", "48 ÷ 8 = 6."), (31, "A", "41 − 17 = 24."), (32, "B", "54 − 40 = 14."),
  (33, "B", "36 ÷ 3 = 12; 12 − 5 = 7."), (34, "A", "100 − 64 = 36; 36 ÷ 4 = 9."),
  (35, "B", "12 − 5 = 7; 7 × 4 = 28."), (36, "C", "3 × 4 = 12; 30 − 12 = 18; 18 ÷ 2 = 9.")]),
 ("F · Information handling", [
  (37, "B", "Express shipments S101, S103, S105: 84 + 71 + 93 = EUR 248."),
  (38, "C", "Standard shipments weigh 30, 22 and 40 kg; S106 at 40 kg is heaviest."),
  (39, "B", "From Madrid: S101 (12 kg) and S104 (22 kg); average (12 + 22) ÷ 2 = 17 kg."),
  (40, "C", "Cost per kg: S101 7.00, S102 2.07, S103 8.88, S104 2.18, S105 6.20, S106 1.88. S106 is lowest.")]),
]
for sec, rows in KEY:
    sub(sec)
    for n, ans, why in rows:
        lines = wrap(why, 8.8, PW_ - 2 * M - 120)
        need(len(lines) * 11 + 6, "G · Answers")
        page.insert_text((M, y + 9), f"{n}.", fontname="hebo", fontsize=9, color=INK)
        page.insert_text((M + 24, y + 9), ans, fontname="hebo", fontsize=9, color=TEAL)
        for ln in lines:
            page.insert_text((M + 112, y + 9), ln, fontname="helv", fontsize=8.8, color=INK); y += 11
        y += 4
    y += 4

# ================================================================== H STRATEGY
newpage("H · Strategy notes")
heading("Section H — Strategy notes by format", section="H · Strategy")
TIPS = [
 ("Numerical (data sheets, TRUE / FALSE / CANNOT SAY)",
  ["Read the statement first, then go to the sheet for exactly the figures it needs. Do not read the whole sheet.",
   "CANNOT SAY is a real answer, not a fallback. Choose it when the required figure is simply absent (e.g. a year or segment not shown) or the statement is about the future.",
   "Keep a running scale check: a 'per employee' or 'per point' figure needs the right units (EUR million ÷ headcount) before you compare.",
   "Percent change = (new − old) ÷ old. Estimate first; only calculate precisely when the statement's threshold is close to your estimate (item 3 was within 1%)."]),
 ("Verbal (passage, TRUE / FALSE / CANNOT SAY)",
  ["Anchor each statement to a specific sentence. If you cannot point to one, it is CANNOT SAY.",
   "Watch for scope words: 'may', 'only', 'every', 'currently', 'will'. They often decide TRUE vs FALSE on their own (items 13, 17, 18).",
   "Do not import what a reasonable company would do. The passage is the whole world."]),
 ("Deductive — switch format",
  ["Read the operator as 'output position k takes input position code[k]'. Say it aloud once and it stays fixed under time pressure.",
   "Spot patterns fast: 3 2 1 is full reversal; 1 3 2 and 2 1 3 are single swaps; 2 3 1 and 3 1 2 are rotations.",
   "For multi-step items, write the intermediate string down — most errors come from doing the second step in your head."]),
 ("Inductive — figure series",
  ["Isolate one attribute at a time: position, count, rotation, shading. Two attributes often change together (item 28).",
   "Check the rule against every panel before answering; a rule that fits three of four is wrong."]),
 ("Numeracy — digit format",
  ["Unwind the equation from the result backwards using inverse operations (÷ undoes ×, − undoes +).",
   "Respect operator precedence: 2 × ? + 3 × 4 means (2 × ?) + 12, not 2 × (? + 3) × 4."]),
 ("Information handling",
  ["Filter first (which rows qualify), then compute. Mark the qualifying rows before adding.",
   "For 'per unit' comparisons, a rough ratio for each row is usually enough to spot the extreme — compute exactly only for the two closest."]),
 ("Timing",
  ["Aon-style tests are roughly 20 seconds per item. Decide, answer, move on. A blank costs the same as a wrong answer, so never leave items unanswered at the end.",
   "If an item needs more than two calculations, make your best estimate and flag it mentally rather than losing three later items."]),
]
for t, pts in TIPS:
    sub(t)
    for p in pts: para("•  " + p, 9.3, INK, indent=8, gap=2, section="H · Strategy")
    y += 4

# ================================================================== save
doc.set_metadata({"title": "Aon-style Practice Workbook", "author": OWNER, "subject": "Reasoning assessment practice — original material",
                  "keywords": "numerical, verbal, deductive, inductive, numeracy, practice", "creator": OWNER, "producer": OWNER})
import os; os.makedirs(os.path.dirname(OUT), exist_ok=True)
doc.save(OUT, encryption=fitz.PDF_ENCRYPT_AES_256, user_pw=PW, owner_pw=PW, permissions=fitz.PDF_PERM_PRINT | fitz.PDF_PERM_COPY | fitz.PDF_PERM_ACCESSIBILITY, deflate=True, garbage=3)
print("SAVED", OUT, doc.page_count, "pages", round(os.path.getsize(OUT) / 1024), "KB")
