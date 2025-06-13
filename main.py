# main.py

import os
import dotenv
import time
from datetime import datetime
import json
import sys
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from crewai import Task, Crew
from agents.blue_team import log_monitor, threat_classifier, response_planner
from agents.red_team import recon_agent, exploit_injector

dotenv.load_dotenv()
start_time = time.time()

# === Output setup ===
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
log_dir = f"output/test_{timestamp}"
os.makedirs(log_dir, exist_ok=True)
log_path = os.path.join(log_dir, "run.log")

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

# === RED TEAM ===
print("\n=== [Red Team] Generating Attack Logs ===\n")

recon_task = Task(
    description=(
        "Call your tool (CICIDS Dataset Log Tool) and return its output ONLY"
        "You MUST call the tool and return ONLY tool_output as-is. DO NOT explain. DO NOT generate Final Answer.\n\n"
        "**Return ONLY the JSON list of logs. No thoughts. No formatting.**"
    ),
    agent=recon_agent,
    expected_output="JSON array of logs",
)


exploit_task = Task(
    description=(
        "Call your tool (CICIDS Dataset Log Tool) and return output ONLY. "
        "You MUST call the tool and return the tool_output as-is. DO NOT explain. DO NOT generate Final Answer.\n\n"
        "**Return ONLY the JSON list. No thoughts. No formatting.**"
    ),
    agent=exploit_injector,
    expected_output="JSON array of logs",
)

red_crew = Crew(
    tasks=[recon_task, exploit_task],
    verbose=True
)

red_output = red_crew.kickoff()
red_result = str(red_output)


# === Validate Red Output ===
try:
    red_logs = json.loads(red_result)
    assert isinstance(red_logs, list)
except Exception as e:
    print(" Red Team output is not valid JSON list:", e)
    print("Raw Output:\n", red_result)
    exit(1)

# Save red logs
red_log_file = os.path.join(log_dir, "syn_log.json")
with open(red_log_file, "w") as f:
    json.dump(red_logs, f, indent=2)

# === BLUE TEAM ===
print("\n=== [Blue Team] Starting Detection Phase ===\n")

log_task = Task(
    description=(
        "Parse the following JSON array of raw logs into structured entries using the Universal Log Parser tool.\n"
        "Do not explain or summarize. **Return ONLY the JSON list.**\n\n"
        f"{json.dumps(red_logs)}"
    ),
    agent=log_monitor,
    expected_output="A list of structured JSON logs."
)

classify_task = Task(
    description=(
        "Use the MITRE Lookup Tool to classify each structured log entry.\n"
        "Map each attack label (e.g., DoS, BruteForce) to MITRE tactics.\n"
        "**Respond ONLY with a JSON list of classification results.**"
    ),
    agent=threat_classifier,
    context=[log_task],
    expected_output="JSON list of classification entries per log"
)

mitigate_task = Task(
    description=(
        "Generate a mitigation plan for each classified threat.\n"
        "Use the Threat Memory Tool to detect repeated attack patterns.\n"
        "**Respond ONLY with a JSON list of {\"event_id\": int, \"mitigation\": str}.**"
    ),
    agent=response_planner,
    context=[classify_task],
    expected_output="JSON list of mitigation plans"
)

blue_crew = Crew(
    tasks=[log_task, classify_task, mitigate_task],
    verbose=True
)

blue_output = blue_crew.kickoff()

# === Save Blue Output ===
print("\n=== [FINAL OUTPUT] ===\n")
print(blue_output)

with open(os.path.join(log_dir, "output.md"), "w") as f:
    f.write(str(blue_output))

end_time = time.time()
print(f"\n Execution completed in {end_time - start_time:.2f} seconds.")
