import pandas as pd
import json

df = pd.read_csv("data/friday.csv", usecols=["Timestamp", "Src IP dec", "Dst IP dec", "Src Port", "Dst Port",
                                             "Protocol", "Flow Duration", "Total Fwd Packet", 
                                             "Total Bwd packets", "Total Length of Fwd Packet", "Label"])

df = df[df['Label'] != 'BENIGN']
df = df.replace([float('inf'), float('-inf')], pd.NA).dropna()
df = df.head(100)

logs = []
for _, row in df.iterrows():
    logs.append({
        "timestamp": row["Timestamp"],
        "src_ip": row["Src IP dec"],
        "dst_ip": row["Dst IP dec"],
        "src_port": row["Src Port"],
        "dst_port": row["Dst Port"],
        "protocol": row["Protocol"],
        "event_type": row["Label"],
        "flow_duration": row["Flow Duration"],
        "packet_count": int(row["Total Fwd Packet"] + row["Total Bwd packets"]),
        "total_length": row["Total Length of Fwd Packet"],
        "severity": "high"
    })

with open("data/friday_sample.json", "w") as f:
    json.dump(logs, f, indent=2)
