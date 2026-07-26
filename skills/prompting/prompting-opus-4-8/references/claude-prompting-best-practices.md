# Claude prompting best practices (all current models)

Baseline techniques that apply to all current Claude models (Claude Fable 5, Claude Mythos 5, Claude Opus 4.8 and earlier 4.x Opus models, Claude Sonnet 5, Claude Sonnet 4.6, Claude Haiku 4.5). The SKILL.md beside this file holds what its model does differently; read this file when composing a full prompt or harness. Paste snippets **verbatim**, the wording is Anthropic's tested prompt language.

## General principles

**Be clear and direct.** Treat Claude as a brilliant but new employee who lacks context on your norms. Golden rule: show your prompt to a colleague with minimal context; if they'd be confused, Claude will be too. Request "above and beyond" behavior explicitly instead of hoping the model infers it: "Create an analytics dashboard" underperforms "Create an analytics dashboard. Include as many relevant features and interactions as possible. Go beyond the basics to create a fully-featured implementation." Use numbered steps when order or completeness matters.

**Give the why.** Motivation generalizes better than a bare rule: "NEVER use ellipses" underperforms "Your response will be read aloud by a text-to-speech engine, so never use ellipses since the text-to-speech engine will not know how to pronounce them."

**Examples steer hardest.** 3 to 5 few-shot examples, mirroring the real use case, diverse enough that the model picks up no unintended pattern, each wrapped in `<example>` tags (the set in `<examples>`). Claude can critique your example set for relevance and diversity or generate more from it.

**Structure with XML tags.** Wrap each content type in its own tag (`<instructions>`, `<context>`, `<input>`), keep tag names consistent across prompts, and nest natural hierarchies.

**Set a role.** One system-prompt sentence focuses behavior and tone: `system: "You are a helpful coding assistant specializing in Python."`

**Long context (20k+ tokens).** Put longform data at the top and the query and instructions at the end (up to 30% better on complex multi-document tasks). Wrap each document in `<document index="n">` with `<source>` and `<document_content>` subtags. Ground the task in quotes: ask for relevant quotes in `<quotes>` tags first, then the task built on them.

**Model identity.** To have Claude identify itself or pick model strings correctly:

```text
The assistant is Claude, created by Anthropic. The current model is Claude Opus 4.8.
```

```text
When an LLM is needed, please default to Claude Opus 4.8 unless the user requests
otherwise. The exact model string for Claude Opus 4.8 is claude-opus-4-8.
```

## Output and formatting

Current models are more direct and grounded, more conversational, and less verbose than earlier generations, and may skip verbal summaries after tool calls. For visibility:

```text
After completing a task that involves tool use, provide a quick summary of the work you've done.
```

Formatting control, in order of leverage:

1. State the target, not the prohibition: "Your response should be composed of smoothly flowing prose paragraphs" beats "Do not use markdown in your response."
2. XML format indicators: "Write the prose sections of your response in \<smoothly_flowing_prose_paragraphs> tags."
3. Match your prompt style to the desired output style; a markdown-free prompt reduces markdown in the output.
4. For hard control over markdown and bullets:

````text
<avoid_excessive_markdown_and_bullet_points>
When writing reports, documents, technical explanations, analyses, or any long-form
content, write in clear, flowing prose using complete paragraphs and sentences. Use
standard paragraph breaks for organization and reserve markdown primarily for `inline
code`, code blocks (```...```), and simple headings (## and ###). Avoid using **bold**
and *italics*.

DO NOT use ordered lists (1. ...) or unordered lists (*) unless: a) you're presenting
truly discrete items where a list format is the best option, or b) the user explicitly
requests a list or ranking

Instead of listing items with bullets or numbers, incorporate them naturally into
sentences. This guidance applies especially to technical writing. Using prose instead of
excessive formatting will improve user satisfaction. NEVER output a series of overly
short bullet points.

Your goal is readable, flowing text that guides the reader naturally through ideas
rather than fragmenting information into isolated points.
</avoid_excessive_markdown_and_bullet_points>
````

Math defaults to LaTeX; for plain text:

```text
Format your response in plain text only. Do not use LaTeX, MathJax, or any markup
notation such as \( \), $, or \frac{}{}. Write all math expressions using standard text
characters (e.g., "/" for division, "*" for multiplication, and "^" for exponents).
```

Document creation (presentations, animations, visual documents) usually lands on the first try:

```text
Create a professional presentation on [topic]. Include thoughtful design elements,
visual hierarchy, and engaging animations where appropriate.
```

**Prefill is gone.** Starting with the Claude 4.6 generation, a prefilled assistant message on the last turn returns a 400 error. Replacements: structured outputs (or a tool with an enum field) for format constraints; "Respond directly without preamble. Do not start with phrases like 'Here is...', 'Based on...'" for preambles; plain clear prompting where prefill steered around refusals; continuations via a user message quoting the interrupted text ("Your previous response was interrupted and ended with `[previous_response]`. Continue from where you left off."); context hydration via user-turn reminders, tools, or compaction.

## Tool use

Models follow tool instructions precisely, so say what to do: "Can you suggest some changes to improve this function?" yields suggestions, "Change this function to improve its performance" yields edits. To set the default posture toward action:

```text
<default_to_action>
By default, implement changes rather than only suggesting them. If the user's intent is
unclear, infer the most useful likely action and proceed, using tools to discover any
missing details instead of guessing. Try to infer the user's intent about whether a tool
call (e.g., file edit or read) is intended or not, and act accordingly.
</default_to_action>
```

Or the conservative posture:

```text
<do_not_act_before_instructions>
Do not jump into implementation or change files unless clearly instructed to make
changes. When the user's intent is ambiguous, default to providing information, doing
research, and providing recommendations rather than taking action. Only proceed with
edits, modifications, or implementations when the user explicitly requests them.
</do_not_act_before_instructions>
```

Recent models respond more strongly to the system prompt than their predecessors; dial aggressive tool-forcing language ("CRITICAL: You MUST use this tool when...") back to normal register ("Use this tool when...") or they overtrigger.

**Parallel tool calls** are the default for independent operations (speculative searches, multi-file reads, parallel bash). To push toward 100%:

```text
<use_parallel_tool_calls>
If you intend to call multiple tools and there are no dependencies between the tool
calls, make all of the independent tool calls in parallel. Prioritize calling tools
simultaneously whenever the actions can be done in parallel rather than sequentially.
For example, when reading 3 files, run 3 tool calls in parallel to read all 3 files into
context at the same time. Maximize use of parallel tool calls where possible to increase
speed and efficiency. However, if some tool calls depend on previous calls to inform
dependent values like the parameters, do NOT call these tools in parallel and instead
call them sequentially. Never use placeholders or guess missing parameters in tool
calls.
</use_parallel_tool_calls>
```

To reduce parallelism: "Execute operations sequentially with brief pauses between each step to ensure stability."

## Thinking

Adaptive thinking (`thinking: {type: "adaptive"}`) lets the model decide when and how much to think, calibrated by the `effort` parameter and query complexity; in Anthropic's evals it reliably beats manual extended thinking. Manual `budget_tokens` is deprecated on the 4.6 generation and returns a 400 error on Claude Opus 4.7 and later and on Fable and Mythos 5. Migration: replace `thinking: {type: "enabled", budget_tokens: N}` with `thinking: {type: "adaptive"}` plus `output_config: {effort: "high"}`, using `max_tokens` as the hard ceiling. Each model's thinking default (off, opt-in, or always on) is stated in its SKILL.md.

Guide reflection between tool calls:

```text
After receiving tool results, carefully reflect on their quality and determine optimal
next steps before proceeding. Use your thinking to plan and iterate based on this new
information, and then take the best next action.
```

Steer triggering when it thinks more often than you'd like (common with large system prompts); measure the effect:

```text
Extended thinking adds latency and should only be used when it will meaningfully improve
answer quality - typically for problems that require multi-step reasoning. When in
doubt, respond directly.
```

When it overthinks (revisits settled decisions, inflates thinking tokens), constrain it or lower `effort`:

```text
When you're deciding how to approach a problem, choose an approach and commit to it.
Avoid revisiting decisions unless you encounter new information that directly
contradicts your reasoning. If you're weighing two approaches, pick one and see it
through. You can always course-correct later if the chosen approach fails.
```

- Prefer general instructions ("think thoroughly") over prescriptive step-by-step plans; the model's own reasoning frequently exceeds what a human would prescribe.
- Few-shot examples can include `<thinking>` tags to model the reasoning pattern; the style generalizes.
- With thinking off, manual chain-of-thought with `<thinking>` and `<answer>` tags still works.
- Ask for a self-check: "Before you finish, verify your answer against [test criteria]." This catches errors reliably in coding and math.

## Agentic systems

**Context awareness** (Claude Sonnet 5, Sonnet 4.6, Sonnet 4.5, Haiku 4.5): the model tracks its remaining token budget and may wrap up work as the limit approaches. If your harness compacts context or persists state to files, say so:

```text
Your context window will be automatically compacted as it approaches its limit, allowing
you to continue working indefinitely from where you left off. Therefore, do not stop
tasks early due to token budget concerns. As you approach your token budget limit, save
your current progress and state to memory before the context window refreshes. Always be
as persistent and autonomous as possible and complete tasks fully, even if the end of
your budget is approaching. Never artificially stop any task early regardless of the
context remaining.
```

The memory tool pairs well with context awareness for managing transitions.

**Multi-context-window tasks:**

1. Use a different prompt for the first window: set up the framework (write tests, create setup scripts), then iterate on a todo list in later windows.
2. Have the model write tests in a structured file (`tests.json`) before starting work, and add: "It is unacceptable to remove or edit tests because this could lead to missing or buggy functionality."
3. Encourage quality-of-life scripts (`init.sh`) that start servers, test suites, and linters, so fresh windows skip repeated setup.
4. Consider a fresh window over compaction when state lives on disk; current models discover state from the filesystem well. Be prescriptive on restart: "Call pwd; you can only read and write files in this directory." "Review progress.txt, tests.json, and the git logs." "Manually run through a fundamental integration test before moving on to implementing new features."
5. Provide verification tools (Playwright MCP, computer use) so correctness doesn't depend on continuous human feedback.
6. Encourage full use of the window:

```text
This is a very long task, so it may be beneficial to plan out your work clearly. It's
encouraged to spend your entire output context working on the task - just make sure you
don't run out of context with significant uncommitted work. Continue working
systematically until you have completed this task.
```

**State:** structured formats (JSON) for structured data like test status, freeform text for progress notes, git for checkpoints and history, and explicit emphasis on incremental progress.

**Autonomy and safety.** To require confirmation before risky actions:

```text
Consider the reversibility and potential impact of your actions. You are encouraged to
take local, reversible actions like editing files or running tests, but for actions that
are hard to reverse, affect shared systems, or could be destructive, ask the user before
proceeding.

Examples of actions that warrant confirmation:
- Destructive operations: deleting files or branches, dropping database tables, rm -rf
- Hard to reverse operations: git push --force, git reset --hard, amending published commits
- Operations visible to others: pushing code, commenting on PRs/issues, sending
messages, modifying shared infrastructure

When encountering obstacles, do not use destructive actions as a shortcut. For example,
don't bypass safety checks (e.g. --no-verify) or discard unfamiliar files that may be
in-progress work.
```

**Research.** Define success criteria, ask for verification across multiple sources, and for complex sweeps:

```text
Search for this information in a structured way. As you gather data, develop several
competing hypotheses. Track your confidence levels in your progress notes to improve
calibration. Regularly self-critique your approach and plan. Update a hypothesis tree or
research notes file to persist information and provide transparency. Break down this
complex research task systematically.
```

**Subagents.** Current models orchestrate subagents natively when subagent tools are well described in tool definitions; no elicitation needed. If the model delegates where direct work is simpler:

```text
Use subagents when tasks can run in parallel, require isolated context, or involve
independent workstreams that don't need to share state. For simple tasks, sequential
operations, single-file edits, or tasks where you need to maintain context across steps,
work directly rather than delegating.
```

**Chaining.** Adaptive thinking and subagents cover most multi-step reasoning internally; chain explicit API calls when you need to inspect intermediates or enforce a pipeline. The common pattern is self-correction: draft, review against criteria, refine, each as a separate call you can log or branch on.

**Temporary files.** Models use scratch scripts to iterate, which improves agentic coding outcomes. To keep the tree clean: "If you create any temporary new files, scripts, or helper files for iteration, clean up these files by removing them at the end of the task."

**Overengineering.** When the model adds files, abstractions, or flexibility nobody asked for:

```text
Avoid over-engineering. Only make changes that are directly requested or clearly
necessary. Keep solutions simple and focused:

- Scope: Don't add features, refactor code, or make "improvements" beyond what was
asked. A bug fix doesn't need surrounding code cleaned up. A simple feature doesn't need
extra configurability.

- Documentation: Don't add docstrings, comments, or type annotations to code you didn't
change. Only add comments where the logic isn't self-evident.

- Defensive coding: Don't add error handling, fallbacks, or validation for scenarios
that can't happen. Trust internal code and framework guarantees. Only validate at system
boundaries (user input, external APIs).

- Abstractions: Don't create helpers, utilities, or abstractions for one-time
operations. Don't design for hypothetical future requirements. The right amount of
complexity is the minimum needed for the current task.
```

**Test-focused shortcuts and hard-coding.** When it optimizes for passing tests over general solutions:

```text
Please write a high-quality, general-purpose solution using the standard tools
available. Do not create helper scripts or workarounds to accomplish the task more
efficiently. Implement a solution that works correctly for all valid inputs, not just
the test cases. Do not hard-code values or create solutions that only work for specific
test inputs. Instead, implement the actual logic that solves the problem generally.

Focus on understanding the problem requirements and implementing the correct algorithm.
Tests are there to verify correctness, not to define the solution. Provide a principled
implementation that follows best practices and software design principles.

If the task is unreasonable or infeasible, or if any of the tests are incorrect, please
inform me rather than working around them. The solution should be robust, maintainable,
and extendable.
```

**Hallucinations about code.** To ground answers in what was actually read:

```text
<investigate_before_answering>
Never speculate about code you have not opened. If the user references a specific file,
you MUST read the file before answering. Make sure to investigate and read relevant
files BEFORE answering questions about the codebase. Never make any claims about code
before investigating unless you are certain of the correct answer - give grounded and
hallucination-free answers.
</investigate_before_answering>
```

## Capability tips

**Vision.** A crop tool or skill that lets the model zoom into image regions gives consistent uplift on image-heavy tasks; Anthropic publishes a crop-tool cookbook. Videos can be analyzed as frames.

**Frontend aesthetics.** The full anti-slop directive (the frontend-defaults.md beside this file, where present, holds the model's specific design defaults and the short variant):

```text
<frontend_aesthetics>
You tend to converge toward generic, "on distribution" outputs. In frontend design, this
creates what users call the "AI slop" aesthetic. Avoid this: make creative, distinctive
frontends that surprise and delight.

Focus on:
- Typography: Choose fonts that are beautiful, unique, and interesting. Avoid generic
fonts like Arial and Inter; opt instead for distinctive choices that elevate the
frontend's aesthetics.
- Color & Theme: Commit to a cohesive aesthetic. Use CSS variables for consistency.
Dominant colors with sharp accents outperform timid, evenly-distributed palettes. Draw
from IDE themes and cultural aesthetics for inspiration.
- Motion: Use animations for effects and micro-interactions. Prioritize CSS-only
solutions for HTML. Use Motion library for React when available. Focus on high-impact
moments: one well-orchestrated page load with staggered reveals (animation-delay)
creates more delight than scattered micro-interactions.
- Backgrounds: Create atmosphere and depth rather than defaulting to solid colors. Layer
CSS gradients, use geometric patterns, or add contextual effects that match the overall
aesthetic.

Avoid generic AI-generated aesthetics:
- Overused font families (Inter, Roboto, Arial, system fonts)
- Clichéd color schemes (particularly purple gradients on white backgrounds)
- Predictable layouts and component patterns
- Cookie-cutter design that lacks context-specific character

Interpret creatively and make unexpected choices that feel genuinely designed for the
context. Vary between light and dark themes, different fonts, different aesthetics. You
still tend to converge on common choices (Space Grotesk, for example) across
generations. Avoid this: it is critical that you think outside the box!
</frontend_aesthetics>
```

## Migrating prompts from earlier generations

1. Describe the desired output explicitly, and add quality modifiers where you want more ("Go beyond the basics to create a fully-featured implementation").
2. Request animations and interactive elements explicitly.
3. Move thinking configuration to adaptive thinking plus `effort` (see Thinking above).
4. Remove last-turn prefills (see Output and formatting above).
5. Dial back anti-laziness and tool-forcing language; current models are more proactive and overtrigger on instructions written for older ones.
