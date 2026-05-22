from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class DataChunk(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    chunk_text: str = Field(..., min_length=1)
    chunk_metadata: dict = Field(default_factory=dict)
    chunk_order: int = Field(..., gt=0)
    chunk_project_id: str

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True
    )
