# Task

This thread created the AAAI2027 paper-writing scaffold for EGR. The work focused on paper story, method formalization, claim boundaries, experiment planning, and an initial LaTeX draft skeleton. No core code was modified.

# Branch / Worktree

- Branch: `main`
- Worktree: `/Users/ebeleagel/Documents/GitHub/EGR`

# Files Changed

Added:

- `doc/aaai2027_paper_outline.md`
- `doc/aaai2027_claims_and_evidence.md`
- `doc/aaai2027_experiment_plan.md`
- `tex/aaai2027_egr_draft.tex`
- `dev_logs/aaai2027/paper_handoff.md`

# New Interfaces

Defined paper-facing terminology:

- `theorem action`: one formal theorem/model ID selected and executed by EGR.
- `P(Y|X)`: theorem selection policy over theorem actions.
- `H(S)`: state entropy, a solving-progress or remaining-uncertainty signal.
- `InfoGain`: `H(S_t)-H(S_{t+1})`.
- `H(Y|X)`: prediction entropy of the theorem-selection distribution.
- `reasoning success`: process-level progress/completion, separate from final answer correctness.
- `final answer accuracy`: gold-answer correctness after answer extraction/normalization.
- `LLM+EGR`: LLM reasoning assisted by EGR theorem candidates, traces, or verification.

Defined planned result schemas and table structures in `doc/aaai2027_experiment_plan.md`.

# Metrics Before / After

This thread did not change metrics. It only referenced existing preliminary repo outputs:

- Runtime theorem-library audit: 56/80 registered models.
- `data/train_with_models_v2.json`: 7,757 samples, 5,359 non-empty model-sequence samples, 20,226 model steps.
- `data/train_state_model_v2.json`: 5,359 samples and 12,460 transitions.
- `outputs/evaluation/main_integration_200/summary.json`: preliminary process success 130/200 = 65.0%, final answer accuracy 21/200 = 10.5%.
- `outputs/evaluation/protocol_200_smoke/summary.json`: smoke process success 147/200 = 73.5%, final answer accuracy 5/200 = 2.5%.
- `outputs/experiments/main_search_ablation_50/ablation_summary.json`: preliminary full EGR final answer accuracy 13/50 = 26.0%, avg steps 4.30.
- `outputs/entropy/training_metrics.json`: learned entropy validation Pearson 0.837 and Spearman 0.849 against normalized remaining steps.
- `outputs/entropy/correlation_summary.json`: learned entropy Pearson 0.833 and Spearman 0.859 over 11,411 entries.

All these metrics need unified evaluation review before being used as final paper results.

# Tests Run

- `perl -ne 'if(/[ \t]$/){print "$ARGV:$.: trailing whitespace\n"}' doc/aaai2027_paper_outline.md doc/aaai2027_claims_and_evidence.md doc/aaai2027_experiment_plan.md tex/aaai2027_egr_draft.tex dev_logs/aaai2027/paper_handoff.md`
- `git diff --check`

LaTeX compilation was not run. The draft uses a generic article preamble because the AAAI2027 official template was not confirmed.

# Known Risks

- AAAI2027 official template or formatting requirements were not confirmed.
- Related work citations are placeholders only; no references were invented.
- Existing repo outputs use multiple protocols and sample sizes, so current numbers are not final.
- The theorem-library count differs across old docs; current runtime count is 56/80.
- The selector has inconsistent metrics across small external evaluation and integrated reasoning logs.
- Final answer accuracy is currently weak and must not be hidden behind process success.
- LLM baseline and LLM+EGR evidence are not yet available.
- The repo `.gitignore` ignores `tex/`, so `tex/aaai2027_egr_draft.tex` exists locally but will not appear in ordinary `git status` unless force-added or the ignore rule is changed.

# Integration Notes

Next paper/integration thread should:

1. Freeze the unified evaluation protocol and split.
2. Runtime-audit theorem coverage and unsupported model IDs.
3. Re-run theorem selection, reasoning process, final answer, entropy, and ablation metrics under one protocol.
4. Fill `TODO: fill after unified evaluation` cells in `tex/aaai2027_egr_draft.tex`.
5. Add verified related-work citations only after checking source papers.
6. Add one or two case studies with theorem sequence, symbolic state changes, and entropy trace.
7. Run direct LLM and LLM+EGR experiments before making any LLM-augmentation claim.
