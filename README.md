# Free LLM API

With LiteLLM, we can access free Large Language Models (LLMs), offering an API that mimics the functionality of the OpenAI API. By leveraging the free model and a local embedding model, users can seamlessly interact with powerful language processing capabilities

## Installation
Clone this repository and install
```bash
git clone https://github.com/kimnt93/free_llm_api.git
cd free_llm_api
pip install .
```

## Configuration

Example under config.yaml file

### Running the Application

You can run the application using the command line interface (CLI) by executing:

```bash
free_llm_api --host 0.0.0.0 --port 8000 --config_path config.yaml
```

Alternatively, you can use Docker Compose to build and run the application:

```bash
docker-compose up --build
```

Ensure that you have Docker installed and configured on your system before running the Docker Compose command.

## API

Once the application is running, you can access the following API endpoints at `http://0.0.0.0:8000`.

### API Endpoints

- `/v1/chat/completions`: Endpoint for chat completions.
- `/v1/completions`: Endpoint for completions.
- `/v1/embeddings`: Endpoint for text embeddings.

Refer to the OpenAI's API documentation [here](https://platform.openai.com/docs/api-reference/introduction) for more details and parameters.

### CURLs

#### Text Embedding Endpoint
```bash
curl http://0.0.0.0:8000/v1/embeddings \
  -H "Content-Type: application/json" \
  -d '{
    "model": "local-e5-large-dim-1024",
    "input": "Hello world!"
  }'
```

#### Completions Endpoint
```bash
curl http://0.0.0.0:8000/v1/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-3.5-turbo",
    "prompt": "Say this is a test",
    "max_tokens": 50
  }'
```

#### Chat Completions Endpoint
```bash
curl http://0.0.0.0:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-3.5-turbo",
    "messages": [{"role": "user", "content": "What is the meaning of life?"}],
    "max_tokens": 50
  }'
```

### OpenAI Python Examples

#### Import OpenAI and Set Endpoint
```python
from openai import OpenAI

client = OpenAI(base_url="http://0.0.0.0:8000/v1", api_key="empty")
```

#### Chat Completions Example
```python
chat = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {
      "role": "user",
      "content": "What is the meaning of life?",
    },
  ],
)
print(chat.choices[0].message.content)
```

#### Completions Example
```python
completion = client.completions.create(
  model="gpt-3.5-turbo",
  prompt="Say this is a test",
)
print(completion.choices[0].text)
```

#### Text Embedding Example
```python
response = client.embeddings.create(
    input="Hello world!",
    model="local-e5-large-dim-1024"
)
print(response.data[0].embedding)
```

### Langchain Examples

For additional language modeling capabilities, you can explore Langchain. Visit the Langchain documentation [here](https://python.langchain.com/) for more details.

#### Initializing Models

```python
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings


# Initialize LLM model
llm = ChatOpenAI(openai_api_base="http://0.0.0.0:8000/v1", openai_api_key="empty", model_name="gpt-3.5-turbo")
llm.invoke("What is the meaning of life?")


# Initialize Embedding model
embeddings = OpenAIEmbeddings(openai_api_base="http://0.0.0.0:8000/v1", openai_api_key="empty", model="local-e5-large-dim-1024")
embeddings.embed_query("Hello world!")
```

With Langchain, you can leverage the power of OpenAI's language models and text embeddings seamlessly within your Python applications.