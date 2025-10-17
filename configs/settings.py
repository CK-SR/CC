"""Runtime configuration helpers for the camera check service.

摄像头巡检服务的运行时配置工具。
"""
from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Optional

try:  # Optional dependency; ignore if unavailable during runtime.
    from dotenv import load_dotenv
except Exception:  # pragma: no cover - import side effect only
    load_dotenv = None  # type: ignore

if load_dotenv is not None:
    # Load variables from a local .env file when present to simplify development.
    load_dotenv()


def _get_bool(value: Optional[str], default: bool = False) -> bool:
    if value is None:
        return default
    return value.lower() in {"1", "true", "yes", "on"}


@dataclass
class RedisSettings:
    """Connection information for the Redis instance used by the service.

    服务运行所需的 Redis 连接信息。
    """

    host: str = os.getenv("REDIS_HOST", "127.0.0.1")
    port: int = int(os.getenv("REDIS_PORT", "6379"))
    password: Optional[str] = os.getenv("REDIS_PASSWORD")
    db: int = int(os.getenv("REDIS_DB", "0"))
    decode_responses: bool = _get_bool(os.getenv("REDIS_DECODE_RESPONSES"), True)


@dataclass
class Settings:
    """Container for all configurable runtime options.

    汇总所有可配置的运行参数。
    """

    redis: RedisSettings = RedisSettings()


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return a cached instance of :class:`Settings`.

    The configuration only needs to be evaluated once because environment
    variables are static for the lifetime of the process.  Reusing the same
    object avoids repeated environment parsing throughout the code base.
    """

    return Settings()


# Provide a module level singleton that mirrors the "settings" pattern used in
# FastAPI projects.
settings: Settings = get_settings()

__all__ = ["Settings", "RedisSettings", "get_settings", "settings"]
