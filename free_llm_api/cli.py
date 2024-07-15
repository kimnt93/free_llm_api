import click
import uvicorn

from free_llm_api.app import create_app


@click.command()
@click.option('--host', default='0.0.0.0', help='Host address')
@click.option('--port', default=8000, help='Port number')
@click.option('--config_path', help='Config path')
def cli(host, port, config_path):
    app = create_app(config_path)
    uvicorn.run(app, host=host, port=port)


if __name__ == '__main__':
    cli()
