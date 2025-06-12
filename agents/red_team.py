from crewai import Agent
from tools.cicids_loader import CICIDSLogTool

recon_agent = Agent(
    role="Reconnaissance Agent",
    goal="Load and simulate reconnaissance activity logs from real attack datasets",
    backstory="An adversary agent analyzing and injecting logs from real-world attacks captured in the CICIDS2017 dataset.",
    tools=[CICIDSLogTool()],
    verbose=True
)

# exploit_injector = Agent(
#     role="Exploit Injector",
#     goal="Emulate mid-stage attacks like infiltration, DoS, brute force from real dataset logs",
#     backstory="An adversary replaying actual attack patterns observed in network traces. Uses verified labeled data to create believable log trails.",
#     tools=[CICIDSLogTool()],
#     verbose=True
# )
