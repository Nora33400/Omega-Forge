# 11 — deepset-ai/haystack Decomposition

Repository: `deepset-ai/haystack`

License from source pack: Apache-2.0.

Haystack is a framework for retrieval pipelines, document processing, and AI workflows. Unlike LlamaIndex, which focuses strongly on indexing and retrieval, Haystack focuses on composable pipelines.

## 1. Role for Omega-Forge

LlamaIndex answered:

```text
How do we understand a repository?
```

Haystack answers:

```text
How do we chain retrieval operations together?
```

For Omega-Forge:

```text
ProjectIndex
↓
Context Retrieval
↓
Planner
↓
Executor
↓
Repair
```

can become:

```text
Pipeline
├─ Retrieve
├─ Filter
├─ Rank
├─ Summarize
└─ Deliver Context
```

## 2. What to study

Study:

```text
pipeline composition
retrieval pipelines
ranking
filtering
document processing
component chaining
```

Likely upstream areas to inspect:

```text
haystack/components/
haystack/pipelines/
haystack/document_stores/
examples/
```

## 3. What could be copied

Default: copy nothing.

Potential future candidates:

```text
small pipeline examples
small component patterns
```

Prefer original implementation.

## 4. What must not be copied

Avoid copying:

```text
pipeline runtime
provider integrations
document store internals
examples wholesale
documentation wholesale
```

Reason: Omega-Forge already has ForgeGraph as its primary orchestration model.

## 5. What should be adapted as original Omega-Forge code

Create:

```text
omega_forge/core/context_pipeline.py
```

Concept:

```text
Retrieve
↓
Filter
↓
Rank
↓
Context Package
```

for Planner and Repair agents.

## 6. Adapter idea

Future:

```text
omega_forge/adapters/haystack_adapter.py
```

Purpose:

```text
optional advanced retrieval pipeline backend
```

## 7. License/compliance notes

Apache-2.0.

Before copying:

```text
record commit SHA
preserve LICENSE
prefer adapters
```

## 8. First concrete integration task

Build:

```text
ContextPipeline
```

Acceptance criteria:

```text
can retrieve context
can filter context
can rank context
can provide context package to agents
CI remains green
```

## 9. Decision

Decision:

```text
Study retrieval pipeline concepts.
Do not copy framework.
Build Omega-native context pipeline.
```

Priority: P1.

Haystack complements LlamaIndex but does not replace it.

## 10. Ω-Forge task proposal

Add:

```text
Build ContextPipeline
Connect ProjectIndex to ContextPipeline
```

Haystack contributes workflow ideas for repository understanding rather than a new core architectural pillar.
