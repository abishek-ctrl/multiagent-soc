# batch_executor.py

import json
from crewai import Task, Crew
from agents.blue_team import threat_classifier, response_planner

def split_batches(logs: list, batch_size: int = 40) -> list:
    return [logs[i:i + batch_size] for i in range(0, len(logs), batch_size)]

def run_blue_team_pipeline(batch: list, batch_id: int = 0) -> dict:
    print(f"\n [Batch {batch_id}] Processing {len(batch)} logs")

    classify_task = Task(
        description=(
            "Classify logs into MITRE ATT&CK format.\n"
            "Output:\n"
            "[{\"src_ip\": ..., \"classification\": ..., \"technique_id\": ..., \"technique\": ..., "
            "\"confidence\": ..., \"timestamp\": ..., \"reason\": ...}]\n\n"
            f"Logs:\n{json.dumps(batch)}"
        ),
        agent=threat_classifier,
        expected_output="A JSON list of classified log entries"
    )

    mitigate_task = Task(
        description=(
            "Generate mitigation plan with timestamp per event.\n"
            "Output:\n"
            "[{\"event_id\": ..., \"classification\": ..., \"timestamp\": ..., \"mitigation\": ..., \"source_event\": {...}}, ...]"
        ),
        agent=response_planner,
        context=[classify_task],
        expected_output="Mitigation report"
    )

    crew = Crew(tasks=[classify_task, mitigate_task], verbose=False)
    result = crew.kickoff()

    return {
        "batch_id": batch_id,
        "result": str(result)
    }
