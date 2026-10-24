# Phase C: Swaps and novelty

**If STATE says `Goal: hackathon`, read `goal_hackathon.md` now. It replaces section 2 below.**

Inputs: STATE.md, Baseline v0 from REQUIREMENTS.md, the failure map (`grep -A40 "## Failure map" RESEARCH.md`), and `fields --keys Claim,Regime,Limits` for the entries you need.

## 1. Swaps (SWAPS.md)

Decompose Baseline v0 into: data, preprocessing, model, validation, decision rule, uncertainty, explanation, UI/3D, deployment. For each piece, write a row:
`| Piece | Baseline | Best alternative [E#] | Swap? | Why in this regime [D#]/[X#] |`.
Keeping the simple piece is often correct.

## 2. Novelty (NOVELTY.md)

1. **Diverge.** Invoke the `adhd` skill, if installed, on: "fixes for these failure modes: <failure-map rows that matter>". If it is not installed, brainstorm 10+ fixes under 3 different frames.
2. **Pick 1-3 fixes.** Each must matter here, not be covered by existing work, and be demonstrable in the time limit. Prefer guarantees that hold by construction.
3. **Novelty search.** Spawn 1 agent, foreground. It runs ≤5 batched queries per fix on Europe PMC, arXiv, GitHub and the web.
   - **Log:** it writes NOVELTY.md with the query, top hits, closest prior work and the exact difference.
   - **New entries:** it writes `research_parts/nov.md` in the Phase B entry format.
   - **Then:** run `merge`, then put the new entries through Phase B gate steps 1-2. `sources` must show 0 FAIL, and every cited entry must be verified.
4. **Wording.** Never write "first" or "no one has done". Write "closest prior work we found is [E#]; it differs in ...".
5. **Spike** (only if cheap). Write one script on the data that shows the failure and the fix, logged as `## X2...` in EXPERIMENTS.md.

STATE: Phase C done. Add key facts: the swaps made, the novel fixes with their closest prior work [E#], and the spike result.
