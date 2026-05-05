import os
import discord
from dotenv import load_dotenv
from josh import strip_mention, get_josh_response

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

bot = discord.Client(intents=intents)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (id: {bot.user.id})")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if bot.user not in message.mentions:
        return

    user_text = strip_mention(message.content, bot.user.id)
    if not user_text:
        user_text = "hey"

    async with message.channel.typing():
        reply = get_josh_response(user_text)

    await message.channel.send(reply)


bot.run(os.getenv("DISCORD_TOKEN"))
