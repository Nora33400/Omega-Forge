# 14 — tauri-apps/tauri Decomposition

Repository: `tauri-apps/tauri`

License from source pack: MIT OR Apache-2.0 for code. Branding assets have separate restrictions.

Tauri is relevant because it provides a path from a web UI to a lightweight desktop application.

## 1. Role for Omega-Forge

React answered:

```text
How do we build the UI?
```

Tauri answers:

```text
How do we deliver the UI as a desktop application?
```

## 2. What to study

Study:

```text
desktop shell architecture
frontend/backend boundary
native capabilities
IPC communication
application packaging
```

Focus on architecture, not runtime internals.

## 3. What could be copied

Default: copy nothing.

Use Tauri as a dependency if selected.

## 4. What must not be copied

Avoid copying:

```text
runtime internals
branding assets
large examples
documentation wholesale
```

Reason: Tauri should remain external infrastructure.

## 5. What should be adapted as original Omega-Forge code

Create desktop concepts:

```text
OmegaForgeDesktop
├─ ForgeGraphView
├─ TaskView
├─ MemoryView
├─ AgentView
└─ SettingsView
```

Keep forge logic in backend services.

## 6. Adapter idea

Not an adapter.

Instead:

```text
React UI
+
Tauri Shell
```

## 7. License/compliance notes

Code is permissive.

Branding/logo restrictions must be respected.

## 8. First concrete integration task

Build frontend/backend API boundary.

Acceptance criteria:

```text
UI talks through API
No forge logic in frontend
Desktop shell replaceable
```

## 9. Decision

Decision:

```text
Useful deployment technology.
Not a core architecture repository.
```

Priority: B-Tier.

## 10. Ω-Forge task proposal

Add:

```text
Define Desktop API
Prepare desktop packaging layer
```

Tauri is the most likely desktop delivery mechanism if Omega-Forge becomes a local application.
