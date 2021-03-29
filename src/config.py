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
        debug=_to_bool(os.environ.get("DEBUG")),
    )


def _to_bool(envvar: Optional[str]) -> bool:
    if envvar is None:
        return False

    if not isinstance(envvar, str):
        raise ValueError(f"A string was expected, got {type(envvar)} instead")

    if envvar.lower() == "true":
        return True

    return False
