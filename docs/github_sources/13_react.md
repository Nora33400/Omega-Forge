# 13 — facebook/react Decomposition

Repository: `facebook/react`

License from source pack: MIT.

React is not a core architecture repository for Omega-Forge. It is a UI foundation.

## 1. Role for Omega-Forge

React answers:

```text
How do we display Omega-Forge?
```

Not:

```text
How do we build Omega-Forge?
```

## 2. What to study

Study:

```text
component architecture
state management
UI composition
reactivity
```

Focus on frontend organization.

## 3. What could be copied

Default: copy nothing.

Use React as a dependency if selected.

## 4. What must not be copied

Avoid copying:

```text
internal runtime
reconciler internals
large examples
documentation wholesale
```

Reason: React should remain an external dependency.

## 5. What should be adapted as original Omega-Forge code

Create UI concepts:

```text
ForgeGraphView
AgentView
TaskView
MemoryView
```

But keep business logic outside React.

## 6. Adapter idea

Not really an adapter.

Instead:

```text
Omega-Forge Web UI
built with React
```

## 7. License/compliance notes

MIT license.

Preserve notices if code is copied.

## 8. First concrete integration task

Build UI models before UI components.

Acceptance criteria:

```text
UI consumes API
UI does not contain forge logic
```

## 9. Decision

Decision:

```text
React is infrastructure.
Not an architectural pillar.
```

Priority: P2.

## 10. Ω-Forge task proposal

Add:

```text
Define frontend API contracts
```

before selecting a frontend framework.
