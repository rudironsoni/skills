# Model routing during a goal run

A goal run splits into three kinds of work, each mapped to the model built for it. Spawn subagents with a model override (Agent tool: `model: "opus"` or `model: "sonnet"`; workflow scripts: `agent(prompt, {model, effort})`). The goal-relevant essentials for each model are inlined here so this skill stands alone; when the `prompting-fable-5`, `prompting-opus-4-8`, and `prompting-sonnet-5` skills are installed, invoke them for each model's full behavior reference and snippet library.

## Routing table

| Subtask                                                                  | Model            | Why                                                        |
| :----------------------------------------------------------------------- | :--------------- | :---------------------------------------------------------- |
| Orchestration, planning, integration, final verification, evaluator evidence | Session (Fable 5) | Long-horizon autonomy, dependable subagent dispatch          |
| Root-cause diagnosis, architecture, cross-cutting design, review/verification passes, dense-image work | Opus 4.8 subagent | Deep reasoning, high bug-finding recall and precision        |
| Well-specified implementation, per-item mechanical migration, test writing, fan-out over similar items | Sonnet 5 subagent | Strong coding/agentic profile, self-verifies, cheap to fan out |

## The session: Claude Fable 5

Run the goal session on Fable 5. It holds a run together across many turns: long-horizon autonomy with strong instruction retention, dependable dispatch and ongoing communication with parallel subagents, and it determines next steps well when the goal leaves room for judgment. Effort `high` is the default; reserve `xhigh` for capability-critical goals.

Goal-relevant steering (full library in `prompting-fable-5`):

- Keep it on orchestration and verification; bounded implementation goes to subagents so the session context stays about the goal, not one subtask's weeds.
- The grounding instruction in [SKILL.md](../SKILL.md) is mandatory here: this model's progress reports are what the evaluator judges.
- At higher effort it can gather context past what a turn needs. Steer with: "When you have enough information to act, act. Do not re-derive facts already established in the conversation, re-litigate a decision the user has already made, or narrate options you will not pursue in user-facing messages. If you are weighing a choice, give a recommendation, not an exhaustive survey. This does not apply to thinking blocks."
- A goal run should not pause to ask what it can decide: "Pause for the user only when the work genuinely requires them: a destructive or irreversible action, a real scope change, or input that only they can provide. If you hit one of these, ask and end the turn, rather than ending on a promise." For fully unattended `-p` runs, `prompting-fable-5` has the longer autonomous-pipeline reminder.

## Deep subtasks: Opus 4.8 subagents

Route here the work where being right matters more than being fast: diagnosis of a failure the goal keeps hitting, architectural or cross-cutting design decisions, review and bug-finding passes over produced changes (recall and precision above prior models), verification of another agent's claim, and detailed screenshot or image interpretation. Use `xhigh` effort for these when the harness exposes effort.

Prompting a single-shot Opus subagent (full library in `prompting-opus-4-8`):

- **Front-load everything.** It performs best with the task, intent, constraints, and expected output specified in the one prompt it gets; it interprets literally and does not generalize scope you didn't state. Say "apply to every module in src/legacy, not just the first" when you mean all of them.
- **Tell it when to use tools.** It favors reasoning over tool calls; if the subtask requires running commands or searching, state when and why.
- **For review passes, demand coverage, not filtering:**

  ```text
  Report every issue you find, including ones you are uncertain about or consider low-severity. Do not filter for importance or confidence at this stage - a separate verification step will do that. Your goal here is coverage: it is better to surface a finding that later gets filtered out than to silently drop a real bug. For each finding, include your confidence level and an estimated severity so a downstream filter can rank them.
  ```

  The orchestrator then filters, which keeps judged-out findings visible instead of silently dropped.

## Scoped subtasks: Sonnet 5 subagents

Route here anything with a crisp spec and a runnable check: implementing a defined function or endpoint, migrating one file among many, writing tests against stated behavior, and fan-out across item-shaped work (one item per subagent keeps each prompt crisp and lets them run in parallel). Strong coding and agentic profile; it reaches for tools and runs self-verification loops readily.

Prompting a Sonnet subagent (full library in `prompting-sonnet-5`):

- **Spec plus check.** Give the exact scope and the verification to run before returning: "migrate src/legacy/billing.ts to ApiV2, then run `npm test -- billing` and include the output."
- **State scope explicitly.** It follows instructions literally and does not infer requests you didn't make, which is exactly what bounded fan-out needs.
- **Match effort to the item.** It respects effort strictly: `high` for normal items, `medium` for genuinely mechanical ones, `xhigh` only when an item turns out hard. At lower effort it does what was asked and nothing more, which keeps fan-out cheap and predictable.

## Subagent prompts that survive the evaluator

The evaluator reads only the session transcript, so a subagent's work counts only when the orchestrator can quote it. Build every subagent prompt with:

1. **The reason, not only the request.** "This is part of [the goal]. The result feeds [next step]. With that in mind: [task]." Intent context measurably improves output.
2. **An evidence clause.** Name what to run and what to paste back (test summary, exit code, file list). A subagent that returns "done" gives the orchestrator nothing to surface.
3. **Constraints from the goal condition.** If the condition says "no test file is modified", every implementation subagent's prompt carries that line, since the subagent never sees the goal itself.

The orchestrator's turn then quotes the returned evidence next to its own verification, which is what the evaluator judges.
