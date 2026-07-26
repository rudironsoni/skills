---
name: prompting-sonnet-5
description: >-
  Prompting reference for Claude Sonnet 5: cross-model baseline plus
  Sonnet-specific behaviors and tested snippets.
---

This skill is all reference: an orientation, then fixes keyed by the un-steered behavior each one addresses. Paste snippets **verbatim**, the wording is Anthropic's tested prompt language. Techniques shared by all current Claude models (clarity, examples, XML structure, long context, formatting control, tool use, thinking, agentic systems) live in [claude-prompting-best-practices.md](references/claude-prompting-best-practices.md); read it when composing a full prompt or harness, since this file holds only what Sonnet 5 does differently. Design and frontend defaults have their own branch in [frontend-defaults.md](references/frontend-defaults.md).

## Orientation

- **Existing prompts carry over.** Sonnet 5 performs well out of the box on Sonnet 4.6 prompts, with particular strengths in coding and agentic tasks.
- **Effort defaults to `high`.** Raise to `xhigh` for the hardest coding and agentic tasks. The rungs:
  - `max`: absolute maximum capability with no constraints on token spending.
  - `xhigh`: recommended for the hardest coding and agentic use cases.
  - `high`: the default; balances token usage and intelligence for most use cases.
  - `medium`: cost-sensitive work that can trade off intelligence.
  - `low`: short, scoped, latency-sensitive tasks that are not intelligence-sensitive.

  Rough cross-model mapping when migrating: Sonnet 5 at `medium` is comparable to Sonnet 4.6 at `high`, and Sonnet 5 at `high` to Sonnet 4.6 at `max`. When benchmarking, match by observed thinking length rather than effort name.
- **Adaptive thinking is on by default**, a change from Sonnet 4.6 where requests without a `thinking` field ran without thinking. Turn it off entirely with `thinking: {type: "disabled"}`. Workloads that ran with thinking off on 4.6 are worth retrying with thinking on at lower effort. Manual extended thinking (`thinking: {type: "enabled", budget_tokens: N}`) returns a 400 error; use adaptive thinking with effort instead.
- **It follows instructions literally**, especially at lower effort: no silent generalization from one item to the next, no inferred requests you didn't make. That precision favors tuned pipelines and structured extraction. When you want breadth, state the scope: "Apply this formatting to every section, not just the first one."
- **Migrating from Sonnet 4.6 also changes API handling**: non-default `temperature`, `top_p`, or `top_k` return a 400 error, and a new tokenizer produces roughly 30% more tokens for the same text. See Anthropic's migration guide for Sonnet 4.6 to Sonnet 5.

## Steering

Each heading names an un-steered behavior; the fix follows.

### Answer length tracks task complexity, not your product's voice

It calibrates response length to the complexity of the task: short on lookups, longer on open-ended analysis. If your product depends on a fixed verbosity, tune for it:

```text
Provide concise, focused responses. Skip non-essential context, and keep examples minimal.
```

Positive examples showing the concision you want work better than instructions about what to avoid.

### Shallow reasoning at low effort

It respects effort strictly, especially at the low end: at `low` and `medium` it scopes work to what was asked rather than going beyond. On moderately complex tasks at `low`, that risks under-thinking. Raise effort to `high` or `xhigh` rather than prompting around it; if latency pins you at `low`, add:

```text
This task involves multi-step reasoning. Think carefully through the problem before responding.
```

### Thinks more often than you'd like

Adaptive thinking's triggering is steerable, and large or complex system prompts can over-trigger it. Measure the effect of any change:

```text
Thinking adds latency and should only be used when it will meaningfully improve answer quality, typically for problems that require multi-step reasoning. When in doubt, respond directly.
```

The reverse case, under-thinking on hard workloads at `medium`: raise effort first, and prompt for depth only when you need finer control.

### Answers truncated at max_tokens

`max_tokens` is a hard limit on total output, thinking plus response text. At `high`, `xhigh`, or `max` effort on long tasks, adaptive thinking can use a large share of the budget; a tight budget shows up as a response that is almost entirely thinking followed by a truncated answer and `stop_reason: "max_tokens"`. Raise `max_tokens` or drop to `medium`. Limits tuned for Sonnet 4.6 need revisiting twice over: thinking is now on by default, and the new tokenizer adds roughly 30% tokens for the same text.

### Missing tool calls with thinking off

Sonnet 5 is more agentic than 4.6 by default, reaching for tools and running self-verification loops readily. With thinking disabled it is less likely to reach for tools or consider searching; if you rely on tool calls with thinking off, add an explicit nudge in the system prompt. Effort is also a lever: `high` and `xhigh` show substantially more tool usage in agentic search and coding. Describe per tool when and why the model should reach for it, for example why and how to use your web search tool.

### Forced progress-update scaffolding now hurts

It already provides regular, higher-quality user-facing updates through long agentic traces. Remove scaffolding like "After every 3 tool calls, summarize progress" and re-test. If the updates are miscalibrated for your product, describe what they should look like and give examples.

### Tone drifts from your product voice

Prose style shifts with any new model, so re-evaluate style prompts against the new baseline. For a warmer voice:

```text
Use a warm, collaborative tone. Acknowledge the user's framing before answering.
```

Stylistic variety that previously came from `temperature` now comes from system-prompt instructions, since non-default sampling parameters return a 400 error.

### A persistent design default

On open-ended frontend and design briefs it may settle into a consistent default visual style, and generic objections shift it to a different fixed palette instead of producing variety. The two fixes that work are in [frontend-defaults.md](references/frontend-defaults.md).

## Harness notes

- **Interactive coding products.** Token usage and behavior differ between single-turn autonomous agents and multi-turn interactive ones. Use `xhigh` or `high` effort, add autonomous features like an auto mode, and reduce required human interactions. Front-load the task, intent, and constraints in the first turn; ambiguous prompts conveyed progressively over turns reduce token efficiency and sometimes performance.
- **Code review harnesses.** A harness tuned for an earlier model can show lower measured recall even though bug-finding ability improved: instructions like "only report high-severity issues" are now followed faithfully, so the model investigates just as deeply and then withholds findings below your stated bar. Move filtering out of the finding step:

  ```text
  Report every issue you find, including ones you are uncertain about or consider low-severity. Do not filter for importance or confidence at this stage - a separate verification step will do that. Your goal here is coverage: it is better to surface a finding that later gets filtered out than to silently drop a real bug. For each finding, include your confidence level and an estimated severity so a downstream filter can rank them.
  ```

  This works even without an actual second step. If you do want single-pass self-filtering, state the bar concretely instead of qualitatively: "report any bugs that could cause incorrect behavior, a test failure, or a misleading result; only omit nits like pure style or naming preferences." Validate recall or F1 changes against a subset of your evals.
- **Computer use.** Supports the `computer_20251124` tool version, across resolutions up to 2576px / 3.75MP. 1080p balances performance and cost; 720p or 1366×768 are lower-cost options with strong performance. Effort settings also tune behavior here.
