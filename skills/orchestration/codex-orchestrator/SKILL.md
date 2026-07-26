---
name: codex-orchestrator
description: >-
  Orchestrate built-in Codex Multi-Agent V2 teams when the user explicitly
  asks for a team, coordinator, scouts, or workers; when work has at least two
  independent substantive workstreams; or when high-stakes work benefits from
  an independent verification track.
---

# Codex Orchestrator

Run the smallest team that creates useful parallelism. Keep the primary
coordinator accountable for the user conversation, approvals, integration, and
final verification.

## 1. Gate delegation

Divide the request into candidate workstreams. Work inline when the task is
narrow, sequential, depends on one shared context, or costs more to brief than
to complete. Form a team for an explicit multi-agent request, at least two
independent substantive workstreams, or a high-stakes independent verification
track.

Completion: state the inline-or-team decision and the concrete benefit expected
from coordination.

## 2. Map ownership

Read the active thread's stated concurrency limit and call `list_agents` to
account for live agents. Treat four total agents, including the coordinator, as
the default only when no other limit is stated.

Create an assignment map with one accountable owner per deliverable. Give
parallel agents non-overlapping investigation angles or write scopes. When a
smart worker may delegate, reserve its child slots before dispatch and keep
those slots assigned to its subtree.

Completion: every requested deliverable has one owner, scopes do not overlap,
and the proposed tree fits the available capacity.

## 3. Build assignments

Keep one model family by default and vary reasoning effort by role:

| Role | Spawn defaults | Ownership |
| --- | --- | --- |
| Scout | `model: "gpt-5.6-sol"`, `reasoning_effort: "low"`, `fork_turns: "none"` | Narrow read-only discovery such as locating files, tracing a path, or finding tests |
| Worker | `model: "gpt-5.6-sol"`, `reasoning_effort: "medium"`, `fork_turns: "none"` | Scoped implementation, checks, or supporting work |
| Smart worker | `model: "gpt-5.6-sol"`, `reasoning_effort: "high"`, `fork_turns: "none"` | Difficult implementation, ambiguity resolution, or a bounded subtree |

Honor an explicit user model or effort choice before these defaults. Prefer a
fresh, self-contained assignment. Use the smallest positive `fork_turns` value
when recent decisions are safer to inherit than restate. Use `fork_turns: "all"`
only when the inherited model and effort already fit the role; omit `model` and
`reasoning_effort` in that branch.

Include these fields in every assignment:

```text
Goal: <one bounded outcome>
Ownership: <paths, subsystem, or investigation angle>
Deliverable: <artifact or evidence returned to the parent>
Allowed changes: <read-only or exact mutation boundary>
Constraints: <task-specific safety and preservation requirements>
Success: <checkable completion criteria>
Dependencies: <canonical teammate target and expected message, or none>
Approval boundary: Report approval-requiring operations to the parent without requesting or executing them.
```

End scout and routine-worker prompts with:

```text
Complete this assignment directly. Do not spawn other agents; your parent's delegation instructions apply only to your parent.
```

Grant a smart worker delegation authority explicitly, with an exact child-slot
budget and ownership boundary. Require every child it creates to use the leaf
boundary above. Without that grant, the smart worker is also a leaf.

Completion: every spawn specifies a unique task name using lowercase letters,
digits, and underscores; plus its role, ownership, deliverable, success
criteria, context choice, mutation authority, approval boundary, and delegation
boundary.

## 4. Coordinate the team

Spawn independent assignments in parallel. Stay available to the user and do
useful coordinator work while agents run. After spawning, send dependent agents
the exact canonical teammate target and expected handoff. Require a critical
peer finding to appear again in the sender's final result so synthesis does not
depend on an inbox-only message.

Use `wait_agent` for required results instead of polling. Use `send_message` to
guide running agents, `followup_task` to give completed agents more work, and
`interrupt_agent` when an assignment becomes obsolete or crosses its boundary.
Rebuild the ownership map when the user changes the request or the topology
changes.

Completion: every required agent has returned a result or a concrete blocker,
and every dependency finding is visible to its accountable parent.

## 5. Integrate and verify

Review each result and any shared-worktree diff before relying on it. Reconcile
conflicts, run final checks at the primary coordinator, and distinguish child
claims from coordinator-verified evidence. For a nested subtree, require the
smart worker to return its child ownership map, results, and unresolved risks.

Completion: every user success criterion has current coordinator-verified
evidence or is reported explicitly as incomplete with its blocker.
