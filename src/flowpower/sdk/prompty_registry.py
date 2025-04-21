# src/flowpower/sdk/prompty_registry.py

import json
from pathlib import Path
from promptflow.core import Prompty

def scan_prompty_blocks(directory="blocks/"):
    registry = {}
    for path in Path(directory).rglob("*.prompty"):
        try:
            prompty = Prompty.load(path)
            registry[path.as_posix()] = {
                "name": prompty._name,
                "inputs": list(prompty._get_input_signature().keys()),
                "output_type": prompty._get_output_signature(include_primitive_output=True),
            }
        except Exception as e:
            registry[path.as_posix()] = {"error": str(e)}
    return registry

def write_prompty_registry(path="prompty_registry.json", directory="blocks/"):
    registry = scan_prompty_blocks(directory)
    with open(path, "w") as f:
        json.dump(registry, f, indent=2)
    return path
