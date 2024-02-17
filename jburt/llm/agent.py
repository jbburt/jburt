from collections import deque
import openai


class Chatbot:
    """Front-end for chat with rolling history buffer.

    Usage:
    >>> model = Chatbot(system="you are a helpful assistant.\n---\n")
    >>> model("What is the capital of France?")

    """

    model = "gpt-4-1106-preview"
    system = "you are an expert machine learning engineer and communicator.\n---\n"
    params = {"temperature": 0.0, "max_tokens": 128, "stream": False, "model": model}

    max_convo_length = 6

    client = openai.OpenAI()
    messages = deque(maxlen=max_convo_length)

    def __init__(self, system=None) -> None:
        self.messages = [{"role": "system", "content": system or self.system}]

    def __call__(self, content: str) -> str:
        self.messages.append({"role": "user", "content": content})
        response = Agent.send_receive(self.messages)
        self.messages.append(response)
        return response["content"]

    def get_convo(self) -> list:
        return list(self.messages)

    @staticmethod
    def send_receive(messages, **kwargs) -> dict:
        if not all(isinstance(m, dict) for m in messages):
            raise ValueError("messages must be a list of dictionaries")
        response = Agent.client.chat.completions.create(
            messages=list(messages), **(Agent.params | (kwargs or {}))
        )
        return {"role": "system", "content": response.choices[0].message.content}


if __name__ == "__main__":
    llm = Chatbot(system="you are a helpful assistant.\n---\n")
    print(llm("What is the capital of France?"))
