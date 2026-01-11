# Verification Report: Theorem Sequence Correspondence

**Date**: 2026-01-11
**Sample Size**: 80 Problems
**Source**: `sampled_problems.md`

## Overview
This report summarizes the manual inspection of 80 randomly sampled problems to verify if the textual "Process" (solution) corresponds to the annotated "Theorem Sequence".

## Summary of Findings
- **High Correspondence**: For the majority (~80-90%) of the sampled items, the Theorem Sequence accurately reflects the mathematical steps and formulas used in the Process text.
- **Key Algorithms Identified**: Complex methods like "Point Difference Method" (点差法) and "Homogenization" (齐次化) are correctly tagged in most cases.
- **Minor Discrepancies**:
    - **Cross-Curve Tagging**: Some problems involving one curve (e.g., Parabola) occasionally contain tags for another (e.g., `Ellipse_Equation_Standard_X`), likely due to noise or multi-curve context in training.
    - **Vector Conditions**: The distinction between `Vector_Perpendicular_Condition` and `Vector_Collinear_Condition` is sometimes blurred in the annotations.
    - **Implicit Steps**: Some geometric steps (like "midpoint implies distance") are sometimes tagged with specific theorems and sometimes not.

## Detailed Examples Analysis

### 1. Perfect Match
**Problem ID**: 2521 (Index 369)
*   **Text**: Parabola $y^2=2px$, chord slope $\sqrt{5}$, midpoint y-coordinate $\sqrt{10}$.
*   **Process**: Uses $k = \frac{2p}{y_1+y_2}$ (derived from point difference).
*   **Theorems**: `Parabola_Equation_Standard_Right`, `Point_Difference_Method`, `Slope_Formula`.
*   **Verdict**: **Consistent**. The tag `Point_Difference_Method` precisely captures the core logic.

### 2. Minor Inconsistency (Phantom Tag)
**Problem ID**: 7729 (Index 1032)
*   **Text**: Interaction between Parabola $C_1$ and Parabola $C_2$.
*   **Process**: Uses definition of parabola ($P$ to Focus = $P$ to Directrix).
*   **Theorems**: `Ellipse_Equation_Standard_X`, `Parabola_Equation_Standard_Right`, `Parabola_Definition`.
*   **Verdict**: **Partial Mismatch**. The `Ellipse_Equation_Standard_X` tag is irrelevant/incorrect for a pure parabola problem. The other tags are correct.

### 3. Ambiguous Tagging
**Problem ID**: 55 (Index 18)
*   **Text**: Hyperbola, circle diameter, $90^\circ$ angle.
*   **Process**: Uses perpendicularity ($k \cdot k' = -1$) and asymptotic symmetry.
*   **Theorems**: `Hyperbola_Equation_Standard_X`, `Vector_Collinear_Condition` (ID 62).
*   **Verdict**: **Questionable**. The process uses perpendicularity (ID 61 `Vector_Perpendicular_Condition`), but the tag is ID 62 `Vector_Collinear_Condition`. This suggests confusion in the model or annotation between collinear and perpendicular vector conditions in this context.

### 4. Logic Alignment
**Problem ID**: 4719 (Index 681)
*   **Text**: Hyperbola, sum of focal radii $|PF_1| + |PF_2| = 2\sqrt{5}$.
*   **Process**: Uses Hyperbola def $|PF_1| - |PF_2| = 2a$. Solves system. Checks Pythagoras.
*   **Theorems**: `Hyperbola_Equation_Standard_X`, `Hyperbola_Definition`, `Pythagorean_Theorem`, `Ellipse_Focal_Triangle_Perimeter`.
*   **Verdict**: **Mostly Consistent**. `Ellipse_Focal_Triangle_Perimeter` is likely triggered by the "Sum of focal radii" pattern usually associated with ellipses, even though the shape is a hyperbola. This highlights a potential pattern-matching bias in the annotation system.

## Conclusion
The dataset is largely reliable for training and retrieval tasks, with a strong signal-to-noise ratio. Users should be aware of occasional "phantom" tags from other conic sections appearing in single-curve problems.
