# Changelog

## 2.0.0

### Major Changes

- [`1207b08`](https://github.com/rudironsoni/skills/commit/1207b0838bc97b7e61571397c70f329f2d30f268) Thanks [@rudironsoni](https://github.com/rudironsoni)! - Replace `herdr-agent-comms` with `herdr-orchestration`, built around Herdr's native interactive-agent lifecycle, scoped delegation, controller verification, and worker cleanup.

### Minor Changes

- [`9db2804`](https://github.com/rudironsoni/skills/commit/9db280448fff30bd1943bd49ac43b17f113b3f8c) Thanks [@rudironsoni](https://github.com/rudironsoni)! - Add a Layout Contract to `herdr-orchestration`: one session per organization (`~/src/<organization>`), one workspace and first tab per repo, worktree tabs at `<repo>.worktrees/<repo>-<branch-folder>`, Conventional Branches naming validated with `git check-ref-format`, and default `codex` worker routing that organization policy skills can override.

- [`488dba3`](https://github.com/rudironsoni/skills/commit/488dba33fd4e107dad256333c4114d51ca6913b0) Thanks [@rudironsoni](https://github.com/rudironsoni)! - Add `rfc2119-engineering-playbooks`: RFC 2119 SOP authoring with three condensed references (`write`, `update`, `rfc2119`) and engineering playbook templates.

### Patch Changes

- [`02d2f6b`](https://github.com/rudironsoni/skills/commit/02d2f6bfbda825c0388e361dac1d2832b25962e2) Thanks [@rudironsoni](https://github.com/rudironsoni)! - Add run-scoped bidirectional messaging to `herdr-orchestration` so workers can push updates, questions, blockers, and results to the controller and receive answers or follow-up instructions through Herdr's native agent prompt channel.

## [1.1.0](https://github.com/rudironsoni/skills/compare/v1.0.0...v1.1.0) (2026-07-27)

### Features

- add herdr-agent-comms skill ([331faa6](https://github.com/rudironsoni/skills/commit/331faa60fc5d12e7ff8d546dbfddc23391b8515a))
- add stop-slop writing skill ([c98f4fe](https://github.com/rudironsoni/skills/commit/c98f4fe6653fd639d0894a5987ea9fb866c5c8c2))

## 1.0.0 (2026-07-26)

### Features

- Published eight reusable skills grouped by orchestration, prompting, engineering, writing, and visualization capabilities.
- Added repository-wide Claude plugin and marketplace metadata alongside Agent Skills installation support.
- Added synchronized package and plugin versioning with structural validation for the canonical skill tree.
