# 15 — cytoscape/cytoscape.js Decomposition

Repository: `cytoscape/cytoscape.js`

License from source pack: MIT.

Cytoscape.js is relevant to Omega-Forge because it specializes in graph visualization. This directly maps to `ForgeGraph`, `KnowledgeGraph`, dependency graphs, task graphs, and repair graphs.

## 1. Role for Omega-Forge

Omega-Forge now has several graph-shaped concepts:

```text
ForgeGraph
KnowledgeGraph
Task dependencies
Agent message flow
Failure/repair relationships
```

Cytoscape answers:

```text
How do we visualize those graphs clearly?
```

## 2. What to study

Study:

```text
graph rendering
node/edge styles
layouts
interactive graph navigation
filtering
selection
large graph handling
```

Likely upstream areas to inspect after cloning:

```text
src/
documentation/
debug/
test/
```

Focus on graph UI behavior, not implementation internals.

## 3. What could be copied

Default: copy nothing.

Potential future candidates after audit:

```text
small styling examples
small graph layout examples
```

Prefer dependency usage.

## 4. What must not be copied

Avoid copying:

```text
rendering engine internals
layout internals
large examples wholesale
documentation wholesale
branding/assets
```

Reason: Cytoscape should remain a frontend dependency, not vendored core code.

## 5. What should be adapted as original Omega-Forge code

Create graph export models:

```text
omega_forge/core/graph_export.py
```

Export format:

```text
GraphExport
├─ nodes
├─ edges
└─ metadata
```

UI graph types:

```text
ForgeGraphView
KnowledgeGraphView
TaskGraphView
FailureGraphView
```

Omega-Forge should output clean graph data. Cytoscape renders it.

## 6. Adapter idea

Frontend adapter:

```text
ui/adapters/cytoscape_graph_view.ts
```

Purpose:

```text
Render Omega-Forge graph exports with Cytoscape.js.
```

## 7. License/compliance notes

MIT license.

Before copying code:

```text
record commit SHA
preserve LICENSE
document copied files
prefer dependency usage
```

## 8. First concrete integration task

Build backend graph export first.

Acceptance criteria:

```text
ForgeGraph can export nodes and edges
KnowledgeGraph can export nodes and edges
Export is frontend-agnostic
Tests cover export structure
CI remains green
```

## 9. Decision

Decision:

```text
Use Cytoscape as a future graph renderer.
Do not copy source code.
Build Omega-native graph export first.
```

Priority: P1.

Cytoscape is not core engine logic, but it is highly relevant to making Omega-Forge understandable.

## 10. Omega-Forge task proposal

Add tasks:

```text
Build GraphExport model
Export ForgeGraph
Export KnowledgeGraph
Prepare Cytoscape UI adapter
```

Cytoscape becomes valuable only after Omega-Forge has real graph data to display.
