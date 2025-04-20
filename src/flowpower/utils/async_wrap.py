# src/flowpower/utils/async_wrap.py

import asyncio

def async_run_allowing_running_loop(func, *args, **kwargs):
    try:
        return asyncio.run(func(*args, **kwargs))
    except RuntimeError as e:
        # Running from within an active loop (e.g., IPython)
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(func(*args, **kwargs))
