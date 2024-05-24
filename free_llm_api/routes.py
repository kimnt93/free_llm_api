"""This server offers RESTful APIs compatible with OpenAI. It supports the following functionalities:

- Chat Completions (Reference: https://platform.openai.com/docs/api-reference/chat)
- Completions (Reference: https://platform.openai.com/docs/api-reference/completions)
- Embeddings (Reference: https://platform.openai.com/docs/api-reference/embeddings)

"""

from fastapi import APIRouter, HTTPException, Depends, Request
import free_llm_api.config as config
from free_llm_api.models import *
from free_llm_api.utils import get_model, handle_completions
from openai import OpenAI

router = APIRouter()
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=config.OPENROUTER_API_KEY,
)


# Endpoint to handle chat completions
@router.post("/v1/chat/completions")
async def chat_completions(request: Request):
    return await handle_completions(request, client.chat.completions.create)


# Endpoint to handle completions
@router.post("/v1/completions")
async def completions(request: Request):
    return await handle_completions(request, client.completions.create)


@router.post("/v1/embeddings", response_model=EmbeddingsResponse)
async def get_embeddings(request: EmbeddingsRequest, model=Depends(get_model)):
    try:
        input_texts = [f"query: {request.input}"]
        embeddings = model.encode(input_texts, normalize_embeddings=True).tolist()
        num_tokens = len(model.tokenizer(request.input, max_length=512, padding=True, truncation=True, return_tensors='pt')["input_ids"][0])

        response = EmbeddingsResponse(
            object="list",
            data=[EmbeddingData(object="embedding", embedding=embeddings[0], index=0)],
            model=request.model,
            usage=EmbeddingsUsage(prompt_tokens=num_tokens, total_tokens=num_tokens)
        )
        return response

    except (ValueError, RuntimeError) as e:
        raise HTTPException(status_code=500, detail=f"Server error: {e}")
