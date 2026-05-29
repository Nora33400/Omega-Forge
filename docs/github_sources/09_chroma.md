# 09 — chroma-core/chroma Decomposition

Repository: `chroma-core/chroma`

License from source pack: Apache-2.0.

Chroma is a vector database and embedding retrieval system. For Omega-Forge, it occupies a similar space to Qdrant and LanceDB, but with a stronger focus on AI workflows and local developer experience.

## 1. Role for Omega-Forge

After mem0, Qdrant, and LanceDB analysis, Omega-Forge needs:

```text
FailureKnowledgeBase
↓
Semantic Retrieval
↓
Vector Storage Backend
```

Chroma is another candidate backend.

## 2. What to study

Study:

```text
collections
embeddings
metadata filters
similarity search
local persistence
retrieval APIs
```

Focus on API design rather than implementation internals.

## 3. What could be copied

Default: copy nothing.

Potential future copy candidates:

```text
small schema examples
small retrieval examples
```

Prefer adapters.

## 4. What must not be copied

Avoid copying:

```text
storage internals
index internals
embedding pipeline internals
server internals
large examples
```

Reason: Omega-Forge should define memory abstractions, not maintain a vector database fork.

## 5. What should be adapted as original Omega-Forge code

Reuse:

```text
VectorMemoryStore
```

Implementations become:

```text
JsonFailureMemoryStore
InMemoryVectorMemoryStore
LanceDbVectorMemoryStore
QdrantVectorMemoryStore
ChromaVectorMemoryStore
```

## 6. Adapter idea

Future optional adapter:

```text
omega_forge/adapters/chroma_adapter.py
```

Purpose:

```text
Store and search failure memories through Chroma.
```

Optional only.

## 7. License/compliance notes

Apache-2.0.

Before copying:

```text
record commit SHA
preserve LICENSE
prefer dependency over vendoring
```

## 8. First concrete integration task

Do not integrate Chroma yet.

Build:

```text
backend-independent VectorMemoryStore
```

first.

## 9. Decision

Decision:

```text
Treat Chroma as another backend candidate.
Do not copy source code.
Use adapters.
```

Priority: P2.

Compared to LanceDB and Qdrant, Chroma currently provides less unique architectural value for Omega-Forge.

## 10. Ω-Forge task proposal

Add:

```text
Chroma adapter boundary definition
```

only after FailureKnowledgeBase and VectorMemoryStore exist.
