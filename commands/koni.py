
from discord.ext import commands
import discord
import random

# 🔒 HARD CODED CHANNEL
KONI_CHANNEL_ID = 1499789770568765571

CAT_AVATAR_URL = "https://cdn.discordapp.com/attachments/1500100689924194326/1500100763815252079/IMG-20260421-WA0051-1.jpg"

MEOWS = [
    "meow","mew","mrrp","nya","mreow","prrr","meow.","meow??","MEOW",
    "meow bro","mew what","mrrp 😭","nyaaa","mreow??","prrrr","meow fr",
    "mew moment","meow 💀","mrrp real","nya pls","mreow?? bro","prrr stop",
    "meow idk","mew ok","mrrp nah","nya what is that","mreow explain",
    "prrr suspicious","meow certified","mew brainrot","mrrp 🧠",
    "nya lowkey","mreow highkey","prrr that’s crazy","meow who asked",
    "mew no way","mrrp skill issue","nya 😭","mreow 💀","prrr fr",
    "meow that’s wild","mew explain yourself","mrrp huh","nyaaaa",
    "mreow ok bro","prrr alright","meow real talk","mew interesting",
    "mrrp wait","nya chill","mreow relax","prrr calm down"
]

class Koni(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.webhook = None

    async def get_webhook(self, channel):
        webhooks = await channel.webhooks()

        for wh in webhooks:
            if wh.name == "Koni":
                return wh

        return await channel.create_webhook(name="Koni")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        if message.content.startswith("."):
            return

        if message.channel.id != KONI_CHANNEL_ID:
            return

        reply = random.choice(MEOWS)

        try:
            if not self.webhook:
                self.webhook = await self.get_webhook(message.channel)

            await self.webhook.send(
                reply,
                username="Koni",
                avatar_url=CAT_AVATAR_URL
            )

        except Exception as e:
            print(f"Koni error: {e}")

async def setup(bot):
    await bot.add_cog(Koni(bot))
