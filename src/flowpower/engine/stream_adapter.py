import time

def stream_as_tokens(response: str):
    """
    Yield tokens from a string, simulating live output.
    """
    for word in response.split():
        yield word + " "
        time.sleep(0.1)  # fake latency
