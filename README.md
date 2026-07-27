# Rudi's Skills

Reusable agent skills grouped by capability and distributed from one canonical repository.

## Install

Install selected skills into Claude Code, Codex, OpenCode, or another Agent Skills-compatible harness:

```bash
npx skills@latest add rudironsoni/skills
```

Install the read-only, repo-wide Claude Code plugin:

```bash
claude plugin marketplace add rudironsoni/skills
claude plugin install rudironsoni-skills@rudironsoni
```

Codex and OpenCode use the Agent Skills installer above. Their native plugin manifests do not support selecting skills across this repository's grouped layout.

Maintainers can link every canonical skill into the local global skill directories:

```bash
make link
```

## Skills

### Orchestration

- [goal-mode](./skills/orchestration/goal-mode/SKILL.md) - Run and bound Claude Code goal loops with evaluator-visible evidence.
- [codex-orchestrator](./skills/orchestration/codex-orchestrator/SKILL.md) - Delegate independent Codex work with explicit ownership and integration checks.
- [herdr-agent-comms](./skills/orchestration/herdr-agent-comms/SKILL.md) - Manage Herdr agent fleets, messaging, delivery verification, and waits.

### Prompting

- [prompting-fable-5](./skills/prompting/prompting-fable-5/SKILL.md) - Prompt Claude Fable 5 and Mythos 5.
- [prompting-opus-4-8](./skills/prompting/prompting-opus-4-8/SKILL.md) - Prompt Claude Opus 4.8.
- [prompting-sonnet-5](./skills/prompting/prompting-sonnet-5/SKILL.md) - Prompt Claude Sonnet 5.

### Engineering

- [linus-torvalds](./skills/engineering/linus-torvalds/SKILL.md) - Review and write code with Linus Torvalds-inspired engineering principles.

### Writing

- [ogilvy-writing](./skills/writing/ogilvy-writing/SKILL.md) - Edit business writing for clarity, brevity, and action.
- [stop-slop](./skills/writing/stop-slop/SKILL.md) - Remove predictable AI writing patterns from prose.

### Visualization

- [obsidian-excalidraw-diagram](./skills/visualization/obsidian-excalidraw-diagram/SKILL.md) - Generate engineering-style Excalidraw diagrams.

## Development

```bash
make validate
make list
make link
make unlink
```

The complete collection and Claude plugin are versioned together. Git tags and GitHub Releases are authoritative.

## License

MIT
