# Fig. 2 — selection–application loop, v3

Mode: built-in imagegen, new rendering. Previous versions preserved.

## 本版结构

横向主线为输入、当前双层状态、模式选择器、模式应用器及后继状态；底部单条粗线将后继状态送入下一轮。上方 RP pool 以虚线向选择器提供候选空间、向应用器提供模式定义。抽象层供选择器使用，符号层以独立细线供应用器读取。应用器提交有效事实并记录来源；后继状态刷新抽象表示。Updated state 是结果卡片，不是第五个核心组件。答案出口从终态读取结果；图省略失败与候选重试分支，初态已可回答的情况由正文算法处理。

## Suggested caption

Overview of Conic-Solver. The problem representation model maintains the symbolic conditions and their abstract descriptors. The pattern selector ranks candidate reasoning patterns from the abstract layer, and the pattern applicator binds, checks, executes, and commits a valid pattern instance using the symbolic layer. The resulting state refreshes the abstract descriptors and enters the next selection–application iteration. The RP pool defines the candidate space and supplies executable pattern definitions. Upon reaching an answer-ready state, the solver extracts the answer and returns it with the accumulated derivation. Thick arrows emphasize the iterative workflow, while thinner connections show state access, knowledge support, and terminal output.

## Generation prompt

Use case: infographic-diagram. Generate a new high-resolution scientific architecture figure for a Knowledge-Based Systems paper. Highest native resolution available, target 3840 x 2160 pixels, landscape. The reader must immediately see "SELECT → APPLY → UPDATE → SELECT AGAIN". Secondary reading reveals the dual-layer state and RP pool support. Elegant simple academic diagram, white background, thin precise navy outlines, restrained flat pale blue/lavender/teal/sand fills, large highly legible English typography, no decorative icons, gradients, shadows, gears, bar charts, neural network cartoons, watermark, or figure number. Favor generous spacing and a few short labels.

EXACT ARCHITECTURE:
A main horizontal row from left to right:
small Input box → large Problem representation model → Pattern selector → Pattern applicator → smaller Updated state card.
A SINGLE thick navy feedback path under the entire main row returns FROM Updated state TO Problem representation model, with one arrowhead at the state end. Label feedback prominently "Next iteration: select → apply → update". This feedback path is lower than every other connector, with clean orthogonal routing. Never point the feedback to Input.
Above selector/applicator, one sand-colored Reasoning-pattern pool box supports BOTH via thin dashed connectors.
At far right BELOW Updated state and to the right of the feedback route, a small output box is reached via a thin exit branch "When answer-ready" / "Extract answer".
Do not place pool in series with the main workflow. The four core components are Problem representation model, Reasoning-pattern pool, Pattern selector, Pattern applicator. Updated state is a compact result card, not a fifth major processing module.

MAIN ROW DETAILS:
1. Input: compact white box "Input" / "Facts F, goal g". Thin arrow to the SYMBOLIC LAYER in state, labeled "Initialize". This arrow represents initial construction.
2. Pale blue large outer box titled "Problem representation model", subtitle "Current state S_t".
Inside two stacked white compartments:
TOP: "Abstract layer" / "S_t^abs: descriptors"
BOTTOM: "Symbolic layer" / "S_t^sym: exact conditions"
A thin upward arrow from Symbolic to Abstract labeled "φ(·, g)" clearly represents deterministic abstraction. Render all mathematical symbols with true subscripts and superscripts, not literal caret notation.
Main thick rightward arrow from TOP abstract compartment to selector, label "State features".
A SECONDARY THIN gray or muted navy connector from BOTTOM symbolic compartment routes UNDER the selector and enters the bottom of the applicator, labeled "Exact conditions". It must NOT connect to the selector. Route this line above the main bottom feedback line and avoid any crossings.
3. Lavender box "Pattern selector", small subtitle "Select", equation p_θ(P_i | S_t^abs).
Thick rightward arrow to applicator labeled "Ranked candidates".
4. Teal box "Pattern applicator", small subtitle "Apply".
Inside, two short lines: "Bind → Check" and "Execute → Write back".
Thick rightward arrow to Updated state labeled "Commit valid step".
The applicator is the only component that commits new symbolic facts.
5. Updated state card with plain light outline and very light blue fill, smaller visual weight than core modules:
title "Updated state"
"S_{t+1} = (S_{t+1}^sym, S_{t+1}^abs)"
small line "Refresh abstraction"
This is the produced successor state, no standalone update engine.
From this card draw the single outer feedback arrow back to current-state outer box, entering its lower-left edge without crossing the symbolic input/read connectors.
6. Small output box in lower right, pale green or plain white:
"Output"
"Answer â + derivation τ"
The exit branch comes FROM UPDATED STATE, not from selector or pool, and is labeled "When answer-ready" and "Extract answer". Draw no decision diamond, failure branch, rejection loop, or repeated readiness boxes.
Under the applicator in small gray text put "Committed steps accumulate in τ"; this is explanatory text, not a separate arrow or processing module.

TOP KNOWLEDGE SUPPORT:
Sand box "Reasoning-pattern pool" / "Λ: 80 patterns" / "G2G · G2A · A2A · A2G".
Two thin DASHED downward connectors: one into selector labeled "Candidate space"; one into applicator labeled "Pattern definitions". Keep labels above main row, separated from main arrows. Pool never updates state directly.

VISUAL HIERARCHY:
Main selection/application/state feedback arrows are dark and about twice the thickness of support links. Static knowledge links dashed; state data read link thin solid. Only the four core components use pronounced tinted boxes and bold headings. Keep input, result card and output smaller and neutral. Align primary modules along a clear left-to-right axis, so the large lower loop is immediately understandable. Use one navy arrow color, not rainbow arrows. No large global title, no elaborate legend, no extra unrelated text.
Critical: symbolic layer feeds applicator directly; abstract layer feeds selector; selector sends ranked candidates; pool supports selector and applicator; valid application produces successor state with refreshed abstraction; successor feeds back for next iteration; final answer is extracted from a terminal state. Use g consistently for solving goal. Do not label geometric versus algebraic tracks as the two layers. Do not show symbolic primitives.

