# 06 — lancedb/lancedb Decomposition

Repository: `lancedb/lancedb`

License from source pack: Apache-2.0.

LanceDB is relevant to Omega-Forge because it offers an embedded, local-first vector database model. Unlike Qdrant, which is often deployed as a service, LanceDB aligns naturally with a portable workspace-oriented architecture.

## 1. Role for Omega-Forge

After mem0 and Qdrant analysis, Omega-Forge needs:

```text
FailureKnowledgeBase
↓
semantic retrieval
↓
vector storage
```

Two broad directions exist:

```text
Qdrant
→ service-oriented
→ scalable
→ infrastructure heavier

LanceDB
→ embedded
→ local-first
→ workspace-friendly
```

For Omega-Forge, LanceDB is currently the closer architectural match.

## 2. What to study

Study concepts rather than implementation internals.

Important patterns:

```text
Embedded vector storage
Tables
Schema evolution
Metadata columns
Hybrid search
Local persistence
Portable databases
Data versioning ideas
```

Likely upstream areas to inspect after cloning:

```text
python/python/lancedb/
rust/
docs/
examples/
tests/
```

Omega-Forge should focus on usage patterns and API boundaries.

## 3. What could be copied

Default: copy nothing.

Possible future copy candidates after exact commit and license audit:

```text
Tiny schema examples
Tiny local database initialization examples
```

Better approach:

```text
Define Omega-Forge memory interfaces first.
Implement LanceDB adapter later.
```

## 4. What must not be copied

Avoid copying:

```text
Storage engine internals
Rust internals
Indexing internals
Query planner internals
Large example suites
Docs wholesale
Branding/assets
```

Reason: Omega-Forge should remain a forge, not become a database project.

## 5. What should be adapted as original Omega-Forge code

Reuse the abstraction proposed during Qdrant analysis:

```text
VectorMemoryStore
```

Implementations:

```text
JsonFailureMemoryStore
InMemoryVectorMemoryStore
LanceDbVectorMemoryStore
QdrantVectorMemoryStore
```

Omega-Forge should not know which backend is active.

Example:

```python
store.search(
    query="python syntax error near validator",
    limit=5,
)
```

should work regardless of backend.

## 6. Adapter idea

Future optional adapter:

```text
omega_forge/adapters/lancedb_adapter.py
```

Purpose:

```text
Persist FailureKnowledgeBase entries locally.
Provide semantic search.
Remain portable with the workspace.
```

Adapter policy:

```text
- optional dependency
- local-first
- usable offline
- no external service required
- CI uses fake/in-memory backend
```

## 7. License/compliance notes

Apache-2.0 is permissive but requires preserving license and notices when copying.

Before copying anything:

```text
1. Clone upstream.
2. Record exact commit SHA.
3. Copy LICENSE into third_party_notices/lancedb_LICENSE if code is copied.
4. Check NOTICE file if present.
5. Document copied files and modifications.
6. Prefer dependency/adapters over vendoring.
```

## 8. First concrete integration task

Do not integrate LanceDB directly yet.

First Omega-native task:

```text
Build backend-independent VectorMemoryStore API
```

Acceptance criteria:

```text
- Backend interface exists.
- FailureKnowledgeBase depends on interface only.
- In-memory backend passes tests.
- Backend selection can be configured.
- CI does not require LanceDB.
- CI remains green.
```

## 9. Decision

Decision: **LanceDB is currently a better future default candidate than Qdrant for Omega-Forge's local-first philosophy, but still via adapter only.**

Integration type:

```text
Optional adapter later
No vendored code now
No hard dependency now
```

Priority: P1.

Potential future default:

```text
FailureKnowledgeBase
↓
LanceDbVectorMemoryStore
```

while keeping:

```text
QdrantVectorMemoryStore
```

available for larger deployments.

## 10. Ω-Forge task proposal

Add tasks:

```text
Build VectorMemoryStore abstraction
Build backend selection mechanism
Prepare LanceDB adapter boundary
```

This keeps Omega-Forge portable while enabling future semantic memory capabilities.
