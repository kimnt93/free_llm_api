from pydantic import BaseModel
from typing import List


class EmbeddingsRequest(BaseModel):
    model: str
    input: str


class EmbeddingData(BaseModel):
    object: str
    embedding: List[float]
    index: int


class EmbeddingsUsage(BaseModel):
    prompt_tokens: int
    total_tokens: int


class EmbeddingsResponse(BaseModel):
    object: str
    data: List[EmbeddingData]
    model: str
    usage: EmbeddingsUsage
