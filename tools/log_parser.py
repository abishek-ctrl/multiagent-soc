from crewai.tools import BaseTool
import json

class LogParserTool(BaseTool):
    name: str = "Log Parser"
    description: str = """Parses raw log text into a structured JSON list.

     Input: Raw multiline string of logs (e.g., Zeek/Syslog/Firewall logs).
     Output: JSON-formatted string list of dicts with fields like:
      - timestamp
      - src_ip
      - dst_ip
      - src_port
      - dst_port
      - protocol
      - event_type
      - sensor
      - severity
      - any protocol-specific fields (e.g., http_uri, username)
    
     Example Output:
    [
      {
        "timestamp": "...",
        "src_ip": "10.0.0.1",
        "dst_ip": "203.0.113.2",
        "event_type": "connection_attempt",
        ...
      }
    ]"""

    def _run(self, logs: str) -> str:
        parsed_logs = []
        for line_number, line in enumerate(logs.strip().split('\n'), start=1):
            if not line.strip():
                continue
            try:
                log = json.loads(line)
                parsed_logs.append(log)
            except json.JSONDecodeError as e:
                parsed_logs.append({
                    "parse_error": str(e),
                    "line_number": line_number,
                    "raw_line": line
                })

        # Batch logs (5 per batch)
        batch_size = 5
        batches = [
            parsed_logs[i:i + batch_size]
            for i in range(0, len(parsed_logs), batch_size)
        ]

        # Format output with metadata
        batched_output = {
            "total_logs": len(parsed_logs),
            "total_batches": len(batches),
            "batches": [
                {
                    "batch_id": idx + 1,
                    "log_count": len(batch),
                    "entries": batch
                }
                for idx, batch in enumerate(batches)
            ]
        }

        return json.dumps(batched_output, indent=2)
