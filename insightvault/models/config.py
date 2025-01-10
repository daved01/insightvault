from pydantic import BaseModel


class DatabaseConfig(BaseModel):
    path: str = "./data/db"
    result_threshold: float = 0.9
    max_num_results: int = 5


class SplitterConfig(BaseModel):
    chunk_size: int = 1024
    chunk_overlap: int = 256


class LlmConfig(BaseModel):
    model: str = "llama3"


class EmbeddingConfig(BaseModel):
    model: str = "all-MiniLM-L6-v2"


class AppConfig(BaseModel):
    database: DatabaseConfig = DatabaseConfig(
        path="./data/db", result_threshold=0.9, max_num_results=5
    )
    splitter: SplitterConfig
    llm: LlmConfig
    embedding: EmbeddingConfig
