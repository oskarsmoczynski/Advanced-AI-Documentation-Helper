from fastapi import FastAPI
from logging import Logger
from uvicorn import run
from threading import Thread

from api.routers.v1.ingestion.ingestion_router import IngestionRouter

class APIServer:
    def __init__(self, logger: Logger, host: str = "127.0.0.1", port: int = 8000, autostart: bool = True) -> None:
        self._logger: Logger = logger
        self._app: FastAPI = FastAPI()
        self._host: str = host
        self._port: int = port
        self._thread: Thread = Thread(target=self.start_server, name="FastAPI Server")
        self.register_routers()

        if autostart:
            self.run_in_thread()

    def run_in_thread(self) -> None:
        try:
            self._thread.start()
        except Exception as e:
            self._logger.error(f"Error starting server: {e}")
            raise e

    def register_routers(self) -> None:
        self._app.include_router(IngestionRouter(self._logger).router, prefix="/v1")

    def start_server(self) -> None:
        run(self._app, host=self._host, port=self._port)
