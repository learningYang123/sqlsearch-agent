from dataclasses import dataclass
from pathlib import Path

from omegaconf import OmegaConf

#文件日志配置
@dataclass
class File:
    enable:bool
    level:str
    path:str
    rotation:str
    retention:str

#控制台日志配置
@dataclass
class Console:
    enable:bool
    level:str

#组合两种日志配置的总配置
@dataclass
class LoggingConfig:
    file:File
    console:Console

#数据库配置
@dataclass
class DBConfig:
    host:str
    port:int
    user:str
    password:str
    database:str

@dataclass
class QdrantConfig:
    host:str
    port:int
    embedding_size:int

@dataclass
class EmbeddingConfig:
    host:str
    port:int
    model:str

@dataclass
class ESConfig:
    host:str
    port:int
    index_name:str

@dataclass
class LLMConfig:
    model_name:str
    api_key:str
    base_url:str

#配置总入口
@dataclass
class AppConfig:
    logging:LoggingConfig
    db_meta:DBConfig
    db_dw:DBConfig
    Qdrant:QdrantConfig
    embedding:EmbeddingConfig
    es:ESConfig
    llm:LLMConfig

#从当前文件出发返回到项目根目录
#再定位到配置文件
config_file=Path(__file__).parents[2]/"conf"/"app_config.yaml"

#读取配置文件
context=OmegaConf.load(config_file)

schema=OmegaConf.structured(AppConfig)

app_config:AppConfig=OmegaConf.to_object(OmegaConf.merge(schema,context))

if __name__=="__main__":
    print(app_config.es.host)