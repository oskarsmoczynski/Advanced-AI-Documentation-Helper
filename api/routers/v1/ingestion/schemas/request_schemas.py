from pydantic import BaseModel, Field


class IngestRequest(BaseModel):
    doc_paths: list[str] = Field(default_factory=list)
    name: str = Field(default="default")
