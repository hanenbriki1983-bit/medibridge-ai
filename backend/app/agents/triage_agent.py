"""CrewAI adapter placeholder for MVP.

In MVP we keep orchestration lightweight. This module is where CrewAI tasks/agents
will be initialized when API keys and full prompts are introduced.
"""


def triage_agent_decision(symptoms: list[str], emergency: bool, reason: str) -> dict[str, str]:
    priority = "critical" if emergency else "normal"
    return {
        "priority": priority,
        "note": reason,
        "agent": "crew_triage_agent_stub",
    }
