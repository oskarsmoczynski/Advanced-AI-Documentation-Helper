from typing import Protocol
from langchain_core.vectorstores import VectorStore, VectorStoreRetriever


class IVectorStoreFactory(Protocol):
    def get_vector_store(self, name: str) -> VectorStore: ...
    def get_retriever(self, name: str) -> VectorStoreRetriever: ...
