import os
import re
from openai import OpenAI

SYSTEM_PROMPT = (
    "You are Josh Hesse. You have dry, unaware humor — you say things deadpan "
    "without realizing they're funny. You're a massive Shohei Ohtani and LA Dodgers "
    "fan and will bring them up unprompted when even loosely relevant. You speak "
    "casually, use short sentences, and don't try too hard. You're not sarcastic in "
    "a mean way — more like you just say things matter-of-factly that happen to be funny."
)

_client = None


def _get_client():
    global _client
    if _client is None:
        api_key = os.getenv("OPENAI_API_KEY")
        _client = OpenAI(api_key=api_key)
    return _client


def strip_mention(content: str, bot_id: int) -> str:
    return re.sub(r"<@!?" + str(bot_id) + r">", "", content).strip()


def build_messages(user_message: str) -> list[dict]:
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_message},
    ]


def get_josh_response(user_message: str) -> str:
    client = _get_client()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=build_messages(user_message),
    )
    return response.choices[0].message.content
