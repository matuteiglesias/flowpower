import time
from promptflow._proxy import ProxyFactory

def stream_as_tokens(response: str):
    """
    Yield tokens from a string, simulating live output.
    """
    for word in response.split():
        yield word + " "
        time.sleep(0.1)  # fake latency


def stream_output_generator(flow, data, run_config):
    proxy = ProxyFactory().create_executor_proxy(flow_path=flow)
    result = proxy.exec_line(inputs=data)  # `inputs` is a dict here
    for token in result.output.split():  # Dummy token streaming
        yield token
