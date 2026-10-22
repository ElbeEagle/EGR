# Fig. 1: Representative reasoning flows

Date: 2026-10-21
Generation: built-in imagegen, reference-based generation.
Reference: user-supplied three-panel diagram, codex-clipboard-375a3fac-ec06-4372-8b2d-9215ad4d8c9a.png.

## 本版内容

左栏仅显示居中的代数轨道；中栏为 G2G→G2A→A2A 的典型路径；右栏为 G2A→A2A→A2G→G2G→G2A→A2A。圆节点表示几何事实，圆角方节点表示代数表达或约束；不把节点等同于完整状态，不把箭头等同于一次 RP 应用。保留旧图及论文源码。

## LaTeX caption

```latex
\caption{Representative reasoning flows for (a) algebraic problem solving, (b) geometry problem solving, and (c) conic-section problem solving. Circles denote geometric facts, and rounded squares denote algebraic expressions or constraints. G2G and A2A advance reasoning within a track, while G2A and A2G transfer information between tracks. Panel (c) highlights how algebraic results establish geometric conditions that enable subsequent reasoning. These schematic flows illustrate selected solution structures rather than an exhaustive classification: geometry solving is not restricted to a one-way transfer into algebra, and individual conic-section solutions need not involve all four transformation types.}
\label{fig:reasoning_flows}
```

## Prompt

Create a high-resolution, publication-quality English scientific diagram for a Knowledge-Based Systems manuscript. Use the attached image as the PRIMARY layout and style reference, with the precise changes below. Generate at highest native resolution, ideally 3840 x 2160 pixels, landscape. Flat vector-like line work, white background, no watermark, no gradients, no shadows, no decorations. Black thin outlines and arrows, muted light blue circular nodes, pale peach rounded-square nodes. Refined serif text for track headings, transition labels and panel captions; bold clean sans serif inside the input/solution boxes. Large legible text, aligned rows, generous spacing. No formulas, RP IDs, system modules, neural networks or title banner.

COMPOSITION: three adjacent equally tall portrait panels arranged left-to-right in one wide figure, each with its own top "Problem Input" rounded box and bottom "Solution" rounded box. The first two panels have fine dash-dot borders; the third has a slightly heavier solid border. Keep all panel captions outside the border directly below the panels. A shared compact legend spans the bottom. Match the reference's simple restrained style. Use three node rows at consistent heights, with equal-size nodes throughout. The first panel may be slightly narrower than the other two if needed, but the three panels must look balanced.

PANEL (a), exact caption "(a) Algebraic Problem Solving":
IMPORTANT CHANGE FROM REFERENCE: remove the Geometric Track ENTIRELY from this panel. There must be only ONE centered track labeled "Algebraic Track", NO vertical divider, NO blue nodes, NO empty reserved geometry column. Center input box, track label, three peach rounded-square nodes and solution box on one vertical line.
Route: Problem Input -> peach node row 1 -> peach node row 2 -> peach node row 3 -> Solution.
Label row1-to-row2 arrow "A2A" and row2-to-row3 arrow "A2A". Input and final solution connectors are unlabeled. Interrupt the input connector around the track heading so it never crosses letters.

PANEL (b), exact caption "(b) Geometry Problem Solving":
Two tracks headed "Geometric Track" on left and "Algebraic Track" on right. A light gray dashed vertical divider between tracks, with small white gaps where horizontal arrows cross it.
Route: input goes into LEFT blue circle row1; vertical down arrow labeled "G2G" to LEFT blue circle row2; horizontal RIGHT arrow labeled "G2A" from LEFT blue circle row2 to RIGHT peach square row2; vertical DOWN arrow labeled "A2A" to RIGHT peach square row3; unlabeled connector to Solution.
No A2G arrow in this panel. No geometry circle row3. Avoid crossing headings with input connector.

PANEL (c), exact caption "(c) Conic-Section Problem Solving":
Same two tracks and dashed divider as (b). EXACT chronological route:
input -> LEFT blue circle row1
LEFT blue circle row1 --G2A--> RIGHT peach square row1
RIGHT peach square row1 --A2A downward--> RIGHT peach square row2
RIGHT peach square row2 --A2G LEFTWARD--> LEFT blue circle row2
LEFT blue circle row2 --G2G downward--> LEFT blue circle row3
LEFT blue circle row3 --G2A RIGHTWARD--> RIGHT peach square row3
RIGHT peach square row3 --A2A downward--> Solution.
The A2G arrow MUST point left. Do not add a direct vertical arrow connecting right row2 to right row3, because this would bypass the geometric reasoning. Do not add any upward or looping arrow. All track-internal reasoning arrows point down; cross-track arrows point horizontally. This zigzag route is the central message. Avoid connecting lines crossing any heading.

SHARED LEGEND below the panel captions, enclosed by a fine rectangular outline:
blue circle followed by "Geometric fact"
peach rounded square followed by "Algebraic expression"
"G2G / A2A: Intra-track"
"G2A / A2G: Cross-track"
Keep it compact and aligned, with four clearly separated entries.

At the very bottom add ONLY this small sentence:
"Representative reasoning flows; individual problems may follow different paths."
This is a conceptual comparison, not a universal classification. Do not add a long caption in the image; a full caption will be typeset separately in LaTeX.

Make the flow graph precise, polished and simple, with consistent stroke thickness, readable arrow labels and no text overlaps. Preserve the reference's minimalist academic character.

