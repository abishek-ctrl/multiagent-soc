import json
from tools.threat_memory_tool import ThreatMemoryTool

tool = ThreatMemoryTool()

print("\n=== [Threat Memory: STORE TEST] ===\n")

sample_logs = [
  {
    "timestamp": "05:02.3",
    "src_ip": "172.16.0.1",
    "dst_ip": "192.168.10.50",
    "src_port": 49178,
    "dst_port": 80,
    "protocol": 6,
    "event_type": "DDoS",
    "severity": "high"
  },
  {
    "timestamp": "02:41.3",
    "src_ip": "172.16.0.1",
    "dst_ip": "192.168.10.50",
    "src_port": 61664,
    "dst_port": 80,
    "protocol": 6,
    "event_type": "DDoS",
    "severity": "high"
  },
  {
    "timestamp": "16:00.6",
    "src_ip": "172.16.0.1",
    "dst_ip": "192.168.10.50",
    "src_port": 64673,
    "dst_port": 80,
    "protocol": 6,
    "event_type": "DDoS",
    "severity": "high"
  }
]

# STORE mode
store_input = json.dumps(sample_logs)
store_result = tool._run(store_input)
print("Result:\n", store_result)

print("\n=== [Threat Memory: QUERY TEST] ===\n")

# QUERY mode
query_input = "192.168.1.10 brute force"
query_result = tool._run(query_input)
print("Result:\n", query_result)
