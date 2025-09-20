from __future__ import annotations

from redis.asyncio import ConnectionPool, Redis

from aiogram_bot_template.models.config import AppConfig


def create_redis(config: AppConfig) -> Redis:
    return Redis(connection_pool=ConnectionPool.from_url(url=config.redis.build_url()))
