import discord
from discord.ext import commands
import asyncio
import random

PRIEST_NAME = "Priest"
NARRATOR_NAME = "Narrator"

PRIEST_PFP = "https://cdn-icons-png.flaticon.com/512/1995/1995574.png"
NARRATOR_PFP = "https://cdn-icons-png.flaticon.com/512/833/833472.png"


class MarriageSetup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.current_typing_name = None

    async def safe_change_nick(self, guild, name):
        if self.current_typing_name == name:
            return

        self.current_typing_name = name

        try:
            await asyncio.wait_for(guild.me.edit(nick=name), timeout=2.5)
        except:
            pass

    async def bot_type(self, channel, guild, name):
        await self.safe_change_nick(guild, name)
        async with channel.typing():
            await asyncio.sleep(random.uniform(0.5, 1.5))

    async def send_webhook(self, channel, guild, webhook, name, pfp, text):
        parts = text.split("\n")

        for part in parts:
            part = part.strip()
            if not part:
                continue

            await asyncio.sleep(1)

            await self.bot_type(channel, guild, name)

            await webhook.send(
                content=part,
                username=name,
                avatar_url=pfp,
                allowed_mentions=discord.AllowedMentions.none()
            )

    async def wait_for_exact(self, ctx, user, text):
        def check(msg):
            return (
                msg.channel == ctx.channel
                and msg.author.id == user.id
                and msg.content.lower().strip() == text.lower()
            )

        while True:
            try:
                msg = await self.bot.wait_for("message", check=check, timeout=120)
                return msg
            except asyncio.TimeoutError:
                await ctx.send(f"{user.mention} reply with `{text}` 😭")

    async def wait_for_any(self, ctx, user):
        def check(msg):
            return msg.channel == ctx.channel and msg.author.id == user.id

        while True:
            try:
                msg = await self.bot.wait_for("message", check=check, timeout=180)
                return msg
            except asyncio.TimeoutError:
                await ctx.send(f"{user.mention} send your vow bro 😭")

    @commands.command(name="marriagesetup")
    @commands.has_permissions(administrator=True)
    async def marriagesetup(self, ctx, partner: discord.Member):
        if partner.bot:
            return await ctx.send("You cannot marry a bot 💀")

        if partner.id == ctx.author.id:
            return await ctx.send("Bro tried to marry himself 😭")

        guild = ctx.guild
        self.current_typing_name = None

        priest_webhook = await ctx.channel.create_webhook(name=PRIEST_NAME)
        narrator_webhook = await ctx.channel.create_webhook(name=NARRATOR_NAME)

        try:
            await self.send_webhook(
                ctx.channel, guild, narrator_webhook, NARRATOR_NAME, NARRATOR_PFP,
                "💒 The wedding begins..."
            )

            await self.send_webhook(
                ctx.channel, guild, narrator_webhook, NARRATOR_NAME, NARRATOR_PFP,
                f"Dearly beloved..."
            )

            await self.send_webhook(
                ctx.channel, guild, narrator_webhook, NARRATOR_NAME, NARRATOR_PFP,
                f"We are gathered here today before God and this server."
            )

            await self.send_webhook(
                ctx.channel, guild, narrator_webhook, NARRATOR_NAME, NARRATOR_PFP,
                f"To witness the union of {ctx.author.mention} and {partner.mention}."
            )

            await self.send_webhook(
                ctx.channel, guild, narrator_webhook, NARRATOR_NAME, NARRATOR_PFP,
                "If anyone has any reason why these two should not be married..."
            )

            await self.send_webhook(
                ctx.channel, guild, narrator_webhook, NARRATOR_NAME, NARRATOR_PFP,
                "Too bad."
            )

            await self.send_webhook(
                ctx.channel, guild, narrator_webhook, NARRATOR_NAME, NARRATOR_PFP,
                "We do not care 💀"
            )

            await self.send_webhook(
                ctx.channel, guild, priest_webhook, PRIEST_NAME, PRIEST_PFP,
                f"{ctx.author.mention}, step forward."
            )

            await self.send_webhook(
                ctx.channel, guild, priest_webhook, PRIEST_NAME, PRIEST_PFP,
                f"Do you take {partner.mention} to be your partner?"
            )

            await self.send_webhook(
                ctx.channel, guild, priest_webhook, PRIEST_NAME, PRIEST_PFP,
                "To love her."
            )

            await self.send_webhook(
                ctx.channel, guild, priest_webhook, PRIEST_NAME, PRIEST_PFP,
                "To care for her."
            )

            await self.send_webhook(
                ctx.channel, guild, priest_webhook, PRIEST_NAME, PRIEST_PFP,
                "And to stay with her even when she takes 15 minutes to reply?"
            )

            await ctx.send(f"{ctx.author.mention} type `I do`")

            await self.wait_for_exact(ctx, ctx.author, "I do")

            await self.send_webhook(
                ctx.channel, guild, priest_webhook, PRIEST_NAME, PRIEST_PFP,
                f"{partner.mention}, step forward."
            )

            await self.send_webhook(
                ctx.channel, guild, priest_webhook, PRIEST_NAME, PRIEST_PFP,
                f"Do you take {ctx.author.mention} to be your partner?"
            )

            await self.send_webhook(
                ctx.channel, guild, priest_webhook, PRIEST_NAME, PRIEST_PFP,
                "To love him."
            )

            await self.send_webhook(
                ctx.channel, guild, priest_webhook, PRIEST_NAME, PRIEST_PFP,
                "To support him."
            )

            await self.send_webhook(
                ctx.channel, guild, priest_webhook, PRIEST_NAME, PRIEST_PFP,
                "And to deal with his overthinking?"
            )

            await ctx.send(f"{partner.mention} type `I do`")

            await self.wait_for_exact(ctx, partner, "I do")

            await self.send_webhook(
                ctx.channel, guild, narrator_webhook, NARRATOR_NAME, NARRATOR_PFP,
                "💍 Ring exchange time."
            )

            await self.send_webhook(
                ctx.channel, guild, priest_webhook, PRIEST_NAME, PRIEST_PFP,
                f"{ctx.author.mention} send 💍"
            )

            await self.wait_for_exact(ctx, ctx.author, "💍")

            await self.send_webhook(
                ctx.channel, guild, priest_webhook, PRIEST_NAME, PRIEST_PFP,
                f"{partner.mention} send 💍"
            )

            await self.wait_for_exact(ctx, partner, "💍")

            await self.send_webhook(
                ctx.channel, guild, narrator_webhook, NARRATOR_NAME, NARRATOR_PFP,
                "The rings have been exchanged."
            )

            await self.send_webhook(
                ctx.channel, guild, priest_webhook, PRIEST_NAME, PRIEST_PFP,
                "Now speak your vows."
            )

            await self.send_webhook(
                ctx.channel, guild, priest_webhook, PRIEST_NAME, PRIEST_PFP,
                f"{ctx.author.mention}, send your custom vow."
            )

            vow1 = await self.wait_for_any(ctx, ctx.author)

            await self.send_webhook(
                ctx.channel, guild, priest_webhook, PRIEST_NAME, PRIEST_PFP,
                "Beautiful..."
            )

            await self.send_webhook(
                ctx.channel, guild, priest_webhook, PRIEST_NAME, PRIEST_PFP,
                f"{partner.mention}, send your custom vow."
            )

            vow2 = await self.wait_for_any(ctx, partner)

            await self.send_webhook(
                ctx.channel, guild, narrator_webhook, NARRATOR_NAME, NARRATOR_PFP,
                "The vows have been spoken."
            )

            await self.send_webhook(
                ctx.channel, guild, narrator_webhook, NARRATOR_NAME, NARRATOR_PFP,
                f"{ctx.author.mention} promised:"
            )

            await self.send_webhook(
                ctx.channel, guild, narrator_webhook, NARRATOR_NAME, NARRATOR_PFP,
                f"“{vow1.content}”"
            )

            await self.send_webhook(
                ctx.channel, guild, narrator_webhook, NARRATOR_NAME, NARRATOR_PFP,
                f"{partner.mention} promised:"
            )

            await self.send_webhook(
                ctx.channel, guild, narrator_webhook, NARRATOR_NAME, NARRATOR_PFP,
                f"“{vow2.content}”"
            )

            await self.send_webhook(
                ctx.channel, guild, narrator_webhook, NARRATOR_NAME, NARRATOR_PFP,
                "The moment we have all been waiting for..."
            )

            await self.send_webhook(
                ctx.channel, guild, priest_webhook, PRIEST_NAME, PRIEST_PFP,
                "By the blessing of God..."
            )

            await self.send_webhook(
                ctx.channel, guild, priest_webhook, PRIEST_NAME, PRIEST_PFP,
                "And by the power this bot definitely should not have..."
            )

            await self.send_webhook(
                ctx.channel, guild, priest_webhook, PRIEST_NAME, PRIEST_PFP,
                f"I now pronounce {ctx.author.mention} and {partner.mention} married."
            )

            await self.send_webhook(
                ctx.channel, guild, narrator_webhook, NARRATOR_NAME, NARRATOR_PFP,
                "You may now celebrate 🥹❤️"
            )

        finally:
            try:
                await priest_webhook.delete()
            except:
                pass

            try:
                await narrator_webhook.delete()
            except:
                pass


async def setup(bot):
    await bot.add_cog(MarriageSetup(bot))
