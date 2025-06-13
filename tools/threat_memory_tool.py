from crewai.tools import BaseTool
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.schema.document import Document
import os
import json

class ThreatMemoryTool(BaseTool):
    name: str = "Threat Memory Lookup Tool"
    description: str = """
        Stores or queries threat memory using vector search. Uses local FAISS + Ollama embedding.

        **INPUT MODES:**
        1. **Store mode:** JSON list of threat logs → stores in memory
        2. **Query mode:** String input like 'brute force from 192.168.1.10'

        **EXAMPLE INPUT (store):**
        '[{"src_ip": "192.168.1.10", "event_type": "Brute Force", "timestamp": "2023-06-01T08:00:00Z"}]'

        **EXAMPLE INPUT (query):**
        'Search similar events for 192.168.1.10'

        **OUTPUT:**
        - JSON list of past matches (with timestamp, src_ip, event_type)

        Respond ONLY with valid JSON. Do NOT output reasoning or commentary.
    """

    def _run(self, query_or_logs: str) -> str:
        try:
            store_path = "data/memory_index"
            embeddings = OllamaEmbeddings(model="all-minilm")

            if os.path.exists(os.path.join(store_path, "index.faiss")):
                vectorstore = FAISS.load_local(
                    store_path,
                    embeddings,
                    allow_dangerous_deserialization=True  #fix
                )
            else:
                dummy_doc = Document(page_content="placeholder", metadata={"note": "placeholder"})
                vectorstore = FAISS.from_documents([dummy_doc], embeddings)


            if query_or_logs.strip().startswith("["):
                logs = json.loads(query_or_logs)
                docs = [
                    Document(
                        page_content=f"{log['src_ip']} {log['event_type']} {log.get('timestamp', '')}",
                        metadata=log
                    )
                    for log in logs
                ]
                vectorstore.add_documents(docs)
                vectorstore.save_local(store_path)
                return f"Stored {len(docs)} logs in memory."

            else:
                results = vectorstore.similarity_search(query_or_logs, k=5)
                return json.dumps([
                    {
                        "src_ip": r.metadata.get("src_ip"),
                        "event_type": r.metadata.get("event_type"),
                        "timestamp": r.metadata.get("timestamp")
                    } for r in results
                ], indent=2)

        except Exception as e:
            return f"Threat memory failed: {e}"
