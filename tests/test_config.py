import os
import pytest
from unittest.mock import patch
from src.core.config import DatabaseConfig, RedisConfig, AppConfig


class TestDatabaseConfig:
    def test_default_values(self):
        config = DatabaseConfig()
        assert config.host == "localhost"
        assert config.port == 5432
        assert config.name == "myapp"
        assert config.user == "postgres"
        assert config.password == ""
    
    def test_custom_values(self):
        config = DatabaseConfig(
            host="db.example.com",
            port=3306,
            name="production",
            user="admin",
            password="secret"
        )
        assert config.host == "db.example.com"
        assert config.port == 3306
        assert config.name == "production"
        assert config.user == "admin"
        assert config.password == "secret"
    
    @patch.dict(os.environ, {
        'DB_HOST': 'env-host',
        'DB_PORT': '3306',
        'DB_NAME': 'env-db',
        'DB_USER': 'env-user',
        'DB_PASSWORD': 'env-pass'
    })
    def test_from_env_with_all_vars(self):
        config = DatabaseConfig.from_env()
        assert config.host == "env-host"
        assert config.port == 3306
        assert config.name == "env-db"
        assert config.user == "env-user"
        assert config.password == "env-pass"
    
    @patch.dict(os.environ, {}, clear=True)
    def test_from_env_with_defaults(self):
        config = DatabaseConfig.from_env()
        assert config.host == "localhost"
        assert config.port == 5432
        assert config.name == "myapp"
        assert config.user == "postgres"
        assert config.password == ""


class TestRedisConfig:
    def test_default_values(self):
        config = RedisConfig()
        assert config.host == "localhost"
        assert config.port == 6379
        assert config.db == 0
        assert config.password is None
    
    @patch.dict(os.environ, {
        'REDIS_HOST': 'redis.example.com',
        'REDIS_PORT': '6380',
        'REDIS_DB': '1',
        'REDIS_PASSWORD': 'redis-pass'
    })
    def test_from_env_with_all_vars(self):
        config = RedisConfig.from_env()
        assert config.host == "redis.example.com"
        assert config.port == 6380
        assert config.db == 1
        assert config.password == "redis-pass"


class TestAppConfig:
    def test_default_values(self):
        config = AppConfig()
        assert config.debug is False
        assert config.secret_key == "dev-secret-key"
        assert config.log_level == "INFO"
        assert isinstance(config.database, DatabaseConfig)
        assert isinstance(config.redis, RedisConfig)
    
    @patch.dict(os.environ, {
        'DEBUG': 'true',
        'SECRET_KEY': 'production-key',
        'LOG_LEVEL': 'DEBUG'
    })
    def test_from_env(self):
        config = AppConfig.from_env()
        assert config.debug is True
        assert config.secret_key == "production-key"
        assert config.log_level == "DEBUG"
