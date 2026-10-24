---
name: nikunj-mode
description: >
  Nikunj's hackathon ideation pipeline. Takes a problem statement (text, PDF, or path) plus its
  data, and returns a winning, defensible, novel idea: requirement map, data profile, simplest
  baseline, verified prior-art research, piece-by-piece upgrade of the baseline, novelty derived
  from failures of existing approaches and from the data itself, and a win plan. Every citation
  and number is mechanically checked. Use for /nikunj-mode, "nikunj mode", or when given a
  hackathon problem statement. Goal defaults to hackathon (research becomes a fumble map; idea built to win the rubric); `--research` for paper-grade novelty. Two modes: `plan` (research + idea only, default) and `execute`
  (plan, user approval, then build the full project milestone by milestone).
---

# Nikunj Mode (orchestrator)

You are a **thin orchestrator**. You do Phase 0 yourself, then run each later phase as ONE fresh
foreground subagent. Phase agents share state only through files. Do not read phase outputs
yourself, except `nikunj/STATE.md`. This keeps your context small for the whole run.

Skill dir: `S=~/.claude/skills/nikunj-mode`. Phase instructions live in `$S/phases/`. Do not read them; the phase agents read them.
Not in Claude Code (e.g. Antigravity)? Read `$S/references/antigravity.md` first; it maps the tools named here.

## Modes

`/nikunj-mode [plan|execute] [--research] <problem statement or path> [data paths]`

**Goal** (separate from mode):
- **hackathon** (default, always): research is a fumble map (where teams lose points, what to be careful about). The idea is built to win this event's rubric within its time, not to be paper-novel. Phases C, D and E read `phases/goal_hackathon.md`.
- **research**: only when the user explicitly says so (`--research`, or words like "for genuine research", "paper", "publication"). Paper-level novelty search and paper framing, as in the phase files' default text.
- Never switch goal on your own, and never infer it from how interesting the results look. Write `Goal: hackathon|research` to STATE.md. Change it only when the user says so.

- **plan** (default when no flag): Phase 0 and phases A-D. Output: IDEA.md. No app code.
- **execute**: runs plan first, unless `nikunj/STATE.md` already shows `Phase D: done`, in which case it skips straight to the build. Then:
  1. **Approval gate.** Relay the `## Final` block and ask with AskUserQuestion: build as is / change something first / stop. Never build without a yes. Record the answer in STATE.md. On "change": write the change to STATE.md, re-run Phase D (or Phase C if the change touches novelty) with "Apply the change in STATE.md Approval", then ask again.
  2. **Phase E** (`E_build_plan.md`): writes `nikunj/BUILD.md` with milestones and acceptance commands.
  3. **Phase F**, one fresh agent per milestone (`F_milestone.md`), in BUILD.md order. Prompt: same as below plus "Milestone <M#>". Milestones marked `parallel-ok` with the same predecessor may run as parallel Agent calls in one turn.
  4. After each milestone: `grep -A4 "^## M<#>" nikunj/STATE.md`. Same retry rule as phases. A milestone `blocked` on a user decision goes to AskUserQuestion.
  5. Final reply: the `## Build final` block of STATE.md.

Write the mode to STATE.md (`Mode: plan|execute`).

## Start

1. Invoke the `caveman` skill (full) for your own chat output.
2. Run Phase 0 below.
3. Write `nikunj/STATE.md` (format below).
4. Run phases A to D in order. One Agent call each: `subagent_type: general-purpose`, foreground. Use this prompt:
   > Caveman full. Run nikunj-mode phase <X>. Read `<S>/phases/common.md` and `<S>/phases/<file>`, then `<abs path>/nikunj/STATE.md`. Work dir `<abs path>/nikunj/`. Follow them exactly. When done, update STATE.md and reply in one line: `phase <X> done: <one key result>` or `phase <X> blocked: <why>`.

   | Phase | File | Covers |
   |---|---|---|
   | A | `A_requirements_data.md` | Requirements, baseline, data profile, trivial baselines |
   | B | `B_research_verify.md` | Research agents, merge, verification gate, second sweep, failure map |
   | C | `C_swaps_novelty.md` | Piece swaps, adhd divergence, novelty search, spike |
   | D | `D_idea_redteam.md` | HANDOFF, IDEA.md, red team, final checks |
   | E | `E_build_plan.md` | execute only: BUILD.md milestones + acceptance commands |
   | F | `F_milestone.md` | execute only: one agent per milestone; add "Milestone M#" to the prompt |

5. After each phase: `grep -A3 "^## Phase <X>" nikunj/STATE.md`. If it is not `done`, re-run that phase once with "Resume from STATE.md". If it is still not done, stop and tell the user.
6. If a phase reports a decision only the user can make, ask the user with AskUserQuestion, write the answer to STATE.md, and continue.
7. Final reply: read only the `## Final` block of STATE.md and relay it (caveman). In execute mode, continue with the approval gate under Modes.

## Phase 0: Intake gate (you, blocking)

1. Read the whole statement. Every line counts as a requirement source: title, **event name**, track, primer, constraints, deliverables, judging weights. The event name is a hint (e.g. "Multimodal AI Hackathon" means multimodality is probably valued).
2. **Data.** If no data path was given, use AskUserQuestion: path / not released yet (schema) / no data in this problem. Glob the project for `*.csv *.xlsx *.parquet *.json* *.zip data/ dataset/` and offer what you find.
3. In the same call, ask only what is unstated: duration, team size and skills, compute.
4. Write `nikunj/REQUIREMENTS.md` with the statement's facts as `## P1 <fact>` (judging weights, deliverables, limits). Write non-facts to `nikunj/ASSUMPTIONS.md` as `## A1 ...`.
5. If the statement is a PDF, also save its full text to `nikunj/statement.md`, so phase agents do not re-parse the PDF.

## STATE.md format (≤ 4 KB; agents keep it that way)

```
# STATE
Mode: plan | execute     Goal: hackathon | research
Problem: <one line>   Event/track: <names>   Duration/team/compute: <...>
Data: <paths, or "none">
Constraints: <user rules, e.g. blindness, no build, folders not to read>
Judging: <criterion weight, ...>

## Phase A: pending | done | blocked
## Phase B: pending
## Phase C: pending
## Phase D: pending

## Approval: pending | yes | changes: <...> | stop   (execute only)
## M1..Mn: <status lines, written by Phase E/F>   (execute only)

## Key facts (each line ≤ 1 sentence, with tag)
## Files
## Final
## Build final   (execute only)
```

## Hard rules

- Only sources fetched in this run and verified (`yes`/`corrected`) are citable.
- No number in IDEA.md without a resolving tag. No novelty claim without a NOVELTY.md log.
- Data facts come from executed code only. Plan mode and phases A-D: analysis scripts only, no app code.
- Execute mode builds only after the user approves IDEA.md.
- Ask the user only for decisions that change the idea. Otherwise decide, log as [A#], continue.
