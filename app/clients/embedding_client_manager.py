import asyncio
from typing import Optional

import httpx
from langchain_core.embeddings import Embeddings

from app.conf.app_config import EmbeddingConfig, app_config


class TEIEmbeddings(Embeddings):
    """访问自托管 Text Embeddings Inference 服务的嵌入客户端"""

    def __init__(self, endpoint_url: str, timeout: float = 60.0):
        self.endpoint_url = endpoint_url.rstrip("/") + "/embed"
        self.timeout = timeout

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        with httpx.Client(timeout=self.timeout) as client:
            resp = client.post(self.endpoint_url, json={"inputs": texts})
            resp.raise_for_status()
            return resp.json()

    def embed_query(self, text: str) -> list[float]:
        return self.embed_documents([text])[0]

    async def aembed_documents(self, texts: list[str]) -> list[list[float]]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            resp = await client.post(self.endpoint_url, json={"inputs": texts})
            resp.raise_for_status()
            return resp.json()

    async def aembed_query(self, text: str) -> list[float]:
        return (await self.aembed_documents([text]))[0]


class EmbeddingClientManager:
    def __init__(self, config: EmbeddingConfig):
        self.client: Optional[Embeddings] = None
        self.config = config

    def _get_url(self):
        return f"http://{self.config.host}:{self.config.port}"

    def init(self):
        self.client = TEIEmbeddings(endpoint_url=self._get_url())


embedding_client_manager = EmbeddingClientManager(app_config.embedding)

if __name__ == "__main__":
    embedding_client_manager.init()
    client = embedding_client_manager.client

    async def test():
        text = "what are you learning?"
        query_result = await client.aembed_query(text)
        print(query_result[:3])

    asyncio.run(test())
