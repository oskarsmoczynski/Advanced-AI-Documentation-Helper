from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from pathlib import Path
from logging import Logger

from vector_store.interfaces.vector_store_factory import IVectorStoreFactory
from common.custom_types import IngestionData


class Ingestion:
    def __init__(self, logger: Logger, factory: IVectorStoreFactory):
        self._factory = factory
        self._text_splitter = RecursiveCharacterTextSplitter(chunk_size=750, chunk_overlap=100)
        self._logger = logger

    def ingest(self, data: IngestionData) -> None:
        if not data.doc_paths:
            self._logger.warning("No documents provided for ingestion")
            return

        if not data.name:
            raise ValueError("Store name is required for ingestion")

        self._logger.info(f"Ingesting {len(data.doc_paths)} documents into store '{data.name}'")

        doc_splits = self._get_doc_splits(data.doc_paths)
        self._logger.info(f"Split documents into {len(doc_splits)} chunks")

        vstore = self._factory.get_vector_store(data.name)
        vstore.add_documents(doc_splits)

        self._logger.info(f"Successfully ingested documents into store '{data.name}'")

    def _get_doc_splits(self, doc_paths: list[Path]) -> list[Document]:
        all_docs = []

        for doc_path in doc_paths:
            if not doc_path.exists():
                self._logger.warning(f"Document not found: {doc_path}")
                continue

            try:
                self._logger.debug(f"Loading document: {doc_path}")
                docs = PyPDFLoader(str(doc_path)).load()
                all_docs.extend(docs)
            except Exception as e:
                self._logger.error(f"Error loading document {doc_path}: {e}")
                continue

        doc_splits = self._text_splitter.split_documents(all_docs)
        return doc_splits
