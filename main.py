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

# === RED TEAM CREWS ===
print("\n=== [Red Team - Recon Phase] ===\n")
recon_task = Task(
    description="Call your CICIDS Dataset Log Tool and return only the tool's JSON output. No commentary.",
    agent=recon_agent,
    expected_output="A JSON list of reconnaissance logs"
)
recon_crew = Crew(tasks=[recon_task], verbose=True)
recon_output = recon_crew.kickoff()

print("\n=== [Red Team - Exploit Phase] ===\n")
exploit_task = Task(
    description="Call your CICIDS Dataset Log Tool and return only the tool's JSON output. No commentary.",
    agent=exploit_injector,
    expected_output="A JSON list of exploit logs"
)
exploit_crew = Crew(tasks=[exploit_task], verbose=True)
exploit_output = exploit_crew.kickoff()

# === Combine all red logs ===
def extract_json_lists(text):
    try:
        blocks = text.split("```json")
        logs = []
        for block in blocks:
            if "]" in block:
                try:
                    data = json.loads(block.split("```")[0].strip())
                    if isinstance(data, list):
                        logs.extend(data)
                except:
                    continue
        return logs
    except Exception as e:
        print(" Log extraction failed:", e)
        return []

all_red_logs = extract_json_lists(str(recon_output)) + extract_json_lists(str(exploit_output))
print(f"\n Total Red Logs Collected: {len(all_red_logs)}")

with open(os.path.join(log_dir, "syn_log.json"), "w") as f:
    json.dump(all_red_logs, f, indent=2)

# === BLUE TEAM CREW ===
print("\n=== [Blue Team - Classification & Mitigation] ===\n")

# === BLUE TEAM ===
from batch_executor import split_batches, run_blue_team_pipeline
from concurrent.futures import ThreadPoolExecutor, as_completed

# === SPLIT RED LOGS INTO BATCHES ===
batches = split_batches(all_red_logs, batch_size=40)
final_mitigations = []

print(f"\n Launching Blue Team on {len(batches)} batches...\n")

# === RUN IN PARALLEL ===
with ThreadPoolExecutor(max_workers=3) as executor:
    futures = {executor.submit(run_blue_team_pipeline, batch, idx): idx for idx, batch in enumerate(batches)}

    for future in as_completed(futures):
        batch_id = futures[future]
        try:
            output = future.result()
            print(f"Batch {batch_id} completed")
            final_mitigations.append(output)
        except Exception as e:
            print(f"Batch {batch_id} failed: {e}")

with open(os.path.join(log_dir, "blue_output.json"), "w") as f:
    json.dump(final_mitigations, f, indent=2)

print("\n All Blue Team batches complete. Output written.")
end_time = time.time()
print(f"\n Execution completed in {end_time - start_time:.2f} seconds.")
