# main.py

import os
import dotenv
import time
from datetime import datetime
import sys
import json

from crewai import Task, Crew
from agents.blue_team import log_monitor, threat_classifier, response_planner
from agents.red_team import recon_agent 
#, exploit_injector

dotenv.load_dotenv()
start_time = time.time()

# === Setup: Output directory ===
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
log_dir = f"output/test_{timestamp}"
os.makedirs(log_dir, exist_ok=True)
log_path = os.path.join(log_dir, "run.log")

# === Log both to console and file ===
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

# === RED TEAM PHASE ===
print("\n=== [Red Team] Generating Attack Logs ===\n")

# Task to pull real attack logs
recon_task = Task(
    description="Load real-world network attack logs from CICIDS2017 dataset (filtered for Friday only).",
    agent=recon_agent,
    expected_output="JSON array of attack logs simulating reconnaissance and infiltration patterns."
)

# exploit_task = Task(
#     description="Load additional logs simulating mid-stage attacks such as brute force and DoS from the dataset.",
#     agent=exploit_injector,
#     expected_output="JSON array of logs representing SSH brute force, DoS Hulk, and other exploit patterns."
# )

red_crew = Crew(
    tasks=[recon_task],
    verbose=True
)
red_output = red_crew.kickoff()

red_log_file = os.path.join(log_dir, "syn_log.txt")
with open(red_log_file, "w") as f:
    f.write(str(red_output))

# === Load Red Team Logs into Blue Team Pipeline ===
print("\n=== [Blue Team] Starting Detection Phase ===\n")

# You can replace this path with your actual dataset or leave as red team output
with open(red_log_file, "r") as f:
    raw_logs = f.read()

# === BLUE TEAM PHASE ===

log_task = Task(
    description=(
        "Parse the following raw logs into structured JSON events:\n\n"
        f"{raw_logs}\n\n"
        "Expected format: JSON list of entries with keys like timestamp, source_ip, dest_ip, event_type, etc."
    ),
    agent=log_monitor,
    expected_output="Parsed and structured logs as JSON array."
)

classify_task = Task(
    description=(
        "Classify the structured logs using MITRE ATT&CK categories. "
        "For each event, return a classification like Initial Access, Execution, Persistence, etc.\n\n"
        "Format: <entry>{\"classification\": \"Execution\", \"confidence\": \"high\"}</entry>"
    ),
    agent=threat_classifier,
    context=[log_task],
    expected_output="A list of threat-tagged logs with MITRE ATT&CK classification."
)

mitigate_task = Task(
    description=(
        "Generate actionable mitigation strategies for each classified event. "
        "Use historical memory to correlate past threats. "
        "Format:\n<entry>{\"mitigation\": \"action plan\", \"event_id\": int}</entry>"
    ),
    agent=response_planner,
    context=[classify_task],
    expected_output="A structured mitigation plan in JSON format."
)

blue_crew = Crew(
    tasks=[log_task, classify_task, mitigate_task],
    verbose=True
)
blue_output = blue_crew.kickoff()

# === Output ===
print("\n=== [FINAL REPORT] Agentic Output ===\n")
print(blue_output)

with open(os.path.join(log_dir, "output.md"), "w") as f:
    f.write(str(blue_output))

end_time = time.time()
print(f"\n✅ Completed in {end_time - start_time:.2f} seconds.")
