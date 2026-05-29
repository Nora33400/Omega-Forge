# Third-Party Notices

This file tracks external projects considered for Omega-Forge.

Omega-Forge keeps third-party code outside the core and prefers adapters over direct copies.

## Policy

Accepted by default after verification:

- MIT
- Apache-2.0
- BSD-2-Clause
- BSD-3-Clause
- ISC

Requires review:

- MPL-2.0
- EPL
- LGPL

Avoid for closed core:

- GPL
- AGPL
- SSPL
- BUSL / BSL

## Candidate projects

| Project | Purpose | Integration preference | Status |
|---|---|---|---|
| Aider | coding assistant adapter | adapter or dependency | pending review |
| OpenHands | developer agent reference | adapter first | pending review |
| LangGraph | workflow orchestration | dependency | pending review |
| GraphRAG | knowledge retrieval | adapter or dependency | pending review |
| Qdrant | vector storage | service adapter | pending review |
| LlamaIndex | document ingestion | dependency | pending review |
| React Flow | graph interface | frontend dependency | pending review |
| Tauri | desktop shell | future shell | pending review |

Each accepted project must later include exact repository URL, license, version or commit, integration mode, and review date.
