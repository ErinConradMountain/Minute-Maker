import os
from typing import Optional


class MissingSecretError(RuntimeError):
    pass


def get_secret(name: str, default: Optional[str] = None) -> str:
    value = os.getenv(name, default)
    if value is None or value == "":
        raise MissingSecretError(f"Missing required secret: {name}")
    return value


def get_qwen_credentials() -> dict:
    return {
        "endpoint": os.getenv("QWEN_API_ENDPOINT", "qwen/qwen2.5-vl-72b-instruct:free"),
        "api_key": get_secret("QWEN_API_KEY"),
    }

