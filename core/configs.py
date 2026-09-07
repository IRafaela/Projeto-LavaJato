from typing import List, ClassVar 
from pydantic_settings import BaseSettings
from sqlalchemy.orm import declarative_base
import secrets

class Settings(BaseSettings):
    API_V1_STR: str = '/api/v1'
    DB_URL: str = 'mysql+aiomysql://root:074596@localhost:3306/sistema_lava_jato'

    DBBaseModel: ClassVar = declarative_base()

    JWT_SECRET: str = secrets.token_urlsafe(32)
    """
    import secrets token: str = secrets.token_urlsafe(32)
    """
    ALGORITHM: str = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7

    class Config:
       case_sensitive = True


settings = Settings()