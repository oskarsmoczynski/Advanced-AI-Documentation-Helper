from logging import Logger

from api.routers.v1.ingestion.schemas.request_schemas import IngestRequest

class IngestionService:
    def __init__(self, logger: Logger) -> None:
        self._logger: Logger = logger
        self._prefix: str = self.__class__.__name__

    async def ingest(self, body: IngestRequest):
        return