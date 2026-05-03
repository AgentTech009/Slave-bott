import discord
from discord.ext import commands
import asyncio
import random

PFP_URL = "https://cdn.discordapp.com/attachments/1500472877210927197/1500564011161223229/images-12.jpg?ex=69f8e4a3&is=69f79323&hm=d603cc0c2c1f531a0f6b010f21cf42850dd53e661bb1766996c4d4b559b3669c&"


class MemoryLane(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def set_bot_nick(self, guild, name):
        try:
            await guild.me.edit(nick=name)
        except:
            pass

    def typing_time(self, msg):
        base = len(msg) * 0.12
        nervous_pause = random.uniform(1.5, 3.5)
        return max(2.5, min(base + nervous_pause, 10))

    async def send_as(self, channel, webhook, guild, name, text):
        parts = text.split("\n")

        for part in parts:
            part = part.strip()
            if not part:
                continue

            await self.set_bot_nick(guild, name)

            async with channel.typing():
                await asyncio.sleep(self.typing_time(part))

            await webhook.send(
                content=part,
                username=name,
                avatar_url=PFP_URL,
                allowed_mentions=discord.AllowedMentions.none()
            )

            await asyncio.sleep(random.uniform(0.8, 1.8))

    @commands.command(name="memmorylane")
    @commands.has_permissions(administrator=True)
    async def memmorylane(self, ctx):
        guild = ctx.guild

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            ctx.author: discord.PermissionOverwrite(
                view_channel=True,
                send_messages=True,
                read_message_history=True
            ),
            guild.me: discord.PermissionOverwrite(
                view_channel=True,
                send_messages=True,
                manage_channels=True,
                manage_webhooks=True,
                manage_nicknames=True,
                read_message_history=True
            )
        }

        channel = await guild.create_text_channel(
            name="July 18 2025",
            overwrites=overwrites
        )

        await ctx.send(f"🌙 Memory lane created. Enter {channel.mention}")

        boy_webhook = await channel.create_webhook(name="A boy")
        girl_webhook = await channel.create_webhook(name="A girl")
        narrator_webhook = await channel.create_webhook(name="Narrator")

        await asyncio.sleep(5)

        script = [
            ("Narrator", narrator_webhook, "**8:47**"),
            ("A boy", boy_webhook, "Mmh\nPinneh ondello"),
            ("A girl", girl_webhook, "Aahmm"),
            ("A boy", boy_webhook, "Neeyoru reply aloicho... 👀"),
            ("A girl", girl_webhook, "Aahhh aloichuuu..."),
            ("A boy", boy_webhook, "Enthaaaa👀"),

            ("Narrator", narrator_webhook, "**Girl eating porotta while boy is dying out there**"),
            ("Narrator", narrator_webhook, "**15 minutes later**"),

            ("A girl", girl_webhook, "Aahhh athhhh"),
            ("A boy", boy_webhook, "Athhh....👀"),
            ("A girl", girl_webhook, "Enikkmm ninnee ishtavaaa"),
            ("A boy", boy_webhook, "Ohhh 👀👀\nYay"),
            ("A girl", girl_webhook, "Mhmmm😂"),
            ("A boy", boy_webhook, "Pinneh enna kaichooo..."),

            (
                "Narrator",
                narrator_webhook,
                "And right there..\n"
                "That was the beginning of..\n"
                "one of gods most beautiful love stories...\n"
                "Babyy..\n"
                "I will always be with you🥹🥹\n"
                "I WILL ALWAYS LOVE YOU🥹🥹\n"
                "-your nervous little boy.."
            )
        ]

        for name, webhook, message in script:
            await send_typing_and_message(channel, webhook, guild, name, message)
            await asyncio.sleep(random.uniform(1, 2))

        for webhook in [boy_webhook, girl_webhook, narrator_webhook]:
            try:
                await webhook.delete()
            except:
                pass


async def send_typing_and_message(channel, webhook, guild, name, text):
    parts = text.split("\n")

    for part in parts:
        part = part.strip()
        if not part:
            continue

        try:
            await guild.me.edit(nick=name)
        except:
            pass

        typing_seconds = max(
            2.5,
            min(len(part) * 0.14 + random.uniform(2, 4), 12)
        )

        async with channel.typing():
            await asyncio.sleep(typing_seconds)

        await webhook.send(
            content=part,
            username=name,
            avatar_url=PFP_URL,
            allowed_mentions=discord.AllowedMentions.none()
        )

        await asyncio.sleep(random.uniform(0.8, 1.8))


async def setup(bot):
    await bot.add_cog(MemoryLane(bot))
