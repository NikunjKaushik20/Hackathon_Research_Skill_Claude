# Common rules for every nikunj-mode phase agent

**Style target.** Use the simplest working baseline as the reference. Swap a piece only when evidence shows it wins in this problem's regime. Novelty comes from failures of existing work and from the data. Prefer guarantees that hold by construction: a gated hierarchy that cannot contradict itself, abstention instead of forced guesses, validation that copies the real test shift, and two independent readers that must agree. Report honestly where it fails. Never tune on the scored set.

**Toolkit:** `T=~/.claude/skills/nikunj-mode/scripts/verify.py`. Run it with `python`.
- `merge OUT parts...`: merges parts, renumbers E#, drops duplicates.
- `fields RESEARCH.md [--ids E1,E2] [--keys Claim,Limits|all] [--status pending]`: compact view of entries.
- `sources RESEARCH.md [--ids ...]`: checks that each source exists, its title matches, its URL is live and its quote is on the page. Prints only non-PASS rows.
- `claims IDEA.md WORKDIR`: checks that every number is tagged, every tag resolves, and every E tag is verified.

## Tags

| Tag | Meaning | File | Header format |
|---|---|---|---|
| `[E#]` | verified source | RESEARCH.md | `### E1 \| title \| year` |
| `[D#]` | data fact | DATA.md | `## D1` |
| `[X#]` | experiment | EXPERIMENTS.md | `## X1` |
| `[A#]` | assumption | ASSUMPTIONS.md | `## A1` |
| `[P#]` | problem statement fact | REQUIREMENTS.md | `## P1` |

## Token rules

1. **Batch.** Put independent searches, fetches and reads in ONE turn.
2. **Never Read RESEARCH.md or research parts whole.** Use `fields`.
3. **Keep tool output small.** Scripts print summaries of ≤150 lines. Send long output to a file and read only what you need.
4. **Subagents reply in one line.** Content goes in files.
5. **Write terse.** Use caveman full style for notes and subagent prompts. Every subagent prompt starts with: "Caveman full. Quotes, titles, numbers, URLs verbatim. Reply one line." Deliverable files (IDEA.md, DATA.md, RESEARCH.md prose) are written in plain English.
6. **Do not read the user's own past projects for style.** The style target replaces them.

## Agent rules

- Spawn subagents in the **foreground** only. Spawn parallel ones as several Agent calls in ONE turn.
- Never poll or sleep-wait for a file. If an agent returns and its file is missing or incomplete, mark those items `pending (agent failed)` and continue.
- Pass the `Constraints:` line from STATE.md to every subagent.

## STATE.md duty

- At the end of the phase, set `## Phase X: done` (or `blocked: <why>`).
- Add at most 8 key-fact lines with tags under `## Key facts`, and the new file names under `## Files`.
- Keep STATE.md at ≤ 3 KB. Replace stale lines instead of appending.
