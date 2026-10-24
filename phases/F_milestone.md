# Phase F: Build one milestone (execute mode only)

Your milestone ID is in your prompt. Read:
- STATE.md
- your `## M#` section of `nikunj/BUILD.md` (grep it, do not read the whole file)
- `docs/api.md`, if it exists
- only the code files your Scope touches

Read IDEA.md only through grep, for the section you need.

## Rules

- **Scope.** Change only the files in your Scope. If you must touch others, keep the change small and record it in STATE.md.
- **Tests first** for logic you add: models, metrics, data transforms, API. Use `superpowers:test-driven-development` if it is installed. UI work needs at least one smoke or e2e check.
- **Leakage discipline.** Every preprocessing, selection and tuning step goes inside training folds. Target columns never reach a model; add a test that fails if one does.
- **Results go in files.** Every metric is written to `results/<name>.json` by a script, never typed into docs by hand.
- **Reality beats the plan.** If a measured number misses its planned `[X#]` value by more than the tolerance, do not tune on the scored set to close the gap. Do two things:
  - Write the real number to STATE.md.
  - Apply the milestone's Fallback, or mark the milestone `blocked: plan claim X# not reproduced (<numbers>)` so the orchestrator asks the user.
- **No new claims.** Docs may only state numbers that exist in `results/*.json`. M7 writes `tools/check_claims.py`, which rebuilds every number in README and the report from `results/` and fails on any mismatch.
- **Stay runnable.** The app must still start with the documented one command after your milestone.
- **Sub-agents.** You may spawn foreground subagents for independent sub-parts. Give them disjoint file scopes, and have them reply in one line.
- **Git.** Do not commit unless STATE.md `Constraints:` says commits are allowed. If they are, use one commit per milestone.
- **Token rules from common.md apply.** Batch reads and commands. Pipe long logs to files and read only the failing lines.

## Done

Run every `Done when` command and paste only each command's last summary line into STATE.md:
```
## M3: done | swaps: RF vessels (+0.03 AUC LAD), Platt; tests 24 passed
```
or `blocked: <why>`.

If this is the last milestone, also write `## Build final` (caveman, 15 lines max), with:
- how to run the app (one command)
- headline results from `results/` with their file names
- the test summary
- the `check_claims` result
- known gaps versus IDEA.md
- the deliverables checklist from REQUIREMENTS.md, each marked ✓ or ✗
