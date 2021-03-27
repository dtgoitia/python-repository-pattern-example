import os
from typing import Optional

import attr


@attr.s(auto_attribs=True, frozen=True)
class AppConfig:
    database_uri: str
    debug: bool


_CACHED_CONFIG: Optional[AppConfig] = None


def get_config() -> AppConfig:
    if _CACHED_CONFIG:
        return _CACHED_CONFIG

    return AppConfig(
        database_uri=os.environ["DATABASE_URI"],
        debug=os.environ.get("DEBUG", False).lower() == "true",
    )
