import os
from pathlib import Path
from typing import ClassVar

from confz import BaseConfig, ConfigSource, EnvSource, FileSource
from pydantic import AnyUrl


class DjangoConfig(BaseConfig):
    server_type: str | None = None
    base_dir: Path | None = Path(__file__).parents[2]
    public_root: Path | None = None
    debug: bool = False
    database_url: AnyUrl = "postgis:///ausgsteckt"
    site_id: int = 1
    timezone: str = "Europe/Vienna"
    use_i18n: bool = True
    use_l10n: bool = False
    use_tz: bool = True
    static_url: str = "/static/"
    media_url: str = "/media/"
    cache_backend: AnyUrl = "locmemcache://"

    CONFIG_SOURCES: ClassVar[list[ConfigSource]] = [
        EnvSource(prefix="DJANGO_"),
        FileSource(file=os.environ.get("DJANGO_CONFIG_FILE", Path(__file__).parents[3] / "config.yaml"), optional=True),
    ]
