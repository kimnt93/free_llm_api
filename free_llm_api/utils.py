from sentence_transformers import SentenceTransformer
from fastapi import Request, HTTPException
from fastapi.responses import StreamingResponse

import free_llm_api.config as config


# Define singleton class for loading embedding model
class TextEmbeddingModel:
    _model = None

    @classmethod
    def get_model(cls):
        if cls._model is None:
            cls._model = SentenceTransformer(config.EMBEDDING_MODEL)
        return cls._model


def get_model():
    return TextEmbeddingModel.get_model()


# Function to handle streaming response
def stream_generator(request_model, stream):
    for chunk in stream:
        chunk = chunk.to_dict()
        chunk['model'] = request_model
        yield chunk.__str__()


# Generic function to handle completions
async def handle_completions(request: Request, completion_func):
    try:
        request_data = await request.json()
        request_model = request_data['model']

        # Update default model and send to Open Router
        request_data['model'] = config.OPENROUTER_MODEL

        # Call OpenAI API from OpenRouter
        completion = completion_func(**request_data)

        if not request_data.get("stream"):
            completion = completion.to_dict()
            completion['model'] = request_model
            return completion
        else:
            return StreamingResponse(stream_generator(request_model, completion), media_type="text/event-stream")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OpenAI API error: {e}")
