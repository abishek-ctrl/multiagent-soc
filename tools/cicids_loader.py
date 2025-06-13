from crewai.tools import BaseTool
import pandas as pd
import json
import ipaddress

class CICIDSLogTool(BaseTool):
    name: str = "CICIDS Dataset Log Tool"
    _return_direct = True
    description: str = """
        "Loads logs from the CICIDS2017 dataset (`data/friday_sample.csv`) and filters by attack type.\n\n"
        "**attack_type** options:\n"
        - 'recon' = Port Scan, Infiltration\n"
        - 'exploit' = DoS, BruteForce, Web Attack\n\n"
        "**INPUT:** None required by the agent. The tool auto-filters by internal setting.\n\n"
        "**OUTPUT:** JSON list of logs with keys: timestamp, src_ip, dst_ip, event_type, protocol, severity\n\n"
        "** Return ONLY the JSON list. Do NOT include explanations.**"
    """

    attack_type: str = "recon"  # default value

    def _run(self, _: str = None) -> str:
        try:
            df = pd.read_csv("data\\friday_sample.csv")

            # Convert IP fields to dotted decimal notation
            df["Src IP"] = df["Src IP"].apply(lambda x: str(ipaddress.IPv4Address(int(x))))
            df["Dst IP"] = df["Dst IP"].apply(lambda x: str(ipaddress.IPv4Address(int(x))))

            df = df.replace([float('inf'), float('-inf')], pd.NA).dropna()

            # Filter based on attack_type
            if self.attack_type == "recon":
                df = df[df["Label"].str.contains("PortScan", case=False, na=False)]
            elif self.attack_type == "exploit":
                df = df[df["Label"].str.contains("DDoS", case=False, na=False)]

            logs = []
            for _, row in df.head(50).iterrows():
                logs.append({
                    "timestamp": row["Timestamp"],
                    "src_ip": row["Src IP"],
                    "dst_ip": row["Dst IP"],
                    "src_port": row["Src Port"],
                    "dst_port": row["Dst Port"],
                    "protocol": row["Protocol"],
                    "event_type": row["Label"],
                    "severity": "high" if row["Label"] != "BENIGN" else "low"
                })

            return json.dumps(logs, indent=2)

        except Exception as e:
            return f"Failed to load CICIDS logs: {str(e)}"
