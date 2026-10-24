# Phase B: Research and verification

Inputs: STATE.md and the R list in REQUIREMENTS.md. Read only the R lines (grep `^- R` or similar), not the whole file.

## 1. Research agents (one turn, in parallel, foreground)

- **3 cluster agents** grouped by requirement (4 if there are more than 20 requirements).
- **1 dataset agent**: external or public datasets usable for validation or for extra modalities.
- **Budget**: each agent makes ≤12 tool calls, batches its searches, and returns 8-15 entries.
- **Output**: each agent writes `research_parts/cN.md` and numbers its own entries E1..En.
- **Search targets**: papers, repos, competition writeups, products, **same-track competitor projects on GitHub**, benchmarks, adjacent fields.
- **Search engines**: Europe PMC, arXiv, Crossref and the web. Never Semantic Scholar (it rate-limits).
- **Hard rules**: fetch every source in your own run, because memory is not a source. `Limits` is never empty.
- **Entry format** (exact):
```
### E1 | <exact title as on the source> | <year>
Kind: paper | repo | writeup | product | benchmark | dataset | docs
arXiv: <id if any>
DOI: <doi if any>
URL: <fetched url; for PMC/PubMed prefer europepmc.org or the DOI>
Quote: "<verbatim sentence(s) from the URL supporting the claim>"
Claim: <what we use it for, incl. number + dataset + setting>
Regime: <data size, modality, compute, assumptions>
Limits: <what breaks it; mark (inferred) if not stated by source>
Reqs: R2, R5
Verified: pending
```
After the agents return: `python $T merge RESEARCH.md research_parts/c*.md`.

## 2. Verification gate

1. **Mechanical check.** Run `python $T sources RESEARCH.md`. On FAIL, replace the entry with a real source or set `Verified: dropped`. Never edit a quote to match a page unless it still supports the Claim.
2. **Verifiers** (fresh, parallel, foreground): one per shard of ≤30 entries.
   - **Input**: write each shard with `fields --keys all --ids ... > research_parts/shard_N.md`.
   - **Task**: open each URL and judge whether the quote supports Claim, Regime and Limits, including the number, dataset and setting.
   - **Output**: write `research_parts/verdicts_N.md` with one line per entry. `E12 | yes`, or `E12 | corrected | Claim: ... | Limits: ...`, or `E12 | dropped | why`.
   - Apply the verdicts with a short script.
3. **Repeat.** Re-run `sources` until it reports 0 FAIL.
4. **Second sweep** (1 agent).
   - **Input**: only the titles, from `fields`.
   - **Targets**: the last 12 months, negative results, critiques of the top approaches, other names for the problem.
   - **Output**: it writes `research_parts/s2.md`.
   - **Then**: run `merge` again and put the new entries through steps 1-3.
5. **Failure map**: append to RESEARCH.md `## Failure map` with columns `| Failure mode | [E#]/[D#] | Who suffers | Matters here? |`. Put data rows first. Use the D facts from STATE and DATA.md headers.

STATE: Phase B done. Add key facts: the `sources` summary line, the number of verified entries, the top 3 failure-map rows, and any competitor project found.
