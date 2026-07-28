---
name: herdr-orchestration
description: >-
  Orchestrate interactive Herdr worker agents for explicit Herdr requests:
  delegate bounded tasks, exchange run-scoped updates, questions, answers, and
  results bidirectionally, inspect lifecycle state, verify reports, integrate
  results, and retire worker panes. Requires HERDR_ENV=1.
---

# Herdr Orchestration

Act as the **controller** for interactive worker agents running in Herdr panes. Own scope, worker state, conflict prevention, verification, integration, and the final answer. Use workers to gather evidence, make bounded changes, run checks, and report through Herdr's native agent lifecycle.

## Invariants

- Operate only from a Herdr-managed pane with `HERDR_ENV=1`.
- Scope every action to the caller workspace unless the user names another target.
- Resolve workspace, tab, pane, and agent IDs from Herdr output. Treat IDs as opaque.
- Keep the caller pane focused. Use `--current`, explicit IDs, and `--no-focus` for background work.
- Place every session, workspace, tab, and worktree per the Layout Contract.
- Start workers as `codex` by default; start `opencode` or `pi` only when the user names them. When an organization policy skill is loaded, its worker-kind and branch-naming rules override these defaults.
- Before provisioning, check whether the target path or named system belongs to an organization with a policy overlay skill (for example, any path under `~/src/Feverup` → `fever-herdr-orchestration`). Load that overlay first; its rules override these defaults.
- The controller writes no work product. Once a task is delegated, never run Edit/Write/sed/perl, gating checks, rebases, or commits inside a worker's worktree while that worker exists. Every change flows through `herdr agent prompt`. The urge to "just fix it quickly" is the signal to send a follow-up packet instead. Sole exception: integration actions in §6 after the owning worker is retired or explicitly paused, stated as such in the report.
- Every worker runs in a worktree checked out on its target branch. Never `agent start` in a pane whose cwd is the repo's primary checkout or whose `git rev-parse --abbrev-ref HEAD` is the default branch (`master`/`main`) — including read-only reviews. A review gets a worktree on the PR branch, fetched first.
- Tab labels are derived, never retyped. Compute `label="<repo>-<branch-folder>"` once, keep it in a shell variable, and pass that same variable to every command taking `--label`. Retyping, shortening, or dropping the `<repo>-` prefix is a contract violation.
- Give each worker an independent objective and file claim. Isolate overlapping edits in separate worktrees.
- Send initial work only to a uniquely resolved worker in `idle` or `done` state. Use the Message Contract for run-scoped traffic; Herdr 0.7.5 can submit that traffic while the target is `working`.
- Treat worker claims as untrusted until the controller verifies them.
- Record a worker's report before closing a pane created for the delegation.

## Layout Contract

| Herdr object | Name | Working directory |
|---|---|---|
| Session | `<organization>` | `~/src/<organization>` |
| Workspace | `<repo>` | `~/src/<organization>/<repo>` |
| First tab of a workspace | `<repo>` | `~/src/<organization>/<repo>` |
| Worktree tab | `<repo>-<branch-folder>` | `~/src/<organization>/<repo>.worktrees/<repo>-<branch-folder>` |

- Launch or attach a session with `herdr --session "<organization>"` from a shell outside Herdr. Inside Herdr, verify the current session serves the target organization.
- Worktree tabs live inside their repo's workspace. Derive `<branch-folder>` by lowercasing the branch name and replacing `/` with `-`.
- Name branches with Conventional Branches: `<type>/<description>`, lowercase kebab-case after the slash. Allowed types: `build`, `chore`, `ci`, `docs`, `feat`, `fix`, `perf`, `refactor`, `revert`, `style`, `test`. Use additional types `feature`, `bugfix`, `hotfix`, `release`, `ai`, `copilot`, `cursor`, `claude`, `codex` only when they match an established repository workflow.
- Validate every generated branch name with `git check-ref-format --branch <name>`.

## 1. Preflight the Session

Verify the execution boundary and inspect the installed CLI before control commands:

```bash
test "${HERDR_ENV:-}" = 1
command -v herdr
herdr status
herdr --help
herdr integration status
herdr pane current --current
herdr agent get "$HERDR_PANE_ID"
herdr agent list
```

Treat the installed binary as the syntax authority. Run `herdr agent`, `herdr pane`, or another command group without a subcommand when its current interface is uncertain. Use `herdr --help` for discovery because bare `herdr` launches or attaches the TUI. Inspect a potentially mutating nested command through help or source documentation instead of trial execution.

Resolve the current session and confirm it serves the target organization (`herdr session list`, `herdr status`). Resolve or create the target repo's workspace and repo tab per the Layout Contract:

```bash
herdr workspace list
herdr workspace create --cwd ~/src/<organization>/<repo> --label <repo> --no-focus
herdr tab list
```

Pin `controller_target="$HERDR_PANE_ID"`; never derive it from UI focus. Create one run ID for this orchestration as `run_id="${HERDR_PANE_ID}-$(date -u +%Y%m%dT%H%M%SZ)"`. Keep both values unchanged for the run and pass them to every worker. Require a current integration for each requested worker kind so lifecycle detection is authoritative. Ask before installing or updating an integration because that changes durable machine state.

**Complete when:** Herdr is reachable, the session matches the target organization, the target repo has a workspace and repo tab matching the Layout Contract, caller workspace/tab/pane IDs and the run ID are recorded, existing agents are inventoried, and every requested worker kind has a usable integration. If `HERDR_ENV=1` is absent, report that this agent is outside Herdr and stop.

## 2. Build Delegation Packets

Create one standalone packet per worker containing:

- exact repository or working-directory path;
- worker kind chosen by the routing invariant;
- objective and expected deliverable;
- files, packages, or behavior in scope;
- explicit exclusions and a unique file claim;
- evidence required, including file references and genuine command output;
- verification commands or user-visible flows;
- stop conditions for unexpected structure, repeated failures, authentication, or out-of-scope edits;
- execution mode: direct by default, or plan-first only when the user requested it;
- the exact run ID, controller target, worker target, task label, and Message Contract.

Prefer small independent slices. Use a lowercase hyphen-case task label without spaces for each packet. Maintain a worker registry with run ID, task label, name, kind, pane ID, reply target, objective, claimed files, state, last callback, pending question, reported checks, controller verification, and final disposition.

For plan-first work, inspect the installed agent's current mode controls, confirm plan mode visibly before sending the packet, review the returned plan against scope, and accept it only when the user requested that execution mode. Derive TUI labels and key sequences from the installed agent because they are version-specific.

**Complete when:** every worker has a non-overlapping contract, a routed kind, required evidence, stop conditions, and a registry entry.

## Message Contract

Use `herdr agent prompt` for bidirectional controller-worker traffic. Send one header line followed by a concise body or a path to a larger report:

```text
[herdr-orchestration run=<run-id> task=<task-label> from=<sender> kind=<kind> reply-to=<target>]
<message>
```

`reply-to` is the exact unique agent name or pane ID that the receiver should target. Workers send `update`, `question`, `blocked`, or `result`; the controller sends `answer`, `follow-up`, or `stop`.

Give every worker this callback pattern with all placeholders already filled:

```bash
herdr agent prompt <controller-target> \
  "[herdr-orchestration run=<run-id> task=<task-label> from=<worker-name> kind=<kind> reply-to=<worker-target>]
<message>"
```

- Send protocol messages without `--wait`. Herdr may accept a prompt while the target is `working`, but a wait observes lifecycle state, not that specific message or turn.
- Treat exit status 0 as submission confirmation only. Do not resend after success and do not treat it as acknowledgement or task completion.
- On a nonzero send, preserve the exact error in the sender's visible final response and settle so the receiver can recover through lifecycle inspection. Do not hide or loop on transport failure.
- Send `update` only at meaningful checkpoints and continue working without expecting a reply.
- Send `question` when the controller can answer from task context; send `blocked` when user authority, authentication, permission, or scope is required. After either message, end the turn and wait for `answer`, `follow-up`, or `stop`.
- Send `result` with changed files, checks, residual risk, and report paths, then end the turn. A result is a claim until the controller verifies it.
- Validate inbound run ID, task label, sender, and reply target against the registry. Ignore and report stale, unknown, or mismatched messages instead of acting on them.
- Keep large logs, diffs, and reports out of prompts. Write them to an accessible Markdown file and send the exact path.

Use normal `idle` or `done` delivery for initial tasks and routine follow-ups when possible. Use working-target delivery only for protocol callbacks and explicit urgent `stop` or scope-correction messages.

## 3. Provision Interactive Workers

For same-repo, non-overlapping work, split a sibling pane in the repo tab. Inspect layout before choosing a direction:

```bash
herdr pane layout --pane "$HERDR_PANE_ID"
herdr pane split --current --direction right --cwd "$PWD" --no-focus
```

Use `down` when the caller pane is narrow or tall. Read the new pane ID from `.result.pane.pane_id`; never infer it from visual order.

For overlapping or isolated work, provision idempotently:

1. **Reuse before create.** Run `herdr worktree list`, `herdr tab list`, and `herdr agent list`. When a worktree, tab, or agent already matches the target branch, reuse it (`herdr worktree open` for an existing checkout). On `worktree_create_failed … already exists`, switch to reuse — never retry with name variations.
2. **Fetch gate.** `git fetch` the base or target ref and require success before creating the worktree. On auth failure (for example `Permission denied (publickey)`), stop and report — never provision a worker against a stale checkout.
3. **Create with a single stored label.** Derive the branch per the Layout Contract, compute `label="<repo>-<branch-folder>"` once, then:

```bash
label="<repo>-<branch-folder>"
herdr worktree create --workspace <repo-workspace-id> --branch <branch> \
  --path ~/src/<organization>/<repo>.worktrees/"$label" \
  --label "$label" --no-focus --json
```

4. **Materialize the tab.** In current Herdr (0.7.x), `worktree create --workspace <ws>` spawns a **new workspace**, not a tab inside `<ws>`. Move the resulting pane into the repo workspace as a tab, passing the same `$label` variable, then close the empty side-effect workspace:

```bash
herdr pane move <new-pane-id> --new-tab --workspace <repo-workspace-id> --label "$label" --no-focus
herdr pane list --workspace <side-effect-workspace-id>   # must be empty
herdr workspace close <side-effect-workspace-id>
```

5. **Read-back gate (mandatory).** Conformance is proven by read-back, never by the create commands' exit codes:

```bash
herdr tab list --workspace <repo-workspace-id>            # tab label == "$label" exactly
git -C <worktree-path> rev-parse --abbrev-ref HEAD        # == target branch
git -C <worktree-path> rev-parse --show-toplevel          # == worktree path
```

Fix any mismatch (`herdr pane rename`, or recreate) before `agent start`.

Read tab and pane IDs from the JSON result. Preserve the mapping between worktree, worker name, and claimed files in the registry.

Start a supported agent in an existing shell pane at an interactive prompt, with the kind routed by the invariants:

```bash
herdr agent start <name> --kind <kind> --pane <pane-id>
```

Pass verified native agent arguments only after `--`. Use model names, permission flags, and startup modes confirmed by the installed agent. Treat `agent start` as complete only after Herdr recognizes the interactive agent and reports it ready.

**Complete when:** `herdr tab list` output shows every planned tab labeled exactly `<repo>-<branch-folder>`, each worktree's `git rev-parse --abbrev-ref HEAD` matches its target branch, no empty side-effect workspaces remain, each worker has a unique valid name, explicit pane ID, authoritative `idle` or `done` state, and the caller remains focused.

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

Confirm acceptance after every dispatch: `herdr agent get <target>` must show `working`, or `agent prompt --wait` must return a settled state after observing activity. If Herdr returns `agent_prompt_stalled`, read the pane once (`herdr agent read <target> --source recent-unwrapped --lines 60`) and diagnose. Do not inject a second Enter after `agent prompt`; it already submits text and Enter atomically.

Set worker configuration (model, effort, permissions) through the delegation packet or verified `agent start` arguments — never by spraying `/model` or `/effort` as raw pane text across a fleet.

**Complete when:** every packet was delivered to its intended worker, `herdr agent get` confirmed each target transitioned out of `idle`, and every dispatch is represented in the registry.

## 5. Observe to a Terminal Outcome

Treat validated callbacks as the primary report channel. On `update`, record the checkpoint. On `question`, answer from established task context or surface the decision to the user, then send `answer` to `reply-to`. On `blocked`, surface the exact external decision and keep the worker. On `result`, record the report and begin verification. Send every response with the same run ID and task label and set `reply-to` to the pinned controller target.

Use lifecycle state as liveness evidence and as the recovery path when a callback is missing. A settled worker without a valid `result` callback is not complete: read its recent output and request the missing result through the Message Contract.

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

An expired `agent wait --timeout` is a check-in, never a failure verdict: re-run `herdr agent get`; when the state is `working`, loop the wait. Declare a worker failed only on a `blocked` state that cannot be answered, an `unknown` state that `agent explain` cannot repair, or no state or output change across 3 consecutive check-ins.

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

After recording the report and disposition, retire each completed worker through this ladder, in order, unless the user asked to keep it:

1. Exit the agent in-pane first: `herdr agent stop <name>` when available, otherwise `herdr pane send-text <pane-id> "/exit"` followed by `herdr pane send-keys <pane-id> Enter`. Confirm the shell prompt returned via `herdr pane read`.
2. Then close the pane: `herdr pane close <pane-id>`.
3. If `pane close` returns `confirmation_required` (the pane belongs to a worktree group), **stop the ladder**. Never escalate to `herdr workspace close` — that destroys the whole worktree group and kills every sibling worker in it. Stay with the in-pane exit from step 1, or ask the user.
4. For worktree tabs the delegation created, remove the checkout only after its changes are integrated or explicitly abandoned: `herdr worktree remove --workspace <id>`.
5. Close side-effect workspaces left over from provisioning only after `herdr pane list --workspace <id>` shows them empty.

Keep existing panes and any pane with unresolved evidence. Require explicit user approval before closing a pane, tab, workspace, session, or server outside the delegation's created scope.

Report the controller result compactly:

```text
Herdr: PASS | PARTIAL | FAIL
Controller: <session>/<workspace>/<tab>/<pane>
Workers: <name>=<state/disposition>, ...
Callbacks: <run-id and handled or missing worker messages>
Verification: <checks rerun>
Retired: <created panes and worktrees closed; retained items with reason>
Blockers: <none or exact evidence>
```

**Complete when:** all workers have outcomes and dispositions, every created pane or worktree tab is closed or explicitly retained with a reason, caller focus is preserved, and the final answer contains only verified results and current blockers.
