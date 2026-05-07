import discord
from discord.ext import commands
import asyncio
import random

PARIS_CATEGORY_ID = None  # put category id or leave None
DATE_COMMAND_CHANNEL_ID = None  # optional command channel only

FRENCH_GUY_PFP = "https://i.imgur.com/8Km9tLL.png"
WAITRESS_PFP = "https://i.imgur.com/8Km9tLL.png"
ROCK_PFP = "https://i.imgur.com/8Km9tLL.png"
NARRATOR_PFP = "https://i.imgur.com/8Km9tLL.png"

PARIS_IMAGE = "https://images.unsplash.com/photo-1502602898657-3e91760cbb34"
RESTAURANT_IMAGE = "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4"
EIFFEL_IMAGE = "https://images.unsplash.com/photo-1543349689-9a4d426bee8e"


class ParisDate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.active = set()

    async def get_webhook(self, channel, name, avatar_url=None):
        hooks = await channel.webhooks()
        for hook in hooks:
            if hook.name == name:
                return hook
        return await channel.create_webhook(name=name, avatar=await self.avatar_bytes(avatar_url))

    async def avatar_bytes(self, url):
        return None

    async def say(self, channel, name, text=None, avatar_url=None, image=None, delay=True):
        hook = await self.get_webhook(channel, name, avatar_url)

        if delay:
            async with channel.typing():
                await asyncio.sleep(random.uniform(0.5, 1.0))

        if image:
            await hook.send(image, username=name, avatar_url=avatar_url)
            await asyncio.sleep(0.5)

        if text:
            if isinstance(text, list):
                for line in text:
                    async with channel.typing():
                        await asyncio.sleep(random.uniform(0.5, 1.0))
                    await hook.send(line, username=name, avatar_url=avatar_url)
            else:
                await hook.send(text, username=name, avatar_url=avatar_url)

    async def wait_choice(self, channel, users, choices, question):
        await channel.send(question)

        picked = {}

        def check(msg):
            return (
                msg.channel == channel
                and msg.author in users
                and not msg.author.bot
                and msg.content.lower().strip() in choices
                and msg.author.id not in picked
            )

        while len(picked) < len(users):
            try:
                msg = await self.bot.wait_for("message", check=check, timeout=180)
            except asyncio.TimeoutError:
                await channel.send("Date cancelled because someone went AFK 💀")
                return None

            choice = msg.content.lower().strip()
            picked[msg.author.id] = choice

            if len(picked) < len(users):
                other = [u for u in users if u.id not in picked][0]
                await msg.reply("okey")
                await channel.send(f"what abt {other.mention}")

        return picked

    @commands.command(name="parisdate")
    async def parisdate(self, ctx, partner: discord.Member):
        if DATE_COMMAND_CHANNEL_ID and ctx.channel.id != DATE_COMMAND_CHANNEL_ID:
            return await ctx.reply("Use this command in the date command channel.")

        if partner.bot or partner == ctx.author:
            return await ctx.reply("Pick a real person genius 💀")

        key = tuple(sorted([ctx.author.id, partner.id]))
        if key in self.active:
            return await ctx.reply("Yall already have a date running.")

        self.active.add(key)

        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(view_channel=False),
            ctx.author: discord.PermissionOverwrite(view_channel=True, send_messages=True),
            partner: discord.PermissionOverwrite(view_channel=True, send_messages=True),
            ctx.guild.me: discord.PermissionOverwrite(view_channel=True, send_messages=True),
        }

        category = ctx.guild.get_channel(PARIS_CATEGORY_ID) if PARIS_CATEGORY_ID else None
        channel = await ctx.guild.create_text_channel(
            name="🇫🇷・paris-date",
            category=category,
            overwrites=overwrites
        )

        await ctx.reply(f"Paris date started: {channel.mention}")

        users = [ctx.author, partner]

        try:
            await channel.send(f"{ctx.author.mention} {partner.mention}")
            await self.say(channel, "Narrator", image=PARIS_IMAGE)
            await self.say(channel, "Narrator", [
                "*Cold evening air brushed across your face as Paris glowed quietly around you...*",
                "*The Eiffel Tower shimmered in the distance while soft music echoed through the streets.*"
            ], NARRATOR_PFP)

            await self.say(channel, "French Guy", [
                "Ahh... welcome lovebirds... to the city of romance 🇫🇷",
                "Tonight... Paris belongs to you two."
            ], FRENCH_GUY_PFP)

            transport = await self.wait_choice(
                channel,
                users,
                ["walk", "taxi", "scooter"],
                "**How shall you arrive at dinner?**\nType: `walk`, `taxi`, or `scooter`"
            )
            if not transport:
                return

            choices = list(transport.values())

            if "scooter" in choices:
                await self.say(channel, "Narrator", [
                    "*The scooter violently shook every 3 seconds.*",
                    "*Romance was alive... barely.*"
                ], NARRATOR_PFP)
                await self.say(channel, "French Guy", "Romance... but dangerous 🇫🇷", FRENCH_GUY_PFP)

            elif "taxi" in choices:
                await self.say(channel, "Taxi Driver", [
                    "Eiffel Tower date eh?",
                    "Happens every Tuesday.",
                    "One couple cried here last week."
                ])

            else:
                await self.say(channel, "Narrator", [
                    "*Your footsteps echoed together across the Paris pavement.*",
                    "*A random cat started following you like it owned the relationship.*"
                ], NARRATOR_PFP)

            await self.say(channel, "Narrator", image=RESTAURANT_IMAGE)
            await self.say(channel, "Le Waitress", [
                "Bonsoirrrr 🎀",
                "Table for two?"
            ], WAITRESS_PFP)

            yes = await self.wait_choice(
                channel,
                users,
                ["yes"],
                "Both type `yes` to enter the restaurant."
            )
            if not yes:
                return

            await self.say(channel, "Le Waitress", "Wonderful... follow me.", WAITRESS_PFP)

            food = await self.wait_choice(
                channel,
                users,
                ["steak", "pasta", "protein"],
                "**What will you order?**\nType: `steak`, `pasta`, or `protein`"
            )
            if not food:
                return

            foods = list(food.values())

            if "protein" in foods:
                await self.say(channel, "Narrator", "*The lights flickered...*", NARRATOR_PFP)
                await self.say(channel, "Dwayne Rock Jhonson", [
                    "THATS WHAT IM TALKING ABOUT 🗣️",
                    "LOVE IS TEMPORARY.",
                    "PROTIEN IS FOREVER."
                ], ROCK_PFP)

            elif "pasta" in foods:
                unlucky = random.choice(users)
                await self.say(channel, "Le Waitress", "Ahh yes... romantic pasta.", WAITRESS_PFP)
                await self.say(channel, "Narrator", f"*{unlucky.mention} somehow spilled sauce. Peak cinema.*", NARRATOR_PFP)

            else:
                await self.say(channel, "Le Waitress", "Steak... classy. Finally someone normal.", WAITRESS_PFP)

            await channel.send("**Mid-date question:** Describe the other person in one word.")

            words = {}

            def word_check(msg):
                return msg.channel == channel and msg.author in users and not msg.author.bot and msg.author.id not in words

            while len(words) < 2:
                msg = await self.bot.wait_for("message", check=word_check)
                words[msg.author.id] = msg.content.strip()
                await msg.reply("noted 🥖")

            await self.say(channel, "Narrator", [
                f"*{ctx.author.display_name} chose: `{words[ctx.author.id]}`*",
                f"*{partner.display_name} chose: `{words[partner.id]}`*",
                "*The waiter pretended not to cry.*"
            ], NARRATOR_PFP)

            await self.say(channel, "Narrator", image=EIFFEL_IMAGE)
            await self.say(channel, "Narrator", [
                "*Paris glowed beneath you as the wind danced softly around the tower.*",
                "*For a moment... everything felt still.*"
            ], NARRATOR_PFP)

            final = await self.wait_choice(
                channel,
                users,
                ["dance", "talk", "hug", "lean"],
                "**What do you do under the Eiffel Tower?**\nType: `dance`, `talk`, `hug`, or `lean`"
            )
            if not final:
                return

            endings = list(final.values())

            if "dance" in endings:
                await self.say(channel, "French Guy", [
                    "OH.",
                    "PEAK CINEMA 🇫🇷😭"
                ], FRENCH_GUY_PFP)

            if "talk" in endings:
                await channel.send("Both of you type one thing you never said before.")

                said = {}

                def talk_check(msg):
                    return msg.channel == channel and msg.author in users and not msg.author.bot and msg.author.id not in said

                while len(said) < 2:
                    msg = await self.bot.wait_for("message", check=talk_check)
                    said[msg.author.id] = msg.content.strip()
                    await msg.reply("...")

                await self.say(channel, "Narrator", "*The night got quieter after that.*", NARRATOR_PFP)

            if "hug" in endings:
                await self.say(channel, "Narrator", "*The cold air no longer felt cold anymore.*", NARRATOR_PFP)

            if "lean" in endings:
                await self.say(channel, "Narrator", "*Someone leaned closer... and Paris minded its business.*", NARRATOR_PFP)

            if random.randint(1, 5) == 1:
                await self.say(channel, "Pickpocket NPC", [
                    "HAND OVER THE BAGUETTE.",
                    "I SAID WHAT I SAID."
                ])

            dessert = await self.wait_choice(
                channel,
                users,
                ["icecream", "cake", "protein shake"],
                "**Before you leave... dessert?**\nType: `icecream`, `cake`, or `protein shake`"
            )
            if not dessert:
                return

            desserts = list(dessert.values())

            if "protein shake" in desserts:
                await self.say(channel, "Dwayne Rock Jhonson", [
                    "MY PEOPLE.",
                    "THIS DATE HAS BEEN APPROVED."
                ], ROCK_PFP)
            else:
                await self.say(channel, "Le Waitress", "Cute choice. Annoyingly cute.", WAITRESS_PFP)

            romance = random.randint(80, 100)
            awkward = random.randint(1, 35)
            protein = "CRITICAL 💀" if "protein" in foods or "protein shake" in desserts else "low. disappointing."

            embed = discord.Embed(
                title="🥖 Paris Date Complete",
                description="A new memory has been added.",
                color=discord.Color.pink()
            )
            embed.add_field(name="Romance", value=f"{romance}%", inline=True)
            embed.add_field(name="Awkwardness", value=f"{awkward}%", inline=True)
            embed.add_field(name="Protein", value=protein, inline=False)
            embed.add_field(name="Final Location", value="Eiffel Tower 🇫🇷", inline=False)

            await channel.send(embed=embed)

        finally:
            self.active.discard(key)


async def setup(bot):
    await bot.add_cog(ParisDate(bot))
