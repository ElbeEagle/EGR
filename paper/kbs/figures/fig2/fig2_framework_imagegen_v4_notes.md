# Fig. 2 — three-stage architecture, v4

Mode: built-in imagegen, reference-based generation followed by a local formula correction.
Layout source: gemini-code-1792586895421.txt and the user's attached ASCII layout image.

## 结构与检查

左：题目输入及表征构建。中：双层表征、中央模式池、上方模式选择器、下方模式应用器。右：答案就绪检查、抽取及结果。符号层向上更新抽象层；抽象层供选择器预测；应用器读取符号层并通过独立反馈线写回；模式池以虚线分别支持选择与应用。答案检查读取当前状态，No 返回选择器，Yes 经终态抽取输出。状态特征数据流与就绪检查控制流同时展示，不表示检查前必须执行模式。

复核了主箭头方向、35 维描述子、80 个 RP、三类符号事实、四步应用及终态抽取公式。按用户的新布局恢复 Answer-Ready? 和 No: continue。保留 v1–v3，未修改论文源码。

## Generation prompt

Use case: infographic-diagram. Create a refined English academic architecture figure for Conic-Solver, following the supplied ASCII layout reference as a COMPOSITION guide, not its monospaced text style. Render at highest available native resolution, ideally 3840x2160 landscape. White background, black thin crisp rounded rectangles, dashed stage boundaries, understated pastel fills, readable serif math and clean bold headings. No watermark, gradients, shadows, complex decorations. Preserve correct subscripts/superscripts and Greek math symbols. Dense but beautifully spaced journal figure, not a slide. No top global title.

THREE STAGES arranged left to right: a narrow Stage 1 (17% width), a large Stage 2 (65% width), Stage 3 (18% width). Each stage has a thin dashed boundary and top heading. Main state-transform cycle is clockwise in Stage 2: symbolic bottom-left UP to abstract top-left, RIGHT to selector top-right, DOWN to applicator bottom-right, LEFT back to symbolic via the bottom feedback route. RP pool sits INSIDE the cycle at its center. The framework has four core components: the dual-layer representation, RP pool, selector, applicator.

STAGE 1 heading "1  Initialization".
Two small stacked white rounded boxes:
"Problem Input" with "x = (F, g)" and "Facts F · Goal g".
Down arrow to "Representation Constructor".
From constructor draw a rightward connection into the SYMBOLIC compartment in Stage 2, label "Initialize S₀". Initialization produces a dual-layer state by initializing symbolic facts then deriving abstraction; do not draw a bypass that makes abstract features independently invented.

STAGE 2 heading "2  Iterative Selection–Application Loop".
LEFT COLUMN: one tall outlined group titled "Dual-layer representation" and "𝓜(S_t)".
TOP compartment pale lavender: "Abstract Layer" / "S_t^abs" (proper superscript) / small line "35 binary descriptors".
Show a tiny vertical vector icon with 5 slots containing 0,1,1,…,0; clearly an illustrative abbreviated vector. Label b_t ∈ {0,1}^35. Do not show all 35 entries or descriptor group lists.
BOTTOM compartment pale warm orange: "Symbolic Layer" / "S_t^sym". Inside three small stacked white strips: "Objects & Expressions", "Geometric Relations", "Algebraic Constraints".
Between these compartments an UPWARD arrow from symbolic to abstract, labeled φ(S_t^sym, g), small "Abstraction update". Never draw an arrow from abstract down to symbolic.

RIGHT TOP module pale lavender: "Pattern Selector" with p_θ(P_i | S_t^abs), plus a SMALL simple neural-network icon if space permits.
Thick horizontal RIGHTWARD arrow from Abstract Layer to selector, label "b_t".
From selector right edge or lower-right edge, route a clean vertical downward arrow on right side of central pool to applicator, label "Top-k candidates 𝓒_t".
RIGHT BOTTOM module pale warm orange: "Pattern Applicator". Four ordered compact cells in a single row or a tidy two-row sequence:
"1  Role Binding"
"2  Check G_i"
"3  Execute A_i"
"4  Write-back W_i".
Show sequence arrows, keeping readable. Do not put shared primitives in a separate component.
Small unobtrusive line under steps: "Reject invalid instances; commit the first valid one".
THIN rightward read connection from Symbolic Layer to applicator at the same lower row, labeled "Read exact conditions".
SEPARATE THICK feedback arrow from applicator bottom, down into lower margin of Stage 2, LEFT, then UP into Symbolic Layer bottom. Label "Write back: S_t^sym → S_{t+1}^sym". This must be visually distinct from the read arrow and have arrowhead AT the symbolic layer. The two parallel routes never merge. On this feedback path add small annotation "Record provenance / accumulate τ".

CENTER between state column and selector/applicator column: pale green "RP Pool Λ" box with a minimal stacked-card icon, lines "80 reasoning patterns", "P_i = ⟨I_i, G_i, A_i, W_i⟩", "G2G · G2A · A2A · A2G". Two THIN DASHED knowledge arrows from pool to selector ("Candidate space") and from pool to applicator ("Pattern definitions"). These arrows must not collide with the main loop or labels. Pool cannot connect directly to symbolic state. Keep pool visually distinct but smaller than state and applicator.

STAGE 3 heading "3  Solution Extraction".
A diamond "Answer-Ready?" receives a THIN state-access connector from the symbolic layer routed in a bottom corridor BELOW the write-back feedback route, ending on the diamond from the left. Label this thin connector "Current state S_t, goal g". The readiness check must read the symbolic state, not the pool or selector.
Diamond YES branch downward labeled "Yes: S_T", to "Answer Extraction" box with Extract(S_T^sym, g).
Then down arrow to "Solution" box with "(â, τ)".
Diamond NO branch goes upward in the right-stage margin then LEFT along an upper reserved corridor into the selector TOP, label "No: continue". This shows iteration only when not answer-ready. Do not merge this with the top-k candidate arrow. No unlabeled floating arrows.
Right stage is compact and clean; state-check connector and feedback remain separate.
This is a schematic main-success workflow; do not add error output nodes or further decision diamonds.

VISUAL:
Abstract + selector in matching pale lavender; symbolic + applicator in matching pale orange; RP pool pale green; other components white. Black or navy text, mostly black connectors. Main clockwise loop thicker than state-read/knowledge connectors. All arrowheads unambiguous, no diagonal spaghetti, use orthogonal routes and no line-text overlaps. Ensure stage headings don't touch borders. Core math readable. Keep no more text than specified. Need a visually clear three-stage framework with a strong upper abstract-selection / lower symbolic-application correspondence.

## Correction prompt

Make exactly ONE typographic correction to the supplied scientific figure. In the rightmost Stage 3, inside the Answer Extraction box, replace the formula Extract(S_t^sym, g) with Extract(S_T^sym, g), using CAPITAL T as the subscript of S, indicating the terminal state. Keep superscript sym. All other letters, formulas, modules, colors, lines, arrows, layout, captions, diagram dimensions and spacing must stay unchanged. Do not change any lowercase t elsewhere. Preserve the preceding diamond branch label Yes: S_T. Render crisp at highest native resolution available, no watermark. This is only a local mathematical subscript correction.

