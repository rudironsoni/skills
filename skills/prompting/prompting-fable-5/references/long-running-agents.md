# Long-running and autonomous Fable 5 agents

Patterns for harnesses where Fable 5 works while the user is away: multi-hour autonomous runs, pipelines, background agents. As in [SKILL.md](../SKILL.md), paste snippets verbatim.

## Restructure the harness before migrating

Individual requests on hard tasks run many minutes at higher effort, and autonomous runs extend for hours. Raise client timeouts, stream output, and add user-facing progress indicators. Check on runs asynchronously, for example through scheduled jobs, rather than blocking on a single call.

## Ground progress claims

In Anthropic's testing, auditing claims against tool results nearly eliminated fabricated status reports, even on tasks designed to elicit them:

```text
Before reporting progress, audit each claim against a tool result from this session. Only report work you can point to evidence for; if something is not yet verified, say so explicitly. Report outcomes faithfully: if tests fail, say so with the output; if a step was skipped, say that; when something is done and verified, state it plainly without hedging.
```

## Early stopping

Deep into a long session, Fable 5 can occasionally end a turn with a text-only statement of intent ("I'll now run X") without issuing the tool call, or ask permission when it already has enough to proceed. Interactively, a "continue" or "go ahead and do it end to end" suffices. Autonomous pipelines get a standing reminder, paired with the checkpoint snippet in [SKILL.md](../SKILL.md):

```text
You are operating autonomously. The user is not watching in real time and cannot answer questions mid-task, so asking "Want me to…?" or "Shall I…?" will block the work. For reversible actions that follow from the original request, proceed without asking. Offering follow-ups after the task is done is fine; asking permission after already discussing with the user before doing the work is not. Before ending your turn, check your last paragraph. If it is a plan, an analysis, a question, a list of next steps, or a promise about work you have not done ("I'll…", "let me know when…"), do that work now with tool calls. End your turn only when the task is complete or you are blocked on input only the user can provide.
```

## Context-budget worry

In very long sessions it can suggest a new session, offer to summarize and hand off, or trim its own work. The usual trigger is a remaining-token countdown shown to the model, so hide explicit context-budget counts where possible. Where the harness must show them, add:

```text
You have ample context remaining. Do not stop, summarize, or suggest a new session on account of context limits. Continue the work.
```

## Unreadable final summaries

After many tool calls it can hand the user dense arrow-chain shorthand, deep implementation detail, references to thinking the user never saw, or labels it invented mid-run. A communication-style addendum mitigates this:

```text
Terse shorthand is fine between tool calls (that's you thinking out loud, and brevity there is good). Your final summary is different: it's for a reader who didn't see any of that.

If you've been working for a while without the user watching (overnight, across many tool calls, since they last spoke), your final message is their first look at any of it. Write it as a re-grounding, not a continuation of your working thread: the outcome first, then the one or two things you need from them, each explained as if new. The vocabulary you built up while working is yours, not theirs; leave it behind unless you re-introduce it.

When you write the summary at the end, drop the working shorthand. Write complete sentences. Spell out terms. Don't use arrow chains, hyphen-stacked compounds, or labels you made up earlier. When you mention files, commits, flags, or other identifiers, give each one its own plain-language clause. Open with the outcome: one sentence on what happened or what you found. Then the supporting detail. If you have to choose between short and clear, choose clear.
```

## send_to_user tool

When the UX depends on the user seeing content exactly as written mid-task (a generated snippet, a drafted message, a progress update with specific numbers, a direct reply to a mid-loop question), give the agent a client-side tool whose input your UI renders directly, returning a simple acknowledgement. Tool inputs are never summarized, so the content arrives intact without ending the turn. For agents that only narrate routine progress, the model's own summaries are adequate.

```json
{
  "name": "send_to_user",
  "description": "Display a message directly to the user. Use this for progress updates, partial results, or content the user must see exactly as written before the task finishes.",
  "input_schema": {
    "type": "object",
    "properties": {
      "message": {
        "type": "string",
        "description": "The content to display to the user."
      }
    },
    "required": ["message"]
  }
}
```

Defining the tool is not enough; without an instruction in the system prompt, Fable 5 rarely calls it. Pair it with:

```text
Between tool calls, when you have content the user must read verbatim (a partial deliverable, a direct answer to their question), call the send_to_user tool with that content. Use send_to_user only for user-facing content, not for narration or reasoning.
```

Route only user-facing content through it; narration and reasoning through this channel defeat its purpose.

## Parallel subagents

Fable 5 dispatches parallel subagents more readily than prior models and manages ongoing communication with long-running subagents and peer agents dependably. Use subagents frequently, say when delegation is appropriate, and prefer asynchronous communication over blocking until each subagent returns. Long-lived subagents that keep context across subtasks save time and cost through cache reads and avoid bottlenecking on the slowest subagent.

```text
Delegate independent subtasks to subagents and keep working while they run. Intervene if a subagent goes off track or is missing relevant context.
```

## Memory

Fable 5 performs particularly well when it can record lessons from previous runs and reference them. A place to write notes, as simple as a Markdown file, is enough:

```text
Store one lesson per file with a one-line summary at the top. Record corrections and confirmed approaches alike, including why they mattered. Don't save what the repo or chat history already records; update an existing note rather than creating a duplicate; delete notes that turn out to be wrong.
```

To bootstrap the memory system from existing history:

```text
Reflect on the previous sessions we've had together. Use subagents to identify core themes and lessons, and store them in [X]. Make sure you know to reference [X] for future use.
```

## Self-verification

Separate, fresh-context verifier subagents tend to outperform self-critique. For long-running tasks, instruct (filling in the interval):

```text
Establish a method for checking your own work at an interval of [X] as you build. Run this every [X interval], verifying your work with subagents against the specification.
```
