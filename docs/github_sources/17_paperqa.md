# 17 — Future-House/paper-qa Decomposition

Repository: `Future-House/paper-qa`

License from source pack: MIT.

PaperQA is focused on answering questions from scientific literature. For Omega-Forge it is not a core execution component, but a knowledge acquisition component.

## 1. Role for Omega-Forge

PaperQA answers:

```text
How do we extract answers from papers?
```

For Omega-Forge:

```text
ResearchAgent
↓
Paper Collection
↓
Evidence Extraction
↓
Structured Knowledge
```

## 2. What to study

Study:

```text
paper ingestion
citation tracking
evidence extraction
answer synthesis
source attribution
```

## 3. What could be copied

Default: copy nothing.

Potential future candidates:

```text
citation schemas
source attribution patterns
```

## 4. What must not be copied

Avoid copying:

```text
prompt systems
provider integrations
large examples
```

## 5. What should be adapted as original Omega-Forge code

Create:

```text
ResearchNote
EvidenceRecord
CitationRecord
```

## 6. Adapter idea

Future:

```text
paperqa_adapter.py
```

Optional only.

## 7. License/compliance notes

MIT.

## 8. First concrete integration task

Build:

```text
ResearchNote model
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
ResearchAgent
CitationRecord
EvidenceRecord
```

PaperQA is valuable when Omega-Forge starts learning from scientific literature rather than only from project artifacts.
