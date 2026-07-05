# Rudi's Skills

Public repository for reusable agent skills.

This repo is structured as a skills distribution for Claude, Codex, and OpenCode. It keeps one canonical `skills/` tree and exposes that tree through each tool's plugin or discovery surface.

## Layout

```text
skills/
  <skill-name>/
    SKILL.md
    agents/openai.yaml
    scripts/
    references/
    assets/
```

Only `SKILL.md` is required for a skill. The other folders are optional and should exist only when a skill needs them.

## Plugin Surfaces

- Claude: `.claude-plugin/plugin.json`
- Codex: `.codex-plugin/plugin.json`
- OpenCode: `.opencode/plugins/rudironsoni-skills.ts`

OpenCode also discovers `SKILL.md` files from `.opencode/skills`, `.claude/skills`, `.agents/skills`, and their global equivalents. Use `make link` to link the canonical skills into local global skill folders.

## Commands

```bash
make help
make validate
make link
make unlink
```

`make validate` checks JSON manifests, skill frontmatter, Codex plugin metadata when the local validator is available, and the OpenCode plugin scaffold.

## Adding a Skill

Create a folder directly under `skills/`:

```text
skills/my-skill/SKILL.md
```

Use lowercase hyphen-case for skill folder names and frontmatter `name` values. Do not add draft, private, or deprecated categories until there is a real distribution need.
