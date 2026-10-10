# Fig. 4 image-generation prompt

Built-in imagegen; 2026-10-08. Content follows the v2 sketch. Style references: Fig. 2 and the user-provided state/action diagram. This is a fixed-replay illustration, not an autonomous-selector evaluation. Native raster dimensions must be checked separately; resolution requests in the prompt are not output guarantees.

Create a beautifully polished English academic journal figure, an exact content-preserving restyling of reference image 1 (the approved Conic-Solver worked-trace sketch). Reference image 2 is the same paper's Fig.2: closely match its elegant serif typography, navy outlines and restrained light-blue/purple/teal palette. Reference image 3 is another architecture figure: only borrow clear grouping and flow, never its content.
Native highest-resolution output requested, ideally 3840 pixels wide or higher, landscape about 2.3:1. Pure white background, flat light pastel fills, crisp vector-like lines, no watermark, no title or figure number, no extra decorative network diagrams, no fabricated probabilities. Ensure all labels and formulas are perfectly legible, large, correctly typeset. Keep compact scientifically meaningful content.

Top strip exact problem: "Given: G: x² = ay, A = (1, 1/4), A ∈ G.    Query: q = Distance(A, Focus(G))."
Main structure left to right: large rounded outer state frame S₀; narrow RP card P₉; large outer state frame S₁; narrow RP card P₁₇; large outer state frame S₂. Each state frame contains an upper Abstract layer box and lower Symbolic layer box. Do NOT split abstract/symbolic into unrelated columns; keep paired within their own outer state. Abstract pale lavender-blue, symbolic pale blue, RP cards pale teal with navy headings. New facts use deep teal plus signs and bold text, inherited facts muted gray.

State S₀ upper text: "Abstract layer"; "Parabola · y-axis"; "Equation · Point on curve"; "Missing focus or focal distance".
State S₀ lower: "Symbolic layer"; "G: x² = ay"; "A = (1, 1/4), A ∈ G"; "Parameter and focal distance unknown".
State S₁ upper EXACTLY SAME abstract descriptors as S₀, no changes.
State S₁ lower: "Symbolic layer"; "Given facts retained"; "+ a = 4, p = 2"; "+ opening = up"; "+ Focus(G) = (0, 1)".
State S₂ upper: "Abstract layer"; "Parabola · y-axis"; "Equation · Point on curve"; "Target deficit removed".
State S₂ lower: "Symbolic layer"; "Facts from S₁ retained"; "+ FocalDistance(A, G) = 5/4".

In EACH state a vertical arrow upward from symbolic box to abstract box, label mathematical φ(S_i^sym, q) with correct i = 0,1,2 respectively.
Two transitions:
1. blue elbow arrow from S₀ ABSTRACT right boundary to TOP of P₉ card, labelled "Select". Separately dark thin arrow from S₀ SYMBOLIC right boundary to LEFT of P₉ card, labelled "Read". P₉ card text: "P₉"; "Recover parameters"; "Bind: G, A"; "1 = a/4"; "a = 4, p = 2". Outgoing coral/teal arrow from P₉ card RIGHT boundary to S₁ SYMBOLIC LEFT boundary labelled "Apply & update".
2. blue elbow arrow from S₁ ABSTRACT right boundary to TOP of P₁₇ card, labelled "Select". Separately dark thin arrow from S₁ SYMBOLIC right boundary to LEFT of P₁₇ card, labelled "Read". P₁₇ card text: "P₁₇"; "Focal distance"; "Bind: G, A"; "y_A + p/2"; "= 1/4 + 1 = 5/4". Outgoing coral/teal arrow from P₁₇ card RIGHT boundary to S₂ SYMBOLIC LEFT boundary labelled "Apply & update".
Place edge labels in clear whitespace; no arrow through words. If Apply & update needs space put below its RP card aligned with outgoing arrow. Every arrow direction matters.
Under S₀: "P₁₇ unavailable: prerequisites missing".
Under S₁: "P₁₇ applicable: prerequisites established".
From S₂ SYMBOLIC draw a short downward arrow to a small neat answer pill "Extract(S₂^sym, q) = 5/4".
Small readable footer: "Fixed-replay illustration; no selector ranking is asserted.  + New facts.  S₀ and S₁ have identical descriptor sets."
All math use correct Greek phi, subscript numerals, superscript sym, no escaped LaTeX text. Do not add geometry drawings, extra facts, query changes, color legends, training blocks, metrics, or extra steps. The semantic distinction between abstract selection and symbolic execution must remain obvious. Refine sizing and spacing from sketch to a compelling professionally balanced composition suited for a journal paper.
