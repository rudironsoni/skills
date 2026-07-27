---
name: herdr-orchestration
description: >-
  Orchestrate interactive Herdr worker agents for explicit Herdr requests:
  delegate bounded tasks, message or inspect existing agents, wait on lifecycle
  states, verify reports, integrate results, and retire worker panes. Requires
  HERDR_ENV=1.
---

# Herdr Orchestration

Act as the **controller** for interactive worker agents running in Herdr panes. Own scope, worker state, conflict prevention, verification, integration, and the final answer. Use workers to gather evidence, make bounded changes, run checks, and report through Herdr's native agent lifecycle.

## Invariants

- Operate only from a Herdr-managed pane with `HERDR_ENV=1`.
- Scope every action to the caller workspace unless the user names another target.
- Resolve workspace, tab, pane, and agent IDs from Herdr output. Treat IDs as opaque.
- Keep the caller pane focused. Use `--current`, explicit IDs, and `--no-focus` for background work.
- Give each worker an independent objective and file claim. Isolate overlapping edits in separate worktrees.
- Send input only to a uniquely resolved worker in `idle` or `done` state.
- Treat worker claims as untrusted until the controller verifies them.
- Record a worker's report before closing a pane created for the delegation.

## 1. Preflight the Session

Verify the execution boundary and inspect the installed CLI before control commands:

```bash
test "${HERDR_ENV:-}" = 1
command -v herdr
herdr status
herdr --help
herdr integration status
herdr pane current --current
herdr agent list
```

Treat the installed binary as the syntax authority. Run `herdr agent`, `herdr pane`, or another command group without a subcommand when its current interface is uncertain. Use `herdr --help` for discovery because bare `herdr` launches or attaches the TUI. Inspect a potentially mutating nested command through help or source documentation instead of trial execution.

Require a current integration for each requested worker kind so lifecycle detection is authoritative. Ask before installing or updating an integration because that changes durable machine state.

**Complete when:** Herdr is reachable, caller workspace/tab/pane IDs are recorded, existing agents are inventoried, and every requested worker kind has a usable integration. If `HERDR_ENV=1` is absent, report that this agent is outside Herdr and stop.

## 2. Build Delegation Packets

Create one standalone packet per worker containing:

- exact repository or working-directory path;
- objective and expected deliverable;
- files, packages, or behavior in scope;
- explicit exclusions and a unique file claim;
- evidence required, including file references and genuine command output;
- verification commands or user-visible flows;
- stop conditions for unexpected structure, repeated failures, authentication, or out-of-scope edits;
- execution mode: direct by default, or plan-first only when the user requested it.

Prefer small independent slices. Maintain a worker registry with name, kind, pane ID, objective, claimed files, state, reported checks, controller verification, and final disposition.

For plan-first work, inspect the installed agent's current mode controls, confirm plan mode visibly before sending the packet, review the returned plan against scope, and accept it only when the user requested that execution mode. Derive TUI labels and key sequences from the installed agent because they are version-specific.

**Complete when:** every worker has a non-overlapping contract, required evidence, stop conditions, and a registry entry.

## 3. Provision Interactive Workers

Default to a sibling pane in the caller tab and current working directory. Inspect layout before choosing a direction:

```bash
herdr pane layout --pane "$HERDR_PANE_ID"
herdr pane split --current --direction right --cwd "$PWD" --no-focus
```

Use `down` when the caller pane is narrow or tall. Read the new pane ID from `.result.pane.pane_id`; never infer it from visual order. Start a supported agent in an existing shell pane at an interactive prompt:

```bash
herdr agent start <name> --kind <kind> --pane <pane-id>
```

Pass verified native agent arguments only after `--`. Use model names, permission flags, and startup modes confirmed by the installed agent. Treat `agent start` as complete only after Herdr recognizes the interactive agent and reports it ready.

When parallel edits overlap, create or open isolated worktrees using the repository's branch conventions, then split each worker pane with `--cwd <worktree-path>`. Preserve the mapping between worktree, worker name, and claimed files in the registry.

**Complete when:** each worker has a unique valid name, explicit pane ID, intended working directory, authoritative `idle` or `done` state, and the caller remains focused.

## 4. Dispatch Work

Resolve each target immediately before sending:

```bash
herdr agent get <name-or-pane-id>
```

Proceed only when the target is unique and its state is `idle` or `done`. Inspect `blocked`, `working`, or `unknown` before deciding the next action. Submit one packet atomically through the agent surface:

```bash
herdr agent prompt <name-or-pane-id> "<delegation-packet>" --wait --timeout 60000
```

For a fleet, resolve and preflight every target first. Dispatch packets without `--wait`, then wait for all targets concurrently when the harness supports parallel calls:

```bash
herdr agent prompt <target> "<delegation-packet>"
herdr agent wait <target> --timeout 60000
```

Use `agent prompt` for agent work. Keep raw-terminal control outside this agent orchestration flow and derive any required pane command from the installed CLI.

**Complete when:** every packet was delivered to its intended worker, each worker showed an observed lifecycle change, and every dispatch is represented in the registry.

## 5. Observe to a Terminal Outcome

Treat a timeout as a check-in interval rather than a worker deadline. After a timeout, inspect current state and recent output, then resume waiting while the objective remains viable:

```bash
herdr agent get <target>
herdr agent read <target> --source recent-unwrapped --lines 160
herdr agent explain <target> --json
herdr agent wait <target> --timeout 60000
```

Interpret states precisely:

| State | Controller action |
|---|---|
| `working` | Continue waiting without sending input. |
| `blocked` | Read the exact question or approval UI. Answer from known task context, or surface authentication, trust, permission, and scope decisions to the user. |
| `unknown` | Run `agent explain`; repair integration or detection before treating output as complete. |
| `idle` | Accept only after the dispatched work produced an observed state change. |
| `done` | Read the unseen completed report. |

Remember that CLI reads do not mark background work as seen. If the alternate-screen transcript is incomplete, ask the settled worker to write its complete report to a temporary Markdown file and return only the path, then read the file directly.

**Complete when:** every dispatched worker is `idle`, `done`, `blocked`, failed, or explicitly timed out with current evidence. Include every worker in the report.

## 6. Verify and Integrate

For each worker report:

1. Re-open every cited file and verify high-impact claims.
2. Review the complete diff and confirm it stays within the worker's claim.
3. Re-run checks that gate acceptance.
4. Resolve worktree commits or overlapping changes deliberately.
5. Record `accepted`, `rejected`, `superseded`, or `blocked` with evidence.

Pause integration when a worker edited outside its claim, changed a shared surface without coordination, or produced evidence the controller cannot reproduce.

**Complete when:** every worker disposition is evidence-backed, all accepted changes are integrated without unresolved overlap, and the controller can independently support the final claims.

## 7. Retire and Report

After recording the report and disposition, close panes created for completed workers unless the user asked to keep them:

```bash
herdr pane close <pane-id>
```

Keep existing panes and any pane with unresolved evidence. Require explicit user approval before closing a pane, tab, workspace, session, or server outside the delegation's created scope.

Report the controller result compactly:

```text
Herdr: PASS | PARTIAL | FAIL
Controller: <workspace>/<tab>/<pane>
Workers: <name>=<state/disposition>, ...
Verification: <checks rerun>
Retired: <created panes closed; retained panes with reason>
Blockers: <none or exact evidence>
```

**Complete when:** all workers have outcomes and dispositions, every created pane is closed or explicitly retained with a reason, caller focus is preserved, and the final answer contains only verified results and current blockers.
