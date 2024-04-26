from functools import lru_cache
from ..schemas import EnvironmentSettings


@lru_cache
def get_environment_settings():
    return EnvironmentSettings()
