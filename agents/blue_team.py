# agents/blue_team.py

from crewai import Agent
from tools.mitigation_planner import MitigationPlannerTool
from tools.threat_memory_tool import ThreatMemoryTool
from config import llm

# 🔍 Threat Classifier Agent (LLM only)
threat_classifier = Agent(
    role="Threat Classifier",
    goal="Analyze logs and assign MITRE ATT&CK categories using reasoning and pattern recognition.",
    backstory=(
        "You're trained on the entire MITRE ATT&CK framework and can classify adversarial behavior from log details "
        "like event type, IP, protocol, ports, and attack pattern."
    ),
    tools=[],  # LLM handles classification
    llm=llm,
    verbose=True
)

# 🛡️ Mitigation Planner Agent
response_planner = Agent(
    role="Mitigation Planner",
    goal=(
        "Create precise mitigation plans for every classified threat. Use past memory when applicable. "
        "Reference classification, technique, and source IP to determine optimal response."
    ),
    backstory=(
        "You're an experienced SOC responder trained in incident response, mitigation, and security hardening. "
        "You generate actionable plans based on structured threat reports."
    ),
    tools=[MitigationPlannerTool(), ThreatMemoryTool()],
    llm=llm,
    verbose=True
)
