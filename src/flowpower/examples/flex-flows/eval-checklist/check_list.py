import json
from pathlib import Path

from promptflow.tracing import trace
# from promptflow.core import Prompty, OpenAIModelConfiguration
from promptflow.core import OpenAIModelConfiguration, Prompty

BASE_DIR = Path(__file__).absolute().parent


@trace
def check(answer: str, statement: str, model_config: OpenAIModelConfiguration):
    """Check the answer applies for the check statement."""
    examples = [
        {
            "answer": "ChatGPT is a conversational AI model developed by OpenAI.",
            "statement": "It contains a brief explanation of ChatGPT.",
            "score": 5,
            "explanation": "The statement is correct. The answer contains a brief explanation of ChatGPT.",
        }
    ]

    prompty = Prompty.load(
        source=BASE_DIR / "eval.prompty",
        model={"configuration": model_config},
    )
    output = prompty(examples=examples, answer=answer, statement=statement)
    output = json.loads(output)
    return output


class EvalFlow:
    def __init__(self, model_config: OpenAIModelConfiguration):
        self.model_config = model_config

    def __call__(self, answer: str, statements: dict):
        """Check the answer applies for a collection of check statement."""
        if isinstance(statements, str):
            statements = json.loads(statements)

        results = {}
        for key, statement in statements.items():
            r = check(
                answer=answer, statement=statement, model_config=self.model_config
            )
            results[key] = r
        return results

    def __aggregate__(self, line_results: list) -> dict:
        """Aggregate the results."""
        total = len(line_results)
        avg_correctness = (
            sum(int(r["correctness"]["score"]) for r in line_results) / total
        )
        return {
            "average_correctness": avg_correctness,
            "total": total,
        }


if __name__ == "__main__":
    from promptflow.tracing import start_trace

    start_trace()

    answer = """ChatGPT is a conversational AI model developed by OpenAI.
    It is based on the GPT-3 architecture and is designed to generate human-like responses to text inputs.
    ChatGPT is capable of understanding and responding to a wide range of topics and can be used for tasks such as
    answering questions, generating creative content, and providing assistance with various tasks.
    The model has been trained on a diverse range of internet text and is constantly being updated to improve its
    performance and capabilities. ChatGPT is available through the OpenAI API and can be accessed by developers and
    researchers to build applications and tools that leverage its capabilities."""
    statements = {
        "correctness": "It contains a detailed explanation of ChatGPT.",
        "consise": "It is a consise statement.",
    }

    config = OpenAIModelConfiguration(
        connection="open_ai_connection", model="gpt-3.5-turbo"
    )
    flow = EvalFlow(config)

    result = flow(
        answer=answer,
        statements=statements,
    )
    print(result)

    # run aggregation
    aggregation_result = flow.__aggregate__([result])
    print(aggregation_result)
