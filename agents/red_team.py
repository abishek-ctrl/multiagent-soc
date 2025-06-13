# agents/red_team.py

from crewai import Agent
from tools.cicids_loader import CICIDSLogTool
from config import llm

#  Reconnaissance Agent
recon_agent = Agent(
    role="Reconnaissance Agent",
    goal="Use your tool and do NOT comment. Your tool's output IS your final answer.",
    backstory=(
        "This agent collects the recon attack logs from the local dataset using the CICIDSLogTool tool it has access to."
    ),
    tools=[CICIDSLogTool(attack_type="recon")],
    llm=llm,
    allow_delegation=True,
    verbose=True
)

#  Exploit Injector Agent
exploit_injector = Agent(
    role="Exploit Injector",
    goal="Use your tool and do NOT comment. Your tool's output IS your final answer.",
    backstory=(
        "This agent collects the exploit logs from the local dataset using the CICIDSLogTool tool it has access to."
    ),
    tools=[CICIDSLogTool(attack_type="exploit")],
    llm=llm,
    allow_delegation=True,
    verbose=True
)
