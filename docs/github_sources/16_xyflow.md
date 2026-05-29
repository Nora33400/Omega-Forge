# 16 — xyflow/xyflow Decomposition

Repository: `xyflow/xyflow`

License from source pack: MIT.

XYFlow (React Flow) is relevant because it specializes in node-based editors and workflow construction. Unlike Cytoscape, which is strongest for graph visualization and exploration, XYFlow excels at interactive graph editing.

## 1. Role for Omega-Forge

Cytoscape answered:

```text
How do we visualize graphs?
```

XYFlow answers:

```text
How do we edit graphs?
```

This directly maps to:

```text
ForgeGraph editor
Workflow editor
Agent workflow editor
Task dependency editor
```

## 2. What to study

Study:

```text
node editing
edge editing
drag-and-drop workflows
workflow composition
custom nodes
custom edges
interactive graph construction
```

Likely upstream areas to inspect:

```text
packages/
examples/
docs/
```

Focus on interaction patterns.

## 3. What could be copied

Default: copy nothing.

Potential future candidates:

```text
small node configuration examples
small editor examples
```

Prefer dependency usage.

## 4. What must not be copied

Avoid copying:

```text
editor internals
rendering internals
large examples wholesale
documentation wholesale
branding/assets
```

Reason: XYFlow should remain a UI dependency.

## 5. What should be adapted as original Omega-Forge code

Create workflow export/import models:

```text
omega_forge/core/workflow_export.py
```

Concept:

```text
WorkflowExport
├─ nodes
├─ edges
└─ metadata
```

Editable graph types:

```text
ForgeGraphEditor
AgentWorkflowEditor
TaskWorkflowEditor
```

## 6. Adapter idea

Frontend adapter:

```text
ui/adapters/xyflow_editor.ts
```

Purpose:

```text
Edit ForgeGraph and workflows visually.
```

## 7. License/compliance notes

MIT license.

Before copying:

```text
record commit SHA
preserve LICENSE
prefer dependency usage
```

## 8. First concrete integration task

Build workflow serialization first.

Acceptance criteria:

```text
ForgeGraph can export workflow definition
Workflow definition can be imported
Format is UI-independent
Tests cover import/export
CI remains green
```

## 9. Decision

Decision:

```text
Use XYFlow as a future workflow editor.
Do not copy source code.
Build Omega-native workflow format first.
```

Priority: P1.

XYFlow complements Cytoscape:

```text
Cytoscape = explore
XYFlow = edit
```

## 10. Omega-Forge task proposal

Add tasks:

```text
Build WorkflowExport model
Export ForgeGraph workflows
Prepare XYFlow editor adapter
```

XYFlow becomes valuable when users need to design or modify forge workflows visually.
