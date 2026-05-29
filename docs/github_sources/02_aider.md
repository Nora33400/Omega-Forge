# 02 — Aider-AI/aider Decomposition

Repository: `Aider-AI/aider`

License from source pack: Apache-2.0.

Aider is a CLI coding assistant focused on editing real repositories with LLM assistance. For Omega-Forge, it is most valuable as a reference for code-editing loops, patch safety, repository context selection, and human-reviewable modifications.

## 1. Role for Omega-Forge

Aider maps directly to the future Omega-Forge auto-repair path:

```text
ArtifactValidator
↓
RepairAgent
↓
Patch planning
↓
File edit
↓
Revalidate
```

Current Omega-Forge has only:

```text
validation error
↓
repair_task text
```

Aider-style capability would evolve this into:

```text
validation error
↓
repair plan
↓
proposed patch
↓
apply patch safely
↓
pytest
↓
commit or block
```

## 2. What to study

Study these patterns:

```text
Repository map / relevant file selection
Editable file set vs read-only context
Patch generation
Diff presentation
Human confirmation before applying risky edits
Git integration
Test command execution after edits
Conversation memory around code changes
Model abstraction / provider separation
```

Likely upstream areas to inspect after cloning:

```text
aider/coders/
aider/repo.py
aider/commands.py
aider/io.py
aider/models.py
aider/scrape.py
tests/
```

## 3. What could be copied

Default: copy no implementation now.

Potential future copy candidates only after exact commit and license audit:

```text
Small prompt-shape examples
Small patch-format examples
Tiny command UX patterns
```

Better than copying:

```text
Implement Omega-Forge's own PatchPlan and PatchApplier.
Use Aider as an optional external adapter.
```

## 4. What must not be copied

Avoid copying:

```text
Full coder engine
Model/provider handling
CLI command system wholesale
Repository map implementation wholesale
Prompt library wholesale
Tests wholesale
Branding or docs wholesale
```

Reason: Omega-Forge needs a deterministic, CI-safe repair loop first, not a full pair-programming CLI embedded inside the project.

## 5. What should be adapted as original Omega-Forge code

Create original modules:

```text
omega_forge/core/patch_plan.py
omega_forge/core/patch_applier.py
omega_forge/agents/patch_repair.py
```

Minimal concepts:

```text
PatchPlan
├─ target_path
├─ reason
├─ before_hash
├─ proposed_content or diff
├─ validation_error
└─ risk_level

PatchApplier
├─ verify target exists
├─ verify before_hash
├─ write proposed content
├─ re-run ArtifactValidator
└─ return applied/blocked
```

First repair loop should be narrow:

```text
Only generated artifacts
Only files inside tmp/workspace or generated output paths
No arbitrary shell command execution
No hidden edits
```

## 6. Adapter idea

Future optional adapter:

```text
omega_forge/adapters/aider_adapter.py
```

Purpose:

```text
Given a failed validation and selected files,
launch or call Aider externally to propose a patch.
```

Adapter policy:

```text
- disabled by default
- requires explicit user opt-in
- produces reviewable patch plan
- never commits automatically at first
```

## 7. License/compliance notes

Apache-2.0 is permissive but requires preservation of license and notices when copying. It also includes patent grant language.

Before copying anything:

```text
1. Clone upstream.
2. Record exact commit SHA.
3. Copy LICENSE into third_party_notices/aider_LICENSE.
4. Check NOTICE file if present.
5. Document copied files and modifications.
6. Prefer adapter/dependency over vendoring.
```

## 8. First concrete integration task

Do not integrate Aider directly yet.

First Omega-native task:

```text
Build PatchPlan and PatchApplier for generated artifacts
```

Acceptance criteria:

```text
- PatchPlan stores target path, reason, expected hash, proposed content.
- PatchApplier refuses to edit files outside the workspace root.
- PatchApplier refuses to edit if before_hash changed.
- PatchApplier validates Python syntax after patch.
- Tests cover accepted patch, changed hash, outside-root path, invalid Python.
- CI remains green.
```

## 9. Decision

Decision: **study and adapt repair-loop patterns, do not copy source code yet**.

Integration type:

```text
Original Omega-Forge patch system first
Optional Aider adapter later
No vendored code now
```

Priority: P0.

## 10. Ω-Forge task proposal

Add tasks:

```text
Build PatchPlan data model
Build safe PatchApplier
Connect RepairAgent to PatchPlan
```

These tasks are more valuable than copying Aider, because Omega-Forge needs its own minimal, safe, testable patch loop before using a full external coding agent.
