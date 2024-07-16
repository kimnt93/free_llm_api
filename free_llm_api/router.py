import os
from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse

from .models import LlmRouter
from .utils import create_stream_generator

api_router = APIRouter()
_LLM = None  # Initialize later with config_path


def initialize_llm_router(config_path: str):
    global _LLM
    _LLM = LlmRouter(config_path=config_path)


@api_router.post("/v1/chat/completions")
async def chat_completions(request: Request):
    request = await request.json()
    stream = request.get('stream', False)
    llm_response = await _LLM.llm_router.acompletion(**request)
    if not stream:
        llm_response = llm_response.to_dict()
        llm_response['model'] = request['model']
        return llm_response
    else:
        return StreamingResponse(create_stream_generator(request['model'], llm_response), media_type="text/event-stream")


# Endpoint to handle completions
@api_router.post("/v1/completions")
async def completions(request: Request):
    request = await request.json()
    stream = request.get('stream', False)
    llm_response = await _LLM.llm_router.atext_completion(**request)
    if not stream:
        llm_response = llm_response.to_dict()
        llm_response['model'] = request['model']
        return llm_response
    else:
        return StreamingResponse(create_stream_generator(request['model'], llm_response), media_type="text/event-stream")


@api_router.post("/v1/embeddings")
async def get_embeddings(request: Request):
    request = await request.json()

    if isinstance(request['input'], str):
        request['input'] = [request['input']]

    if request['model'] not in _LLM.local_embedding_router:
        llm_response = await _LLM.llm_router.aembedding(**request)
        llm_response = llm_response.to_dict()
    else:
        llm_response = _LLM.local_embedding(**request)

    llm_response['model'] = request['model']
    return llm_response
