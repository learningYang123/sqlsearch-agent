import asyncio
import random
from typing import Optional

from huggingface_hub import create_collection
from qdrant_client import AsyncQdrantClient,models
from app.conf.app_config import QdrantConfig,app_config
from examples.qdrant_quick_start_demo import CONNECTION_NAME


class QdrantClientManager:
    def __init__(self,qdrant_config:QdrantConfig):
        self.qdrant_config=qdrant_config
        self.client:Optional[AsyncQdrantClient] =None
    def _get_url(self):
        return f"http://{self.qdrant_config.host}:{self.qdrant_config.port}"

    def init(self):
        self.client=AsyncQdrantClient(url=self._get_url())

    async def close(self):
        await self.client.close()

qdrant_client_manager=QdrantClientManager(app_config.Qdrant)


if __name__=="__main__":
    qdrant_client_manager.init()

    async def test():
        client=qdrant_client_manager.client
        if not await client.collection_exists("my_collection"):
            await client.create_collection(
                collection_name="my_collection",
                vectors_config=models.VectorParams(
                    size=10,
                    distance=models.Distance.COSINE
                )
            )

        await client.upsert(
            collection_name="my_collection",
            points=[models.PointStruct(
                id=1,
                vector=[random.random() for _ in range(10)]
            ) for i in range(100)
            ]
        )

        res=await client.query_points(
            collection_name="my_collection",
            query=[random.random() for _ in range(10)],  # type: ignore
            limit=10,
            score_threshold=0.8
        )
        print(res)
    asyncio.run(test())




