# Repository Instructions

This repository is a public distribution for Rudimar Ronsoni's reusable agent skills.

## Canonical Structure

- Keep canonical skills under `skills/<capability>/<skill-name>/`.
- Use lowercase hyphen-case for capability and skill folder names.
- Keep skill names globally unique across capability folders.
- Do not copy skills, categories, or content from other public skill repositories.
- Do not add draft, private, deprecated, or catch-all folders unless there is a real distribution need.
- Prefer a `Makefile` target over a standalone shell script for repository automation.

## Distribution

- Ship one repo-wide Claude Code plugin through `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json`.
- List every published skill explicitly in the Claude plugin's `skills` array.
- Keep `package.json` and `.claude-plugin/plugin.json` on the same strict semantic version.
- Keep Codex and OpenCode installation on the Agent Skills standard and `make link`; do not add an incomplete native plugin surface for the grouped tree.
- Add every published skill to its capability README and the top-level README.

## Releases

- Add a `.changeset/<slug>.md` file for every releasable change, with `"rudironsoni-skills": patch`, `minor`, or `major` in its frontmatter.
- Use `minor` for new skills, `patch` for compatible fixes, and `major` for breaking changes.
- Changesets accumulate on `main`; the release workflow maintains one rolling version pull request.
- Merge the version pull request to publish the Git tag and GitHub Release. The package is private and is not published to npm.
- Keep `package.json`, `package-lock.json`, and `.claude-plugin/plugin.json` on the same strict semantic version.

## Skill Shape

Each skill must include `SKILL.md` with YAML frontmatter containing at least:

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
- `templates/`

Keep each skill self-contained. If several skills require the same reference, copy it into each skill and validate the copies are identical.

## Validation

- Run `make validate` before committing.
- Run `claude plugin validate . --strict` after changing either Claude manifest.
- Run `git diff --check` and review the final diff before publishing.
