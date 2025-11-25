from fastapi import APIRouter, Body, status
from fastapi.responses import Response
from logging import Logger

from api.routers.v1.ingestion.ingestion_service import IngestionService
from api.routers.v1.ingestion.schemas.request_schemas import IngestRequest


class IngestionRouter:
    def __init__(self, logger: Logger) -> None:
        self._logger: Logger = logger
        self._router: APIRouter = APIRouter(prefix="/ingestion", tags=["ingestion"])
        self._service: IngestionService = IngestionService(logger)
        self._prefix: str = self.__class__.__name__
        self.register_routes()

    def register_routes(self) -> None:
        self._logger.info(f"{self._prefix}: Registering routes...")

        self._router.post("/ingest")(self.ingest)

        self._logger.info(f"{self._prefix}: Routes registered")

    async def ingest(self, body: IngestRequest = Body(...)) -> Response:
        await self._service.ingest(body)
        return Response(status_code=status.HTTP_201_CREATED)

    @property
    def router(self) -> APIRouter:
        return self._router
