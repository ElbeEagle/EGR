# Fig. 4 v2 — 双层状态与执行轨迹

日期：2026-10-21

## 文件与用途

- `fig4_trace_imagegen_v2.png`：通过 imagegen 生成的新版论文轨迹图；保留 v1。
- 本文档：记录图的设计约束、数学内容和生成提示词。

## 本版调整

- 保留 S0 → RP9 → S1 → RP17 → S2，突出具体的候选、符号读取、应用和提交。
- S1 的 Focus 描述子由 0 变为 1；目标缺口仍为 1。S2 在距离求出后将目标缺口改为 0。
- 新增事实使用深青色及加号，保留事实使用灰色；应用卡分为 Bind / Check、Execute、Commit。
- 候选及检查为示意内容，不表示真实模型排名、概率或已验证的自主执行记录。
- RP17 的可执行依据为已建立的 p=2、开口向上和 A 在曲线上，不将焦点坐标当作该公式执行的必需输入。
- 统一目标符号 g；答案抽取不包含额外推导。

## 数学核对

G: x²=ay，A=(1,1/4)，A∈G。因此 1=a/4，a=4；按 x²=2py 得 p=2，开口向上，焦点为 (0,1)。焦半径 y_A+p/2=1/4+1=5/4。

图中 Bind / Check 的 Positive branch verified 是应用过程的核验摘要，依赖系数求解结果，不应理解为 S0 已知开口方向。

## 生成提示词

Create a polished English scientific figure for a Knowledge-Based Systems journal paper. This is Fig. 4, a concrete dual-layer state-transition trace for Conic-Solver. Use the attached old figure only as a structural reference; comprehensively redesign the spacing and correct its contents according to the instructions below. Render at the highest available native resolution, ideally 3840x2160 landscape, crisp mathematical typography, white background, no watermark, no decorative illustration, no title "Fig. 4" or full caption inside the image.

PURPOSE: A reader immediately follows S0 -> RP9 instance -> S1 -> RP17 instance -> S2, and sees how abstract descriptors propose patterns, symbolic checks determine applicability, execution derives new facts, and committing those facts refreshes the abstract state. This is an illustrative mathematical trace, NOT an empirical selector evaluation.

LAYOUT: Five columns horizontally: three wider state cards S0, S1, S2, separated by two sufficiently wide application cards. Each state has an upper pale lavender Abstract layer and a lower pale apricot Symbolic layer, with a vertical upward arrow labeled phi(S_t^sym,g) between them. Equal vertical alignment across the three states. Generous margins, whitespace and readable print-sized text. State cards have light gray outer boundaries, dark navy thin outlines. Intervening RP cards have a small candidate annotation at the top and a pale warm-neutral application block below. Use coherent restrained typography: clean sans serif labels and proper serif mathematical notation. No gradients, shadows, textures or 3D. Pale lavender abstract layer, pale orange symbolic layer, dark teal new facts and descriptor changes. All English labels spelled correctly.

HEADER BAND:
"Given: G: x² = ay, A = (1, 1/4), A ∈ G.    Goal: g = Distance(A, Focus(G))."
Use proper mathematical typesetting of superscripts, subscripts and fractions.

S0 upper:
"Abstract layer"
small "Selected descriptors"
"Parabola · y-axis"
"Equation · Point on curve"
"Focus: 0"
"Missing focus or focal distance: 1"
S0 lower:
"Symbolic layer"
"G: x² = ay"
"A = (1, 1/4), A ∈ G"
small gray "Parameters and opening unknown"

BETWEEN S0 AND S1:
Above the application block place a small lightweight area titled "Illustrative candidates" with three short rows:
"RP17: prerequisites missing"
"RP10: downward branch inconsistent"
"RP9: valid instance"
These rows must NOT be numbered or display probabilities/rank. An abstract-layer outgoing arrow labeled "Propose" leads to this area. A short arrow leads to RP9 application below.
Application block heading "RP9 — Recover parameters".
Three compact sections divided by thin rules:
"Bind / Check"
"G, A; equation and incidence"
"Positive branch verified"
"Execute"
"1 = a/4 ⇒ a = 4"
"x² = 2py ⇒ p = 2"
"Commit"
"Parameters, opening, focus"
Do not suggest opening direction was known before execution; the positive branch is verified from the recovered coefficient.
A thin gray arrow from S0 symbolic layer into RP9 labeled "Read".
A stronger dark orange arrow from RP9 to S1 symbolic layer labeled "Commit".

S1 upper:
"Abstract layer"
small "Selected descriptors"
"Parabola · y-axis"
"Equation · Point on curve"
"Focus: 0 → 1" (bold dark teal)
"Missing focus or focal distance: 1"
S1 lower:
"Symbolic layer"
gray "Given facts retained"
dark teal:
"+ a = 4, p = 2"
"+ opening = up"
"+ Focus(G) = (0, 1)"
Immediately below S1, a concise teal annotation "RP17 enabled: p = 2 and opening = up".
Upward phi arrow ties new symbolic facts to changed abstract descriptor.

BETWEEN S1 AND S2:
Small top area titled "Candidate check"
"RP17: prerequisites satisfied"
An arrow from S1 abstract layer labeled "Propose" leads to this area and then down to application.
Application heading "RP17 — Focal distance"
Three sections:
"Bind / Check"
"G, A; A ∈ G"
"p = 2, opening = up"
"Execute"
"|AF| = y_A + p/2"
"= 1/4 + 1 = 5/4"
"Commit"
"Requested distance"
Here F denotes Focus(G), defined briefly as "F = Focus(G)" inside this card if needed.
Thin gray Read arrow from S1 symbolic to RP17. Strong dark orange Commit arrow from RP17 to S2 symbolic.

S2 upper:
"Abstract layer"
small "Selected descriptors"
"Parabola · y-axis"
"Equation · Point on curve"
"Focus: 1"
"Missing focus or focal distance:"
"1 → 0" (bold dark teal)
S2 lower:
"Symbolic layer"
gray "Facts from S1 retained"
dark teal "+ Distance(A, Focus(G))"
dark teal "= 5/4"
Below S2 a small "Answer-ready" label and downward arrow from its SYMBOLIC layer to a modest box:
"Extract(S₂^sym, g) = 5/4"

ARROW SEMANTICS:
Propose arrows muted purple from abstract to candidate labels.
Read arrows thin gray from symbolic to application.
Commit arrows thicker dark orange to NEXT state's symbolic layer.
Refresh arrows vertical upward within each state.
No crossing arrows, no arrow through text, no accidental shortcut from abstract directly to result.
State time left-to-right. Keep application cards large enough that Bind / Check, Execute, Commit can be read.

FOOTNOTE across bottom, small but legible:
"Illustrative candidates; no selector ranking is asserted. Only selected descriptors are shown. + denotes newly committed facts."
Do NOT repeat the old false footnote "S0 and S1 have identical descriptor sets". Do not add directrix steps, G2G, performance scores, neural network icons, RP pool or shared symbolic primitives. This is a trace, not an architecture figure. Preserve accurate math and state indices above all else.

