# __init__.py

# Expose FlowpowerClient at the top level
from .sdk.client import FlowpowerClient

# Shortcut for programmatic access
fp = FlowpowerClient()

from .config import Config
from .logger import get_logger
