from fastapi import FastAPI

from free_llm_api.router import initialize_llm_router, api_router


def create_app(config_path: str) -> FastAPI:
    app = FastAPI()
    initialize_llm_router(config_path)
    app.include_router(api_router)
    return app
