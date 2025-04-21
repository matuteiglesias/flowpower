import os
import re
from typing import Any, Union

ENV_PATTERN = re.compile(r"\${(\w+)}|\{\$(\w+)\}")

def resolve_env_vars(obj: Any) -> Any:
    if isinstance(obj, str):
        return _resolve_string(obj)
    elif isinstance(obj, dict):
        return {k: resolve_env_vars(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [resolve_env_vars(item) for item in obj]
    return obj

def _resolve_string(s: str) -> str:
    def replacer(match):
        var_name = match.group(1) or match.group(2)
        return os.environ.get(var_name, "")
    return ENV_PATTERN.sub(replacer, s)
