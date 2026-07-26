---
name: goal-mode
description: >-
  Techniques for Claude Code goal mode (/goal): choosing the right loop,
  writing conditions the evaluator can verify, running and bounding goals,
  and routing work across models mid-run.
---

`/goal` (Claude Code v2.1.139+) sets a completion condition and Claude keeps working across turns until it holds. After each turn, a small fast model (default Haiku) judges the condition against the conversation: "no" starts another turn with the judge's reason as guidance, "yes" clears the goal. This skill covers picking the right loop, writing a condition that survives many turns, running the goal, and delegating mid-run. Which model carries which work, and how to prompt each as a subagent, is in [model-routing.md](references/model-routing.md).

## Pick the right loop

`/goal` fits substantial work with a verifiable end state: migrating a module until every call site compiles and tests pass, implementing a design doc until all acceptance criteria hold, splitting a large file until each piece is under a size budget, draining a labeled issue backlog until the queue is empty.

| Approach  | Next turn starts when      | Stops when                                     |
| :-------- | :------------------------- | :--------------------------------------------- |
| `/goal`   | The previous turn finishes | The evaluator confirms the condition is met    |
| `/loop`   | A time interval elapses    | You stop it, or Claude decides the work is done |
| Stop hook | The previous turn finishes | Your own script or prompt decides               |

A Stop hook lives in settings, applies to every session in its scope, and can run a script for deterministic checks; `/goal` is the session-scoped shortcut with a model-evaluated condition. Auto mode is complementary, not an alternative: it approves tool calls within a turn, `/goal` starts the next turn. Pair them so goal turns run unattended.

## The evaluator reads only the transcript

The evaluator runs no commands and reads no files; it judges the condition against what has been surfaced in the conversation, and it is a small fast model, so the evidence must be explicit and legible. Two working rules follow:

- **Write the condition around evidence that can land in the transcript.** "All tests in `test/auth` pass" works because the test run's output appears in the conversation. "The code is well-factored" gives the evaluator nothing checkable.
- **End every turn with the receipts.** Run the stated check and show its result: the test summary line, the exit code, the file count, `git status` output. A turn that ends mid-work without evidence earns a "no" and burns an evaluation round.

Progress claims feed the evaluator, so an ungrounded claim can end the goal early on false evidence. Add Anthropic's grounding instruction to the session or system prompt for the run:

```text
Before reporting progress, audit each claim against a tool result from this session. Only report work you can point to evidence for; if something is not yet verified, say so explicitly. Report outcomes faithfully: if tests fail, say so with the output; if a step was skipped, say that; when something is done and verified, state it plainly without hedging.
```

## Write the condition

A condition that holds up across many turns has four parts (up to 4,000 characters):

1. **One measurable end state**: a test result, a build exit code, a file count, an empty queue.
2. **A stated check**: how Claude proves it, such as "`npm test` exits 0" or "`git status` is clean". Prefer a check that is cheap to re-run, since it gets re-surfaced every turn.
3. **Constraints that must hold on the way there**: "no other test file is modified", "public API signatures unchanged".
4. **A bound clause**: "or stop after 20 turns". Claude reports progress against it each turn and the evaluator judges it from the conversation.

The evaluator's "no" reason becomes guidance for the next turn, so a condition with observable subparts ("every file in src/legacy/ migrated, `npm test` exits 0, lint clean") produces actionable reasons ("lint step still failing") instead of a flat restatement.

```text
/goal every call site of the old client in src/api is migrated to ApiV2, `npm test` exits 0, and `npm run lint` is clean; no test file is modified; or stop after 25 turns
```

## Run it

- **Set:** `/goal <condition>` starts a turn immediately with the condition as the directive; no separate prompt needed. Setting a new goal replaces the active one (one per session). A `◎ /goal active` indicator shows run time.
- **Status:** `/goal` with no argument shows the condition, duration, turns evaluated, token spend, and the evaluator's most recent reason. After completion it shows the achieved entry.
- **Clear:** `/goal clear` (aliases: `stop`, `off`, `reset`, `none`, `cancel`). `/clear` also removes the goal along with the conversation.
- **Resume:** an active goal is restored with `--resume`/`--continue`; the condition carries over but turn count, timer, and token baseline reset. Achieved or cleared goals do not restore.
- **Non-interactive:** `claude -p "/goal <condition>"` runs the loop to completion in one invocation; Ctrl+C interrupts. For unattended runs, pair the condition's bound clause with auto mode and the grounding instruction above.

## Delegate mid-run

A goal run is an orchestration problem: the session model plans, integrates results, runs the final checks, and surfaces evidence for the evaluator, while bounded subtasks go to subagents on the model that fits them. Read [model-routing.md](references/model-routing.md) before spawning: it maps subtask types to models, gives each model's capability profile, and shows how to prompt each one so its results survive the evaluator.

## Requirements

`/goal` is a wrapper around a session-scoped prompt-based Stop hook, so it needs the workspace trust dialog accepted, and it is unavailable when `disableAllHooks` is set at any settings level or `allowManagedHooksOnly` is set in managed settings. Evaluation tokens are billed on the configured small fast model and are typically negligible next to main-turn spend.
