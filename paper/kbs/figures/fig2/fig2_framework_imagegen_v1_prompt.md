# Fig. 2 generation prompt

Generated with the built-in imagegen tool on 2026-10-08. The approved v2 sketch supplies the content; the three images in ../ref supply style references only. Output is a raster PNG, not an editable vector drawing.

Create a polished English scientific architecture figure for the Conic-Solver research paper, using image 1 as the AUTHORITATIVE CONTENT AND CONNECTIVITY sketch. Images 2–4 are STYLE REFERENCES ONLY; do not copy their model names, networks, examples or extra mechanisms.

Use case: infographic-diagram. Final journal figure, clean original academic vector-like design on pure white background, precise crisp thin outlines, elegant restrained pastel fills, professional typography, spacious but compact layout. Landscape aspect ratio around 2:1, request native high resolution 3840 x 1920 or highest available. No watermark, logos, caption, figure number, large title, gradient, shadows, 3D effects, decorative brain/robot icons. All text in English, sharp and readable at double-column width. Beautiful modern scholarly schematic with meticulous alignment and generous text-to-arrow clearance.

Preserve the sketch's topology EXACTLY while improving aesthetics. Composition: left compact input; center-left a grouped dual-layer representation; center-right selector above applicator; far-right RP pool; bottom extraction and output.
Required nodes and exact texts:
1 "Formal input" with "Facts F, query q".
2 enclosing group heading "Problem representation model". Upper inner box "Abstract layer" with math S_t^{abs} and small descriptor-vector strip (schematic, no numbers); lower box "Symbolic layer" with math S_t^{sym} and subtitle "Exact facts". Use pale blue state group, two distinct light blue intensities.
3 "Pattern selector" with equation p_θ(P_i | S_t^{abs}). Muted lavender.
4 "Pattern applicator" with "Apply (P_i, θ)". Pale teal. NO internal step list.
5 "RP pool" with "Λ: 80 patterns". Pale sand, small understated stack-of-pattern-cards motif permitted within this node.
6 "Answer extraction" with equation Extract(S_T^{sym}, q).
7 "Output" with "Answer â + trace τ".

Directed connections, all required:
Formal input -> Symbolic layer, label "Construct".
Symbolic layer -> Abstract layer vertically upward inside group, label φ(S_t^{sym}, q).
Abstract layer -> Pattern selector.
Pattern selector -> Pattern applicator vertically downward, label "Ranked RPs".
Symbolic layer -> Pattern applicator horizontally right, label "Read state".
RP pool -> Pattern selector, label "Pattern IDs".
RP pool -> Pattern applicator, label "Definitions".
Pattern applicator -> Symbolic layer using clearly visible teal return arrow looping beneath the main nodes, label "Update state: S_t → S_{t+1}". Arrowhead MUST point into the SYMBOLIC layer, not abstract layer.
Symbolic layer -> Answer extraction along a lower path separate from update loop, label "Final state S_T".
Answer extraction -> Output.
Pattern applicator -> Output along a separate clean path, label "Derivation trace".

Avoid line crossings; preserve distinct update and final-output routes. No arrow should pass through text or unrelated boxes. Each edge ends at its correct box boundary. Use subtle semantic colors for major paths and dark slate text with strong contrast. Primary reading order and learning/execution loop dominate. Use precise typesetting for Greek θ, φ, Λ, τ; superscripts abs and sym; subscripts t and T; hat on a. No extra content, in particular DO NOT include "Answer-ready?", "Reject", "Unresolved", "No: continue", symbolic primitives, LLM, entropy, parser, training pipeline, metrics, empirical numbers or invented mathematical examples. Only a polished, publication-oriented rendering of this approved simplified architecture.
