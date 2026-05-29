# 08 — crewAIInc/crewAI Decomposition

Repository: `crewAIInc/crewAI`

License from source pack: MIT.

CrewAI is relevant to Omega-Forge as a reference for defining clear agent roles and simple team workflows. Compared with AutoGen, which is most useful for message coordination, CrewAI is most useful for role modeling.

## 1. Role for Omega-Forge

Omega-Forge already has several role-like components:

```text
PlannerAgent
ExecutorAgent
RepairAgent
Future ValidatorAgent
Future ReporterAgent
```

CrewAI suggests making these roles explicit instead of leaving responsibilities hidden inside code.

Target idea:

```text
AgentRole
↓
Agent implementation
↓
WorkflowDefinition
```

## 2. What to study

Study:

```text
role definitions
goal definitions
task ownership
sequential workflows
hierarchical workflows
tool assignment
crew-level coordination
```

Likely upstream areas to inspect after cloning:

```text
src/crewai/
examples/
tests/
docs/
```

## 3. What could be copied

Default: copy nothing.

Potential future copy candidates after exact commit and license audit:

```text
small role schema ideas
small workflow examples
small terminology patterns
```

Better approach:

```text
create an Omega-native role schema
```

## 4. What must not be copied

Avoid copying:

```text
runtime framework
provider integrations
prompt collections
examples wholesale
documentation wholesale
branding/assets
```

Reason: Omega-Forge should not become a stack of external agent frameworks. It needs a compact role system matching its own forge pipeline.

## 5. What should be adapted as original Omega-Forge code

Create original modules:

```text
omega_forge/core/agent_role.py
omega_forge/core/workflow_definition.py
```

Minimal role model:

```text
AgentRole
- name
- responsibilities
- allowed_tools
- inputs
- outputs
- escalation_rules
```

Example roles:

```text
planner: creates and prioritizes tasks
executor: produces artifacts
validator: validates artifacts and tests
repair: creates repair tasks or patch plans
reporter: summarizes results
```

## 6. Adapter idea

Future optional adapter:

```text
omega_forge/adapters/crewai_adapter.py
```

Purpose:

```text
run an Omega-Forge workflow through CrewAI if explicitly enabled
```

Policy:

```text
optional only
not a hard dependency
no vendored code now
```

## 7. License/compliance notes

MIT is permissive, but copied code still requires preserving license notices.

Before copying anything:

```text
1. clone upstream
2. record exact commit SHA
3. preserve LICENSE
4. document copied files
5. prefer adapter or original implementation
```

## 8. First concrete integration task

Build an original role schema.

Acceptance criteria:

```text
AgentRole exists
roles can declare responsibilities
roles can declare allowed tools
workflow can map roles to agents
tests cover role creation and mapping
CI remains green
```

## 9. Decision

Decision: study role and workflow modeling, but do not copy CrewAI source code yet.

Integration type:

```text
architecture inspiration now
Omega-native AgentRole first
optional adapter later
```

Priority: P1.

## 10. Omega-Forge task proposal

Add tasks:

```text
Build AgentRole model
Build WorkflowDefinition model
Map AgentRole to existing agents
```

CrewAI complements AutoGen: AutoGen inspires communication, CrewAI inspires responsibility structure.
