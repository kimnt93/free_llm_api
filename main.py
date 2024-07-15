from free_llm_api.app import create_app


if __name__ == "__main__":
    import uvicorn
    app = create_app("config.yaml")
    uvicorn.run(app, host='0.0.0.0', port=8000)
