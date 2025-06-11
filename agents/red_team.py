from crewai import Agent
from tools.attack_log_generator import AttackLogGeneratorTool

# 🕵️ Reconnaissance Agent
recon_agent = Agent(
    role="Reconnaissance Agent",
    goal="Simulate early-stage network reconnaissance via port scans and service fingerprinting",
    backstory=(
        "An adversary conducting stealthy network scans to discover open ports and live hosts "
        "using tools like Nmap or Masscan. Generates Zeek-style connection logs."
    ),
    tools=[AttackLogGeneratorTool(attack_type="recon")],
    verbose=True
)

# 🚨 Exploit Injector Agent
exploit_injector = Agent(
    role="Exploit Injector",
    goal="Emulate mid-stage attack behaviors like SSH brute-force or web exploit injection",
    backstory=(
        "An attacker attempting to gain unauthorized access to systems using SSH brute force "
        "and exploiting known CVEs via HTTP requests. Generates logs with realistic attack entries."
    ),
    tools=[AttackLogGeneratorTool(attack_type="exploit")],
    verbose=True
)
