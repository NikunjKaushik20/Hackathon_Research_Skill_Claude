# Running nikunj-mode outside Claude Code (Antigravity IDE / agy CLI)

The skill text names Claude Code tools. Map them as below. Everything else (phases, STATE.md,
verify.py, hard rules) is unchanged.

Skill dir: `S=~/.gemini/config/skills/nikunj-mode` (a link to `~/.claude/skills/nikunj-mode`;
both paths work, including `T=~/.claude/skills/nikunj-mode/scripts/verify.py` in common.md).
On Windows, expand `~` to the absolute home path before passing it to a shell or subagent.

| Skill says | Antigravity |
|---|---|
| Agent call, `subagent_type: general-purpose`, foreground | `invoke_subagent` with `TypeName: self` (full capability); wait for its reply before the next step. Read-only lookups may use `research`. |
| Several Agent calls in ONE turn (parallel) | Several `invoke_subagent` calls in one turn if the harness allows; else run them one after another. Same prompts. |
| AskUserQuestion | Ask in chat as a short numbered list of options (+ "other"), then stop and wait for the reply. Never assume the answer. |
| `caveman` skill | If not installed: write your own chat output and subagent prompts terse (drop filler/articles, fragments OK). Never compress quotes, titles, numbers, URLs, or deliverable files. |
| `adhd` / `impeccable` skill | Use if installed; otherwise follow the fallback written next to it in the phase file. Inside `adhd`, "Agent/Task tool" = `invoke_subagent` (`TypeName: self`), all branches in one turn, none seeing another's output. |
| `grep -A3 "^## Phase X" nikunj/STATE.md` | Same command in the terminal, or a file-search tool. Read only that block. |
| WebSearch / WebFetch | The built-in web search and URL-read tools. Batch independent queries in one turn. |
| Todo tracking | A task artifact checklist (`write_to_file`, `IsArtifact: true`, `ArtifactType: "task"`), if you want one. |

## No subagent tool available

Run each phase inline, in order, with the same discipline: before a phase, read only
`common.md` + that phase's file + STATE.md; do the work; update STATE.md; then treat earlier
phase files and outputs as closed (re-read files from disk, not from memory). Phase B
research/verifier fan-out becomes sequential batches, each with the same call budget.
