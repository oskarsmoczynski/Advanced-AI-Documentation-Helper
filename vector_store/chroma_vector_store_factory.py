from logging import Logger

from langchain_core.vectorstores import VectorStoreRetriever
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma


class ChromaVectorStoreFactory:
    def __init__(self, logger: Logger):
        self._logger = logger
        self._embeddings = OpenAIEmbeddings()

    def get_vector_store(self, name: str) -> Chroma:
        return Chroma(
            embedding_function=self._embeddings,
            persist_directory=f"./vector_store/db/{name}",
            collection_name=name,
        )

    def get_retriever(self, name: str) -> VectorStoreRetriever:
        return self.get_vector_store(name).as_retriever()
