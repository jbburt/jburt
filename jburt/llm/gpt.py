import openai

from jburt.log import LLMCache

MODEL = "gpt-4-1106-preview"

_client = openai.OpenAI()
_cache = LLMCache((MODEL,))
_default_kwargs = {
    "temperature": 0.0,
    "max_tokens": 1024,
    "stream": False,
    "model": MODEL,
}


def get_response(
    query: str, system_prompt: str = None, **kwargs
) -> openai.types.chat.chat_completion.ChatCompletion:
    """
    Send messages to the OpenAI chatbot.

    Args:
        query (str): The query to send to the chatbot.
        system_prompt (str): The system prompt to send to the chatbot.
        chat_log (Union[pathlib.Path, None]): The path to the chat log.
            If None, the chat log is not saved.

    Returns:
        openai.types.chat.chat_completion.ChatCompletion: The OpenAI chatbot response.
    """
    chat_completion_prompt = (
        [{"role": "system", "content": system_prompt}]
        if system_prompt
        else [] + [{"role": "user", "content": query}]
    )
    args = kwargs | _default_kwargs
    # print(args)
    response = _client.chat.completions.create(messages=chat_completion_prompt, **args)
    print(type(response))
    _cache(query, response, debug=True)
    return response


if __name__ == "__main__":
    get_response("What is the capital of France?", max_tokens=10)
