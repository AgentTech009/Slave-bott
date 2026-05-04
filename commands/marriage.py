import discord
from discord.ext import commands
import asyncio
import random

PRIEST_NAME = "le priest"
NARRATOR_NAME = "Narrator"

PRIEST_PFP = "https://cdn-icons-png.flaticon.com/512/1995/1995574.png"
NARRATOR_PFP = "https://cdn-icons-png.flaticon.com/512/833/833472.png"

WAITRESS_PFP = "https://cdn.discordapp.com/attachments/1500472877210927197/1500485690251804943/IMG_20260503_172534.jpg?ex=69f89bb2&is=69f74a32&hm=cfd1ded3cfd73b3962ac94cc3bd2a9c7ea397ee222d86e27559f216e7e9ada24&"
ROCK_PFP = "https://cdn.discordapp.com/attachments/1500472877210927197/1500485690553663599/images-1.jpg?ex=69f89bb2&is=69f74a32&hm=286c96be0388932f09cefa9fc1ba5ece597974b5fbab5b8d20234a76021803a4&"
KONI_PFP = "https://cdn.discordapp.com/attachments/1500100689924194326/1500100763815252079/IMG-20260421-WA0051-1.jpg?ex=69f886b4&is=69f73534&hm=6c66a91dc63a312f432cf58a617025be58b7a8a5d777bb4e7367487c31faf8c2&"


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
        for part in text.split("\n"):
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

    async def wait_for_exact(self, channel, user, text):
        def check(msg):
            return (
                msg.channel == channel
                and msg.author.id == user.id
                and msg.content.lower().strip() == text.lower()
            )

        while True:
            try:
                return await self.bot.wait_for("message", check=check, timeout=120)
            except asyncio.TimeoutError:
                await channel.send(f"{user.mention} reply with `{text}` 😭")

    async def wait_for_any(self, channel, user):
        def check(msg):
            return msg.channel == channel and msg.author.id == user.id

        while True:
            try:
                return await self.bot.wait_for("message", check=check, timeout=180)
            except asyncio.TimeoutError:
                await channel.send(f"{user.mention} send your vow bro 😭")

    async def wait_until_both_enter(self, channel, user1, user2):
        entered = set()

        await channel.send(
            f"{user1.mention} {user2.mention}\n"
            "Send any message here when you enter le church ⛪"
        )

        def check(msg):
            return msg.channel == channel and msg.author.id in [user1.id, user2.id]

        while len(entered) < 2:
            msg = await self.bot.wait_for("message", check=check)
            entered.add(msg.author.id)

            if len(entered) == 1:
                await channel.send("Waiting for the other person 👀")

        await channel.send("Both have entered. The wedding shall begin 💒")

    @commands.command(name="marriagesetup")
    @commands.has_permissions(administrator=True)
    async def marriagesetup(self, ctx, partner: discord.Member):
        if partner.bot:
            return await ctx.send("You cannot marry a bot 💀")

        if partner.id == ctx.author.id:
            return await ctx.send("Bro tried to marry himself 😭")

        guild = ctx.guild
        self.current_typing_name = None

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            ctx.author: discord.PermissionOverwrite(
                view_channel=True,
                send_messages=True,
                read_message_history=True
            ),
            partner: discord.PermissionOverwrite(
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
            name="le-church",
            overwrites=overwrites
        )

        await ctx.send(f"⛪ Wedding channel created: {channel.mention}")

        await self.wait_until_both_enter(channel, ctx.author, partner)

        priest_webhook = await channel.create_webhook(name=PRIEST_NAME)
        narrator_webhook = await channel.create_webhook(name=NARRATOR_NAME)
        waitress_webhook = await channel.create_webhook(name="Le weightress")
        rock_webhook = await channel.create_webhook(name="Dwayne Rock Jhonson")
        koni_webhook = await channel.create_webhook(name="Koni")

        try:
            await self.send_webhook(channel, guild, narrator_webhook, NARRATOR_NAME, NARRATOR_PFP, "💒 The wedding begins...")
            await self.send_webhook(channel, guild, narrator_webhook, NARRATOR_NAME, NARRATOR_PFP, "Dearly beloved...")
            await self.send_webhook(channel, guild, narrator_webhook, NARRATOR_NAME, NARRATOR_PFP, "We are gathered here today before God and this server.")
            await self.send_webhook(channel, guild, narrator_webhook, NARRATOR_NAME, NARRATOR_PFP, f"To witness the union of {ctx.author.mention} and {partner.mention}.")
            await self.send_webhook(channel, guild, narrator_webhook, NARRATOR_NAME, NARRATOR_PFP, "If anyone has any reason why these two should not be married...")
            await self.send_webhook(channel, guild, narrator_webhook, NARRATOR_NAME, NARRATOR_PFP, "Too bad.")
            await self.send_webhook(channel, guild, narrator_webhook, NARRATOR_NAME, NARRATOR_PFP, "We do not care 💀")

            await self.send_webhook(channel, guild, priest_webhook, PRIEST_NAME, PRIEST_PFP, f"{ctx.author.mention}, step forward.")
            await self.send_webhook(channel, guild, priest_webhook, PRIEST_NAME, PRIEST_PFP, f"Do you take {partner.mention} to be your partner?")
            await self.send_webhook(channel, guild, priest_webhook, PRIEST_NAME, PRIEST_PFP, "To love her.")
            await self.send_webhook(channel, guild, priest_webhook, PRIEST_NAME, PRIEST_PFP, "To care for her.")
            await self.send_webhook(channel, guild, priest_webhook, PRIEST_NAME, PRIEST_PFP, "And to stay with her...")
            await self.send_webhook(channel, guild, priest_webhook, PRIEST_NAME, PRIEST_PFP, " even when she takes 15 minutes to reply...")

            await channel.send(f"{ctx.author.mention} type `I do`")
            await self.wait_for_exact(channel, ctx.author, "I do")

            await self.send_webhook(channel, guild, priest_webhook, PRIEST_NAME, PRIEST_PFP, f"{partner.mention}, step forward.")
            await self.send_webhook(channel, guild, priest_webhook, PRIEST_NAME, PRIEST_PFP, f"Do you take {ctx.author.mention} to be your partner?")
            await self.send_webhook(channel, guild, priest_webhook, PRIEST_NAME, PRIEST_PFP, "To love him.")
            await self.send_webhook(channel, guild, priest_webhook, PRIEST_NAME, PRIEST_PFP, "To support him.")
            await self.send_webhook(channel, guild, priest_webhook, PRIEST_NAME, PRIEST_PFP, "And to deal with his overthinking?")

            await channel.send(f"{partner.mention} type `I do`")
            await self.wait_for_exact(channel, partner, "I do")

            await self.send_webhook(channel, guild, narrator_webhook, NARRATOR_NAME, NARRATOR_PFP, "💍 Ring exchange time.")

            await self.send_webhook(channel, guild, priest_webhook, PRIEST_NAME, PRIEST_PFP, f"{ctx.author.mention} send 💍")
            await self.wait_for_exact(channel, ctx.author, "💍")

            await self.send_webhook(channel, guild, priest_webhook, PRIEST_NAME, PRIEST_PFP, f"{partner.mention} send 💍")
            await self.wait_for_exact(channel, partner, "💍")

            await self.send_webhook(channel, guild, narrator_webhook, NARRATOR_NAME, NARRATOR_PFP, "The rings have been exchanged.")

            await self.send_webhook(channel, guild, priest_webhook, PRIEST_NAME, PRIEST_PFP, "Now speak your vows.")
            await self.send_webhook(channel, guild, priest_webhook, PRIEST_NAME, PRIEST_PFP, f"{ctx.author.mention}, send your custom vow.")
            vow1 = await self.wait_for_any(channel, ctx.author)

            await self.send_webhook(channel, guild, priest_webhook, PRIEST_NAME, PRIEST_PFP, "Beautiful...")
            await self.send_webhook(channel, guild, priest_webhook, PRIEST_NAME, PRIEST_PFP, f"{partner.mention}, send your custom vow.")
            vow2 = await self.wait_for_any(channel, partner)

            await self.send_webhook(channel, guild, narrator_webhook, NARRATOR_NAME, NARRATOR_PFP, "The vows have been spoken.")
            await self.send_webhook(channel, guild, narrator_webhook, NARRATOR_NAME, NARRATOR_PFP, f"{ctx.author.mention} promised:")
            await self.send_webhook(channel, guild, narrator_webhook, NARRATOR_NAME, NARRATOR_PFP, f"“{vow1.content}”")
            await self.send_webhook(channel, guild, narrator_webhook, NARRATOR_NAME, NARRATOR_PFP, f"{partner.mention} promised:")
            await self.send_webhook(channel, guild, narrator_webhook, NARRATOR_NAME, NARRATOR_PFP, f"“{vow2.content}”")

            await self.send_webhook(channel, guild, narrator_webhook, NARRATOR_NAME, NARRATOR_PFP, "The moment we have all been waiting for...")
            await self.send_webhook(channel, guild, priest_webhook, PRIEST_NAME, PRIEST_PFP, "By the blessing of God...")
            await self.send_webhook(channel, guild, priest_webhook, PRIEST_NAME, PRIEST_PFP, "And by the power this bot definitely should not have...")
            await self.send_webhook(channel, guild, priest_webhook, PRIEST_NAME, PRIEST_PFP, f"I now pronounce {ctx.author.mention} and {partner.mention} married.")
            await self.send_webhook(channel, guild, narrator_webhook, NARRATOR_NAME, NARRATOR_PFP, "You may now Kiss 🥹❤️")

            await asyncio.sleep(3)


            await self.send_webhook(
                channel, guild, waitress_webhook, "Le weightress", WAITRESS_PFP,
                "I will never forget how you laughed at that poor child thoo...🥹🎀"
            )

            await self.send_webhook(
                channel, guild, rock_webhook, "Dwayne Rock Jhonson", ROCK_PFP,
                "MAKE SURE TO GIVE MY BOY A LOTTO PROTIEN"
            )

            await self.send_webhook(
                channel, guild, koni_webhook, "Koni", KONI_PFP,
                "Mew \n*licks her own ahh*"
            )

        finally:
            for webhook in [
                priest_webhook,
                narrator_webhook,
                waitress_webhook,
                rock_webhook,
                koni_webhook
            ]:
                try:
                    await webhook.delete()
                except:
                    pass


async def setup(bot):
    await bot.add_cog(MarriageSetup(bot))
