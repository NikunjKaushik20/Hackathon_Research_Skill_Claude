# Phase E: Build plan (execute mode only)

Inputs:
- STATE.md: the `Approval` line, plus any change it records.
- IDEA.md sections 2, 4, 9 and 10.
- HANDOFF.md.

If `Goal: hackathon`: order milestones by the demo script and the scope cut in IDEA.md (demo path first, then polish, video and docs). Reserve the last 20% of the time for polish, video and buffer. Anything marked "cut" in IDEA.md is not built.

Output: `nikunj/BUILD.md` and the M lines in STATE.md. Write no app code in this phase.

## Project layout

The code lives in the **project root**, not in `nikunj/`. Pick a conventional layout for the stack, for example `ml/`, `backend/`, `frontend/`, `results/`, `docs/`, `tests/`. If a repo already exists, follow its conventions.

## Milestones

Derive the milestones from IDEA.md section 10. Order them by time to a working demo. Each later milestone must keep the app runnable. The default skeleton is below; adapt it to the idea:

| M | Goal | Notes |
|---|---|---|
| M1 | **Baseline v0 end to end**: data load, baseline model, minimal API, minimal UI, safety text if required. Define the **API contract** (request/response schema) in `docs/api.md`. | Must run with one command. |
| M2 | **Validation suite**: the validation protocol from IDEA.md, written to `results/*.json`. | Results are always files, never console-only. |
| M3 | **Swaps**: one by one, each compared against the baseline on the same folds. | `parallel-ok` with M5 after M1. |
| M4 | **Novel pieces**, with the experiment that proves each one. | |
| M5 | **UI/3D/dashboard** to the ambition level in REQUIREMENTS.md. | Use the `impeccable` skill if it is installed. `parallel-ok` with M3. |
| M6 | **Integration and hardening**: tests across layers, reproducibility (lock files, seeds, one-command setup). | |
| M7 | **Docs and claims**: README, report (respecting the deliverable page limit), demo script. | Every number comes from `results/*.json` via a check script. |

For each milestone, write the following in BUILD.md:
```
## M1 <goal>
Depends on: <M#s>   parallel-ok: <M#s or none>
Scope: <files/dirs it may create or change>
Done when (commands that must pass):
- <e.g. python -m pytest -q tests/test_baseline.py>
- <e.g. curl -s localhost:8000/api/predict -d @tests/sample.json | python -c "...">
Expected numbers: <the [X#] values from planning this milestone should reproduce, with tolerance>
Fallback: <from IDEA.md section 9>
```

Write one STATE.md line per milestone: `## M1: pending | <goal>`. Set `## Phase E: done`.
