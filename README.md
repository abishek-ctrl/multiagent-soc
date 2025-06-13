# 🧠 multiagent-soc
### Autonomous Multi-Agent Security Operations Center Simulation (Red Team vs Blue Team)

This project simulates a simplified version of the Red Team vs. Blue Team operation using autonomous agents, powered by LLMs, to process, classify, and respond to cyber threats from real-world logs. Built using the CrewAI framework, it emulates how a Security Operations Center (SOC) could operate with agentic intelligence and threat memory.

## ⚙️ Project Structure
```
multiagent-soc/
├── main.py              # Entry point: launches Red & Blue team pipelines
├── agents/              # Role definitions for autonomous red/blue team agents
├── tools/               # Tools for parsing logs, threat memory, mitigation, etc.
├── data/                # Contains CICIDS logs and MITRE ATT&CK JSON
├── batch_executor.py    # Enables log batching and distributed processing
├── output/              # Timestamped log runs
└── README.md            # You're here
```

## 🔁 Workflow Overview

1. 🟥 **Red Team Phase (Simulated Attacker)**
   - **Recon Agent:** Loads simulated PortScan logs from the CICIDS2017 dataset
   - **Exploit Injector Agent:** Loads DDoS/BruteForce logs from the same dataset
   - Both agents use the CICIDS Dataset Log Tool and output realistic logs in structured format.

2. 🟦 **Blue Team Phase (Autonomous Defense)**
   - **Threat Classifier:** Analyzes logs using LLMs and classifies threat types like "Privilege Escalation", "Initial Access", etc.
   - **Mitigation Planner:** Crafts actionable responses per threat (e.g., block IP, reset credentials), and stores/checks memory with a FAISS vector DB
   - All logs are processed in batches of 40 for performance, reducing latency and hallucination.

## 🧪 Real-World Simulation Features
| Component         | Description                                                      |
|-------------------|------------------------------------------------------------------|
| ✅ Log Batching   | Improves speed and avoids LLM overflow (40–45 logs per crew execution) |
| ✅ FAISS Memory   | Stores past threats, enables proactive mitigation pattern search  |
| ✅ Tool Isolation | Agents use tools directly; no hallucinated outputs from LLMs     |
| ✅ CICIDS Dataset | Real network flows, filtered per attack type                     |
| ✅ LLM-Driven     | All reasoning/classification uses Ollama + all-minilm embeddings |

## ⏱️ Performance Comparison (100 Samples)
| Mode    | Duration (s) | Accuracy Notes                        |
|---------|--------------|---------------------------------------|
| 🧠 Normal | 167.70       | Missed ~10 logs due to token loss      |
| ⚡ Batched| 149.55       | All logs processed with memory        |

Log batching provided ~11% performance gain and reduced LLM failure edge cases.

## 🚀 How to Run

### 🔧 Install dependencies:
```bash
pip install -r requirements.txt
```

### 📁 Ensure:
- CICIDS dataset is placed in `data/friday.csv`
### ▶ Run the main entry point:
```bash
python main.py
```

## 🛠 Customization
- Add more Red Team agents: Command & Control, Persistence, Exfiltration
- Add Blue Team logic: Alert Prioritizer, Incident Reporter
- Extend batching logic in `batch_executor.py`
- Swap embeddings (currently using OllamaEmbeddings + FAISS)
- Replace file-based logs with Kafka or socket streaming

## 📈 Roadmap
- 🌐 Web UI for real-time monitoring of agent decisions and logs
- 📦 Dockerized multi-agent deployment
- 🧩 Integration with Zeek/NIDS for live packet streams
- 📊 Automatic markdown + PDF incident reports

## 📚 References
- [CICIDS2017 Dataset](https://www.unb.ca/cic/datasets/malmem-2022.html)
- [CrewAI Framework](https://github.com/joaomdmoura/crewAI)
- [LangChain FAISS & Embeddings](https://python.langchain.com/docs/integrations/vectorstores/faiss)
