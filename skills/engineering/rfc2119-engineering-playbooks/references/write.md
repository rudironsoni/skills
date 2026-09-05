# Write an SOP

Produce one `.sop.md` playbook. Load [rfc2119.md](rfc2119.md) when you set requirement keywords.

## Steps

1. Ask purpose, if missing: what workflow, when to use it, what done looks like.
2. Pick one type: analysis, implementation, deploy, or maintenance. One SOP, one job.
3. Write the file from the skeleton below. Keep that section order.
4. Title: `# {Action Verb} {Outcome}`. File name: kebab-case, `.sop.md`.
5. Each step starts with an imperative verb, does one action, and ends with **Validation** that a later reader can check.
6. Put reusable values in `{parameter}` and list them under Parameters. Use them in the steps.
7. Apply RFC 2119 keywords from [rfc2119.md](rfc2119.md).
8. Walk the steps once. Fix anything that cannot run as written.

## Skeleton

```markdown
# {Action Verb} {Outcome}

## Overview

{What this SOP does, when to use it, why this path.}

## Parameters

- **{Name}**: {parameter_name} - meaning and example values

## Prerequisites

### Required Tools
- {tool} ({version or higher})

### Required Knowledge
- {fact the agent must already have}

### Required Setup
- {env, credentials, or files that must exist}

## Steps

1. {Imperative action}
   - {detail}
   - **Validation**: {checkable result}

2. {Next action}
   - **Validation**: {checkable result}

## Success Criteria

- [ ] {measurable outcome}
- [ ] {measurable outcome}

## Error Handling

### Error: {name}

**Symptoms**: {what you see}
**Cause**: {why}
**Resolution**:
1. {action}
2. {action}

## Related SOPs

- **{name}**: when to use it instead, or next
```

## Instruction rules

- Active voice. Numbered lists for sequence. Bullets for unordered detail.
- Success criteria are measurable (command exit, coverage number, health check).
- Error handling names symptoms, cause, and a resolution path.
- Related SOPs name a real sibling or "none".

## Done

- The file exists at the agreed path with a kebab-case `.sop.md` name.
- Every MUST is checkable.
- A walk-through of the steps succeeds without unstated tools or knowledge.
