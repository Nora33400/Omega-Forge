# 01 — langchain-ai/langgraph Decomposition

Repository: `langchain-ai/langgraph`

License from source pack: MIT.

Upstream positioning checked from public repository: LangGraph is described as a low-level orchestration framework for building long-running, stateful agents. Its README emphasizes durable execution, human-in-the-loop control, memory, debugging/observability, and production deployment.

## 1. Role for Omega-Forge

LangGraph is the strongest architectural reference for turning Omega-Forge from a linear pipeline into a resumable execution graph.

Current Omega-Forge loop:

```text
SPEC
↓
Planner
↓
TaskQueue
↓
Executor
↓
ArtifactValidator
↓
RepairAgent
↓
Report
```

Target Omega-Forge loop inspired by LangGraph:

```text
ForgeGraph
├─ plan_node
├─ execute_node
├─ validate_node
├─ repair_node
├─ report_node
└─ checkpoint_state
```

## 2. What to study

Study concepts, not copy implementation first.

Important patterns:

```text
StateGraph-like abstraction
Node functions
Edges / conditional routing
Checkpointing
Durable state
Human-in-the-loop pauses
Resume after failure
Short-term state vs long-term memory
Graph visualization/debug traces
```

Likely upstream areas to inspect after cloning:

```text
libs/langgraph/langgraph/graph/
libs/langgraph/langgraph/checkpoint/
libs/langgraph/langgraph/pregel/
libs/langgraph/langgraph/types.py
examples/
docs/
```

## 3. What could be copied

Default: copy nothing at first.

Potentially copy only after exact commit/license audit:

```text
Small interface ideas
Small naming conventions if useful
Tiny example snippets adapted into docs with attribution
```

Do not copy core engine files into Omega-Forge unless there is a very strong reason. The value is in the architecture pattern, not raw code copying.

## 4. What must not be copied

Avoid copying:

```text
Core graph runtime implementation
Checkpoint backend internals
Pregel runtime internals
Docs wholesale
Examples wholesale
Branding, logos, badges
LangSmith-specific deployment or observability code
```

Reason: Omega-Forge needs a small original engine aligned with its own TaskQueue, ProjectState, ArtifactValidator, and RepairAgent. Copying a mature framework would bloat the repo and create maintenance/licensing complexity.

## 5. What should be adapted as original Omega-Forge code

Create an original Omega-Forge module:

```text
omega_forge/core/forge_graph.py
```

Minimal concepts:

```python
ForgeGraph
ForgeNode
ForgeEdge
ForgeGraphState
ForgeCheckpoint
```

Omega-specific graph state:

```text
spec_path
queue_path
state_path
current_task_id
last_agent_result
last_validation
repair_needed
reports
```

Omega-specific nodes:

```text
plan
execute
validate
repair
report
stop
```

## 6. Adapter idea

Possible future adapter:

```text
omega_forge/adapters/langgraph_adapter.py
```

Purpose:

```text
Export Omega-Forge flow to LangGraph-compatible concepts
or run a LangGraph-backed orchestration mode if dependency installed.
```

But this should remain optional:

```text
pip install omega-forge[langgraph]
```

No hard dependency in the foundation.

## 7. License/compliance notes

MIT is permissive, but still requires preserving copyright and license notices when copying substantial code.

Before any copying:

```text
1. Clone upstream.
2. Record exact commit SHA.
3. Copy LICENSE into third_party_notices/langgraph_LICENSE.
4. Document copied files and modifications.
5. Prefer adapter/dependency use over vendoring.
```

## 8. First concrete integration task

Implement an original tiny graph engine:

```text
omega_forge/core/forge_graph.py
```

First behavior:

```text
state enters plan
plan creates tasks
execute generates artifact
validate checks artifact
if validation ok -> report
if validation fails -> repair
repair creates repair task
report writes markdown
```

No external dependency.

## 9. Decision

Decision: **study and adapt, do not copy source code yet**.

Integration type:

```text
Architecture inspiration now
Optional adapter later
No vendored code now
```

Priority: P0.

## 10. Ω-Forge task proposal

Add a task:

```text
Build ForgeGraph minimal execution engine
```

Acceptance criteria:

```text
- ForgeGraph can register nodes.
- ForgeGraph can register fixed and conditional edges.
- ForgeGraph can run from an initial node.
- ForgeGraph stores state transitions.
- Tests cover linear routing and conditional routing.
- CI remains green.
```
