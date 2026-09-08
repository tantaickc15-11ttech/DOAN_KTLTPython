"""Đọc cấu hình YAML và cung cấp giá trị mặc định an toàn."""

from copy import deepcopy
from pathlib import Path

import yaml


DEFAULT_CONFIG = {
    "app": {
        "title": "Wazuh Security Monitor",
        "demo_mode": True,
        "auto_load_sample": True,
    },
    "telegram": {
        "enabled": False,
        "bot_token": "",
        "chat_id": "",
        "minimum_level": 8,
        "timeout_seconds": 10,
    },
}


def load_config(file_path):
    """Đọc config.yml; nếu chưa có thì sử dụng cấu hình mặc định."""
    config = deepcopy(DEFAULT_CONFIG)
    path = Path(file_path)

    if not path.exists():
        return config

    try:
        with path.open("r", encoding="utf-8") as file:
            user_config = yaml.safe_load(file) or {}
    except (OSError, yaml.YAMLError) as error:
        print(f"Không đọc được cấu hình, dùng giá trị mặc định: {error}")
        return config

    for section in ("app", "telegram"):
        values = user_config.get(section)
        if isinstance(values, dict):
            config[section].update(values)

    return config

