import json
import pathlib
from collections import deque
from os import environ as e_
from typing import Any

import openai
from openai.types.chat import ChatCompletion

from jburt.objects import dotdict

__all__ = ["Conversation", "Response", "Cache", "ConvoCache"]


class CacheConfig:
    dir = pathlib.Path(e_["HOME"]) / "Downloads" / "my-openai-history"
    dir.mkdir(exist_ok=True, parents=True)

    filename = "jburt-openai-message-dataset.jsonl"
    path = dir / filename

    system_key = "system"
    user_key = "user"
    assistant_key = "assistant"


class Response:
    """

    Attributes:
        response         : openai.types.chat.ChatCompletion response object.
        model       (str): The chat model.
        fingerprint (str): The backend configuration.
        id          (str): A unique identifier for the chat completion.
        created     (int): Unix timestamp (s) of when completion was created.
        role        (str): The role assigned to the responder.
        content     (str): The content of the response.

    """

    def __init__(self, response: ChatCompletion):
        super().__init__()
        self.id: str = response.id
        self.model: str = response.model
        self.fingerprint: str = response.system_fingerprint
        self.role: str = response.choices[0].message.role
        self.content: str = response.choices[0].message.content
        self.created: int = response.created
        self.usage: dict = response.usage.model_dump_json()
        self.response = response

    def to_msg(self) -> dict:
        return {"role": self.role, "content": self.content}

    def to_json(self) -> dict:
        return {
            "model": self.model,
            "id": self.id,
            "fingerprint": self.fingerprint,
            "role": self.role,
            "content": self.content,
            "created": self.created,
        } | self.usage


class Role:
    pass


class MLE(Role):
    assignment = "you are an expert ML engineer and sysadmin.\n---\n"


class Model:
    client: Any = None
    max_hist_len = 10  # max length of convo history
    model = "gpt-4-1106-preview"
    temperature = 0.0
    max_tokens = 128
    stream = False

    def __init__(self, system=MLE.assignment) -> None:
        self.client = openai.OpenAI()
        self.system = system

    def create(self, messages, **kwargs):
        kw = self.get_api_params() | kwargs
        return Response(
            self.client.chat.completions.create(
                messages=messages,
                **kw,
            )
        )

    def get_api_params(self):
        return dotdict(
            model=self.model,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            stream=self.stream,
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


class Conversation(Cache, Model):
    _messages: deque[dict] = deque(maxlen=Model.max_hist_len)

    @classmethod
    def from_history(cls, history: list[dict]) -> "Conversation":
        self = cls()
        self._messages = deque(history, maxlen=cls.max_hist_len)
        return self

    def __init__(self):
        super().__init__()
        self.id = str(self.cache_size() + 1).zfill(6)

        self._messages = deque(maxlen=self.max_hist_len)
        self._messages.append(self.system_message())

        self.last_response = None

    def send_receive(self, messages, debug=False, **kwargs) -> dict:
        params = self.get_api_params | (kwargs or {})
        response = self.last_response = self.create(messages, **params)
        self._messages.append(response.to_msg())
        self.write_to_cache(id=self.id, messages=self._messages, debug=debug)

    def __call__(self, prompt: str) -> str:
        self._messages.append({"role": self.user_key, "content": prompt})
        self.send_receive(list(self._messages))
        print(self._messages[-1]["content"])
        return self._messages[-1]["content"]

    def system_message(self) -> dict:
        return {"role": self.system_key, "content": self.system}

    @property
    def messages(self) -> list[dict]:
        return list(self._messages)


# alias
Convo = Conversation


class Agent:
    def __init__(self):
        super().__init__()


agent = Agent()
agent("hello")
