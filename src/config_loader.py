import base64
import os
from collections import defaultdict
from typing import Dict, List, Tuple

import yaml

from src.stores.file_store import ConfigFileStore

second_map = {
    "s": 1,
    "m": 60,
    "h": 3600,
    "d": 86400,
    "w": 604800,
    "M": 2592000,
    "y": 31536000,
}


def get_config(file_base64: str) -> Dict[str, List[Tuple[int, int]]]:
    """
    Get the configuration from a base64 encoded string.
    Configuration is expected to be in YAML format:
    ```
    <resource_name>:
        <time>: <limit>
    ```
    Example:
    ```
    email:
        1s: 5
        1m: 10
        1h: 100
    ```

    :param file_base64: The base64 encoded string.
    :return: The configuration.
    :raises ValueError: If the configuration is invalid.
    """
    file_content = base64.b64decode(file_base64).decode("utf-8")
    data = yaml.safe_load(file_content)

    config_map = defaultdict(list)

    for resource_name, usage_map in data.items():
        for interval, limit in usage_map.items():
            if interval[-1] not in second_map:
                raise ValueError("Invalid time unit")
            config_map[resource_name].append(
                (int(interval[:-1]) * second_map[interval[-1]], limit)
            )

    return config_map


def load_config_from_env(config_store: ConfigFileStore) -> None:
    """
    Load the configuration from the environment variable.

    :param config_store: The configuration store.
    """
    file_base64 = os.environ.get("CONFIG")
    if file_base64 is None or len(file_base64) == 0:
        raise ValueError("No configuration found")

    config = get_config(file_base64)
    raw_content = base64.b64decode(file_base64).decode("utf-8")
    config_store.update_configs(raw_content=raw_content, config_map=config)
