from pydantic import BaseModel, Field
from pathlib import Path


class IngestionData(BaseModel):
    doc_paths: list[Path] = Field(default_factory=list)
    name: str = Field(default="default")
