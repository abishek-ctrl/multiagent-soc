# Autonomous Multi-Agent Threat Intelligence System

This project simulates a Red Team vs. Blue Team scenario using autonomous agents to generate, classify, and mitigate cyber threats based on real-world datasets and the MITRE ATT&CK framework.

## Project Structure

- `main.py` — Entry point; orchestrates the Red/Blue team workflow.
- `agents/` — Contains agent definitions for both teams.
- `tools/` — Custom tools for log loading, threat memory, mitigation planning, etc.
- `data/` — Datasets (e.g., CICIDS2017, MITRE ATT&CK).
- `scripts/` — Utility scripts for data processing.

## Workflow

1. **Red Team Phase**
   - *Reconnaissance Agent*: Loads and outputs reconnaissance attack logs from the dataset.
   - *Exploit Injector Agent*: Loads and outputs exploit attack logs.

2. **Blue Team Phase**
   - *Threat Classifier*: Analyzes logs and classifies threats using the MITRE ATT&CK framework.
   - *Mitigation Planner*: Generates actionable mitigation plans for each classified threat, referencing past incidents via the Threat Memory Tool.

3. **Logging**
   - All actions and results are logged to a timestamped file in the `output/` directory.

## How to Run

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
2. Ensure datasets are present in the `data/` directory.
3. Run the main workflow:
   ```
   python main.py
   ```

## Customization

- Modify agent logic in `agents/`.
- Add or update tools in `tools/`.
- Update datasets in `data/`.

## References

- [MITRE ATT&CK](https://attack.mitre.org/)
- [CICIDS2017 Dataset](https://www.unb.ca/cic/datasets/malmem-2022.html)
