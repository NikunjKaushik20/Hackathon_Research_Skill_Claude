# Phase D: IDEA.md, red team, final checks

**If STATE says `Goal: hackathon`, read `goal_hackathon.md` now. Its IDEA.md structure and red-team checklist replace sections 2-3 below.**

## 1. HANDOFF.md (≤ 2 pages)

Build it from STATE.md, the R lines and Baseline v0, the key D and X headers, the failure map, SWAPS.md, the NOVELTY.md decisions and (hackathon goal) WIN.md. Do not re-read the big files. Use `fields` for any E# you cite.

## 2. IDEA.md

Every number or factual claim carries a tag: `[E#]` (verified only), `[D#]`, `[X#]`, `[A#]` or `[P#]`. Sections:
1. **One-liner.**
2. **Requirement coverage**: every R maps to a component.
3. **What the data told us**: 3-5 D facts.
4. **Architecture**: kept, swapped and novel pieces, plus a Mermaid diagram.
5. **What is different**: a `| | Usual | Ours |` table.
6. **Why it is novel**: per novel piece, the failure, the evidence, the closest prior work and the difference.
7. **Why it is Nikunj style.**
8. **How it wins**: per judging criterion; the 30-second demo moment; the one number for the first slide; likely judge questions with answers.
9. **Risks and fallbacks**, plus known weaknesses.
10. **Build plan**: baseline first.
11. **Paper potential, 1-10.** If 7+: the claim, the experiments needed and the venue.

## 3. Red team

Attack IDEA.md as a judge and as a reviewer:
- Is a novelty claim already published? Is a requirement uncovered? Is the plan unrealistic for the time? Is there complexity with no scored gain?
- **For every headline number, what is the unit?** Per patient, or summed over CV folds and repeats? A per-run mean, or the best run? Restate each number in its most honest unit.
- Is the event or track hint used? Are external datasets used where they are available? Does each high-weight criterion get top-3-level ambition?

Fix what breaks. Put what survives into section 9.

## 4. Final checks (both must be clean)

- `python $T claims IDEA.md .` must report 0 problems. Pending E tags fail it.
- `python $T sources RESEARCH.md` must report 0 FAIL.

## 5. STATE.md `## Final` block (caveman, ≤ 15 lines)

- One-liner.
- Novel pieces, each with its closest prior work.
- Why it wins, in 3 bullets.
- Paper score.
- The summary lines of both checkers.
- File list.
- Open decisions for the user.

Set `## Phase D: done`.
