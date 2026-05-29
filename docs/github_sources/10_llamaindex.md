# 10 — run-llama/llama_index Decomposition

Repository: `run-llama/llama_index`

License from source pack: MIT.

LlamaIndex is one of the most strategically important repositories remaining because it focuses on turning raw project information into structured, retrievable knowledge.

## 1. Role for Omega-Forge

Current Omega-Forge knows how to:

```text
Generate
Validate
Repair
Remember failures
```

It does not yet know how to:

```text
Understand a repository
Understand documentation
Understand project history
Understand large codebases
```

LlamaIndex addresses this gap.

## 2. What to study

Study:

```text
document ingestion
index construction
chunking
retrieval
metadata enrichment
multi-source indexing
query engines
```

Likely upstream areas to inspect:

```text
llama_index/core/
llama_index/readers/
llama_index/indices/
llama_index/retrievers/
examples/
```

## 3. What could be copied

Default: copy nothing.

Potential future copy candidates:

```text
small ingestion patterns
small indexing examples
```

Prefer original implementation.

## 4. What must not be copied

Avoid copying:

```text
full indexing engine
provider integrations
retrieval engine internals
examples wholesale
documentation wholesale
```

Reason: Omega-Forge needs repository understanding, not another giant framework.

## 5. What should be adapted as original Omega-Forge code

Create:

```text
omega_forge/core/project_index.py
omega_forge/core/context_index.py
```

Minimal capabilities:

```text
index files
index docs
index reports
retrieve relevant context
```

## 6. Adapter idea

Future:

```text
omega_forge/adapters/llamaindex_adapter.py
```

Purpose:

```text
optional advanced indexing backend
```

## 7. License/compliance notes

MIT license.

Before copying:

```text
record commit SHA
preserve LICENSE
document copied files
```

## 8. First concrete integration task

Build:

```text
ProjectIndex
```

Acceptance criteria:

```text
can index repository files
can retrieve files by relevance
can expose context to Planner and Repair agents
CI remains green
```

## 9. Decision

Decision:

```text
Study repository understanding patterns.
Build Omega-native indexing.
Do not copy framework.
```

Priority: P0.

This is the first remaining repository that significantly improves Omega-Forge's understanding capabilities.

## 10. Ω-Forge task proposal

Add:

```text
Build ProjectIndex
Build ContextIndex
Connect ProjectIndex to PlannerAgent
```

LlamaIndex fills the gap between memory and understanding.
