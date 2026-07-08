# Theorem Library V2

This package is the opt-in implementation of the new theorem/application
paradigm.  The legacy implementation remains under `src/theorems/` and is not
modified or imported by v2.

## First batch

Registered model IDs:

```text
0-13, 21, 29, 75
```

The batch covers conic definitions, standard equations, ellipse/hyperbola
parameter relations, eccentricity, hyperbola asymptotes, parabola directrices,
and circle standard equations.

## Minimal example

```python
from fractions import Fraction

from src.theorems_v2 import (
    ApplicatorV2,
    InformationState,
    PolynomialEquation,
    TheoremLibraryV2,
)

state = InformationState().declare("G", "Hyperbola")
state.add_given(
    "ExpressionPolynomial",
    "G",
    value=PolynomialEquation(
        x2=Fraction(1, 4),
        y2=Fraction(-1, 25),
        constant=-1,
    ),
)

library = TheoremLibraryV2()
applicator = ApplicatorV2()

standard = applicator.apply(library.get_model(5), state)
asymptote = applicator.apply(library.get_model(21), standard.state_after)
```

`apply()` never mutates its input state.  A successful result contains a new
`state_after`, a typed `StateDelta`, the selected binding, and evidence IDs.
Conflicts, ambiguous bindings, missing matches, and idempotent replay are
reported with separate `ApplicationStatus` values.

## Boundaries

- `InformationState` stores typed, entity-scoped facts.
- A theorem matches facts and derives a delta; it does not edit state.
- `ApplicatorV2` commits the delta atomically after conflict and postcondition
  checks.
- `ConservativeSolver` performs exact rational simplification and preserves
  symbolic expressions as typed terms.  A richer algebra backend can replace
  it without changing theorem interfaces.
- Parsing natural-language/formal Conic10K facts into `InformationState` is a
  separate next step.

See `doc/high_frequency_theorem_information_space_design.md` for the complete
design and migration plan.
