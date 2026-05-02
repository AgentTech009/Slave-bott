from discord.ext import commands
import discord
import random
import json
import os

CONFIG_FILE = "koni_config.json"

CAT_AVATAR_URL = "https://cdn.discordapp.com/attachments/1500100689924194326/1500100763815252079/IMG-20260421-WA0051-1.jpg?ex=69f73534&is=69f5e3b4&hm=97abec711668fed3434ceed9e7284d4bc9a6fa3cebdd23425f58c81c7b2d658e&"

# BIG DUMB CAT LIST 😈
MEOWS = [
    "meow",
    "mew",
    "mrrp",
    "nya",
    "mreow",
    "prrr",
    "meow.",
    "meow??",
    "MEOW",
    "meow bro",
    "mew what",
    "mrrp 😭",
    "nyaaa",
    "mreow??",
    "prrrr",
    "meow fr",
    "mew moment",
    "meow 💀",
    "mrrp real",
    "nya pls",
    "mreow?? bro",
    "prrr stop",
    "meow idk",
    "mew ok",
    "mrrp nah",
    "nya what is that",
    "mreow explain",
    "prrr suspicious",
    "meow certified",
    "mew brainrot",
    "mrrp 🧠",
    "nya lowkey",
    "mreow highkey",
    "prrr that’s crazy",
    "meow who asked",
    "mew no way",
    "mrrp skill issue",
    "nya 😭",
    "mreow 💀",
    "prrr fr",
    "meow that’s wild",
    "mew explain yourself",
    "mrrp huh",
    "nyaaaa",
    "mreow ok bro",
    "prrr alright",
    "meow real talk",
    "mew interesting",
    "mrrp wait",
    "nya chill",
    "mreow relax",
    "prrr calm down"
]

def load_config():
    if not os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "w") as f:
            json.dump({"channel_id": None, "webhook_url": None}, f)

    with open(CONFIG_FILE, "r") as f:
        return json.load(f)

def save_config(data):
    with open(CONFIG_FILE, "w") as f:
        json.dump(data, f, indent=4)

class Koni(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = load_config()

    @commands.command(name="setkoni")
    @commands.has_permissions(manage_webhooks=True)
    async def setkoni(self, ctx):
        webhook = await ctx.channel.create_webhook(name="Koni")

        self.config["channel_id"] = ctx.channel.id
        self.config["webhook_url"] = webhook.url
        save_config(self.config)

        await ctx.send("Koni enabled 🐈")

    @commands.command(name="offkoni")
    @commands.has_permissions(manage_webhooks=True)
    async def offkoni(self, ctx):
        self.config["channel_id"] = None
        self.config["webhook_url"] = None
        save_config(self.config)

        await ctx.send("Koni off 😿")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        if message.content.startswith("."):
            return

        if message.channel.id != self.config.get("channel_id"):
            return

        webhook_url = self.config.get("webhook_url")
        if not webhook_url:
            return

        reply = random.choice(MEOWS)  # ONE message only now

        try:
            webhook = discord.Webhook.from_url(
                webhook_url,
                session=self.bot.http._HTTPClient__session
            )

            await webhook.send(
                reply,
                username="Koni",
                avatar_url=CAT_AVATAR_URL
            )

        except Exception as e:
            print(f"Koni error: {e}")

async def setup(bot):
    await bot.add_cog(Koni(bot))
