# tools/threat_memory_tool.py
from crewai.tools import BaseTool
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.schema.document import Document
import os
import json

class ThreatMemoryTool(BaseTool):
    name: str = "Threat Memory Lookup Tool"
    description: str = (
        "Stores and searches past threat log entries using vector similarity over event context."
    )

    def _run(self, query_or_logs: str) -> str:
        try:
            store_path = "data/memory_index"
            embeddings = OllamaEmbeddings(model="all-minilm")

            if os.path.exists(store_path):
                vectorstore = FAISS.load_local(store_path, embeddings)
            else:
                vectorstore = FAISS.from_documents([], embeddings)

            if query_or_logs.strip().startswith("["):
                # It's a batch of new logs
                logs = json.loads(query_or_logs)
                docs = [
                    Document(
                        page_content=f"{log['src_ip']} {log['dst_ip']} {log['event_type']} {log.get('timestamp', '')}",
                        metadata=log
                    )
                    for log in logs
                ]
                vectorstore.add_documents(docs)
                vectorstore.save_local(store_path)
                return f"Stored {len(docs)} logs in vector memory."
            else:
                # It's a query string
                results = vectorstore.similarity_search(query_or_logs, k=5)
                return json.dumps([
                    {"score": r.metadata.get("event_type"), "ip": r.metadata.get("src_ip"), "timestamp": r.metadata.get("timestamp")}
                    for r in results
                ], indent=2)
        except Exception as e:
            return f"Memory tool failed: {e}"
