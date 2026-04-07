from dataclasses import dataclass
from typing import Optional
import os


@dataclass
class DatabaseConfig:
    host: str = "localhost"
    port: int = 5432
    name: str = "myapp"
    user: str = "postgres"
    password: str = ""
    
    @classmethod
    def from_env(cls) -> 'DatabaseConfig':
        return cls(
            host=os.getenv('DB_HOST', cls.host),
            port=int(os.getenv('DB_PORT', str(cls.port))),
            name=os.getenv('DB_NAME', cls.name),
            user=os.getenv('DB_USER', cls.user),
            password=os.getenv('DB_PASSWORD', cls.password)
        )


@dataclass
class RedisConfig:
    host: str = "localhost"
    port: int = 6379
    db: int = 0
    password: Optional[str] = None
    
    @classmethod
    def from_env(cls) -> 'RedisConfig':
        return cls(
            host=os.getenv('REDIS_HOST', cls.host),
            port=int(os.getenv('REDIS_PORT', str(cls.port))),
            db=int(os.getenv('REDIS_DB', str(cls.db))),
            password=os.getenv('REDIS_PASSWORD')
        )


@dataclass
class AppConfig:
    debug: bool = False
    secret_key: str = "dev-secret-key"
    log_level: str = "INFO"
    database: DatabaseConfig = None
    redis: RedisConfig = None
    
    def __post_init__(self):
        if self.database is None:
            self.database = DatabaseConfig.from_env()
        if self.redis is None:
            self.redis = RedisConfig.from_env()
    
    @classmethod
    def from_env(cls) -> 'AppConfig':
        return cls(
            debug=os.getenv('DEBUG', 'false').lower() == 'true',
            secret_key=os.getenv('SECRET_KEY', cls.secret_key),
            log_level=os.getenv('LOG_LEVEL', cls.log_level),
            database=DatabaseConfig.from_env(),
            redis=RedisConfig.from_env()
        )


config = AppConfig.from_env()
