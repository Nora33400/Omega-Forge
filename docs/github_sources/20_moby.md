# 20 — moby/moby Decomposition

Repository: `moby/moby`

License from source pack: Apache-2.0.

Moby is the foundation project behind Docker. For Omega-Forge, it is primarily relevant as an execution isolation and sandbox technology.

## 1. Role for Omega-Forge

Omega-Forge eventually wants:

```text
Generate code
Run code
Test code
Repair code
Repeat
```

Moby answers:

```text
Where should untrusted generated code run?
```

Answer:

```text
Sandbox containers
```

## 2. What to study

Study:

```text
containers
image lifecycle
isolation
resource limits
volumes
network controls
execution environments
```

## 3. What could be copied

Default: copy nothing.

Use container runtime externally.

## 4. What must not be copied

Avoid:

```text
container engine
runtime internals
network stack
storage stack
```

Reason:

```text
Moby already solved these problems.
```

## 5. What should be adapted as original Omega-Forge code

Create:

```text
SandboxSession
SandboxManager
ExecutionEnvironment
```

Capabilities:

```text
start sandbox
copy workspace
run tests
capture logs
destroy sandbox
```

## 6. Adapter idea

Create:

```text
moby_adapter.py
```

or

```text
docker_adapter.py
```

Purpose:

```text
manage container lifecycle
```

## 7. License/compliance notes

Apache-2.0.

Prefer runtime usage over code reuse.

## 8. First concrete integration task

Build:

```text
SandboxManager
```

Acceptance criteria:

```text
create sandbox
execute command
collect output
destroy sandbox
CI remains green
```

## 9. Decision

Decision:

```text
Critical execution infrastructure.
Do not copy source code.
Use runtime.
```

Priority: S-Tier.

## 10. Omega-Forge task proposal

Add:

```text
Build SandboxManager
Build SandboxSession
Connect RepairAgent execution loop
```

Moby provides the safe execution layer required for autonomous code generation and repair.
