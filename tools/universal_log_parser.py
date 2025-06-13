from crewai.tools import BaseTool
import json
import os

class UniversalLogParserTool(BaseTool):
    name: str = "Universal Log Parser"
    description: str = """
        Parses raw logs (JSON list, .csv path, or multi-line string) into structured JSON entries.

        **INPUT:**
        - A raw JSON string representing a list of log entries
        - OR a file path to `.csv` or `.log` file (e.g., 'data/friday_sample.csv')

        **EXPECTED LOG ENTRY FIELDS (if JSON):**
        - timestamp, source_ip, dest_ip, src_port, dst_port, protocol, event_type

        **EXAMPLE INPUT (JSON):**
        '[{"timestamp": "2023-01-01T12:00:00Z", "source_ip": "192.168.1.10", "destination_port": 22, "protocol": "TCP"}]'

        **OUTPUT:**
        - A well-formatted JSON list of parsed entries

         Respond ONLY with a valid JSON list. No commentary or explanation.
    """

    def _run(self, logs_or_path: str) -> str:
        try:
            if not isinstance(logs_or_path, str):
                return "Input must be a string (file path or JSON string)."

            if not logs_or_path.strip().startswith("["):
                return "Error: Input must be a JSON array string or path to a CSV/log file."
            
            if os.path.exists(logs_or_path):
                if logs_or_path.endswith(".csv"):
                    return self._parse_csv(logs_or_path)
                with open(logs_or_path, "r") as f:
                    logs_or_path = f.read()

            if logs_or_path.strip().startswith("["):
                logs = json.loads(logs_or_path)
                return json.dumps(logs, indent=2)

            return self._parse_raw_logs(logs_or_path)

        except Exception as e:
            return f"Universal parser failed: {str(e)}"

    def _parse_csv(self, file_path: str) -> str:
        import pandas as pd
        df = pd.read_csv(file_path)
        return df.head(10).to_json(orient="records", indent=2)

    def _parse_raw_logs(self, raw_text: str) -> str:
        lines = raw_text.strip().split("\n")
        logs = [{"raw_line": l} for l in lines if l.strip()]
        return json.dumps(logs, indent=2)