import asyncio
import os

import discord
from dotenv import load_dotenv

from josh import get_josh_response, strip_mention

load_dotenv()


def _require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"{name} environment variable is not set")
    return value


intents = discord.Intents.default()
intents.message_content = True

bot = discord.Client(intents=intents)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (id: {bot.user.id})")


@bot.event
async def on_message(message):
    if message.author.bot:
        return
    if bot.user not in message.mentions:
        return

    user_text = strip_mention(message.content, bot.user.id)
    if not user_text:
        user_text = "hey"

    async with message.channel.typing():
        loop = asyncio.get_event_loop()
        try:
            reply = await loop.run_in_executor(None, get_josh_response, user_text)
        except Exception:
            reply = "Something broke. Probably not Ohtani's fault."

    await message.channel.send(reply)


bot.run(_require_env("DISCORD_TOKEN"))
