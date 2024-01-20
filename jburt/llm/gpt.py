import json

import openai

from jburt.log import QACache

MODEL = "gpt-4-1106-preview"

_client = openai.OpenAI()

_cache = QACache((MODEL,))

_default_kwargs = {
    "temperature": 0.0,
    "max_tokens": 1024,
    "stream": False,
    "model": MODEL,
}


class Dataset(QACache):
    """
    A dataset of cached LLM response data, eg for fine-tuning an LLM.
    """

    def __init__(self, dataset: str, parts, **kwargs):
        super().__init__(parts=(*parts, dataset), **kwargs)
        self.dataset = dataset

    def load(self):
        """
        Load the dataset.

        Returns:
            list: The dataset.
        """
        with open(self.path, "r") as f:
            return [json.loads(line) for line in f.readlines()]


def get_response(
    query: str,
    system_prompt: str = None,
    cache: bool = True,
    **kwargs,
) -> openai.types.chat.chat_completion.ChatCompletion:
    """
    Send messages to the OpenAI chatbot.

    Args:
        query (str): The query to send to the chatbot.
        system_prompt (str): The system prompt to send to the chatbot.
        cache (bool): Whether to cache the response.
        **kwargs: Additional arguments to pass to the OpenAI ChatCompletion API.

    Returns:
        openai.types.chat.chat_completion.ChatCompletion: The AI response.
    """
    chat_completion_prompt = (
        [{"role": "system", "content": system_prompt}]
        if system_prompt
        else [] + [{"role": "user", "content": query}]
    )
    args = kwargs | _default_kwargs
    response = _client.chat.completions.create(messages=chat_completion_prompt, **args)
    _cache.append(query, response, system=system_prompt or "", debug=not cache)
    return response


if __name__ == "__main__":
    result = get_response(
        "Show an example of the syntax for defining a function in zshrc that accepts one argument and uses its value in an evaluated expression.",
        max_tokens=100,
    )
    print(result)
