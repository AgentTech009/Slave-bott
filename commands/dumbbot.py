from discord.ext import commands
import urllib.request
import urllib.error
import json
import os
import asyncio

CONFIG_FILE = "dumbbot_channel.json"

def get_key():
    return os.getenv("GROQ_API_KEY")

def load_config():
    if not os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "w") as f:
            json.dump({"channel_id": None}, f)

    with open(CONFIG_FILE, "r") as f:
        return json.load(f)

def save_config(data):
    with open(CONFIG_FILE, "w") as f:
        json.dump(data, f, indent=4)

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
                    "Be chaotic but harmless."
                )
            },
            {
                "role": "user",
                "content": message
            }
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
        self.config = load_config()

    @commands.command(name="setdumbbot")
    async def set_dumbbot(self, ctx):
        self.config["channel_id"] = ctx.channel.id
        save_config(self.config)
        await ctx.send(f"Dumb chatbot enabled in {ctx.channel.mention} 🧠💀")

    @commands.command(name="offdumbbot")
    async def off_dumbbot(self, ctx):
        self.config["channel_id"] = None
        save_config(self.config)
        await ctx.send("Dumb chatbot disabled 💀")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        if message.content.startswith("."):
            return

        if self.config.get("channel_id") != message.channel.id:
            return

        if not self.api_key:
            return await message.channel.send("Groq key missing. Add `GROQ_API_KEY` in Railway variables 💀")

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
