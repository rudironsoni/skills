---
name: prompting-fable-5
description: >-
  Prompting reference for Claude Fable 5 and Claude Mythos 5: cross-model
  baseline plus Fable-specific behaviors and tested snippets.
---

Fable 5 and Mythos 5 share one underlying model. Fable 5 adds safety classifiers, Mythos 5 ships without them to approved organizations, so everything here applies to both. This skill is all reference: an orientation, then paste-ready snippets keyed by the un-steered behavior each one fixes. Paste snippets **verbatim**, the exact wording is what Anthropic tested. Techniques shared by all current Claude models (clarity, examples, XML structure, long context, formatting control, tool use, thinking, agentic systems) live in [claude-prompting-best-practices.md](references/claude-prompting-best-practices.md); read it when composing a full prompt or harness, since this file holds only what Fable 5 does differently. Harnesses where the model runs while the user is away have their own patterns in [long-running-agents.md](references/long-running-agents.md).

## Orientation

Five facts that change how you prompt:

- **Assign it your hardest problems.** Fable 5 handles work that was too complex, long-running, or ambiguous for prior models, including end-to-end tasks that take a person hours to weeks. Testing it only on simple workloads undersells its range; it still performs reliably there. Have it scope the task, ask clarifying questions, and execute.
- **Effort is the primary dial** for intelligence vs latency vs cost. Default `high`, reserve `xhigh` for the most capability-sensitive work, use `medium` or `low` for routine tasks. Low effort on Fable 5 often still beats `xhigh` on prior models, so reduce effort when tasks complete correctly but slowly, or when you want a snappier interactive feel.
- **One brief instruction steers.** Instruction following is strong enough that a short statement of the target behavior replaces an enumerated list of cases. A prompt that lists every variant of a behavior is a migration smell: collapse it into one sentence and re-test.
- **Turns run long.** Hard tasks run many minutes at higher effort, and autonomous runs extend for hours. Raise client timeouts, stream output, and surface progress before migrating. See [long-running-agents.md](references/long-running-agents.md).
- **Refusals are a stop reason to handle.** Safety classifiers target offensive cybersecurity, biology and life-sciences methods, and extraction of the model's summarized thinking; benign work in those domains can trigger them too. Handle `stop_reason: "refusal"` with server-side or client-side fallback to Claude Opus 4.8.

## Steering snippets

Each heading names an un-steered behavior; the snippet under it is the fix.

### Overplans instead of acting

On ambiguous tasks at higher effort, Fable 5 can keep gathering context and deliberating past the point of usefulness.

```text
When you have enough information to act, act. Do not re-derive facts already established in the conversation, re-litigate a decision the user has already made, or narrate options you will not pursue in user-facing messages. If you are weighing a choice, give a recommendation, not an exhaustive survey. This does not apply to thinking blocks.
```

### Tidies, refactors, and hardens beyond the task

Higher effort buys rigorous verification and sophisticated reasoning, and it also invites unrequested cleanup around the actual change.

```text
Don't add features, refactor, or introduce abstractions beyond what the task requires. A bug fix doesn't need surrounding cleanup and a one-shot operation usually doesn't need a helper. Don't design for hypothetical future requirements: do the simplest thing that works well. Avoid premature abstraction and half-finished implementations. Don't add error handling, fallbacks, or validation for scenarios that cannot happen. Trust internal code and framework guarantees. Only validate at system boundaries (user input, external APIs). Don't use feature flags or backwards-compatibility shims when you can just change the code.
```

### Writes more than the reader needs

Un-steered, it surveys options it won't pursue, explains root causes at length, produces heavily structured PR descriptions, and writes comments that narrate the next line. One brevity instruction replaces listing those patterns:

```text
Lead with the outcome. Your first sentence after finishing should answer "what happened" or "what did you find": the thing the user would ask for if they said "just give me the TLDR." Supporting detail and reasoning come after. Being readable and being concise are different things, and readability matters more.

The way to keep output short is to be selective about what you include (drop details that don't change what the reader would do next), not to compress the writing into fragments, abbreviations, arrow chains like A → B → fails, or jargon.
```

### Pauses at checkpoints it could pass

To have it stop only where it genuinely needs the user, state the boundary once instead of enumerating cases:

```text
Pause for the user only when the work genuinely requires them: a destructive or irreversible action, a real scope change, or input that only they can provide. If you hit one of these, ask and end the turn, rather than ending on a promise.
```

### Acts when you wanted an assessment

It can occasionally take unrequested actions, such as drafting an email nobody asked for or creating defensive git-branch backups. State what a report is and what an action is:

```text
When the user is describing a problem, asking a question, or thinking out loud rather than requesting a change, the deliverable is your assessment. Report your findings and stop. Don't apply a fix until they ask for one. Before running a command that changes system state (restarts, deletes, config edits), check that the evidence actually supports that specific action. A signal that pattern-matches to a known failure may have a different cause.
```

## Authoring requests

Fable 5 performs better when it knows the intent behind a request: context lets it connect the task to relevant information rather than inferring intent on its own. This matters most for long-running agents drawing on multiple workstreams. Frame requests as:

```text
I'm working on [the larger task] for [who it's for]. They need [what the output enables]. With that in mind: [request].
```

## Migrating from earlier Claude models

- **Prune prescriptive prompts and skills.** Skills written for prior models are often too prescriptive for Fable 5 and can degrade output. Remove an instruction, re-test, and keep it out when default behavior is better. Fable 5 also updates skills on the fly from what it learns in the task.
- **Remove "show your reasoning" instructions.** Telling the model to echo, transcribe, or explain its internal reasoning as response text triggers the `reasoning_extraction` refusal category and elevated fallbacks. Read the structured `thinking` blocks from adaptive thinking instead, and surface progress with a send-to-user tool ([long-running-agents.md](references/long-running-agents.md)).
- **Update API handling.** Adaptive thinking only, no extended-thinking budgets, summarized-only thinking output, and the `refusal` stop reason. See Anthropic's "Introducing Claude Fable 5 and Claude Mythos 5" docs page.
- **Re-test guardrails.** A capability jump this size is a prompt to re-evaluate which instructions, tools, and guardrails are still needed at all.
