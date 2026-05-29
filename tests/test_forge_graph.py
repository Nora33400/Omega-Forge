from omega_forge.core.forge_graph import ForgeGraph


def test_forge_graph_runs_linear_flow():
    graph = ForgeGraph()
    graph.add_node("start", handler=lambda state: {"seen_start": True})
    graph.add_node("end", handler=lambda state: {"seen_end": True})
    graph.add_edge("start", "end")

    result = graph.run("start")

    assert result.path == ["start", "end"]
    assert result.state["seen_start"] is True
    assert result.state["seen_end"] is True
    assert result.stopped_reason == "no_next_edge"


def test_forge_graph_conditional_edge():
    graph = ForgeGraph()
    graph.add_node("validate")
    graph.add_node("repair")
    graph.add_node("done")
    graph.add_condition("has_error", lambda state: state.get("error") is True)
    graph.add_edge("validate", "repair", condition_name="has_error")
    graph.add_edge("validate", "done")

    failed = graph.run("validate", {"error": True})
    passed = graph.run("validate", {"error": False})

    assert failed.path == ["validate", "repair"]
    assert passed.path == ["validate", "done"]


def test_forge_graph_export():
    graph = ForgeGraph()
    graph.add_node("a")
    graph.add_node("b")
    graph.add_edge("a", "b", label="next")

    exported = graph.export()

    assert exported["nodes"][0]["name"] == "a"
    assert exported["edges"][0]["label"] == "next"
