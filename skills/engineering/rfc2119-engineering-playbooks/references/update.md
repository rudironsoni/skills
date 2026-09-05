# Update an SOP

Change an existing `.sop.md`. Load [rfc2119.md](rfc2119.md) if keywords move.

## Steps

1. Name the SOP and the trigger (tool change, process change, incident, or feedback).
2. Read the current file. Note the version if one exists.
3. Classify the bump:
   - **patch**: clarify wording, fix a typo, refresh an example
   - **minor**: add a non-breaking step, parameter, or error path
   - **major**: replace a tool or change the process so old steps no longer work
4. Edit the affected sections. Keep RFC 2119 keywords true.
5. Write the changelog. For a major bump, add a migration note.
6. If the SOP is retired, deprecate it and keep the old body under the notice.
7. Check Related SOPs still point at live files.

## Changelog

Put this under the title:

```markdown
**Version**: {x.y.z}
**Last Updated**: {YYYY-MM-DD}

## Changelog

### v{x.y.z} ({YYYY-MM-DD})
- {change}
- {change}

*Reason: {why}*
```

## Migration note (major)

```markdown
## Migration from v{old}.x

1. **{Change}**
   - **Old**: {behavior}
   - **New**: {behavior}
   - **Action**: {what the user must do}
```

## Deprecate

Replace the title block with:

```markdown
# DEPRECATED: {Old title}

**Status**: DEPRECATED as of {YYYY-MM-DD}
**Replaced By**: {new-file.sop.md}
**Reason**: {why}

## Migration

1. {step}

---

## Original SOP

{keep the old body here}
```

## Done

- Version bumped to match the change class.
- Changelog has date, bullets, and reason.
- Prerequisites, examples, and Related SOPs match the current process.
- A walk-through of the new steps succeeds.
