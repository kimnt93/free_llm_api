import uvicorn
from fastapi import FastAPI
from free_llm_api.routes import router
import argparse

app = FastAPI()

app.include_router(router)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run FastAPI server")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="Host address")
    parser.add_argument("--port", type=int, default=8000, help="Port number")
    args = parser.parse_args()

    uvicorn.run(app, host=args.host, port=args.port)
