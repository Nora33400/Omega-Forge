# 03 — OpenHands/OpenHands Decomposition

Repository: `OpenHands/OpenHands`

License from source pack: MIT for core; enterprise directory excluded from integration scope.

OpenHands is relevant to Omega-Forge as a software-engineering agent reference: it is not just a code generator, but a system that can operate in a workspace, reason over tasks, interact with tools, and work toward software changes.

## 1. Role for Omega-Forge

OpenHands is the strongest reference in the pack for the future “agent in a controlled workspace” layer.

Current Omega-Forge:

```text
Planner
↓
Executor
↓
ArtifactValidator
↓
RepairAgent
```

Future Omega-Forge inspired by OpenHands:

```text
ForgeWorkspace
↓
SandboxSession
↓
ToolPolicy
↓
AgentAction
↓
Observation
↓
Validation
↓
Repair / Report
```

OpenHands is useful for thinking about:

```text
workspace isolation
tool execution boundaries
action/observation loops
agent state
file editing
terminal commands
browser/UI integrations
human review
```

## 2. What to study

Study patterns, not implementation copying.

Likely upstream areas to inspect after cloning:

```text
openhands/core/
openhands/runtime/
openhands/controller/
openhands/events/
openhands/storage/
openhands/server/
frontend/
tests/
```

Important concepts:

```text
Agent action model
Observation model
Runtime abstraction
Sandboxed command execution
File read/write operations
Event stream
State persistence
Web/server separation
User approval boundaries
```

## 3. What could be copied

Default: copy no source now.

Possible future copy candidates only after exact commit and license audit:

```text
Small event naming ideas
Small schema inspiration
Tiny examples showing action/observation format
```

Better approach:

```text
Build Omega-Forge's own minimal action/observation model.
Use OpenHands as a reference for what the mature version could become.
```

## 4. What must not be copied

Avoid copying:

```text
Full runtime layer
Docker/sandbox internals
Controller internals
Frontend code
Server code
Enterprise directory
Prompt libraries wholesale
Tool execution code wholesale
Branding/assets/docs wholesale
```

Reason: OpenHands is a large system. Copying pieces directly would likely bloat Omega-Forge, introduce hidden dependencies, and blur security boundaries.

## 5. What should be adapted as original Omega-Forge code

Create minimal original modules:

```text
omega_forge/core/actions.py
omega_forge/core/observations.py
omega_forge/core/tool_policy.py
omega_forge/core/sandbox_session.py
```

Initial action types:

```text
ReadFileAction
WriteFileAction
ValidateArtifactAction
CreateRepairTaskAction
ReportAction
```

Initial observation types:

```text
FileReadObservation
FileWrittenObservation
ValidationObservation
RepairTaskObservation
PolicyDeniedObservation
```

Initial tool policy:

```text
- deny arbitrary shell execution
- allow only workspace-contained file operations
- allow generated artifact validation
- require explicit policy for external tools
```

This matches Omega-Forge's safety-first direction.

## 6. Adapter idea

Possible future adapter:

```text
omega_forge/adapters/openhands_adapter.py
```

Purpose:

```text
Send a bounded Omega-Forge repair task to an OpenHands environment.
Receive proposed changes as reviewable patches.
```

Adapter policy:

```text
- optional dependency
- disabled by default
- never runs arbitrary commands without policy
- never commits without review in early versions
- must preserve workspace root restrictions
```

## 7. License/compliance notes

MIT is permissive for core, but the source pack explicitly flags enterprise areas as excluded.

Before copying anything:

```text
1. Clone upstream.
2. Record exact commit SHA.
3. Copy LICENSE into third_party_notices/openhands_LICENSE.
4. Confirm no copied file comes from excluded enterprise paths.
5. Document copied files and modifications.
6. Prefer adapter/dependency over vendoring.
```

## 8. First concrete integration task

Do not integrate OpenHands directly yet.

First Omega-native task:

```text
Build Action/Observation data model
```

Acceptance criteria:

```text
- Define action dataclasses.
- Define observation dataclasses.
- Add ToolPolicy with allow/deny decisions.
- Add tests for allowed workspace file operations.
- Add tests for denied outside-root paths.
- Add tests for denied shell command by default.
- CI remains green.
```

## 9. Decision

Decision: **study sandbox and action/observation patterns; do not copy OpenHands source code yet**.

Integration type:

```text
Architecture inspiration now
Original Omega-Forge sandbox/action layer first
Optional OpenHands adapter later
No vendored code now
```

Priority: P0/P1.

It is P0 conceptually for the long-term forge, but P1 practically because Omega-Forge first needs its own small PatchPlan/PatchApplier loop.

## 10. Ω-Forge task proposal

Add tasks:

```text
Build Action and Observation models
Build ToolPolicy
Build minimal SandboxSession
```

This creates the bridge between the current safe deterministic executor and a future agentic workspace runtime.
