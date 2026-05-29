# 07 — microsoft/autogen Decomposition

Repository: `microsoft/autogen`

License from source pack: MIT code, CC-BY-4.0 documentation.

AutoGen is relevant because Omega-Forge already contains the beginnings of multiple specialized roles:

```text
Planner
Executor
ArtifactValidator
RepairAgent
```

AutoGen's strongest contribution is not code generation. It is agent coordination.

## 1. Role for Omega-Forge

Current Omega-Forge:

```text
TaskQueue
↓
Executor
↓
Validator
↓
Repair
```

Future Omega-Forge:

```text
PlannerAgent
↓
ExecutorAgent
↓
ValidatorAgent
↓
RepairAgent
↓
ReporterAgent
```

AutoGen answers:

```text
How do multiple agents cooperate?
How do they exchange messages?
How do they delegate tasks?
How do they stop infinite loops?
```

## 2. What to study

Important concepts:

```text
Agent roles
Message passing
Group chats
Delegation
Termination conditions
Tool invocation
Shared context
Task decomposition
Human approval points
```

Likely upstream areas to inspect after cloning:

```text
autogen_agentchat/
autogen_core/
autogen_ext/
examples/
tests/
```

The focus should be on coordination patterns.

## 3. What could be copied

Default: copy nothing.

Potential future copy candidates after audit:

```text
Small message schema ideas
Tiny role definitions
Small orchestration examples
```

Better approach:

```text
Design Omega-Forge message protocol.
```

## 4. What must not be copied

Avoid copying:

```text
Full orchestration runtime
Provider integrations
Prompt libraries
Agent framework internals
Examples wholesale
Docs wholesale
```

Reason: Omega-Forge should remain understandable and deterministic.

## 5. What should be adapted as original Omega-Forge code

Create:

```text
omega_forge/core/agent_message.py
omega_forge/core/agent_bus.py
omega_forge/core/agent_registry.py
```

Message model:

```text
AgentMessage
├─ sender
├─ recipient
├─ type
├─ payload
├─ timestamp
└─ correlation_id
```

Bus responsibilities:

```text
route
log
trace
terminate loops
```

## 6. Adapter idea

Future:

```text
omega_forge/adapters/autogen_adapter.py
```

Purpose:

```text
Run Omega-Forge roles through AutoGen when desired.
```

Optional only.

## 7. License/compliance notes

MIT code is permissive.

Documentation is CC-BY-4.0.

Meaning:

```text
Code copying rules
!=
Documentation copying rules
```

Documentation excerpts require attribution.

## 8. First concrete integration task

Build:

```text
AgentMessage
AgentBus
```

Acceptance criteria:

```text
Planner can send message to Executor.
Executor can return result.
Messages are logged.
Correlation IDs tracked.
Tests pass.
CI remains green.
```

## 9. Decision

Decision:

```text
Study coordination model.
Do not copy framework.
Build Omega-native messaging.
```

Priority: P0.

## 10. Ω-Forge task proposal

Add:

```text
Build AgentMessage
Build AgentBus
Build AgentRegistry
```

This is likely the shortest path toward coordinated multi-agent behavior without introducing a large external dependency.
