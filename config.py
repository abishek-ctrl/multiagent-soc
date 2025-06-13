from crewai import LLM
import os
import dotenv

# Load environment variables from .env file
dotenv.load_dotenv()

# llm = LLM(
#     model="ollama/phi3.5:latest",
#     base_url="http://localhost:11434",
#     api_key="none"
# )

from crewai import LLM

llm = LLM(
    model="gemini/gemini-2.0-flash-lite",
    temperature=0.7,
)

# llm = LLM(
#     model="groq/llama3-70b-8192",
#     api_key=os.getenv("GROQ_API_KEY"),  # Use the environment variable for the API key
# )

# # Access the API key from environment variables
# openrouter_api_key = os.getenv("OPENROUTER_API_KEY")

# # It's good practice to add a check to ensure the key is loaded
# if not openrouter_api_key:
#     raise ValueError("OPENROUTER_API_KEY not found in environment variables. Please set it in your .env file.")

# llm = LLM(
#     model="mistralai/devstral-small:free",
#     base_url="https://openrouter.ai/api/v1",
#     api_key=openrouter_api_key # Use the variable that holds the environment value
# )


# from langchain.chat_models import ChatOpenAI
# from dotenv import load_dotenv
# import os

# load_dotenv()

# llm = ChatOpenAI(
#     temperature=0.7,
#     openai_api_key=os.getenv("OPENROUTER_API_KEY"),
#     openai_api_base="https://openrouter.ai/api/v1",
#     model="mistralai/devstral-small:free"
# )
# from langchain_ollama import ChatOllama

# llm = ChatOllama(
#     model="qwen2.5-coder:0.5b",
#     temperature=0,
# )