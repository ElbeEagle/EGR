# EGR AAAI2027 Subagent Prompts

This directory stores copy-paste prompts for running five parallel Codex subagents in the same EGR checkout, without git worktrees.

## Execution Mode

- Use one main control thread to launch and coordinate subagents.
- Do not use git worktrees for this round.
- Each subagent must only edit its allowed file scope.
- The main thread is responsible for final review, conflict resolution, integration, tests, and evaluation.
- Hot files should be integrated by the main thread only:
  - `src/reasoning/reasoning_engine.py`
  - `src/reasoning/model_selector.py`
  - `src/theorems/theorem_library.py`
  - `tex/icml2026.tex`

## Recommended Order

First parallel wave:

1. `01_eval_protocol_agent.md`
2. `02_symbolic_solver_agent.md`
3. `03_theorem_audit_agent.md`
4. `04_entropy_estimator_agent.md`

Second wave:

5. `05_search_strategies_agent.md`

`search-strategies` depends most heavily on the evaluation schema and is most likely to touch hot reasoning files, so it should first produce a design/interface draft and let the main thread decide what to integrate.

## Handoff Format

Every subagent must finish by writing a handoff file under `dev_logs/aaai2027/`:

```markdown
# Task
# Branch / Worktree
# Files Changed
# New Interfaces
# Metrics Before / After
# Tests Run
# Known Risks
# Integration Notes
```

Use `Branch / Worktree` to record that this was run in the shared checkout, for example:

```markdown
# Branch / Worktree
shared checkout: /Users/ebeleagel/Documents/GitHub/EGR
branch: <output of git branch --show-current>
```

## Main Thread Integration Checklist

After all subagents complete:

1. Read all `dev_logs/aaai2027/*_handoff.md`.
2. Run `git status --short`.
3. Review modified files by ownership scope.
4. Integrate any suggested hot-file patches manually.
5. Run the fastest relevant tests first.
6. Run a unified smoke evaluation.
7. Write `dev_logs/aaai2027/integration_handoff.md`.
