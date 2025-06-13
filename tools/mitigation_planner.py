from crewai.tools import BaseTool
import json

class MitigationPlannerTool(BaseTool):
    name: str = "Detailed Mitigation Planner"
    description: str = (
        "Generates per-event mitigation strategies based on MITRE-style classification.\n\n"
        "**INPUT:**\n"
        "- JSON string: List of log entries with fields: classification, confidence, src_ip, timestamp, etc.\n\n"
        "**PROCESS:**\n"
        "- Maps classifications to concrete remediation actions.\n\n"
        "**OUTPUT:**\n"
        "- JSON list: Each item contains event_id, classification, mitigation, timestamp, and full source_event\n\n"
        "**EXAMPLE:**\n"
        "[{\"event_id\": 1, \"classification\": \"Credential Access\", \"mitigation\": \"Reset passwords...\", \"timestamp\": \"08:01:00\", \"source_event\": {...}}]"
    )

    def _run(self, classified_logs: str) -> str:
        try:
            entries = json.loads(classified_logs)
            mitigations = []

            for idx, log in enumerate(entries):
                classification = log.get("classification", "unknown")
                src_ip = log.get("src_ip", "unknown")
                confidence = log.get("confidence", "unknown")
                timestamp = log.get("timestamp", "unknown")

                mitigation = "Monitor the system for unusual activity."

                mapping = {
                    "Initial Access": f"Block IP {src_ip} at the perimeter and scan for phishing or malware delivery.",
                    "Execution": "Restrict script execution and enforce command logging.",
                    "Persistence": "Harden startup processes and remove persistence mechanisms.",
                    "Privilege Escalation": "Patch local exploits and audit admin privilege use.",
                    "Credential Access": "Reset affected user passwords and enforce MFA.",
                    "Discovery": "Throttle reconnaissance tools and limit endpoint enumeration.",
                    "Lateral Movement": "Enable network segmentation and isolate east-west traffic.",
                    "Collection": "Limit access to sensitive data folders and monitor clipboard/USB.",
                    "Command and Control": "Block outbound C2 domains and monitor DNS anomalies.",
                    "Exfiltration": "Monitor large outbound transfers and disable unnecessary protocols.",
                    "Impact": "Verify backups, implement anti-DDoS measures, and disable destructive tools."
                }

                mitigation = mapping.get(classification, mitigation)

                mitigations.append({
                    "event_id": idx + 1,
                    "classification": classification,
                    "confidence": confidence,
                    "timestamp": timestamp,
                    "mitigation": mitigation,
                    "source_event": log
                })

            return json.dumps(mitigations, indent=2)

        except Exception as e:
            return f"Mitigation planning failed: {e}"
