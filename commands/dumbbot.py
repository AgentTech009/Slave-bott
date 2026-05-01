from discord.ext import commands
import urllib.request
import json
import os
import asyncio

KEY_FILE = "groq_key.txt"
CONFIG_FILE = "dumbbot_channel.json"

def get_key():
    if not os.path.exists(KEY_FILE):
        return None

    with open(KEY_FILE, "r") as f:
        key = f.read().strip()

    if not key or key == "PASTE_GROQ_KEY_HERE":
        return None

    return key

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
                    "No long answers. No serious essays. "
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
    @commands.has_permissions(administrator=True)
    async def set_dumbbot(self, ctx):
        self.config["channel_id"] = ctx.channel.id
        save_config(self.config)

        await ctx.send(f"Dumb chatbot enabled in {ctx.channel.mention} 🧠💀")

    @commands.command(name="offdumbbot")
    @commands.has_permissions(administrator=True)
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

        channel_id = self.config.get("channel_id")

        if channel_id is None:
            return

        if message.channel.id != channel_id:
            return

        if not self.api_key:
            return await message.channel.send("no groq key bro im broke 💀")

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

            except Exception as e:
                await message.channel.send(f"brain exploded: `{e}`")

async def setup(bot):
    await bot.add_cog(DumbBot(bot))