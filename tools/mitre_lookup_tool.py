from crewai.tools import BaseTool
import json

class MITRELookupTool(BaseTool):
    name: str = "MITRE ATT&CK Lookup Tool"
    description: str = """
        Maps attack labels to MITRE ATT&CK techniques from enterprise-attack.json.

        **INPUT:**
        - A string representing an attack label (e.g., 'Brute Force', 'Port Scan')

        **OUTPUT:**
        - JSON list of matched ATT&CK techniques

        **EXAMPLE INPUT:**
        'Brute Force'

        **EXAMPLE OUTPUT:**
        '[{"name": "Brute Force", "id": "T1110", "description": "..."}]'

         Respond ONLY with a JSON list of mappings. No explanation.
    """

    def _run(self, attack_label: str) -> str:
        try:
            with open("data/enterprise-attack.json", "r") as f:
                data = json.load(f)
            results = []
            for obj in data["objects"]:
                if obj.get("type") == "attack-pattern" and attack_label.lower() in obj.get("name", "").lower():
                    results.append({
                        "name": obj.get("name"),
                        "id": obj.get("external_references", [{}])[0].get("external_id"),
                        "description": obj.get("description", "")[:200]
                    })
            return json.dumps(results or [{"note": "No matches"}], indent=2)
        except Exception as e:
            return f"MITRE lookup failed: {str(e)}"