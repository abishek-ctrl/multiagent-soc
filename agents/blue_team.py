from crewai import Agent, LLM
# from tools.log_parser import LogParserTool
from tools.mitigation_planner import MitigationPlannerTool
from tools.mitre_lookup_tool import MITRELookupTool
from tools.threat_memory_tool import ThreatMemoryTool
from tools.universal_log_parser import UniversalLogParserTool
import dotenv
import os

dotenv.load_dotenv()

# llm = LLM(
#     model="openrouter/mistralai/devstral-small:free",
#     base_url="https://openrouter.ai/api/v1",
#     api_key=os.getenv("OPENROUTER_API_KEY"),
# )

llm = LLM(
    model="groq/llama-3.1-8b-instant",
    api_key=os.getenv("GROQ_API_KEY"),  # Use the environment variable for the API key
)
# llm = LLM(
#     model="ollama/phi3.5:latest",
#     base_url="http://192.168.1.15:11434",
#     api_key="noonecares"
# )


# log_monitor = Agent(
#     role="Log Monitor",
#     goal="Transform raw log data into clean, structured formats suitable for threat detection. Identify anomalies and malformed entries.",
#     backstory=(
#         "Stationed inside a next-generation Security Operations Center (SOC), this agent is the front-line processor "
#         "for incoming telemetry from across the enterprise. It ingests unstructured logs from firewalls, IDS, servers, "
#         "and endpoint sensors, and converts them into structured JSON formats. Its job is critical for ensuring data "
#         "consistency and accuracy in the threat intelligence pipeline."
#     ),
#     tools=[LogParserTool()],
#     verbose=True
# )

log_monitor = Agent(
    role="Log Monitor",
    goal="Parse various log types into structured formats for downstream threat analysis.",
    backstory="A versatile agent with capability to parse CICIDS datasets, Zeek, Syslog, and Apache logs into clean JSON structures.",
    tools=[UniversalLogParserTool()],
    verbose=True
)


# threat_classifier = Agent(
#     role="Threat Classifier",
#     goal="Contextually analyze structured logs and assign relevant MITRE ATT&CK classifications using reasoning and pattern recognition.",
#     backstory=(
#         "An AI-powered analyst trained on the entire MITRE ATT&CK framework. "
#         "Rather than rely on fixed rules, this agent leverages contextual awareness and pattern interpretation "
#         "to determine adversarial behavior. It understands the subtle indicators of initial access, execution, persistence, "
#         "and other tactics across kill chains. Capable of classifying unknown behaviors with appropriate reasoning."
#     ),
#     llm=llm,
#     verbose=True
# )



threat_classifier = Agent(
    role="Threat Classifier",
    goal="Use MITRE ATT&CK mappings and contextual reasoning to classify cyber events.",
    backstory="Trained on the entire MITRE corpus, this agent matches patterns to known adversarial techniques. It combines structured knowledge with live log insights.",
    llm=llm,
    tools=[MITRELookupTool()],
    verbose=True
)


# response_planner = Agent(
#     role="Mitigation Planner",
#     goal=(
#         "For every detected threat, craft a corresponding mitigation strategy that is both precise and actionable. "
#         "The strategy should include the classification, confidence, and rationale behind the response. "
#         "Final output format: per-event JSON entries tying back to source logs."
#     ),
#     backstory=(
#         "A senior cyber defense strategist with deep experience in blue team operations and incident response. "
#         "This agent knows how to translate adversary behaviors into concrete actions: from isolating compromised hosts "
#         "to hardening authentication systems. Its goal is to minimize dwell time and eradicate threats with minimal impact "
#         "on business continuity."
#     ),
#     tools=[MitigationPlannerTool()],
#     verbose=True,
#     llm=llm
# )
response_planner = Agent(
    role="Mitigation Planner",
    goal=(
        "Correlate current threats with historical patterns. For each detected event, "
        "propose actionable mitigations. Reference memory if similar threats were seen before."
    ),
    backstory="A senior SOC strategist using historical attack memory to suggest evidence-based responses.",
    tools=[MitigationPlannerTool(), ThreatMemoryTool()],
    verbose=True,
    llm=llm
)