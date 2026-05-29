# 05 — qdrant/qdrant Decomposition

Repository: `qdrant/qdrant`

License from source pack: Apache-2.0.

Qdrant is relevant to Omega-Forge as a production-grade vector database candidate. For Omega-Forge, the immediate question is not “copy Qdrant”, but “when should the simple local FailureKnowledgeBase graduate from JSON/SQLite to vector search?”

## 1. Role for Omega-Forge

Current memory target after the mem0 analysis:

```text
FailureKnowledgeBase
↓
local JSON entries
↓
find by exact error_signature
```

Future memory with vector search:

```text
FailureKnowledgeBase
↓
embed error + context + repair result
↓
vector search
↓
retrieve similar failures
↓
propose better repair
```

Qdrant fits the future layer:

```text
FailureMemoryVectorStore
```

Not the first local memory layer.

## 2. What to study

Study these concepts:

```text
Collections
Points
Vectors
Payload metadata
Similarity search
Filtering by payload
Upsert/delete/search lifecycle
Persistence
Local vs server deployment
Client/server boundary
```

Likely upstream areas to inspect after cloning:

```text
lib/
src/
client/
docs/
tests/
```

But Omega-Forge should mostly use Qdrant as an external service/library through a client, not study or copy the Rust internals.

## 3. What could be copied

Default: copy nothing.

Qdrant is a mature database. Omega-Forge should not copy database internals.

Potential future copy candidates only after exact commit and license audit:

```text
Tiny example payload schemas
Tiny configuration examples
```

Better approach:

```text
Implement an adapter interface in Omega-Forge.
Use qdrant-client or server deployment externally.
```

## 4. What must not be copied

Avoid copying:

```text
Rust storage engine
Indexing internals
API server internals
Cluster/distributed code
Client libraries wholesale
Docs wholesale
Benchmark code wholesale
Branding/assets
```

Reason: Omega-Forge needs an abstraction over vector memory, not its own fork of a vector database.

## 5. What should be adapted as original Omega-Forge code

Create original interface:

```text
omega_forge/core/vector_memory.py
```

Minimal protocol:

```python
class VectorMemoryStore:
    def upsert(entry): ...
    def search(query, filters=None, limit=5): ...
    def delete(entry_id): ...
```

Initial implementations:

```text
JsonFailureMemoryStore        # immediate, no dependency
InMemoryVectorMemoryStore     # tests only, fake similarity
QdrantVectorMemoryStore       # optional later
```

Omega-specific vector entry:

```text
VectorMemoryEntry
├─ id
├─ text
├─ vector
├─ payload
│  ├─ project_type
│  ├─ task_title
│  ├─ template_name
│  ├─ error_signature
│  ├─ status
│  └─ created_at
```

## 6. Adapter idea

Future optional adapter:

```text
omega_forge/adapters/qdrant_adapter.py
```

Purpose:

```text
Store FailureMemoryEntry embeddings in Qdrant.
Search for semantically similar past failures.
Filter by project_type, template_name, or status.
```

Adapter policy:

```text
- optional dependency
- disabled by default
- local JSON/SQLite remains default
- no network service required for tests
- tests use a fake/in-memory store first
```

## 7. License/compliance notes

Apache-2.0 is permissive but requires preserving license and notices when copying. Because Qdrant is a database, Omega-Forge should depend on it rather than copy internals.

Before copying anything:

```text
1. Clone upstream.
2. Record exact commit SHA.
3. Copy LICENSE into third_party_notices/qdrant_LICENSE if code is copied.
4. Check NOTICE file if present.
5. Document copied files and modifications.
6. Prefer external dependency/service over vendoring.
```

## 8. First concrete integration task

Do not integrate Qdrant directly yet.

First Omega-native task:

```text
Define VectorMemoryStore protocol
```

Acceptance criteria:

```text
- Protocol/interface exists.
- In-memory fake implementation exists for tests.
- FailureKnowledgeBase can depend on the interface later.
- No Qdrant dependency is required for CI.
- Tests cover upsert/search/delete behavior using fake store.
- CI remains green.
```

## 9. Decision

Decision: **do not copy Qdrant; design Omega-Forge vector memory interface first**.

Integration type:

```text
Optional adapter later
No vendored code now
No hard dependency now
```

Priority: P1.

Qdrant is valuable when Omega-Forge has enough memory entries to need semantic retrieval. It is premature before a local FailureKnowledgeBase exists.

## 10. Ω-Forge task proposal

Add tasks:

```text
Build VectorMemoryStore protocol
Build InMemoryVectorMemoryStore
Design Qdrant adapter boundary
```

This prepares Omega-Forge for scalable memory without locking the foundation to one database.
