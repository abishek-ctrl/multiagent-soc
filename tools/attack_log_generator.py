from crewai.tools import BaseTool
import random
import json
from datetime import datetime, timedelta

class AttackLogGeneratorTool(BaseTool):
    name: str = "Attack Log Generator"
    description: str =(
        "Generates simulated attack logs based on specific attack types.\n"
        "Use this tool to emulate offensive behavior such as recon or exploit steps.\n"
        "Input:\n"
        "- None (configured via internal attack_type).\n"
        "Output:\n"
        "- JSON string: list of generated synthetic log entries mimicking real attacks.\n"
        "Each log has fields: timestamp, src_ip, dst_ip, event_type, protocol, severity."
    )

    attack_type: str = "recon"  # default

    def _run(self, _: str = None) -> str:
        now = datetime.utcnow()
        logs = []

        if self.attack_type == "recon":
            for i in range(3):
                logs.append({
                    "timestamp": (now + timedelta(seconds=i)).isoformat() + "Z",
                    "src_ip": f"192.168.1.{random.randint(2, 254)}",
                    "dst_ip": "10.0.0.5",
                    "src_port": random.randint(1024, 65535),
                    "dst_port": 22,
                    "protocol": "tcp",
                    "event_type": "port_scan",
                    "sensor": "honeypot",
                    "severity": "medium"
                })

        elif self.attack_type == "exploit":
            for i in range(2):
                logs.append({
                    "timestamp": (now + timedelta(seconds=i)).isoformat() + "Z",
                    "src_ip": f"203.0.113.{random.randint(10, 200)}",
                    "dst_ip": "10.0.0.8",
                    "src_port": random.randint(1024, 65535),
                    "dst_port": 445,
                    "protocol": "tcp",
                    "event_type": "exploit_attempt",
                    "exploit": "EternalBlue",
                    "sensor": "IDS",
                    "severity": "high"
                })

        return json.dumps(logs, indent=2)
