# config.py

import os
import yaml
from pathlib import Path
from typing import Any, Optional, Dict
from collections.abc import MutableMapping

CONFIG_DIR = Path.home() / ".flowpower"
GLOBAL_CONFIG_FILE = CONFIG_DIR / "config.yaml"
PROJECT_CONFIG_FILE = Path(".flowpower/config.yaml").resolve()

# 💡 Default values (can be nested)
_DEFAULTS = {
    "trace": {
        "enabled": True,
        "log_inputs": False,
    },
    "stream": {
        "default": False,
    },
    "log": {
        "level": "INFO",
    },
    "user": {
        "name": os.getenv("USER", "anonymous"),
    }
}

# from collections.abc import Mapping
# def _flatten(d: Mapping) -> dict:
def _flatten(d: dict, parent_key: str = "", sep: str = ".") -> dict:
    items = {}
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.update(_flatten(v, new_key, sep=sep))
        else:
            items[new_key] = v
    return items

def _unflatten(d: Dict[str, Any], sep=".") -> Dict[str, Any]:
    """Convert dot-notation flat dict into nested dict."""
    result = {}
    for key, value in d.items():
        parts = key.split(sep)
        current = result
        for part in parts[:-1]:
            current = current.setdefault(part, {})
        current[parts[-1]] = value
    return result

class Config:
    _global = {}
    _project = {}
    _runtime = {}
    _loaded = False

    @classmethod
    def load(cls):
        if cls._loaded:
            return

        def _read(path: Path):
            if path.exists():
                with open(path) as f:
                    return yaml.safe_load(f) or {}
            return {}

        cls._global = _flatten(_read(GLOBAL_CONFIG_FILE))
        cls._project = _flatten(_read(PROJECT_CONFIG_FILE))
        cls._loaded = True

    @classmethod
    def get(cls, key: str, default: Optional[Any] = None) -> Any:
        cls.load()
        return (
            cls._runtime.get(key)
            or cls._project.get(key)
            or cls._global.get(key)
            or _flatten(_DEFAULTS).get(key)
            or default
        )

    @classmethod
    def set(cls, key: str, value: Any, scope: str = "global"):
        cls.load()
        if scope == "runtime":
            cls._runtime[key] = value
            return

        target = cls._project if scope == "project" else cls._global
        target[key] = value
        cls._save(scope)

    @classmethod
    def all(cls, include_runtime: bool = True) -> Dict[str, Any]:
        cls.load()
        flat = {
            **_flatten(_DEFAULTS),
            **cls._global,
            **cls._project,
            **(cls._runtime if include_runtime else {}),
        }
        return _unflatten(flat)

    @classmethod
    def _save(cls, scope: str):
        path = PROJECT_CONFIG_FILE if scope == "project" else GLOBAL_CONFIG_FILE
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w") as f:
            yaml.safe_dump(_unflatten(cls._project if scope == "project" else cls._global), f)

    @classmethod
    def reload(cls):
        cls._loaded = False
        cls._global = {}
        cls._project = {}
        cls._runtime = {}
        cls.load()

    @classmethod
    def source(cls, key: str) -> str:
        """Return where the config value came from."""
        cls.load()
        if key in cls._runtime:
            return "runtime"
        elif key in cls._project:
            return "project"
        elif key in cls._global:
            return "global"
        elif key in _flatten(_DEFAULTS):
            return "default"
        return "undefined"
