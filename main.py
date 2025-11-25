from dotenv import load_dotenv
from logging import getLogger, DEBUG, StreamHandler
from time import time
from contextlib import contextmanager

from vector_store.ingestion import Ingestion
from vector_store.retriever import Retriever
from vector_store.chroma_vector_store_factory import ChromaVectorStoreFactory
from api.server import APIServer


logger = getLogger("docs-helper")
logger.setLevel(DEBUG)
logger.addHandler(StreamHandler())


def main():
    stime = time()
    ingestion, retriever = init()
    logger.info(f"Initialization completed in {round(time() - stime, 2)} seconds")


def init() -> tuple[Ingestion, Retriever]:
    logger.info("---------- Initialization ----------")

    with log_step("Loading environment variables"):
        load_dotenv()

    with log_step("Starting API server"):
        server = APIServer(logger, autostart=True)

    with log_step("Initializing Chroma vector store factory"):
        factory = ChromaVectorStoreFactory(logger)

    with log_step("Initializing ingestion"):
        ingestion = Ingestion(logger, factory)

    with log_step("Initializing retriever"):
        retriever = Retriever(logger, factory)

    return ingestion, retriever


@contextmanager
def log_step(message: str):
    """Context manager that logs a start message and appends 'Done' on completion."""
    logger.info(f"{message}...")
    try:
        yield
        logger.info(f"{message}... Done")
    except Exception as e:
        logger.error(f"{message}... Failed: {e}")
        raise


if __name__ == "__main__":
    main()
