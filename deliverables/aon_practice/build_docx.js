const fs = require("fs");
const D = require("docx");
const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, WidthType, ShadingType, AlignmentType,
  HeadingLevel, ImageRun, PageBreak, LevelFormat, BorderStyle, Header, Footer, PageNumber, TabStopType } = D;

const OWNER = "Ali Almuhanna";
const NAVY = "1A3866", TEAL = "0D8080", GREY = "6A6D75", LIGHT = "F0F2F5";
const FONT = "Arial";
const FIG = "/tmp/claude-0/-home-user-smartguard360/2c4fcbd6-b83d-5759-85d0-e0ec32e3778b/scratchpad/docx_figs/";

// ---------- helpers
const run = (t, o = {}) => new TextRun({ text: t, font: FONT, size: o.size || 20, bold: o.bold, color: o.color, italics: o.italics });
const P = (t, o = {}) => new Paragraph({ children: Array.isArray(t) ? t : [run(t, o)], spacing: { after: o.after ?? 100, before: o.before ?? 0 }, alignment: o.align, indent: o.indent, heading: o.heading, numbering: o.numbering, keepNext: o.keepNext });
const H1 = (t) => new Paragraph({ heading: HeadingLevel.HEADING_1, spacing: { before: 200, after: 120 }, children: [new TextRun({ text: t, font: FONT, size: 30, bold: true, color: NAVY })] });
const H2 = (t) => new Paragraph({ heading: HeadingLevel.HEADING_2, spacing: { before: 160, after: 80 }, keepNext: true, children: [new TextRun({ text: t, font: FONT, size: 22, bold: true, color: "1F2228" })] });
const note = (t) => P(t, { color: GREY, size: 19, after: 140 });
const bullet = (t) => new Paragraph({ numbering: { reference: "bul", level: 0 }, spacing: { after: 60 }, children: [run(t, { size: 19 })] });
const brk = () => new Paragraph({ children: [new PageBreak()] });

function pngSize(p) { const b = fs.readFileSync(p); return { w: b.readUInt32BE(16), h: b.readUInt32BE(20), b }; }
function img(name, widthPx) {
  const { w, h, b } = pngSize(FIG + name + ".png");
  return new Paragraph({ spacing: { after: 120 }, children: [new ImageRun({ type: "png", data: b, transformation: { width: widthPx, height: Math.round(widthPx * h / w) } })] });
}

function qhead(n, text) {
  return P([run(` ${n} `, { bold: true, color: "FFFFFF", size: 18, }), run("  " + text, { size: 20 })], { after: 40, keepNext: true, }).addChildElement ? null : null;
}
function Q(n, text) {
  return new Paragraph({ spacing: { before: 120, after: 40 }, keepNext: true, children: [
    new TextRun({ text: ` ${n} `, font: FONT, size: 18, bold: true, color: "FFFFFF", shading: { type: ShadingType.CLEAR, fill: NAVY, color: "auto" } }),
    run("   " + text, { size: 20 })] });
}
const TFC = () => P([run("☐ TRUE          ☐ FALSE          ☐ CANNOT SAY", { color: GREY, size: 18 })], { indent: { left: 560 }, after: 80 });
const OPTS = (arr) => arr.map((o, i) => P(`${"ABCD"[i]}.   ${o}`, { indent: { left: 560 }, after: 20, size: 19 }));

function table(headers, rows, widths) {
  const total = widths.reduce((a, b) => a + b, 0);
  const cell = (t, w, hdr, shade) => new TableCell({ width: { size: w, type: WidthType.DXA }, shading: hdr ? { type: ShadingType.CLEAR, fill: NAVY, color: "auto" } : shade ? { type: ShadingType.CLEAR, fill: LIGHT, color: "auto" } : undefined,
    margins: { top: 60, bottom: 60, left: 90, right: 90 },
    children: [new Paragraph({ children: [new TextRun({ text: String(t).replace(/^\*/, ""), font: FONT, size: 18, bold: hdr || String(t).startsWith("*"), color: hdr ? "FFFFFF" : "1F2228" })] })] });
  return new Table({ width: { size: total, type: WidthType.DXA }, columnWidths: widths, rows: [
    new TableRow({ tableHeader: true, children: headers.map((h, i) => cell(h, widths[i], true)) }),
    ...rows.map((r, ri) => new TableRow({ children: r.map((c, i) => cell(c, widths[i], false, ri % 2 === 0)) }))] });
}
const gap = () => P("", { after: 120 });

// ---------- content
const KEY = [
  ["A · Numerical", [[1, "TRUE", "2,150 ÷ 1,840 = 1.168 → growth of 16.8%, more than 15%."], [2, "FALSE", "FY1 margin 630 ÷ 1,840 = 34.2%; FY3 margin 730 ÷ 2,150 = 34.0%. FY3 is slightly lower."], [3, "FALSE", "EUR 260m ÷ 6,900 employees = EUR 37,681 per employee, below EUR 38,000."], [4, "TRUE", "645 ÷ 2,150 = 0.300 exactly, i.e. 30%."], [5, "CANNOT SAY", "Segment revenue is given for FY3 only; there is no FY2 segment figure to compare."], [6, "TRUE", "FY1→FY2: 35 ÷ 410 = 8.5%. FY2→FY3: 25 ÷ 445 = 5.6%. The later rise is smaller."], [7, "TRUE", "Segment C sits furthest right (3.5% growth) and highest (40% share)."], [8, "FALSE", "Twice Segment A is 2 × EUR 120m = EUR 240m; Segment B is EUR 230m, which is less."], [9, "TRUE", "FY2 total 8.9k; FY3 total 10.1k; rise 1.2 ÷ 8.9 = 13.5%."], [10, "TRUE", "Increases: Europe +0.4k, Americas +0.2k, Asia +0.6k."], [11, "CANNOT SAY", "The chart shows current share and growth; it says nothing about next year."], [12, "FALSE", "A: 120 ÷ 15 = 8.0 per point. C: 410 ÷ 40 = 10.25 per point. C is higher."]]],
  ["B · Verbal", [[13, "FALSE", "A fixed weekly schedule must be approved in advance, so days cannot vary week to week."], [14, "TRUE", "Warehouse and driving roles are explicitly excluded."], [15, "CANNOT SAY", "The review 'did not measure productivity'."], [16, "TRUE", "62% is more than half."], [17, "FALSE", "Refusals only on operational grounds and 'every refusal must be documented'."], [18, "FALSE", "The policy 'will be extended' next year, so it does not currently apply."]]],
  ["C · Deductive (switch)", [[19, "A", "Output 7 4 2 takes input position 2, then 1, then 3 → 2 1 3."], [20, "B", "Output 1 5 8 takes position 3, then 1, then 2 → 3 1 2."], [21, "A", "Full reversal → 3 2 1."], [22, "C", "Position 1 kept, 2 and 3 swapped → 1 3 2."], [23, "A", "1 4 8 → (2 3 1) → 4 8 1 → (2 1 3) → 8 4 1."], [24, "B", "6 2 9 → (3 1 2) → 9 6 2 → (3 2 1) → 2 6 9."]]],
  ["D · Inductive", [[25, "A", "Filled cell moves one step clockwise round the outer ring → bottom-right."], [26, "B", "Counts 1, 3, 2, 4, 3: alternately +2 then −1 → 5."], [27, "A", "Arrow rotates 90° clockwise each panel → up again."], [28, "B", "Count +1 each panel (2, 3, 4 → 5); fill alternates black, white, black → white."]]],
  ["E · Numeracy (digit)", [[29, "C", "7 × 3 = 21."], [30, "B", "48 ÷ 8 = 6."], [31, "A", "41 − 17 = 24."], [32, "B", "54 − 40 = 14."], [33, "B", "36 ÷ 3 = 12; 12 − 5 = 7."], [34, "A", "100 − 64 = 36; 36 ÷ 4 = 9."], [35, "B", "12 − 5 = 7; 7 × 4 = 28."], [36, "C", "3 × 4 = 12; 30 − 12 = 18; 18 ÷ 2 = 9."]]],
  ["F · Information handling", [[37, "B", "S101 + S103 + S105: 84 + 71 + 93 = EUR 248."], [38, "C", "Standard shipments weigh 30, 22, 40 kg; S106 is heaviest."], [39, "B", "(12 + 22) ÷ 2 = 17 kg."], [40, "C", "Cost per kg lowest for S106 at 1.88."]]],
];
const TIPS = [
  ["Numerical (data sheets, TRUE / FALSE / CANNOT SAY)", ["Read the statement first, then go to the sheet for exactly the figures it needs.", "CANNOT SAY is a real answer: choose it when the required figure is absent or the statement is about the future.", "Check units before comparing (EUR million ÷ headcount).", "Percent change = (new − old) ÷ old. Estimate first; calculate precisely only when the threshold is close."]],
  ["Verbal (passage, TRUE / FALSE / CANNOT SAY)", ["Anchor each statement to a specific sentence; if you cannot, it is CANNOT SAY.", "Watch scope words: may, only, every, currently, will.", "Do not import outside assumptions — the passage is the whole world."]],
  ["Deductive — switch format", ["Read the operator as 'output position k takes input position code[k]'.", "3 2 1 is full reversal; 1 3 2 and 2 1 3 are single swaps; 2 3 1 and 3 1 2 are rotations.", "For multi-step items write the intermediate string down."]],
  ["Inductive — figure series", ["Isolate one attribute at a time: position, count, rotation, shading.", "Check the rule against every panel before answering."]],
  ["Numeracy — digit format", ["Unwind from the result using inverse operations.", "Respect operator precedence: 2 × ? + 3 × 4 means (2 × ?) + 12."]],
  ["Information handling", ["Filter the qualifying rows first, then compute.", "For per-unit comparisons, rough ratios usually reveal the extreme."]],
  ["Timing", ["About 20 seconds per item: decide, answer, move on. Never leave items blank.", "If an item needs more than two calculations, estimate and move on."]],
];

const body = [];
// cover
body.push(new Paragraph({ spacing: { before: 2400, after: 200 }, children: [new TextRun({ text: "Aon-style Assessment", font: FONT, size: 56, bold: true, color: NAVY })] }));
body.push(new Paragraph({ spacing: { after: 300 }, children: [new TextRun({ text: "Practice Workbook", font: FONT, size: 56, bold: true, color: NAVY })] }));
body.push(P("Numerical · Verbal · Deductive (switch) · Inductive · Numeracy (digit) · Information handling", { color: GREY, size: 21 }));
body.push(P("40 original practice items with figures, answer key and worked reasoning", { color: GREY, size: 21, after: 400 }));
body.push(P(`Prepared for: ${OWNER}`, { bold: true, size: 22, after: 200 }));
body.push(note("Purpose: timed practice in the item formats used by Aon-style online reasoning assessments. Every data sheet, chart, passage and item in this workbook is original practice material — none is taken from a live test."));
body.push(H2("How to use this workbook"));
["Work each section against the clock shown in its header. The real tests are short and dense; pace matters more than perfection.", "For TRUE / FALSE / CANNOT SAY items, use only the data sheet or passage in front of you. Outside knowledge makes a statement CANNOT SAY, never TRUE.", "Attempt everything before opening the answer key (Section G). Then read the reasoning for every item you got wrong or guessed."].forEach(t => body.push(bullet(t)));
body.push(H2("Contents"));
["A  Numerical reasoning — 2 data sheets, 12 items (10 min)", "B  Verbal reasoning — 1 passage, 6 items (5 min)", "C  Deductive reasoning, switch format — 6 items (4 min)", "D  Inductive reasoning, figure series — 4 items (4 min)", "E  Numeracy, digit format — 8 items (4 min)", "F  Information handling — 1 table, 4 items (4 min)", "G  Answer key with worked reasoning", "H  Strategy notes for each format"].forEach(t => body.push(P(t, { size: 19, after: 30, indent: { left: 360 } })));
body.push(brk());

// A
body.push(H1("Section A — Numerical reasoning"));
body.push(note("Recommended time: 10 minutes for 12 items. Decide whether each statement is TRUE, FALSE or CANNOT SAY using only the data sheet above it."));
body.push(H2("Data sheet 1 — Meridian Metals plc, income statement (EUR million)"));
body.push(table(["", "FY1", "FY2", "FY3"], [["Revenue", "1,840", "1,960", "2,150"], ["Cost of sales", "1,210", "1,290", "1,420"], ["*Gross profit", "*630", "*670", "*730"], ["Operating expenses", "410", "445", "470"], ["*Operating profit", "*220", "*225", "*260"], ["Employees (year end)", "6,200", "6,450", "6,900"]], [3800, 1500, 1500, 1500]));
body.push(gap());
body.push(table(["FY3 revenue by segment", "EUR million"], [["Construction", "860"], ["Automotive", "645"], ["Energy", "430"], ["Other", "215"]], [3800, 1500]));
[[1, "Revenue grew by more than 15% between FY1 and FY3."], [2, "Gross margin (gross profit as a percentage of revenue) was higher in FY3 than in FY1."], [3, "Operating profit per employee in FY3 exceeded EUR 38,000."], [4, "The Automotive segment accounted for exactly 30% of FY3 revenue."], [5, "The Construction segment's revenue grew between FY2 and FY3."], [6, "Operating expenses rose by a smaller percentage from FY2 to FY3 than from FY1 to FY2."]].forEach(([n, t]) => { body.push(Q(n, t)); body.push(TFC()); });
body.push(brk());
body.push(H2("Data sheet 2 — Client segments and workforce"));
body.push(img("bubble", 520)); body.push(img("bars", 500));
[[7, "Segment C has both the highest market share and the highest market growth of the three segments."], [8, "Revenue from Segment B is more than twice the revenue from Segment A."], [9, "Total employees across the three regions increased by more than 12% from FY2 to FY3."], [10, "Asia had the largest absolute increase in employees between FY2 and FY3."], [11, "Segment A's market share will fall next year."], [12, "Segment A generates more revenue per percentage point of market share than Segment C."]].forEach(([n, t]) => { body.push(Q(n, t)); body.push(TFC()); });
body.push(brk());

// B
body.push(H1("Section B — Verbal reasoning"));
body.push(note("Recommended time: 5 minutes for 6 items. TRUE = follows logically from the passage; FALSE = contradicts it; CANNOT SAY = the passage gives no basis to decide."));
body.push(new Paragraph({ shading: { type: ShadingType.CLEAR, fill: LIGHT, color: "auto" }, spacing: { after: 160 }, indent: { left: 200, right: 200 }, children: [run("Northgate Logistics introduced a hybrid-working policy in March. Under the policy, office-based staff may work remotely for up to three days per week, provided their line manager has approved a fixed weekly schedule in advance. Warehouse and driving roles are excluded because they require physical presence. A review after six months found that 62% of eligible staff had adopted a hybrid schedule, and that average reported job satisfaction among adopters had risen by four points on the company's ten-point scale. The review did not measure productivity. Managers were instructed that requests could be refused only on operational grounds and that every refusal must be documented. The company has announced that the policy will be extended to its two Irish subsidiaries next year.", { size: 20 })] }));
[[13, "Eligible staff may choose a different set of remote days each week."], [14, "Warehouse staff are excluded from the hybrid-working policy."], [15, "Hybrid working has increased productivity at Northgate Logistics."], [16, "More than half of eligible staff adopted a hybrid schedule."], [17, "A manager may refuse a hybrid-working request without recording the reason."], [18, "The policy currently applies to the company's Irish subsidiaries."]].forEach(([n, t]) => { body.push(Q(n, t)); body.push(TFC()); });
body.push(brk());

// C
body.push(H1("Section C — Deductive reasoning, switch format"));
body.push(note("Recommended time: 4 minutes for 6 items. An operator is a three-digit code that re-orders the input: the first digit says which INPUT position goes to OUTPUT position 1, the second digit which input position goes to output position 2, and so on. Example: operator 2 1 3 applied to 4 7 2 gives 7 4 2."));
body.push(P("Items 19–22: which operator produced the output?  Items 23–24: apply the operators in order and choose the output.", { size: 20, after: 120 }));
[19, 20, 21, 22, 23, 24].forEach(n => body.push(img("sw" + n, 460)));
body.push(brk());

// D
body.push(H1("Section D — Inductive reasoning, figure series"));
body.push(note("Recommended time: 4 minutes for 4 items. Work out the rule that links the panels, then choose the option that correctly continues it."));
[25, 26, 27, 28].forEach(n => { body.push(H2(`${n}.  Which panel comes next?`)); body.push(img("q" + n, 400)); });
body.push(brk());

// E
body.push(H1("Section E — Numeracy, digit format"));
body.push(note("Recommended time: 4 minutes for 8 items. Find the missing number or operator. No calculator."));
[[29, "7  ?  3  =  21   — which operator replaces the question mark?", ["+", "−", "×", "÷"]], [30, "48  ÷  ?  =  6", ["6", "8", "7", "9"]], [31, "?  +  17  =  41", ["24", "26", "34", "23"]], [32, "9  ×  6  −  ?  =  40", ["12", "14", "16", "24"]], [33, "( 5  +  ? )  ×  3  =  36", ["6", "7", "8", "9"]], [34, "100  −  4  ×  ?  =  64", ["9", "8", "12", "16"]], [35, "?  ÷  4  +  5  =  12", ["24", "28", "32", "68"]], [36, "2  ×  ?  +  3  ×  4  =  30", ["7", "8", "9", "11"]]].forEach(([n, t, o]) => { body.push(Q(n, t)); OPTS(o).forEach(p => body.push(p)); });
body.push(brk());

// F
body.push(H1("Section F — Information handling"));
body.push(note("Recommended time: 4 minutes for 4 items. Answer using the shipment log below."));
body.push(table(["Shipment", "Origin", "Destination", "Weight (kg)", "Service", "Cost (EUR)"], [["S101", "Madrid", "Berlin", "12", "Express", "84"], ["S102", "Lyon", "Madrid", "30", "Standard", "62"], ["S103", "Berlin", "Lyon", "8", "Express", "71"], ["S104", "Madrid", "Lyon", "22", "Standard", "48"], ["S105", "Lyon", "Berlin", "15", "Express", "93"], ["S106", "Berlin", "Madrid", "40", "Standard", "75"]], [1400, 1500, 1700, 1600, 1500, 1500]));
[[37, "What is the total cost of all Express shipments?", ["EUR 233", "EUR 248", "EUR 256", "EUR 185"]], [38, "Which is the heaviest Standard shipment?", ["S102", "S104", "S106", "S105"]], [39, "What is the average weight of shipments originating in Madrid?", ["16 kg", "17 kg", "18 kg", "34 kg"]], [40, "Which shipment has the lowest cost per kilogram?", ["S102", "S104", "S106", "S101"]]].forEach(([n, t, o]) => { body.push(Q(n, t)); OPTS(o).forEach(p => body.push(p)); });
body.push(brk());

// G
body.push(H1("Section G — Answer key and worked reasoning"));
body.push(note("Check every item, not just the ones you missed: the reasoning shows the fastest route, which is what the time limit rewards."));
KEY.forEach(([sec, rows]) => {
  body.push(H2(sec));
  body.push(table(["#", "Answer", "Reasoning"], rows.map(([n, a, w]) => [String(n), "*" + a, w]), [700, 1500, 7000]));
  body.push(gap());
});
body.push(brk());

// H
body.push(H1("Section H — Strategy notes by format"));
TIPS.forEach(([t, pts]) => { body.push(H2(t)); pts.forEach(p => body.push(bullet(p))); });

const doc = new Document({
  creator: OWNER, lastModifiedBy: OWNER, title: "Aon-style Practice Workbook", subject: "Reasoning assessment practice — original material", description: "Prepared for " + OWNER,
  styles: { default: { document: { run: { font: FONT, size: 20 } } } },
  numbering: { config: [{ reference: "bul", levels: [{ level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 560, hanging: 280 } } } }] }] },
  sections: [{
    properties: { page: { margin: { top: 1300, bottom: 1200, left: 1300, right: 1300 } } },
    headers: { default: new Header({ children: [new Paragraph({ alignment: AlignmentType.RIGHT, children: [new TextRun({ text: "Aon-style Practice Workbook  ·  " + OWNER, font: FONT, size: 16, color: GREY })] })] }) },
    footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ children: ["Page ", PageNumber.CURRENT], font: FONT, size: 16, color: GREY })] })] }) },
    children: body,
  }],
});
Packer.toBuffer(doc).then(b => { fs.writeFileSync(process.argv[2], b); console.log("wrote", process.argv[2], b.length, "bytes"); });
