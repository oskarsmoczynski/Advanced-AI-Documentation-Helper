from logging import Logger

from langchain_core.vectorstores import VectorStoreRetriever

from vector_store.interfaces.vector_store_factory import IVectorStoreFactory


class Retriever:
    def __init__(self, logger: Logger, factory: IVectorStoreFactory) -> None:
        self._factory = factory
        self._logger = logger

    def invoke(self, name: str, prompt: str):
        retriever = self._get_retriever(name)
        return retriever.invoke(prompt)

    def _get_retriever(self, name: str) -> VectorStoreRetriever:
        return self._factory.get_retriever(name)
