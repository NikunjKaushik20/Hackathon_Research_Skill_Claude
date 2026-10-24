# Phase A: Requirements and data

Inputs: STATE.md, `statement.md` (or the statement file), and the P# facts in REQUIREMENTS.md.

## 1. Requirements (append to REQUIREMENTS.md)

- List R1..Rn: explicit, implicit and judging requirements. Quote each one's source line and give the simplest solution for it.
- **Baseline v0**: the simplest end-to-end system that meets every R.
- **Traps**: shift, leakage, unseen domains, metric quirks, compute limits.
- **Ambition check per judging criterion**: what a top-3 entry would show for that criterion. UX/3D/demo criteria get attention in proportion to their weight, same as model criteria.
- **Event-name hint**: what the event or track name implies beyond the task text.

## 2. Data profile (DATA.md, EXPERIMENTS.md)

Skip this section if STATE says "no data". If there is only a schema, profile the schema and log the rest as A#.

Write one script, `profile.py`, and run it once with compact output. Record each fact as `## D1 <fact with number>`.
- **Coverage:** every file and **every sheet**, including empty-looking sheets. Size, types, missingness, duplicates, label distribution, groups.
- **Shift:** train vs test, or train vs deployment. **Row order**: does the index predict the label, and does the first part of the file differ from the last? Report the adversarial-validation AUC.
- **Leakage:** IDs, timestamps, near-duplicates, post-outcome features.
- **Label logic:** is a parent label the OR of its child labels? List label conflicts.
- **Raw rows:** write 30+ raw rows, including the hardest and most ambiguous ones, to `raw_rows.txt`. Then write down what you see in them.
- **Baselines:** Baseline v0 score as `## X1`, plus the dominant error types. Score **trivial baselines** (majority class, most-common-category prior) for every target. A model that does not beat the prior is a finding.

STATE: Phase A done. Add key facts: Baseline v0 score, the 3-5 most design-relevant D facts, and the event hint.
