from omega_forge.core.knowledge_graph import KnowledgeGraph


def test_add_nodes_and_edges():
    graph = KnowledgeGraph()

    task = graph.add_node("Task", "Build API", metadata={"priority": 1})
    artifact = graph.add_node("Artifact", "main.py")
    edge = graph.add_edge(task.id, artifact.id, "generated")

    assert graph.get_node(task.id).label == "Build API"
    assert graph.get_node(task.id).metadata["priority"] == 1
    assert edge.source == task.id
    assert edge.target == artifact.id
    assert edge.relation == "generated"


def test_find_nodes_by_type_and_label():
    graph = KnowledgeGraph()
    graph.add_node("Task", "Build API")
    graph.add_node("Task", "Build CLI")
    graph.add_node("Artifact", "api.py")

    task_nodes = graph.find_nodes(type="Task")
    api_nodes = graph.find_nodes(label_contains="api")

    assert len(task_nodes) == 2
    assert {node.label for node in api_nodes} == {"Build API", "api.py"}


def test_incoming_outgoing_and_neighbors():
    graph = KnowledgeGraph()
    task = graph.add_node("Task", "Build API")
    artifact = graph.add_node("Artifact", "main.py")
    failure = graph.add_node("Failure", "ModuleNotFoundError")

    graph.add_edge(task.id, artifact.id, "generated")
    graph.add_edge(artifact.id, failure.id, "failed_with")

    assert graph.outgoing(task.id)[0].relation == "generated"
    assert graph.incoming(failure.id)[0].relation == "failed_with"
    assert {node.label for node in graph.neighbors(artifact.id)} == {"Build API", "ModuleNotFoundError"}


def test_summary_counts_types_and_relations():
    graph = KnowledgeGraph()
    a = graph.add_node("Task", "A")
    b = graph.add_node("Task", "B")
    c = graph.add_node("Artifact", "C")
    graph.add_edge(a.id, c.id, "generated")
    graph.add_edge(b.id, c.id, "generated")

    summary = graph.summary()

    assert summary["node_count"] == 3
    assert summary["edge_count"] == 2
    assert summary["node_types"] == {"Artifact": 1, "Task": 2}
    assert summary["relations"] == {"generated": 2}


def test_export_and_import_roundtrip():
    graph = KnowledgeGraph()
    task = graph.add_node("Task", "Build API")
    artifact = graph.add_node("Artifact", "main.py")
    graph.add_edge(task.id, artifact.id, "generated")

    restored = KnowledgeGraph.from_export(graph.export())

    assert restored.summary() == graph.summary()
    assert restored.get_node(task.id).label == "Build API"
    assert restored.outgoing(task.id)[0].target == artifact.id
