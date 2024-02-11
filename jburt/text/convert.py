import pathlib

from langchain.text_splitter import RecursiveCharacterTextSplitter
from openai import OpenAI

client = OpenAI()


def tts(body, outdir, fname="speech.mp3"):
    speech_file = pathlib.Path(str(outdir)) / fname
    response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=body,
    )
    with open(speech_file, "wb") as f:
        f.write(response.audio)


def dump(responses, outdir):
    for i, r in enumerate(responses):
        with open(outdir / f"response_{i}.txt", "w") as f:
            f.write(r.choices[0].message.content)


def split(text: str, chars: int = 4000) -> list[str]:
    return RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", " "],
        is_separator_regex=True,
        chunk_size=chars,
        chunk_overlap=0,
        length_function=len,
    ).split_text(text)
