# sdk/run_config.py

from typing import Optional, Union, Dict, Any
import os
from pathlib import Path

def build_run_config(
    flow: Union[str, dict],
    data: Optional[Union[str, dict]] = None,
    stream: bool = False,
    variant: Optional[str] = None,
    resume_from: Optional[str] = None,
    column_mapping: Optional[Dict[str, str]] = None,
    name: Optional[str] = None,
    display_name: Optional[str] = None,
    tags: Optional[Dict[str, str]] = None,
    init: Optional[dict] = None,
    connections: Optional[dict] = None,
    environment_variables: Optional[dict] = None,
    code: Optional[str] = None,
    **kwargs
) -> Dict[str, Any]:
    """
    Assemble run configuration for PFClient.run(), based on user inputs.
    """

    config = {}

    # Required
    config["flow"] = str(flow)

    if data:
        config["data"] = str(data)

    # Optional
    if column_mapping:
        config["column_mapping"] = column_mapping
    if variant:
        config["variant"] = variant
    if resume_from:
        config["resume_from"] = resume_from
    if name:
        config["name"] = name
    if display_name:
        config["display_name"] = display_name
    if tags:
        config["tags"] = tags
    if init:
        config["init"] = init
    if connections:
        config["connections"] = connections
    if environment_variables:
        config["environment_variables"] = environment_variables
    if code:
        config["code"] = code

    # Capture any extra kwargs
    config.update(kwargs)

    return config
