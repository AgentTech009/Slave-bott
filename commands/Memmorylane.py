import discord
from discord.ext import commands
import asyncio
import random

BOY_GIRL_PFP = "https://cdn.discordapp.com/attachments/1500472877210927197/1500564011161223229/images-12.jpg?ex=69f8e4a3&is=69f79323&hm=d603cc0c2c1f531a0f6b010f21cf42850dd53e661bb1766996c4d4b559b3669c&"

NARRATOR_PFP = "https://cdn-icons-png.flaticon.com/512/833/833472.png"


class MemoryLane(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def set_bot_nick(self, guild, name):
        try:
            await guild.me.edit(nick=name)
        except:
            pass

    def typing_time(self, msg, narrator=False):
        if narrator:
            return random.uniform(0.5, 1.5)

        base = len(msg) * 0.10
        nervous = random.uniform(1.5, 3.0)
        return max(2.0, min(base + nervous, 8.5))

    async def send_as(self, channel, webhook, guild, name, text, pfp, narrator=False):
        parts = text.split("\n")

        for part in parts:
            part = part.strip()
            if not part:
                continue

            await self.set_bot_nick(guild, name)

            async with channel.typing():
                await asyncio.sleep(self.typing_time(part, narrator=narrator))

            await webhook.send(
                content=part,
                username=name,
                avatar_url=pfp,
                allowed_mentions=discord.AllowedMentions.none()
            )

            if narrator:
                await asyncio.sleep(random.uniform(0.4, 0.8))
            else:
                await asyncio.sleep(random.uniform(0.8, 1.5))

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
            ("Narrator", narrator_webhook, "**8:47**", NARRATOR_PFP, True),

            ("A boy", boy_webhook, "Mmh\nPinneh ondello", BOY_GIRL_PFP, False),
            ("A girl", girl_webhook, "Aahmm", BOY_GIRL_PFP, False),
            ("A boy", boy_webhook, "Neeyoru reply aloicho... 👀", BOY_GIRL_PFP, False),
            ("A girl", girl_webhook, "Aahhh aloichuuu...", BOY_GIRL_PFP, False),
            ("A boy", boy_webhook, "Enthaaaa👀", BOY_GIRL_PFP, False),

            ("Narrator", narrator_webhook, "**Girl eating porotta while boy is dying out there**", NARRATOR_PFP, True),
            ("Narrator", narrator_webhook, "**15 minutes later**", NARRATOR_PFP, True),

            ("A girl", girl_webhook, "Aahhh athhhh", BOY_GIRL_PFP, False),
            ("A boy", boy_webhook, "Athhh....👀", BOY_GIRL_PFP, False),
            ("A girl", girl_webhook, "Enikkmm ninnee ishtavaaa", BOY_GIRL_PFP, False),
            ("A boy", boy_webhook, "Ohhh 👀👀\nYay", BOY_GIRL_PFP, False),
            ("A girl", girl_webhook, "Mhmmm😂", BOY_GIRL_PFP, False),
            ("A boy", boy_webhook, "Pinneh enna kaichooo...", BOY_GIRL_PFP, False),

            (
                "Narrator",
                narrator_webhook,
                "And right there..\n"
                "That was the beginning of..\n"
                "one of gods most beautiful love stories...\n"
                "Babyy..\n"
                "I will always be with you🥹🥹\n"
                "I WILL ALWAYS LOVE YOU🥹🥹\n"
                "-your nervous little boy..",
                NARRATOR_PFP,
                True
            )
        ]

        for name, webhook, message, pfp, narrator in script:
            await self.send_as(channel, webhook, guild, name, message, pfp, narrator)
            await asyncio.sleep(0.6 if narrator else random.uniform(1.0, 1.8))

        for webhook in [boy_webhook, girl_webhook, narrator_webhook]:
            try:
                await webhook.delete()
            except:
                pass


async def setup(bot):
    await bot.add_cog(MemoryLane(bot))
