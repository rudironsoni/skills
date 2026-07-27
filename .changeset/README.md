# Changesets

Every change that affects distributed skills needs a changeset:

```bash
npm run changeset
```

Choose `minor` for a new skill, `patch` for a compatible fix, or `major` for a breaking change. The release workflow collects these fragments into one rolling version pull request. Merging that pull request creates the Git tag and GitHub Release.
