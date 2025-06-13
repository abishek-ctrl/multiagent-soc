import os
import dotenv
import time
from datetime import datetime
import json
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from crewai import Task, Crew
from agents.blue_team import threat_classifier, response_planner
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

print("\n=== [Red Team] Generating Logs ===\n")

recon_task = Task(
    description=(
        "You MUST use your tool, and return ONLY the tool output."
        "DO NOT generate any commentary."
        "DO NOT wrap anything in Final Answer or markdown."
        "Respond with JSON list ONLY. No other format will be accepted."
    ),
    agent=recon_agent,
    expected_output="JSON array of logs",
)


exploit_task = Task(
    description=(
        "You MUST use your tool, and return ONLY the tool output."
        "DO NOT generate any commentary."
        "DO NOT wrap anything in Final Answer or markdown."
        "Respond with JSON list ONLY. No other format will be accepted."
    ),
    agent=exploit_injector,
    expected_output="JSON array of logs",
)

red_crew = Crew(tasks=[recon_task, exploit_task], verbose=True)
red_output = red_crew.kickoff()

# === Combine both red agent outputs ===
def extract_logs(output_str):
    try:
        return json.loads(str(output_str))
    except:
        return []

all_red_logs = []
for entry in str(red_output).split("```json"):
    if "]" in entry:
        try:
            logs = json.loads(entry.split("```")[0].strip())
            if isinstance(logs, list):
                all_red_logs.extend(logs)
        except:
            continue

print(f"\n Total Red Logs Collected: {len(all_red_logs)}")

red_log_file = os.path.join(log_dir, "syn_log.json")
with open(red_log_file, "w") as f:
    json.dump(all_red_logs, f, indent=2)

# === Blue Team Tasks ===
print("\n=== [Blue Team] Threat Classification & Mitigation ===\n")

classify_task = Task(
    description=(
        "Classify each log below using MITRE ATT&CK tactics and techniques.\n"
        "Return format:\n"
        "[\n"
        "  {\"src_ip\": \"...\", \"classification\": \"...\", \"technique_id\": \"...\", \"technique\": \"...\", \"confidence\": \"high\", \"reason\": \"...\"},\n"
        "  ...\n"
        "]\n\n"
        "Input logs:\n\n"
        f"{json.dumps(all_red_logs)}"
    ),
    agent=threat_classifier,
    expected_output="A JSON list of MITRE-classified logs"
)

mitigate_task = Task(
    description=(
        "Generate mitigation plans based on the classified threat logs.\n"
        "Return format:\n"
        "[{\"event_id\": 1, \"classification\": \"...\", \"mitigation\": \"...\", \"source_event\": {...}}, ...]"
    ),
    agent=response_planner,
    context=[classify_task],
    expected_output="A JSON list of mitigation entries"
)

blue_crew = Crew(tasks=[classify_task, mitigate_task], verbose=True)
blue_output = blue_crew.kickoff()

# === Save Blue Output ===
print("\n=== [FINAL BLUE OUTPUT] ===\n")
print(blue_output)

with open(os.path.join(log_dir, "blue_output.json"), "w") as f:
    f.write(str(blue_output))

end_time = time.time()
print(f"\n Execution completed in {end_time - start_time:.2f} seconds.")