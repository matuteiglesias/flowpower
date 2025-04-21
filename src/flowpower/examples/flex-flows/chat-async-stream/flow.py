import asyncio
import os
from pathlib import Path

from promptflow.tracing import trace
# from promptflow.core import OpenAIModelConfiguration, Prompty
from promptflow.core import OpenAIModelConfiguration, Prompty

BASE_DIR = Path(__file__).absolute().parent
 

def log(message: str):
    verbose = os.environ.get("VERBOSE", "false")
    if verbose.lower() == "true":
        print(message, flush=True)

# from collections.abc import AsyncGenerator

class ChatFlow:
    def __init__(
        self, model_config: OpenAIModelConfiguration, max_total_token=1100
    ):
        self.model_config = model_config
        self.max_total_token = max_total_token

    @trace
    async def __call__(
        self, question: str = "What is ChatGPT?", chat_history: list = None
    ):
        """Flow entry function."""

        prompty = Prompty.load(
            source=BASE_DIR / "chat.prompty",
            model={"configuration": self.model_config},
        )

        chat_history = chat_history or []
        # Try to render the prompt with token limit and reduce the history count if it fails
        while len(chat_history) > 0:
            token_count = prompty.estimate_token_count(
                question=question, chat_history=chat_history
            )
            if token_count > self.max_total_token:
                chat_history = chat_history[1:]
                log(
                    f"Reducing chat history count to {len(chat_history)} to fit token limit"
                )
            else:
                break

        # output is a generator of string as prompty enabled stream parameter
        for output in prompty(question=question, chat_history=chat_history):
            yield output


if __name__ == "__main__":
    from promptflow.tracing import start_trace

    start_trace()
    # config = OpenAIModelConfiguration(
    #     connection="open_ai_connection", model="gpt-3.5-turbo"
    # )

    config = OpenAIModelConfiguration(
    connection="open_ai_connection",
    model="gpt-3.5-turbo"
    )
    
    flow = ChatFlow(model_config=config)
    result = flow("What's Azure Machine Learning?", [])


    # print result in stream manner
    async def consume_result():
        async for output in result:
            print(output, end="")
            await asyncio.sleep(0.01)

    asyncio.run(consume_result())
