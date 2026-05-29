# GitHub Sources — Repo-by-Repo Decomposition Index

This folder decomposes each accepted repository from `omega_github_sources_pack(1).zip` one by one.

The goal is not to dump external source code into Omega-Forge. The goal is to decide, for each repository:

1. what to understand;
2. what to copy only if justified;
3. what not to copy;
4. what to adapt internally;
5. what should become an adapter;
6. what license constraints must be preserved.

## Source pack inputs

Accepted list contains 20 repositories:

| # | Repo | Category | License note from pack | Status |
|---:|---|---|---|---|
| 01 | `langchain-ai/langgraph` | orchestration | MIT | to decompose |
| 02 | `microsoft/autogen` | orchestration | MIT code + CC-BY-4.0 docs | to decompose |
| 03 | `crewAIInc/crewAI` | orchestration | MIT | to decompose |
| 04 | `chroma-core/chroma` | vector_memory | Apache-2.0 | to decompose |
| 05 | `qdrant/qdrant` | vector_memory | Apache-2.0 | to decompose |
| 06 | `lancedb/lancedb` | vector_memory | Apache-2.0 | to decompose |
| 07 | `run-llama/llama_index` | document_rag | MIT | to decompose |
| 08 | `deepset-ai/haystack` | document_rag | Apache-2.0 | to decompose |
| 09 | `OpenHands/OpenHands` | coding_agents | MIT core; enterprise directory excluded | to decompose |
| 10 | `Aider-AI/aider` | coding_agents | Apache-2.0 | to decompose |
| 11 | `facebook/react` | ui | MIT | to decompose |
| 12 | `tauri-apps/tauri` | ui | MIT OR Apache-2.0 code; logo restricted | to decompose |
| 13 | `cytoscape/cytoscape.js` | visualization | MIT | to decompose |
| 14 | `xyflow/xyflow` | visualization | MIT | to decompose |
| 15 | `mem0ai/mem0` | memory | Apache-2.0 | to decompose |
| 16 | `microsoft/graphrag` | knowledge_graph | MIT | to decompose |
| 17 | `Future-House/paper-qa` | science_rag | Apache-2.0 | to decompose |
| 18 | `ourresearch/openalex-guts` | science_data | MIT | to decompose |
| 19 | `networkx/networkx` | graph_algorithms | BSD-3-Clause | to decompose |
| 20 | `moby/moby` | sandbox_runtime | Apache-2.0 | to decompose |

Rejected/cautious list:

| Repo | Reason |
|---|---|
| `memgraph/memgraph` | BSL-1.1 + MEL; reject for now. |
| `neo4j/neo4j` | GPL/AGPL/commercial mixed; caution. |
| Docker Desktop | proprietary/commercial terms; use Moby instead. |

## Decomposition template

Each repo gets its own file with this structure:

```text
1. Role for Omega-Forge
2. What to study
3. What could be copied
4. What must not be copied
5. What should be adapted as original Omega-Forge code
6. Adapter idea
7. License/compliance notes
8. First concrete integration task
9. Decision
```

## Immediate priority order

P0 for current Omega-Forge:

1. `langchain-ai/langgraph` — execution graph model.
2. `Aider-AI/aider` — code editing/repair loop patterns.
3. `OpenHands/OpenHands` — software-engineering sandbox patterns.
4. `mem0ai/mem0` — repair/failure memory pattern.
5. `qdrant/qdrant` or `lancedb/lancedb` — memory backend candidate.

## Policy

Do not copy source files into `omega_forge/` until a repo-specific decomposition explicitly says what file or idea is safe and useful.

Default approach:

```text
Study architecture
↓
Create original Omega-Forge abstraction
↓
Use external repo as dependency or adapter
↓
Only vendor/copy tiny pieces when license and value justify it
```
