# Repository Instructions

This repository is a public distribution for reusable agent skills.

## Rules

- Keep one canonical skill tree under `skills/`.
- Put each skill directly under `skills/<skill-name>/`.
- Use lowercase hyphen-case for skill folder names.
- Do not copy skills, categories, or content from other public skill repositories.
- Do not add draft, private, deprecated, or category folders unless there is a real distribution need.
- Prefer a `Makefile` target over standalone shell scripts for repository automation.
- Keep Claude, Codex, and OpenCode plugin surfaces pointed at the canonical skill tree.
- Validate with `make validate` before committing.

## Skill Shape

Each skill must include `SKILL.md` with YAML frontmatter:

```yaml
---
name: skill-name
description: Short trigger-focused description.
---
```

Optional per-skill folders are allowed only when needed:

- `agents/`
- `scripts/`
- `references/`
- `assets/`
