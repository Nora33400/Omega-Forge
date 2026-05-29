# 18 — OpenAlex Decomposition

Project: OpenAlex

OpenAlex is a large open scholarly metadata source. Unlike PaperQA, which focuses on extracting answers from papers, OpenAlex focuses on discovering papers, authors, institutions, topics, and citation networks.

## 1. Role for Omega-Forge

OpenAlex answers:

```text
How do we discover relevant research?
```

For Omega-Forge:

```text
ResearchAgent
↓
OpenAlex Search
↓
Paper Discovery
↓
PaperQA
↓
Research Notes
```

## 2. What to study

Study:

```text
paper discovery
author discovery
citation networks
topic discovery
metadata exploration
```

## 3. What could be copied

Default: nothing.

Prefer API integration.

## 4. What must not be copied

Avoid:

```text
large datasets
mirrors
metadata dumps
```

## 5. What should be adapted as original Omega-Forge code

Create:

```text
ResearchQuery
PaperReference
AuthorReference
```

## 6. Adapter idea

Future:

```text
openalex_adapter.py
```

Purpose:

```text
discover literature
feed PaperQA
```

## 7. License/compliance notes

Prefer API usage and source attribution.

## 8. First concrete integration task

Build:

```text
ResearchQuery
```

## 9. Decision

Decision:

```text
Useful for research mode.
Not required for Omega-Forge V1.
```

Priority: P2.

## 10. Omega-Forge task proposal

Add:

```text
ResearchQuery
PaperReference
OpenAlex adapter boundary
```

OpenAlex complements PaperQA by helping find knowledge before extracting it.
