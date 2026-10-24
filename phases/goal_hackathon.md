# Goal: hackathon (default)

The research is not the product. It is a **fumble map**: where teams lose points, what judges
will poke, and which shortcuts look good but break. The goal is to win THIS event: its rubric,
its time limit, its judges, its demo format. A paper is a side effect, never the target.

Win formula: **cover every criterion at a top-3 level, be visibly better in 1-2 places a judge
can verify in 3 minutes, and leave no easy attack.**

## C2. Differentiators (replaces Phase C section 2) -> WIN.md

### Step 1. Fumble map

Turn every failure-map row, every trap, and every D fact that matters into a row:
`| Fumble | How it costs points (criterion [P#]) | Evidence [E#]/[D#]/[X#] | Guard | Guard cost (hours) |`

A guard is one of:
- **test**: e.g. a leakage unit test.
- **feature**: e.g. abstention.
- **slide/answer**: e.g. "why our accuracy is lower than papers".
- **scope cut**: do not build it.

Mark rows that every team will fall into as `common`. Guarding a common fumble is a cheap differentiator.

### Step 2. The default entry

Describe what most teams on this track will submit: the problem statement read literally, plus the obvious stack. Base it on competitor repos found in research, past winners, and Baseline v0. That entry is the bar to clear. It is not your idea.

### Step 3. Candidates

Invoke `adhd` (if installed) on: "ways to beat the default entry on <criteria>, given these fumbles: <top rows>". If `adhd` is not installed, write 10+ candidates under 3 frames: judge, user, competitor.

### Step 4. Score each candidate

Score per criterion, then compute value per effort:
`| Candidate | Criterion: weight [P#] | Points gained vs default (0-3) | Visible in demo in <30 s? | Effort (person-days) | Risk | Value/effort |`

Value = Σ(weight × points). A candidate that a judge cannot see or verify in the demo, the report or the repo scores 0 on visibility. Drop it, or fold it into a guard.

### Step 5. Pick

- **Cover first.** Every criterion reaches its top-3 bar from REQUIREMENTS.md. Use the cheapest candidates that do it.
- **Then spike.** Choose 1-2 differentiators with the best value/effort that a judge sees in under 30 seconds. Go deep in one place rather than shallow everywhere.
- **Pass the honesty test.** Each differentiator must still hold under a judge's hardest question. Research shows which ones survive.

### Step 6. Light prior check

Run ≤2 queries per differentiator plus a competitor-repo search. Use one foreground agent, with results into NOVELTY.md and new entries through Phase B gate steps 1-2. This is enough to avoid claiming something a competitor or a well-known tool already does. Never write "first".

### Step 7. Scope cut

Fit the build into ~80% of the time and leave ~20% for polish, video and buffer.
- Everything not chosen goes into `| Cut | Why |`.
- Anything that needs resources the team does not have is cut, or kept only as a stretch goal.

### Optional spike

If cheap, write one script that shows the main differentiator's effect on the real data (`## X#`).

## D2. IDEA.md structure (replaces Phase D section 2)

Every number or factual claim carries a resolving tag, same as before.

1. **One-liner**: what a judge remembers after the demo.
2. **The story in 3 beats**:
   - the problem as the judge feels it
   - the insight from our data or research [D#]/[E#]
   - what we show
3. **Rubric plan**: `| Criterion | Weight [P#] | Default entry gets | We show | Evidence/guard |`. Every criterion covered.
4. **Differentiators** (1-2): what, why it beats the default, evidence, the 30-second demo proof, and the closest existing thing [E#].
5. **Fumble guards**: the top fumble-map rows with their guards. Show which ones the default entry falls into.
6. **Requirement coverage**: every R maps to a component.
7. **Architecture**: kept, swapped and new pieces, plus a Mermaid diagram. Simplest pieces wherever judges don't look.
8. **Demo script**:
   - the minute-by-minute video plan within the format limits [P#]
   - the opening 30 seconds
   - the one number for the first slide, in its honest unit
9. **Judge Q&A**: the 8 hardest questions, each answered with evidence (from research, mostly fumble rows).
10. **Build plan and scope cut**:
    - day-by-day plan, demo path first
    - the cut list
    - the 20% buffer
    - who does what, by team skills [A#]
11. **Risks and fallbacks**: each one reverts to the simple piece.
12. **Later**: one line on whether this could become a paper. No more.

## D3. Red team (replaces Phase D section 3)

Attack as **3 judges**:
- a domain expert (is it correct and safe?)
- an engineer (does it run, is it reproducible, is the code clean?)
- a product/design judge (is it clear, and does the demo land?)

Then check:
- **Coverage.** Is any criterion below its top-3 bar? Is any requirement or deliverable missing, such as the video, the page limit or the disclaimer?
- **Demo.** Can each differentiator be shown in under 30 seconds? Is anything that took days invisible in the demo? If so, cut it or make it visible.
- **Honest units.** Is every headline number stated in its most honest unit (per patient or summed over folds, mean or best run)?
- **Fumbles.** Does any fumble-map row stay unguarded while the default entry would also fail on it? Guarding it is a free win.
- **Time.** Is the build realistic for the team and time with the 20% buffer? If not, cut.
- **Event hint.** Is the event or track hint used? Are external datasets used where they help a criterion?
- **Over-engineering.** Is there research-grade complexity that no judge will notice? Cut it.

Fix what breaks. Put what survives into section 11.
