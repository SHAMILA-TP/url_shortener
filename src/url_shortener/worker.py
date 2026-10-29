from collections.abc import Callable
from typing import Any, ClassVar

from arq.connections import RedisSettings

from url_shortener.core.config import get_settings
from url_shortener.jobs.clicks import record_click


class WorkerSettings:
    functions: ClassVar[list[Callable[..., Any]]] = [record_click]
    redis_settings: ClassVar[RedisSettings] = RedisSettings.from_dsn(
        get_settings().redis_url
    )
