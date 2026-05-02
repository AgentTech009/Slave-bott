from discord.ext import commands
import urllib.request
import urllib.error
import json
import os
import asyncio

DUMBBOT_CHANNEL_ID = 1496866222237548697

def get_key():
    return os.getenv("GROQ_API_KEY")

def ask_groq(api_key, message):
    url = "https://api.groq.com/openai/v1/chat/completions"

    data = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a funny dumb Discord chatbot. "
                    "Reply very short. Use silly Gen Z humor. "
                    "Act confused sometimes. Do not be smart unless asked. "
                    "No long answers. No serious essays. "
                    "Be chaotic but harmless."
                )
            },
            {"role": "user", "content": message}
        ],
        "temperature": 1.1,
        "max_tokens": 80
    }

    body = json.dumps(data).encode("utf-8")

    req = urllib.request.Request(
        url,
        data=body,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
            "User-Agent": "Mozilla/5.0"
        },
        method="POST"
    )

    with urllib.request.urlopen(req, timeout=60) as response:
        result = json.loads(response.read().decode())

    return result["choices"][0]["message"]["content"]

class DumbBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.api_key = get_key()

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        if message.content.startswith("."):
            return

        if message.channel.id != DUMBBOT_CHANNEL_ID:
            return

        if not self.api_key:
            return await message.channel.send("Groq key missing in `.env` 💀")

        async with message.channel.typing():
            try:
                reply = await asyncio.to_thread(
                    ask_groq,
                    self.api_key,
                    message.content
                )

                if len(reply) > 1900:
                    reply = reply[:1900] + "..."

                await message.reply(reply, mention_author=False)

            except urllib.error.HTTPError as e:
                error_text = e.read().decode("utf-8")
                await message.channel.send(f"Groq error:\n```{error_text[:1500]}```")

            except Exception as e:
                await message.channel.send(f"brain exploded: `{e}`")

async def setup(bot):
    await bot.add_cog(DumbBot(bot))
