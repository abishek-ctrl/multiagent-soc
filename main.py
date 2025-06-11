# main.py
from crewai import Task, Crew
from agents.blue_team import log_monitor, threat_classifier, response_planner
from agents.red_team import recon_agent, exploit_injector
import dotenv
import os
import time
from datetime import datetime
import sys

dotenv.load_dotenv()
start_time = time.time()

# Timestamped output directory
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
log_dir = f"output/test_{timestamp}"
os.makedirs(log_dir, exist_ok=True)
log_path = os.path.join(log_dir, "run.log")

# Redirect all prints to both console and run.log
class TeeLogger:
    def __init__(self, *streams):
        self.streams = streams
    def write(self, msg):
        for stream in self.streams:
            stream.write(msg)
            stream.flush()
    def flush(self):
        for stream in self.streams:
            stream.flush()

log_file = open(log_path, "w")
sys.stdout = TeeLogger(sys.__stdout__, log_file)

# # Red Team Phase
# recon_task = Task(
#     description="Generate reconnaissance activity logs such as port scans using realistic patterns.",
#     agent=recon_agent,
#     expected_output="A JSONL stream of port scan events from attacker IPs."
# )

# exploit_task = Task(
#     description="Generate exploit logs simulating brute-force attempts or web attacks.",
#     agent=exploit_injector,
#     expected_output="A JSONL stream of login attempts or CVE-based payloads."
# )

# print("\n=== [Red Team] Generating Attack Logs ===\n")
# red_crew = Crew(tasks=[recon_task, exploit_task], verbose=True)
# red_output = red_crew.kickoff()

# red_log_file = os.path.join(log_dir, "syn_log.txt")
# with open(red_log_file, "w") as f:
#     f.write(str(red_output))

with open("data\syn_log.txt", 'r') as f:
    raw_logs = f.read()

# Blue Team Phase
log_task = Task(
    description=(
        "Parse the following raw logs into structured JSON events:\n\n"
        f"{raw_logs}\n\n"
        "Expected format: List of JSON objects with keys like timestamp, source_ip, dest_ip, event_type, etc."
    ),
    agent=log_monitor,
    expected_output="Parsed and structured logs as JSON array.",
)

classify_task = Task(
    description=(
        "Classify the structured logs using MITRE ATT&CK categories. "
        "For each event, return a classification like Initial Access, Execution, Privilege Escalation, etc. "
        "Example: Format the result as:\n"
        "<entry>{\"classification\": \"Privilege Escalation\", \"confidence\": \"high\"}</entry>"
    ),
    agent=threat_classifier,
    context=[log_task],
    expected_output="A list of threat-tagged logs with MITRE classification.",
)

mitigate_task = Task(
    description=(
        "Generate actionable mitigation strategies based on the classified threat logs. "
        "Use realistic remediation steps like isolating hosts, resetting credentials, etc.\n"
        "Respond using format:\n"
        "<entry>{\"mitigation\": \"solution\"}</entry>"
    ),
    agent=response_planner,
    context=[classify_task],
    expected_output="A mitigation plan in structured JSON or tagged format.",
)

print("\n===  Blue Team: Detect & Mitigate ===\n")
blue_crew = Crew(tasks=[log_task, classify_task, mitigate_task], verbose=True)
blue_output = blue_crew.kickoff()

print("\n===  Final Agentic Output ===\n")
print(blue_output)

with open(os.path.join(log_dir, "output.md"), "w") as f:
    f.write(str(blue_output))

end_time = time.time()
print(f"\nCompleted in {end_time - start_time:.2f} seconds.")
