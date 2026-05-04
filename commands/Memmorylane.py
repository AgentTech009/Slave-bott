import discord
from discord.ext import commands
import asyncio
import random

GIRL_NAME = "linet_sara_"
BOY_NAME = "kokachi._"
NARRATOR_NAME = "Narrator"
FINAL_BOY_NAME = "niranjannnnnn.____"

GIRL_PFP = "https://cdn.discordapp.com/attachments/1500472877210927197/1500573861866115234/IMG_20260504_003425.jpg?ex=69f8edcf&is=69f79c4f&hm=baeaf89fd0d95b2b8d19fe4af0397015ee82ddc409586d0ab3a11ae93f2e3c53&"
BOY_PFP = "https://cdn.discordapp.com/attachments/1500472877210927197/1500573862146867391/50d7438ff1dd2822ed0cf84e7aaf4965.jpg?ex=69f8edd0&is=69f79c50&hm=57ee1f5c8cbba303bd4df99f5b7cb178d83b5653890b05da29bda600b95b259a&"
NARRATOR_PFP = "https://cdn-icons-png.flaticon.com/512/833/833472.png"
FINAL_BOY_PFP = "https://cdn.discordapp.com/attachments/1500472877210927197/1500578549000700038/533388631_18070949531471399_510634509294917079_n.jpg?ex=69f8f22d&is=69f7a0ad&hm=b426d103eda23a1de09a3070dbe2aa0c5b801af90576d2061c47e98e4f23430b&"


class MemoryLane(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.current_typing_name = None

    def typing_time(self, msg, narrator=False):
        if narrator:
            return random.uniform(0.6, 1.4)

        return max(2.0, min(len(msg) * 0.12 + random.uniform(1.3, 2.8), 8.0))

    async def safe_change_nick(self, guild, name):
        if self.current_typing_name == name:
            return

        self.current_typing_name = name

        try:
            await asyncio.wait_for(guild.me.edit(nick=name), timeout=2.5)
        except:
            pass

    async def fake_typing_only(self, channel, guild, name, seconds):
        await self.safe_change_nick(guild, name)

        async with channel.typing():
            await asyncio.sleep(seconds)

    async def send_as(self, channel, webhook, guild, name, text, pfp, narrator=False):
        parts = text.split("\n")

        for part in parts:
            part = part.strip()
            if not part:
                continue

            await asyncio.sleep(5)

            await self.safe_change_nick(guild, name)

            async with channel.typing():
                await asyncio.sleep(self.typing_time(part, narrator))

            await webhook.send(
                content=part,
                username=name,
                avatar_url=pfp,
                allowed_mentions=discord.AllowedMentions.none()
            )

            if part == "Athhh....👀":
                await asyncio.sleep(8)

    @commands.command(name="memmorylane")
    @commands.has_permissions(administrator=True)
    async def memmorylane(self, ctx):
        guild = ctx.guild
        self.current_typing_name = None

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
            name="july-18-2025",
            overwrites=overwrites
        )

        await ctx.send(f"🌙 Memory lane created. Enter {channel.mention}")

        boy_webhook = await channel.create_webhook(name=BOY_NAME)
        girl_webhook = await channel.create_webhook(name=GIRL_NAME)
        narrator_webhook = await channel.create_webhook(name=NARRATOR_NAME)
        final_webhook = await channel.create_webhook(name=FINAL_BOY_NAME)

        await asyncio.sleep(5)

        script = [
            (NARRATOR_NAME, narrator_webhook, "**8:47**", NARRATOR_PFP, True),

            (BOY_NAME, boy_webhook, "Mmh\nPinneh ondello", BOY_PFP, False),
            (GIRL_NAME, girl_webhook, "Aahmm", GIRL_PFP, False),
            (BOY_NAME, boy_webhook, "Neeyoru reply aloicho... 👀", BOY_PFP, False),
            (GIRL_NAME, girl_webhook, "Aahhh aloichuuu...", GIRL_PFP, False),
            (BOY_NAME, boy_webhook, "Enthaaaa👀", BOY_PFP, False),

            (NARRATOR_NAME, narrator_webhook, "**The girl went to eat porotta while the boy was dying..**", NARRATOR_PFP, True),
            (NARRATOR_NAME, narrator_webhook, "**15 minutes later...**", NARRATOR_PFP, True),

            (GIRL_NAME, girl_webhook, "Aahhh athhhh", GIRL_PFP, False),
            (BOY_NAME, boy_webhook, "Athhh....👀", BOY_PFP, False),
            (GIRL_NAME, girl_webhook, "Enikkmm ninnee ishtavaaa", GIRL_PFP, False),
            (BOY_NAME, boy_webhook, "Ohhh 👀👀\nYay", BOY_PFP, False),
            (GIRL_NAME, girl_webhook, "Mhmmm😂", GIRL_PFP, False),
            (BOY_NAME, boy_webhook, "Pinneh enna kaichooo...", BOY_PFP, False),

            (
                NARRATOR_NAME,
                narrator_webhook,
                "**And right there..**\n"
                "**That was the beginning of..**\n"
                "**One of gods most beautiful love stories...**",
                NARRATOR_PFP,
                True
            )
        ]

        for name, webhook, message, pfp, narrator in script:
            await self.send_as(channel, webhook, guild, name, message, pfp, narrator)

        await asyncio.sleep(5)

        await self.fake_typing_only(channel, guild, "someone", 5)

        final_lines = [
            "Babyy..🥹🥹",
            "I will always be with you🥹🥹",
            "I WILL ALWAYS LOVE YOU🥹🥹",
            "MWAAAAAAAHHHH🥹🥹🥹🥹🥹💋💋💋💋💋💋💋💋💋💋"
        ]

        first = True

        for line in final_lines:
            await asyncio.sleep(5)

            if not first:
                await self.fake_typing_only(channel, guild, FINAL_BOY_NAME, 2)

            await final_webhook.send(
                content=line,
                username=FINAL_BOY_NAME,
                avatar_url=FINAL_BOY_PFP,
                allowed_mentions=discord.AllowedMentions.none()
            )

            first = False

        for webhook in [boy_webhook, girl_webhook, narrator_webhook, final_webhook]:
            try:
                await webhook.delete()
            except:
                pass


async def setup(bot):
    await bot.add_cog(MemoryLane(bot))
