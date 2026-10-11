# Fig. 1: Two reasoning strands

Date: 2026-10-11
Mode: built-in imagegen, new image.
Source: paper/doc/Geometry-Algebra perspective.md, example in Section II.

## Design

左右纵向双带：左几何、右代数，按箭头顺序向下阅读。颜色与 G2G/G2A/A2A/A2G 文字共同区分推理形式。七张内容卡片不是七次 RP 应用；六条箭头展示微观推理转换。原文识别开口方向、确立焦点和准线合并为一个 A2G 转换。左下角为几何关系示意，非精确比例作图。

## Checks

题目 x²=ay、A=(1,1/4)，得到 a=4、p=2、F=(0,1)、准线 y=-1；焦半径等于点到准线距离，结果为 5/4。四种箭头方向、公式与最终答案经人工视觉核对。此文件记录生成过程，不修改论文正文或模型实现。

## Prompt

Use case: scientific-educational.
Create a polished English journal-paper motivation figure illustrating ONE exact conic-section solution as a continuous route through TWO VERTICAL REASONING LANES. Highest native resolution, target 2400 x 2600 pixels if available. White background, crisp vector-like drawing, no watermark, no figure number, no decorative title. Refined navy serif mathematical typography, restrained pale blue left lane and pale lavender right lane, ample space for arrows. This is a reasoning explanation, NOT an AI architecture. No selector, RP IDs, neural networks, abstract/symbolic layers, or extra classifications.

MAIN DESIGN:
Two parallel vertical lanes, left header "Geometric reasoning", right header "Algebraic reasoning". Chronological progress goes down the page. Lane backgrounds very pale, individual content cards white with thin outlines. A generous central gutter allows prominent horizontal arrows with labels. All actual inference arrows must have visible arrowheads and one of exactly four labels, color and text redundant: G2A teal #138C87 (rightward); A2G ochre #B97B24 (leftward); G2G blue #376CA6 (downward in left lane); A2A violet #8060B0 (downward in right lane). Make these four forms the dominant visual feature.

Above lanes, a compact full-width problem strip:
"Given: parabola G: x² = ay through A(1, 1/4).    Find: |AF|, where F is the focus."
Render fractions properly as math. This supplies both the geometric and algebraic data. No inference arrows from this strip are needed.

EXACT ROUTE: seven content cards, connected by exactly six main arrows. Use tiny neutral numbered circles 1 to 7 to clarify reading order. Arrange as follows:
ROW 1: LEFT card 1 "Point on the parabola" with large "A ∈ G". RIGHT card 2 "Incidence constraint" with large "1 = a · 1/4". Horizontal teal arrow from card 1 to card 2, labeled prominently "G2A" and small "Substitute coordinates".
ROW 2: RIGHT card 3 "Recovered parameters" with "a = 4,    x² = 4y" and "2p = 4,    p = 2". Vertical violet arrow from card 2 down to card 3, labeled "A2A", small "Solve and compare coefficients".
ROW 2: LEFT card 4 "Established geometric facts" with three lines: "Opens upward", "Focus F = (0, 1)", "Directrix ℓ: y = −1". Horizontal ochre arrow FROM RIGHT card 3 TO LEFT card 4, pointing LEFT, labeled "A2G", small "Interpret the standard form".
ROW 3: LEFT card 5 "Parabola definition" with large "|AF| = d(A, ℓ)". Vertical blue arrow from card 4 down to card 5, labeled "G2G", small "Relate geometric distances". This uses the retained fact A ∈ G and the established focus/directrix.
ROW 3: RIGHT card 6 "Distance expression" with large "d(A, ℓ) = |y_A + 1|". Horizontal teal arrow from card 5 to card 6, labeled "G2A", small "Express distance in coordinates".
ROW 4: RIGHT card 7 "Requested focal distance" with large "|AF| = |1/4 + 1| = 5/4". Light green fill for this answer card. Vertical violet arrow from card 6 down to card 7 labeled "A2A", small "Evaluate".

ROW 4 LEFT: a small explanatory geometric illustration ONLY, no arrows connecting it to route: parabola x²=4y opening upward, origin (0,0), focus F at (0,1), point A at (1,1/4) on the right branch, horizontal dashed directrix y=-1, H=(1,-1) foot of perpendicular from A. Show segments AF and AH with matching tick marks representing equal lengths. A must be BELOW F in height and to its right; directrix is below origin. Label F, A, H and ℓ; keep this diagram mathematically correct, thin elegant strokes, equal coordinate scales, no unnecessary tick labels. Put a tiny caption "Geometric meaning of |AF| = d(A, ℓ)" underneath. Do not add an extra inference arrow into this illustration.

BOTTOM LEGEND, separate from lanes, four compact entries with arrows showing correct directions:
blue down "G2G  Geometric deduction"
teal right "G2A  Algebraic formulation"
violet down "A2A  Algebraic reasoning"
ochre left "A2G  Geometric interpretation"
Arrange as a tidy 2x2 legend with legible labels.
Bottom single short sentence: "Reasoning advances within and between the two strands."

Critical constraints: maintain all six connector directions; no straight downward connectors between disconnected left/right cards other than specified. Route is left-to-right, down-right, right-to-left, down-left, left-to-right, down-right. Do NOT add a loop arrow. p is defined through standard form x²=2py with p>0 for this upward parabola. The initial coefficient a is not a semiaxis. Never write p=4 or focus=(0,2). All formulas, labels and geometry must be correct. Fit labels without crossing text or borders. Balanced compact academic composition, readable at manuscript size.

