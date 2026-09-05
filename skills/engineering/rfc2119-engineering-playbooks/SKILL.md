---
name: rfc2119-engineering-playbooks
description: >-
  RFC 2119 engineering playbooks (SOPs). Use when writing or updating a
  Standard Operating Procedure, choosing MUST/SHOULD/MAY, or running a named
  playbook (API review, TDD, production debug, code-review quality, refactor).
---

# RFC 2119 Engineering Playbooks

Write and run engineering SOPs with RFC 2119 requirement keywords. Load only the file the current branch needs.

## RFC 2119

| Keyword | Meaning |
| --- | --- |
| MUST | Absolute requirement |
| MUST NOT | Absolute prohibition |
| SHOULD | Strong recommendation |
| SHOULD NOT | Strong discouragement |
| MAY | Optional |

Keyword rules: [rfc2119.md](references/rfc2119.md)

## Branch

| Task | Load |
| --- | --- |
| Write a new SOP | [write.md](references/write.md), then [rfc2119.md](references/rfc2119.md) when choosing keywords |
| Update an SOP | [update.md](references/update.md) |
| Check keywords | [rfc2119.md](references/rfc2119.md) |
| Run a named playbook | matching `templates/*.sop.md` only |

## Templates

| Playbook | File |
| --- | --- |
| API design review | [api-design-review.sop.md](templates/api-design-review.sop.md) |
| Code-review quality | [code-review-quality.sop.md](templates/code-review-quality.sop.md) |
| Production debug | [debug-production-issue.sop.md](templates/debug-production-issue.sop.md) |
| TDD feature | [implement-feature-tdd.sop.md](templates/implement-feature-tdd.sop.md) |
| Refactor | [refactor-for-maintainability.sop.md](templates/refactor-for-maintainability.sop.md) |

## File rules

- kebab-case name
- `.sop.md` extension
