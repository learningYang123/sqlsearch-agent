import asyncio
from sqlalchemy import text
from sqlalchemy.ext.asyncio import (AsyncEngine,async_sessionmaker,create_async_engine)

from app.conf.app_config import DBConfig,app_config

class MysqlClientManager:

    def __init__(self,config:DBConfig):
        self.engine:AsyncEngine |None=None
        self.session=None
        self.config=config

    def _get_url(self):
        return f"mysql+asyncmy://{self.config.user}:{self.config.password}@{self.config.host}/{self.config.port}?charset=utf8mb4"


    def init(self):
        self.engine=create_async_engine(url=self._get_url(),pool_size=10,pool_pre_ping=True)
        self.session=async_sessionmaker(self.engine,autoflush=True,expire_on_commit=False)


    async def close(self):
        await self.engine.dispose()

meta_mysql_client_manager=MysqlClientManager(app_config.db_meta)
dw_mysql_client_manager=MysqlClientManager(app_config.db_dw)

# if __name__=="__main__":


