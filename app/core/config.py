"""
应用配置管理
从环境变量读取配置，支持.env文件
"""
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """应用配置"""

    # 应用配置
    app_host: str = Field(default="0.0.0.0", env="APP_HOST")
    app_port: int = Field(default=8000, env="APP_PORT")
    log_level: str = Field(default="INFO", env="LOG_LEVEL")

    # DeepSeek
    deepseek_api_key: str = Field(default="", env="DEEPSEEK_API_KEY")
    deepseek_base_url: str = Field(default="https://api.deepseek.com", env="DEEPSEEK_BASE_URL")
    deepseek_model: str = Field(default="deepseek-chat", env="DEEPSEEK_MODEL")

    # 通义千问
    qwen_api_key: str = Field(default="", env="QWEN_API_KEY")
    qwen_base_url: str = Field(
        default="https://dashscope.aliyuncs.com/compatible-mode/v1",
        env="QWEN_BASE_URL"
    )

    # 通义万相（图片）
    wanx_api_key: str = Field(default="", env="WANX_API_KEY")

    # 即梦（视频）
    seedance_api_key: str = Field(default="", env="SEEDANCE_API_KEY")

    # PostgreSQL
    postgres_user: str = Field(default="postgres", env="POSTGRES_USER")
    postgres_password: str = Field(default="postgres", env="POSTGRES_PASSWORD")
    postgres_db: str = Field(default="ecommerce_ai", env="POSTGRES_DB")
    postgres_host: str = Field(default="localhost", env="POSTGRES_HOST")
    postgres_port: int = Field(default=5432, env="POSTGRES_PORT")

    # Redis
    redis_host: str = Field(default="localhost", env="REDIS_HOST")
    redis_port: int = Field(default=6379, env="REDIS_PORT")
    redis_password: str = Field(default="", env="REDIS_PASSWORD")

    # MinIO
    minio_endpoint: str = Field(default="localhost:9000", env="MINIO_ENDPOINT")
    minio_access_key: str = Field(default="minioadmin", env="MINIO_ACCESS_KEY")
    minio_secret_key: str = Field(default="minioadmin", env="MINIO_SECRET_KEY")
    minio_bucket: str = Field(default="ecommerce-ai", env="MINIO_BUCKET")

    # Chroma
    chroma_host: str = Field(default="localhost", env="CHROMA_HOST")
    chroma_port: int = Field(default=8000, env="CHROMA_PORT")
    chroma_collection: str = Field(default="product_knowledge", env="CHROMA_COLLECTION")

    # 卖家精灵
    sellersprite_api_key: str = Field(default="", env="SELLERSPRITE_API_KEY")

    @property
    def database_url(self) -> str:
        """数据库连接URL"""
        return (
            f"postgresql://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    @property
    def redis_url(self) -> str:
        """Redis连接URL"""
        if self.redis_password:
            return f"redis://:{self.redis_password}@{self.redis_host}:{self.redis_port}/0"
        return f"redis://{self.redis_host}:{self.redis_port}/0"

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
