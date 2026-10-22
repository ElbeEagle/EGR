# Fig. 2 v5 — simplified state-transform architecture

Generation mode: built-in imagegen, editing fig2_framework_imagegen_v4.png. Prior versions preserved.

## 本版修改

右区采用 Answer Check & Extraction，并注明每轮检查；主循环使用粗实线，状态读取及控制分支减弱为灰色细线，知识支持保持细虚线。表示组件统一为 Problem Representation Model；抽象层改用横向示意向量。保留选择器中的三层神经网络图标与模式池卡片图标，去除模式池中的四种转换类型列表。应用器精简为 Bind → Check → Execute → Commit。初始化注明 S_0^sym，候选注明 Ranked top-k candidates。终态抽取使用 S_T^sym。

## 图注建议

Overview of Conic-Solver. The problem representation model maintains exact symbolic conditions and abstract descriptors. The selector ranks candidate patterns from the abstract layer, while the applicator reads the symbolic layer to bind, check, execute, and commit a valid pattern instance. The committed facts update the symbolic state and its abstraction for the next iteration. The reasoning-pattern pool supplies the candidate space and pattern definitions. Answer readiness is checked before each iteration; once the goal is satisfied, the answer is extracted from the terminal symbolic state and returned with the accumulated derivation. Bold arrows emphasize the state-transform cycle; thinner connections indicate state access, control, and knowledge support.

## Prompt

Use case: precise-object-edit. Refine the attached English scientific architecture figure into a cleaner publication-quality Conic-Solver overview. Keep its three-zone composition, four core components, clockwise loop, pastel lavender abstract/selector, pale orange symbolic/applicator, green RP pool, white background and dashed boundaries. Preserve mathematical meaning and connector topology. Generate at maximum native resolution, ideally 3840 x 2160 pixels, no watermark. Crisp text, flat fills, clean vector-like lines. No added decorative elements.

Apply exactly these improvements:
1. Right zone heading becomes "Answer Check & Extraction", wrapped on two lines to fit. REMOVE the leading 3 from this heading, since readiness checking occurs every iteration. Under the heading add small "Check before each iteration". Keep diamond Answer-Ready?, its No: continue branch returning to selector and its Yes: S_T branch leading down to Answer Extraction and Solution. Keep extraction formula EXACTLY Extract(S_T^sym, g), CAPITAL T.
2. The four main clockwise connectors should dominate: Symbolic Layer UP to Abstract Layer; Abstract Layer RIGHT to Pattern Selector; selector DOWN to applicator; applicator feedback LEFT and UP into symbolic layer. Make these dark navy/black solid strokes approximately twice as thick as support lines. Make the independent "Read exact conditions" line, the bottom state-access line to readiness diamond, and the No: continue control return THIN muted gray, while their text remains legible dark gray. Keep RP pool knowledge links thin dashed. Maintain separate state read and state write-back routes. Do not add any new arrows.
3. Replace heading "Dual-layer representation" with "Problem Representation Model", allowed to wrap over two lines. Subtitle "Dual-layer state 𝓜(S_t)" below it.
4. In Abstract Layer remove the tall vertical 0/1 vector icon. Replace it by compact HORIZONTAL math:
b_t = [0, 1, 1, …, 0] ∈ {0,1}^35.
Keep "Abstract Layer", S_t^abs, and "35 binary descriptors". Use real subscripts/superscripts. Compact the abstract compartment modestly and use freed space for clear separation and readable abstraction arrow φ(S_t^sym,g); do not enlarge surrounding blank regions excessively.
5. Keep the neural network icon inside the Pattern Selector in its SAME location under probability formula, and SAME layered arrangement (three inputs, three hidden nodes, one output). Make it slightly smaller, perfectly aligned, with clean straight thin connections only between adjacent layers. No new labels on the icon. Keep p_θ(P_i | S_t^abs).
6. In RP pool KEEP the stacked-card icon and make it crisp. REMOVE ONLY the row "G2G · G2A · A2A · A2G". Rename its heading "Reasoning-Pattern Pool Λ", using two lines if necessary. Keep "80 reasoning patterns" and P_i=⟨I_i,G_i,A_i,W_i⟩. Reduce box height to eliminate empty space after removing the row. Keep it inside the loop and keep Candidate space and Pattern definitions links.
7. Simplify the Pattern Applicator interior: remove the four individually boxed numbered steps and the long reject sentence. Instead use one large, highly legible centered line:
"Bind → Check → Execute → Commit"
Keep title "Pattern Applicator". No other interior sentence is needed. The exact executable details are explained in another figure. Do not remove incoming candidates, exact conditions, pattern definitions or outgoing write-back line. The applicator should feel clean, comfortably spaced, and still substantial enough to anchor the bottom-right of the loop.
8. Initialization arrow label becomes "Initialize S₀^sym" (proper superscript sym). Keep Problem Input x=(F,g), Facts F · Goal g, Representation Constructor.
9. Selector-to-applicator arrow label becomes "Ranked top-k candidates 𝓒_t", split over two lines with no overlap with the line or neighboring pool.
10. Bottom feedback main label stays "Write back: S_t^sym → S_{t+1}^sym". Replace small text "Record provenance / accumulate τ" with "Record derivation τ".
11. State-access connector to Answer-Ready? must begin at the BOTTOM edge of the Symbolic Layer compartment itself, not at the outer representation container. Keep this a distinct thin line routed in the bottommost corridor below the thick write-back loop. Label it "Current state S_t, goal g". Avoid merging or crossing lines. In particular this read line must not appear to originate from applicator, selector or pool.
12. Solution box still displays (â, τ). Stage 1 and 2 headings can stay "1 Initialization" and "2 Iterative Selection–Application Loop". Keep all lettering English.

Optimize alignment, legibility and white space without redesigning the architecture. Preserve every existing mathematical subscript other than explicitly requested changes; never confuse S_t with S_T. The functional loop and two supporting layers should be obvious at a glance. No captions or legend outside the three zones.

