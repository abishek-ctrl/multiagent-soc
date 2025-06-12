# tools/universal_log_parser.py
from crewai.tools import BaseTool
import json
import pandas as pd
import re

class UniversalLogParserTool(BaseTool):
    name: str = "Universal Log Parser"
    description: str = (
        "Parses various raw log formats (CICIDS CSV, Zeek, Syslog, Apache). "
        "Auto-detects structure and outputs unified structured JSON logs."
    )

    def _run(self, logs_or_path: str) -> str:
        if logs_or_path.endswith(".csv"):
            return self._parse_csv(logs_or_path)
        else:
            return self._parse_raw_logs(logs_or_path)

    def _parse_csv(self, file_path: str) -> str:
        logs = []
        try:
            chunks = pd.read_csv(file_path, usecols=[
                "Timestamp", "Src IP", "Dst IP", "Src Port", "Dst Port",
                "Protocol", "Flow Duration", "Total Fwd Packet",
                "Total Bwd packets", "Total Length of Fwd Packet", "Label"
            ], chunksize=1000)

            for chunk in chunks:
                chunk = chunk.replace([float('inf'), float('-inf')], pd.NA).dropna()
                for _, row in chunk.iterrows():
                    if row["Label"] == "BENIGN":
                        continue
                    logs.append({
                        "timestamp": row["Timestamp"],
                        "src_ip": row["Src IP"],
                        "dst_ip": row["Dst IP"],
                        "src_port": row["Src Port"],
                        "dst_port": row["Dst Port"],
                        "protocol": row["Protocol"],
                        "event_type": row["Label"],
                        "flow_duration": row["Flow Duration"],
                        "packet_count": int(row["Total Fwd Packet"] + row["Total Bwd packets"]),
                        "total_length": row["Total Length of Fwd Packet"],
                        "severity": "high"
                    })
                    if len(logs) >= 50:
                        break  # quick batch simulation
                if len(logs) >= 50:
                    break
        except Exception as e:
            return json.dumps({"error": str(e)})

        return json.dumps(logs, indent=2)

    def _parse_raw_logs(self, raw_text: str) -> str:
        logs = []
        for line in raw_text.strip().split('\n'):
            line = line.strip()
            if not line:
                continue
            try:
                # Zeek
                if '\t' in line:
                    fields = line.split('\t')
                    logs.append({
                        "timestamp": fields[0],
                        "src_ip": fields[2],
                        "dst_ip": fields[4],
                        "protocol": fields[6],
                        "event_type": "zeek_connection",
                        "severity": "medium"
                    })
                # Apache
                elif re.match(r'^\d+\.\d+\.\d+\.\d+', line) and "GET" in line:
                    logs.append({
                        "timestamp": line.split()[3][1:],  # remove [ from date
                        "src_ip": line.split()[0],
                        "event_type": "http_request",
                        "severity": "low"
                    })
                # Syslog
                elif re.match(r'^\w{3} \d{1,2} ', line):
                    logs.append({
                        "timestamp": line[:15],
                        "event_type": "syslog_event",
                        "message": line[16:],
                        "severity": "low"
                    })
                # JSON line
                else:
                    logs.append(json.loads(line))
            except Exception as e:
                logs.append({
                    "parse_error": str(e),
                    "raw_line": line
                })
        return json.dumps(logs, indent=2)
