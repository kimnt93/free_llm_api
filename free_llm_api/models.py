from typing import Union, List, Optional, Dict
from sentence_transformers import SentenceTransformer
from litellm import Router
import yaml


class EmbeddingModel:
    def __init__(self, model_name, pretrained, prompt_template, cuda):
        self.model_name = model_name
        self.pretrained = pretrained
        self.prompt_template = prompt_template
        self.model = SentenceTransformer(self.pretrained)
        if cuda:
            self.model = self.model.to('cuda')

    def generate(self, queries: Union[List[str], str]):
        if isinstance(queries, str):
            queries = [queries]

        # generate prompt
        queries = [self.prompt_template.format(query=query) for query in queries]
        embeddings = self.model.encode(queries).tolist()
        total_tokens = sum([len(self.model.tokenizer(query, return_tensors='pt')["input_ids"][0]) for query in queries])
        return {
            "object": "list",
            "data": [
                {
                    "object": "embedding",
                    "embedding": embedding,
                    "index": i
                } for i, embedding in enumerate(embeddings)
            ],
            "model": self.model_name,
            "usage": {
                "prompt_tokens": total_tokens,
                "total_tokens": total_tokens
            }
        }


class LlmRouter:

    def __init__(self, config_path):
        self.llm_router: Optional[Router] = None
        self.local_embedding_router: Optional[Dict[str, EmbeddingModel]] = dict()
        self.config: Optional[dict] = None
        # load yaml config
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)

        # load config
        self.llm_router = Router(model_list=self.config['llm'] + self.config['embedding'])
        # load local embedding
        for model_config in self.config['local_embedding']:
            model_name = model_config['model_name']
            pretrained = model_config['params']['pretrained']
            prompt_template = model_config['params']['prompt_template']
            cuda = model_config['params']['cuda']
            self.local_embedding_router[model_name] = EmbeddingModel(model_name=model_name, pretrained=pretrained, prompt_template=prompt_template, cuda=cuda)

    def local_embedding(self, **kwargs):
        model = kwargs['model']
        input_ = kwargs['input']
        if model not in self.local_embedding_router:
            raise KeyError(f"Model {model} not found")
        return self.local_embedding_router[model].generate(queries=input_)
