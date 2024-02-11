import json
import pathlib
from collections import deque
from os import environ as e_

import openai
from openai.types.chat import ChatCompletion

__all__ = ["Conversation", "Response", "Cache", "ConvoCache"]


class CacheConfig:
    dir = pathlib.Path(e_["HOME"]) / "Downloads" / "my-openai-history"
    dir.mkdir(exist_ok=True, parents=True)

    filename = "jburt-openai-message-dataset.jsonl"
    path = dir / filename

    system_key = "system"
    user_key = "user"
    assistant_key = "assistant"


class Response(CacheConfig):
    """

    Attributes:
        response (openai.types.ChatCompletion): The response.
        model (str): The chat model.
        fingerprint (str): The backend configuration.
        id (str): A unique identifier for the chat completion.
        created (int): The time the chat completion was created.
        role (str): The role assigned to the responder.
        content (str): The content of the response.

    """

    def __init__(self, response):
        super().__init__()
        self.response: ChatCompletion = response
        self.fingerprint: str = response.system_fingerprint
        self.model = response.model
        # self.id: str = response.id
        self.role: str = response.choices[0].message.role
        self.content: str = response.choices[0].message.content
        # self.usage: dict = response.choices[0].message.usage

    def message(self) -> dict:
        return {
            # "model": self.model,
            # "fingerprint": self.fingerprint,
            # "id": self.id,
            # "created": self.created,
            "role": self.role,
            "content": self.content,
        }

    def dict(self) -> dict:
        return {
            "model": self.model,
            "fingerprint": self.fingerprint,
            "id": self.id,
            "role": self.role,
            "content": self.content,
        }


class Role:
    pass


class MLE(Role):
    assignment = "you are an expert ML engineer and sysadmin.\n---\n"


class LMConfig:
    client = None
    # gpt model
    model = "gpt-4-1106-preview"
    # max length of convo history
    nhistbuf = 10
    # api parameters
    params_ = {
        "temperature": 0.0,
        "max_tokens": 128,
        "stream": False,
        "model": model,
    }

    def __init__(self, system=MLE.assignment) -> None:
        self.client = openai.OpenAI()
        self.system = system

    def create(self, messages, **kwargs):
        print(messages)
        return Response(
            self.client.chat.completions.create(messages=messages, **kwargs)
        )


class Cache(CacheConfig):
    def __init__(self):
        super().__init__()
        if not self.path.exists():
            self.path.touch()
        self.text = self.path.read_text().strip()
        self.data = self.text.split("\n")

    def __len__(self):
        return len(self.data)

    def __getitem__(self, i):
        return self.data[i]

    def keys(self):
        return self.data.keys()

    def cache_size(self):
        return len(self)

    def write_to_cache(self, id, messages, debug: bool = True):
        content = json.dumps({id: str(messages)})
        with open(self.path, "a") as f:
            write = print if debug else f.write
            write(content + "\n")


class Conversation(Cache, LMConfig):
    messages: deque[dict] = deque(maxlen=LMConfig.nhistbuf)

    def system_message(self) -> dict:
        return {"role": self.system_key, "content": self.system}

    @classmethod
    def from_history(cls, history: list[dict]) -> "Conversation":
        self = cls()
        self.messages = deque(history, maxlen=cls.nhistbuf)
        return self

    def __init__(self):
        super().__init__()
        self.id = str(self.cache_size() + 1).zfill(6)
        self.messages = deque(maxlen=self.nhistbuf)
        self.messages.append(self.system_message())

    def send_receive(self, messages, debug=False, **kwargs) -> dict:
        params = self.params_ | (kwargs or {})
        response = self.create(messages, **params)
        self.messages.append(response.message())
        self.write_to_cache(
            id=self.id,
            messages=self.messages,
            debug=debug,
        )

    def __call__(self, prompt: str) -> str:
        self.messages.append({"role": self.user_key, "content": prompt})
        self.send_receive(list(self.messages))
        print(self.messages[-1]["content"])
        return self.messages[-1]["content"]


class Agent(Conversation):
    def __init__(self):
        super().__init__()


agent = Agent()
agent("hello")

agent("bro what did you just say to me")
