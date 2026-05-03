import discord
from discord.ext import commands
import asyncio
import random

GIRL_PFP = "https://cdn.discordapp.com/attachments/1500472877210927197/1500573861866115234/IMG_20260504_003425.jpg?ex=69f8edcf&is=69f79c4f&hm=baeaf89fd0d95b2b8d19fe4af0397015ee82ddc409586d0ab3a11ae93f2e3c53&"
BOY_PFP = "https://cdn.discordapp.com/attachments/1500472877210927197/1500573862146867391/50d7438ff1dd2822ed0cf84e7aaf4965.jpg?ex=69f8edd0&is=69f79c50&hm=57ee1f5c8cbba303bd4df99f5b7cb178d83b5653890b05da29bda600b95b259a&"
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

        return max(2.0, min(len(msg) * 0.12 + random.uniform(1.5, 3.2), 9))

    async def send_as(self, channel, webhook, guild, name, text, pfp, narrator=False):
        parts = text.split("\n")

        for part in parts:
            part = part.strip()
            if not part:
                continue

            await self.set_bot_nick(guild, name)

            async with channel.typing():
                await asyncio.sleep(self.typing_time(part, narrator))

            try:
                await webhook.send(
                    content=part,
                    username=name,
                    avatar_url=pfp,
                    allowed_mentions=discord.AllowedMentions.none()
                )
            except Exception as e:
                await channel.send(f"Error sending message: `{e}`")
                continue

            await asyncio.sleep(random.uniform(0.4, 0.9) if narrator else random.uniform(0.8, 1.6))

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
            name="july-18-2025",
            overwrites=overwrites
        )

        await ctx.send(f"🌙 Memory lane created. Enter {channel.mention}")

        boy_webhook = await channel.create_webhook(name="kokachi._")
        girl_webhook = await channel.create_webhook(name="_sara_")
        narrator_webhook = await channel.create_webhook(name="Narrator")

        await asyncio.sleep(5)

        script = [
            ("Narrator", narrator_webhook, "**8:47**", NARRATOR_PFP, True),

            ("kokachi._", boy_webhook, "Mmh\nPinneh ondello", BOY_PFP, False),
            ("_sara_", girl_webhook, "Aahmm", GIRL_PFP, False),
            ("kokachi._", boy_webhook, "Neeyoru reply aloicho... 👀", BOY_PFP, False),
            ("_sara_", girl_webhook, "Aahhh aloichuuu...", GIRL_PFP, False),
            ("kokachi._", boy_webhook, "Enthaaaa👀", BOY_PFP, False),

            ("Narrator", narrator_webhook, "**Girl eating porotta while boy is dying out there**", NARRATOR_PFP, True),
            ("Narrator", narrator_webhook, "**15 minutes later**", NARRATOR_PFP, True),

            ("_sara_", girl_webhook, "Aahhh athhhh", GIRL_PFP, False),
            ("kokachi._", boy_webhook, "Athhh....👀", BOY_PFP, False),
            ("_sara_", girl_webhook, "Enikkmm ninnee ishtavaaa", GIRL_PFP, False),
            ("kokachi._", boy_webhook, "Ohhh 👀👀\nYay", BOY_PFP, False),
            ("_sara_", girl_webhook, "Mhmmm😂", GIRL_PFP, False),
            ("kokachi._", boy_webhook, "Pinneh enna kaichooo...", BOY_PFP, False),

            ("Narrator", narrator_webhook, "And right there..\nThat was the beginning of..\none of gods most beautiful love stories...", NARRATOR_PFP, True),

            ("kokachi._", boy_webhook, "Babyy..\nI will always be with you🥹🥹\nI WILL ALWAYS LOVE YOU🥹🥹\n-your nervous little boy..", BOY_PFP, False)
        ]

        for name, webhook, message, pfp, narrator in script:
            await self.send_as(channel, webhook, guild, name, message, pfp, narrator)
            await asyncio.sleep(random.uniform(0.5, 1.2))

        for webhook in [boy_webhook, girl_webhook, narrator_webhook]:
            try:
                await webhook.delete()
            except:
                pass


async def setup(bot):
    await bot.add_cog(MemoryLane(bot))
