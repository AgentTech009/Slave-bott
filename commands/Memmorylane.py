import discord
from discord.ext import commands
import asyncio

INSTAGRAM_DEFAULT_PFP = "https://i.imgur.com/8Km9tLL.png"


class MemoryLane(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def set_bot_nick(self, guild, name):
        me = guild.me
        try:
            await me.edit(nick=name)
        except discord.Forbidden:
            pass
        except discord.HTTPException:
            pass

    async def send_as(self, channel, webhook, guild, character_name, message):
        await self.set_bot_nick(guild, character_name)

        typing_time = max(1.5, min(len(message) * 0.08, 6))

        async with channel.typing():
            await asyncio.sleep(typing_time)

        await webhook.send(
            content=message,
            username=character_name,
            avatar_url=INSTAGRAM_DEFAULT_PFP,
            allowed_mentions=discord.AllowedMentions.none()
        )

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
                read_message_history=True
            )
        }

        channel = await guild.create_text_channel(
            name="July 18 2025",
            overwrites=overwrites
        )

        await ctx.send(f"🌙 Memory lane created. Enter {channel.mention}")

        webhook = await channel.create_webhook(name="Memory Lane")

        await asyncio.sleep(5)

        script = [
            ("A boy", "Mmh\nPinneh ondello"),
            ("A girl", "Aahmm"),
            ("A boy", "Neeyoru reply aloicho... 👀"),
            ("A girl", "Aahhh aloichuuu..."),
            ("A boy", "Enthaaaa👀"),
            ("narrator", "**Girl eating porotta while boy is dying out there**"),
            ("narrator", "**15 minutes later**"),
            ("A girl", "Aahhh athhhh"),
            ("A boy", "Athhh....👀"),
            ("A girl", "Enikkmm ninnee ishtavaaa"),
            ("A boy", "Ohhh 👀👀\nYay"),
            ("A girl", "Mhmmm😂"),
            ("A boy", "Pinneh enna kaichooo..."),
            ("narrator", "**And right there.. That was the beginning of one of God's most beautiful love stories...**")
        ]

        for character, message in script:
            if character == "narrator":
                await self.set_bot_nick(guild, "Narrator")
                async with channel.typing():
                    await asyncio.sleep(2)
                await channel.send(message)
            else:
                await self.send_as(channel, webhook, guild, character, message)

            await asyncio.sleep(1)

        try:
            await webhook.delete()
        except discord.HTTPException:
            pass


async def setup(bot):
    await bot.add_cog(MemoryLane(bot))
