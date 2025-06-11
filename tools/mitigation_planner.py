from crewai.tools import BaseTool
import json

class MitigationPlannerTool(BaseTool):
    name: str = "Detailed Mitigation Planner"
    description: str =(
        "Proposes per-event mitigation strategies based on classification.\n"
        "Input:\n"
        "- JSON string: a list of classified log dictionaries with fields like:\n"
        "  - classification (e.g., Initial Access), confidence, src_ip, dst_ip, timestamp\n\n"
        "Processing:\n"
        "- Maps MITRE-style threat types to actionable response strategies.\n"
        "- Each result links back to the event ID and includes the full source log.\n\n"
        "Output:\n"
        "- JSON list of mitigation entries. Each entry includes:\n"
        "  - event_id (auto-indexed), classification, confidence, mitigation, source_event"
    )

    def _run(self, classified_logs: str) -> str:
        try:
            entries = json.loads(classified_logs)
            mitigations = []

            for idx, log in enumerate(entries):
                classification = log.get("classification", "unknown")
                src_ip = log.get("src_ip", "unknown")
                confidence = log.get("confidence", "unknown")

                mitigation = "Monitor the system for unusual activity."

                if classification == "Initial Access":
                    mitigation = f"Block IP {src_ip} at the perimeter firewall and scan for phishing emails."
                elif classification == "Execution":
                    mitigation = "Restrict script execution and enable command logging."
                elif classification == "Persistence":
                    mitigation = "Audit startup processes and restrict persistence mechanisms."
                elif classification == "Credential Access":
                    mitigation = "Reset passwords and enable MFA for compromised users."
                elif classification == "Lateral Movement":
                    mitigation = "Apply network segmentation and restrict lateral protocols."
                elif classification == "Command and Control":
                    mitigation = "Block known C2 domains and isolate affected endpoints."
                elif classification == "Exfiltration":
                    mitigation = "Monitor outbound data transfers and disable unnecessary uploads."

                mitigations.append({
                    "entry": {
                        "event_id": idx + 1,
                        "classification": classification,
                        "confidence": confidence,
                        "mitigation": mitigation,
                        "source_event": log
                    }
                })

            return json.dumps(mitigations, indent=2)

        except Exception as e:
            return f"Mitigation planning failed: {e}"
