from crewai import Agent, LLM
from tools.log_parser import LogParserTool
from tools.mitigation_planner import MitigationPlannerTool
import dotenv
import os

dotenv.load_dotenv()

# llm = LLM(
#     model="openrouter/mistralai/devstral-small:free",
#     base_url="https://openrouter.ai/api/v1",
#     api_key=os.getenv("OPENROUTER_API_KEY"),
# )

# llm = LLM(
#     model="groq/qwen-qwq-32b",
#     api_key=os.getenv("GROQ_API_KEY"),  # Use the environment variable for the API key
# )
llm = LLM(
    model="ollama/phi3.5:latest",
    base_url="http://192.168.1.15:11434",
    api_key="noonecares"
)


log_monitor = Agent(
    role="Log Monitor",
    goal="Transform raw log data into clean, structured formats suitable for threat detection. Identify anomalies and malformed entries.",
    backstory=(
        "Stationed inside a next-generation Security Operations Center (SOC), this agent is the front-line processor "
        "for incoming telemetry from across the enterprise. It ingests unstructured logs from firewalls, IDS, servers, "
        "and endpoint sensors, and converts them into structured JSON formats. Its job is critical for ensuring data "
        "consistency and accuracy in the threat intelligence pipeline."
    ),
    tools=[LogParserTool()],
    verbose=True
)

threat_classifier = Agent(
    role="Threat Classifier",
    goal="Contextually analyze structured logs and assign relevant MITRE ATT&CK classifications using reasoning and pattern recognition.",
    backstory=(
        "An AI-powered analyst trained on the entire MITRE ATT&CK framework. "
        "Rather than rely on fixed rules, this agent leverages contextual awareness and pattern interpretation "
        "to determine adversarial behavior. It understands the subtle indicators of initial access, execution, persistence, "
        "and other tactics across kill chains. Capable of classifying unknown behaviors with appropriate reasoning."
    ),
    llm=llm,
    verbose=True
)

response_planner = Agent(
    role="Mitigation Planner",
    goal=(
        "For every detected threat, craft a corresponding mitigation strategy that is both precise and actionable. "
        "The strategy should include the classification, confidence, and rationale behind the response. "
        "Final output format: per-event JSON entries tying back to source logs."
    ),
    backstory=(
        "A senior cyber defense strategist with deep experience in blue team operations and incident response. "
        "This agent knows how to translate adversary behaviors into concrete actions: from isolating compromised hosts "
        "to hardening authentication systems. Its goal is to minimize dwell time and eradicate threats with minimal impact "
        "on business continuity."
    ),
    tools=[MitigationPlannerTool()],
    verbose=True,
    llm=llm
)
