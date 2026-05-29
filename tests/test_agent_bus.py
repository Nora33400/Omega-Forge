from omega_forge.core.agent_bus import AgentBus
from omega_forge.core.agent_message import AgentMessage


def test_agent_message_roundtrip():
    message = AgentMessage(
        sender="planner",
        receiver="executor",
        message_type="TaskCreated",
        payload={"title": "Build"},
        correlation_id="root-1",
    )

    restored = AgentMessage.from_dict(message.to_dict())

    assert restored.id == message.id
    assert restored.sender == "planner"
    assert restored.receiver == "executor"
    assert restored.payload["title"] == "Build"
    assert restored.correlation_id == "root-1"


def test_agent_bus_publish_calls_subscriber():
    bus = AgentBus()
    received = []
    bus.subscribe("TaskCreated", received.append)

    message = AgentMessage(sender="planner", message_type="TaskCreated")
    bus.publish(message)

    assert received == [message]
    assert bus.history() == [message]
    assert bus.count() == 1


def test_agent_bus_ignores_unsubscribed_message_types():
    bus = AgentBus()
    received = []
    bus.subscribe("TaskCreated", received.append)

    bus.publish(AgentMessage(sender="validator", message_type="ValidationPassed"))

    assert received == []
    assert bus.count() == 1


def test_agent_bus_clear_history():
    bus = AgentBus()
    bus.publish(AgentMessage(sender="a", message_type="Ping"))

    bus.clear()

    assert bus.history() == []
    assert bus.count() == 0
