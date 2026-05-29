# Ω-Forge Architecture V1

## Purpose

Ω-Forge is a graph-driven autonomous software forge.

Its long-term objective is:

```text
Discover
Analyze
Plan
Generate
Validate
Repair
Learn
Repeat
```

while remaining auditable and modular.

---

# Core Architecture

```text
User Request
    │
    ▼
ForgeGraph
    │
    ├── PlannerAgent
    ├── ExecutorAgent
    ├── ValidatorAgent
    ├── RepairAgent
    └── ReporterAgent
    │
    ▼
AgentBus
    │
    ▼
Workspace
    │
    ├── ProjectIndex
    ├── ContextPipeline
    ├── PatchPlan
    ├── SandboxManager
    └── FailureMemory
```

---

# Major Components

## ForgeGraph

Inspired by:

```text
LangGraph
NetworkX
```

Responsibilities:

```text
Task decomposition
Execution flow
Dependency tracking
Agent orchestration
```

---

## AgentBus

Inspired by:

```text
AutoGen
```

Responsibilities:

```text
Message routing
Traceability
Correlation tracking
Loop prevention
```

---

## ProjectIndex

Inspired by:

```text
LlamaIndex
```

Responsibilities:

```text
Repository understanding
Documentation indexing
Context retrieval
```

---

## ContextPipeline

Inspired by:

```text
Haystack
```

Responsibilities:

```text
Retrieve
Filter
Rank
Package context
```

---

## KnowledgeGraph

Inspired by:

```text
GraphRAG
NetworkX
```

Node examples:

```text
Project
Task
Artifact
Error
Patch
Agent
```

Edge examples:

```text
generated
failed_with
repaired_by
depends_on
```

---

## FailureMemory

Inspired by:

```text
mem0
```

Responsibilities:

```text
Store failures
Store repairs
Store outcomes
Enable learning
```

---

## PatchPlan

Inspired by:

```text
Aider
```

Responsibilities:

```text
Repair planning
Target selection
Patch generation
```

---

## SandboxManager

Inspired by:

```text
OpenHands
Moby
```

Responsibilities:

```text
Create sandbox
Execute code
Run tests
Capture logs
Destroy sandbox
```

---

# Storage Layer

## VectorMemoryStore

Potential implementations:

```text
JSON
InMemory
LanceDB
Qdrant
Chroma
```

Storage backend must remain replaceable.

---

# User Interfaces

## Visualization

Inspired by:

```text
Cytoscape
```

Views:

```text
ForgeGraphView
KnowledgeGraphView
FailureGraphView
```

## Editing

Inspired by:

```text
XYFlow
```

Views:

```text
WorkflowEditor
AgentWorkflowEditor
TaskEditor
```

## Application Shell

Inspired by:

```text
React
Tauri
```

---

# Future Research Layer

Inspired by:

```text
PaperQA
OpenAlex
```

Future modules:

```text
ResearchAgent
ResearchNote
EvidenceRecord
CitationRecord
```

Not required for V1.

---

# V1 Priorities

Priority order:

```text
1. ForgeGraph
2. AgentBus
3. FailureMemory
4. PatchPlan
5. SandboxManager
6. ProjectIndex
7. KnowledgeGraph
```

These components unlock autonomous repository analysis and integration.
