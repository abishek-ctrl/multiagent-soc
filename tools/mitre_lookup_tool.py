# tools/mitre_lookup_tool.py
from crewai.tools import BaseTool
import json

class MITRELookupTool(BaseTool):
    name: str = "MITRE ATT&CK Lookup Tool"
    description: str = (
        "Maps attack terms (e.g., 'brute force', 'infiltration') to MITRE ATT&CK techniques and tactics using offline JSON."
    )

    def _run(self, attack_label: str) -> str:
        try:
            with open("data/enterprise-attack.json", "r") as f:
                data = json.load(f)

            matches = []
            for obj in data["objects"]:
                if obj.get("type") == "attack-pattern":
                    if attack_label.lower() in obj.get("name", "").lower():
                        matches.append({
                            "name": obj.get("name"),
                            "id": obj.get("external_references", [{}])[0].get("external_id"),
                            "description": obj.get("description", "")[:200],
                        })

            return json.dumps(matches if matches else [{"note": "No direct matches found"}], indent=2)
        except Exception as e:
            return f"MITRE lookup failed: {str(e)}"
