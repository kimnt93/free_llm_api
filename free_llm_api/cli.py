import click
import uvicorn
from fastapi import FastAPI
from free_llm_api.routes import router

app = FastAPI()
app.include_router(router)


@click.command()
@click.option('--host', default='0.0.0.0', help='Host address')
@click.option('--port', default=8000, help='Port number')
def cli(host, port):
    uvicorn.run(app, host=host, port=port)


if __name__ == '__main__':
    cli()
