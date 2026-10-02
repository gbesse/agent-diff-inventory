# Agent Diff Inventory

**Find non-ignored files an agent changed on disk, even if its review panel missed them.**

English · [Français](README.fr.md) · [Español](README.es.md)

## Related projects

- [Codex #50202](https://github.com/openai/codex/issues/50202) — Reports script-created edits missing from one review view.
- [Agent Diff Auditor](https://github.com/gaye-lamine/Agent-Diff-Auditor) — Reviews an already supplied diff; this tool independently inventories the worktree before and after.

## Try it

```sh
python3 inventory.py demo --lang en
```

## Use your own data

```sh
python3 inventory.py snapshot --repo /path/to/repo --out /tmp/agent-baseline.json
python3 inventory.py compare --repo /path/to/repo --baseline /tmp/agent-baseline.json --lang en
```

Take a baseline outside the Git worktree before an agent run, then compare afterward. Uses `git ls-files` plus SHA-256 to report added, modified, and deleted tracked or non-ignored untracked files.

## Scope and limits

Real Git integration; no Codex UI integration. You must compare its file list to the review panel yourself. Ignored files are excluded. The snapshot JSON contains file names and hashes, so keep it local.

## Test

```sh
python3 -m unittest discover -s tests -v
```

Python 3.11+ · MIT · v0.1.0-alpha.1
