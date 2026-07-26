---
name: prompting-opus-4-8
description: >-
  Prompting reference for Claude Opus 4.8: cross-model baseline plus
  Opus-specific behaviors and tested snippets.
---

This skill is all reference: an orientation, then fixes keyed by the un-steered behavior each one addresses. Paste snippets **verbatim**, the wording is Anthropic's tested prompt language. Techniques shared by all current Claude models (clarity, examples, XML structure, long context, formatting control, tool use, thinking, agentic systems) live in [claude-prompting-best-practices.md](references/claude-prompting-best-practices.md); read it when composing a full prompt or harness, since this file holds only what Opus 4.8 does differently. Design and frontend defaults have their own branch in [frontend-defaults.md](references/frontend-defaults.md).

## Orientation

- **Existing prompts carry over.** Opus 4.8 performs well out of the box on Opus 4.7 prompts, with particular strengths in long-horizon agentic work, knowledge work, vision, and memory tasks.
- **Effort matters more than on any prior Opus**, so experiment with it actively when upgrading. Start `xhigh` for coding and agentic use cases, and use a minimum of `high` for intelligence-sensitive work. The rungs:
  - `max`: can deliver gains but shows diminishing returns from token usage and is sometimes prone to overthinking; test it on intelligence-demanding tasks.
  - `xhigh`: the best setting for most coding and agentic use cases.
  - `high`: balances token usage and intelligence; the floor for intelligence-sensitive work.
  - `medium`: cost-sensitive work that can trade off intelligence.
  - `low`: short, scoped, latency-sensitive tasks that are not intelligence-sensitive.

  At `max` or `xhigh`, set a large max output token budget (start at 64k) so the model has room to think and act across subagents and tool calls.
- **Thinking is off by default.** Enable it explicitly with `thinking: {type: "adaptive"}`.
- **It follows instructions literally**, especially at lower effort: no silent generalization from one item to the next, no inferred requests you didn't make. That precision favors tuned pipelines and structured extraction. When you want breadth, state the scope: "Apply this formatting to every section, not just the first one."
- **Migrating from Opus 4.7 also changes API handling** (sampling parameters, effort default, 1M context window default, mid-conversation system messages, refusal stop details). See Anthropic's migration guide for Opus 4.7 to 4.8.

## Steering

Each heading names an un-steered behavior; the fix follows.

### Answer length tracks task complexity, not your product's voice

It calibrates response length to how complex it judges the task: short on lookups, long on open-ended analysis. If your product depends on a fixed verbosity, tune for it:

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

### Reasons instead of calling tools

It favors reasoning over tool calls, which produces better results in most cases. When you want more tool use, especially in knowledge work and agentic search, raise effort: `high` and `xhigh` show substantially more tool usage. Also describe per tool when and why the model should reach for it, for example why and how to use your web search tool.

### Spawns fewer subagents

Steerable with explicit guidance on when subagents are desirable:

```text
Do not spawn a subagent for work you can complete directly in a single response (e.g. refactoring a function you can already see).

Spawn multiple subagents in the same turn when fanning out across items or reading multiple files.
```

### Forced progress-update scaffolding now hurts

It already provides regular, higher-quality user-facing updates through long agentic traces. Remove scaffolding like "After every 3 tool calls, summarize progress" and re-test. If the updates are miscalibrated for your product, describe what they should look like and give examples.

### Tone drifts from your product voice

The baseline is direct and opinionated, with minimal validation-forward phrasing and sparing emoji use. Re-evaluate style prompts against that baseline. For a warmer voice:

```text
Use a warm, collaborative tone. Acknowledge the user's framing before answering.
```

### A persistent design house style

On open-ended frontend and slide briefs it returns a consistent cream-and-serif style, and generic objections shift it to a different fixed palette instead of producing variety. The two fixes that work are in [frontend-defaults.md](references/frontend-defaults.md).

## Harness notes

- **Interactive coding products.** It uses more tokens in interactive, multi-turn settings because it reasons more after user turns, which helps long-horizon coherence but costs tokens. Use `xhigh` or `high` effort, add autonomous features like an auto mode, and reduce required human interactions. Front-load the task, intent, and constraints in the first turn; ambiguous prompts conveyed progressively over turns reduce token efficiency and sometimes performance.
- **Code review harnesses.** Bug-finding recall and precision are higher than prior models, but a harness tuned for an earlier model can show lower measured recall: instructions like "only report high-severity issues" are now followed faithfully, so the model investigates just as deeply and then withholds findings below your stated bar. Move filtering out of the finding step:

  ```text
  Report every issue you find, including ones you are uncertain about or consider low-severity. Do not filter for importance or confidence at this stage - a separate verification step will do that. Your goal here is coverage: it is better to surface a finding that later gets filtered out than to silently drop a real bug. For each finding, include your confidence level and an estimated severity so a downstream filter can rank them.
  ```

  This works even without an actual second step. If you do want single-pass self-filtering, state the bar concretely instead of qualitatively: "report any bugs that could cause incorrect behavior, a test failure, or a misleading result; only omit nits like pure style or naming preferences." Validate recall or F1 changes against a subset of your evals.
- **Computer use.** Works across resolutions up to 2576px / 3.75MP. 1080p balances performance and cost; 720p or 1366×768 are lower-cost options with strong performance. Effort settings also tune behavior here.
