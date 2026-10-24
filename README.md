# nikunj-mode

An agent skill that turns a hackathon problem statement (plus its data) into a winning, defensible idea, and can optionally build it.

It produces:

- a requirement map and a profile of the data
- the simplest working baseline
- prior-art research where every source is fetched and checked by a script
- a piece-by-piece upgrade of the baseline
- novelty taken from where existing approaches fail and from the data itself
- a win plan built around the event's judging rubric

Every citation and every number in the final `IDEA.md` is checked mechanically by `scripts/verify.py`.

## Install

The skill expects to live at `~/.claude/skills/nikunj-mode` (the phase files use that path), so clone it there:

```bash
git clone https://github.com/<owner>/hackathon-research ~/.claude/skills/nikunj-mode
```

Requirements: Python 3 (standard library only) and an agent with web search and subagents. It's written for Claude Code. For Antigravity or other agents, see `references/antigravity.md`.

Optional skills it uses if installed: `caveman`, `adhd`, `impeccable`, `superpowers:test-driven-development`. Each one has a fallback if it's missing.

## Use

```
/nikunj-mode [plan|execute] [--research] <problem statement or path> [data paths]
```

- `plan` (default): research and the idea only. Output goes to `nikunj/IDEA.md` in the project.
- `execute`: plans first, asks for your approval, then builds the project milestone by milestone.
- `--research`: aims for paper-grade novelty instead of winning a hackathon rubric.

All working files go in a `nikunj/` folder in the current project. `nikunj/STATE.md` tracks progress, so an interrupted run can resume.

## Layout

| Path | What it is |
|---|---|
| `SKILL.md` | Orchestrator: intake, then one fresh subagent per phase |
| `phases/` | Instructions for phases A–F, shared rules, and the hackathon goal |
| `scripts/verify.py` | Merges research, checks sources and quotes, checks claims |
| `references/antigravity.md` | Tool mapping for agents other than Claude Code |
