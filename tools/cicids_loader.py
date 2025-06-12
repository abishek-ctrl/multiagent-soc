# tools/cicids_loader.py
from crewai.tools import BaseTool
import json

class CICIDSLogTool(BaseTool):
    name: str = "CICIDS Dataset Log Tool"
    description: str = (
        "Loads real attack logs from CICIDS2017 dataset (JSON format). "
        "Outputs attack flows as JSON logs."
    )

    def _run(self, _: str = None) -> str:
        # Load the preprocessed JSON file with attack logs
        with open("data/friday_sample.json", "r") as f:
            logs = json.load(f)

        # Optionally limit number of logs returned to prevent endless output
        limit = 10
        limited_logs = logs[:limit]

        return json.dumps(limited_logs, indent=2)
