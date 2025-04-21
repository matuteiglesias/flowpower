
import os
from pathlib import Path

from dotenv import load_dotenv
from promptflow.tracing import trace
from promptflow.core import OpenAIModelConfiguration, Prompty

BASE_DIR = Path(__file__).absolute().parent

# Load environment variables (OpenAI API Key and Base URL)
load_dotenv()


@trace
def chat(question: str = "What's the capital of France?") -> str:
    """Flow entry function."""

    prompty = Prompty.load(
        source=BASE_DIR / "chat.prompty",
        model={
            "configuration": OpenAIModelConfiguration(
                connection="open_ai_connection",
                model="gpt-3.5-turbo"
            )
        }
    )

    output = prompty(question=question)
    return output


if __name__ == "__main__":
    from promptflow.tracing import start_trace

    start_trace()
    result = chat("What's the capital of France?")
    print(result)




# import os

# from dotenv import load_dotenv
# from pathlib import Path
# from promptflow.tracing import trace
# from promptflow.core import Prompty

# BASE_DIR = Path(__file__).absolute().parent


# @trace
# def chat(question: str = "What's the capital of France?") -> str:
#     """Flow entry function."""

#     if "OPENAI_API_KEY" not in os.environ and "OPENAI_API_KEY" not in os.environ:
#         # load environment variables from .env file
#         load_dotenv()

#     prompty = Prompty.load(source=BASE_DIR / "chat.prompty")
#     output = prompty(question=question)
#     return output


# if __name__ == "__main__":
#     from promptflow.tracing import start_trace

#     start_trace()

#     result = chat("What's the capital of France?")
#     print(result)
