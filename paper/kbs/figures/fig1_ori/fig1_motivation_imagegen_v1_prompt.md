# Fig. 1 imagegen rendering

Mode: built-in imagegen; reference-based generation followed by geometry refinement.

References: fig1_motivation_sketch_v1.png and ../fig2/fig2_framework_imagegen_v2.png.

Note: Equations and conclusions checked. Generated ellipse drawings remain schematic, not exact scale constructions. Native pixel dimensions should be considered when preparing the submission; this is a raster image, not a vector export.

## Generation prompt

Create a polished English scientific manuscript figure from reference image 1 (approved content/layout sketch), using reference image 2 ONLY for visual style: refined dark navy typography, restrained pastel lavender/teal/sand accents, thin outlines, ample white space, exceptionally readable mathematical typography. Output at the highest available native resolution. White background, no watermark, no top title or figure number, no decorative icons, no shadows or 3D effects. This is a motivation figure, not a system architecture. Use three equal-width side-by-side panels, with a small gap between them. Do NOT connect panels with arrows: they illustrate related concepts, not a sequential computation. Each panel has a short bold header, precise mathematical example, and a distinct bold conclusion in a pale tinted bottom strip. Align all conclusion strips. Match publication-quality vector-style typesetting. Use the exact content below, preserving mathematical correctness. Avoid unnecessary repeated text. All text must be English.

Panel (a), title "Geometric roles determine algebraic identities".
Given: x²/m + y²/4 = 1, |F₁F₂| = 2.
Small note: "Two alternative given conditions".
Two separate side-by-side case cards:
Left: "Foci on x-axis". A small mathematically accurate ellipse centered at origin with horizontal semiaxis √5 and vertical semiaxis 2, thin x/y coordinate axes, two foci on the horizontal axis at ±1. Show m = a², 4 = b², then boxed m = 5.
Right: "Foci on y-axis". Small mathematically accurate ellipse centered at origin with horizontal semiaxis √3 and vertical semiaxis 2, thin x/y coordinate axes, two foci on vertical axis at ±1. Show 4 = a², m = b², then boxed m = 3.
These ellipses should be subtly wider/taller, not exaggerated; both are near-circular. Color corresponding major-axis parameter identities consistently. Under the two cards show common relation c = 1, a² = b² + c².
Panel conclusion: "Roles determine parameter meaning."

Panel (b), title "Algebraic results establish geometric conditions".
Given: G: x²/9 + y²/4 = 1.
Vertical sequence of three clean equation boxes with slender downward arrows:
a² = 9, b² = 4
c² = a² − b² = 5
Foci(G) = {(-√5, 0), (√5, 0)}
Below show an accurate horizontal ellipse centered at origin with semiaxes 3 and 2, x/y axes, foci at (-√5,0) and (√5,0), each small colored focus dot accurately placed well inside the left/right vertices. Caption "Derived foci". Use teal to emphasize the derived objects.
Panel conclusion: "Parameters establish geometric objects."

Panel (c), title "The query determines which information is needed".
Note "Same given curve; different queries".
Given: G: x²/9 + y²/4 = 1.
Two parallel query cards, with independent paths:
Left card header "Eccentricity"; q = e; downward arrow; "Need a, c"; a = 3, c = √5; then e = c/a = √5/3.
Right card header "Major-axis length"; q = L; downward arrow; "Need a"; a = 3; then L = 2a = 6.
Below both cards, a clear compact gray note: "For L, neither c nor the foci need to be derived."
Panel conclusion: "Queries determine relevant dependencies."

At the very bottom, outside panels, a single restrained sentence:
"Each reasoning step depends on geometric roles, established facts, and the query."

Aim for elegant, high-impact journal figure quality: balanced three-panel composition, compact but highly legible equations, consistent font sizes, harmonious muted color accents, minimal visual clutter. Do not add modules, inference-pattern names, projection names, or claims beyond this content. This is a final polished rendering of the approved sketch, not a sketch.

## Refinement prompt

Edit this scientific figure. Preserve all text, equations, three-panel layout, colors, and typography exactly. Correct ONLY the three ellipse diagrams so they use equal x/y unit scales and mathematically accurate geometry. Panel a left ellipse x²/5+y²/4=1 must be almost circular, width/height ratio sqrt(5)/2 = 1.118, focus offsets from center equal 0.4472 times horizontal semiaxis. Panel a right ellipse x²/3+y²/4=1 must be almost circular, width/height ratio sqrt(3)/2 = 0.866, focus offsets equal 0.5 times vertical semiaxis. Panel b ellipse x²/9+y²/4=1 must have width/height ratio 1.5, focus offsets equal sqrt(5)/3 = 0.74536 times horizontal semiaxis. Fit each diagram inside its existing white region without overlapping text. Use thin navy curves, gray axes, colored focus dots. Preserve absolutely every formula and all labels. Render at highest native resolution, ideally 3840 pixels wide, crisp publication-quality English text, no watermark.

