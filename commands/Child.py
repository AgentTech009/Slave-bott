import discord
from discord.ext import commands
import asyncio
import random

MALE_CHILD_IMG = "https://cdn.discordapp.com/attachments/1500472877210927197/1501944584811450560/images-13.jpg?ex=69fdea65&is=69fc98e5&hm=b960692439c65b16c4816e0465c4beee5dabf1a8a9635d0262f32a1b97de7224&"
FEMALE_CHILD_IMG = "https://cdn.discordapp.com/attachments/1500472877210927197/1501944584349941801/images-14.jpg?ex=69fdea65&is=69fc98e5&hm=7844c88fa5c1b1603b30ad22edd748d01cdd6f29f75fae1a9cfbbe4af077822f&"


class NameModal(discord.ui.Modal):
    def __init__(self, cog, ctx, channel, parents, done_callback):
        super().__init__(title="Name the CHILD")
        self.cog = cog
        self.ctx = ctx
        self.channel = channel
        self.parents = parents
        self.done_callback = done_callback

        self.child_name = discord.ui.TextInput(
            label="Child name",
            placeholder="Type secretly here",
            max_length=30
        )
        self.add_item(self.child_name)

    async def on_submit(self, interaction: discord.Interaction):
        if interaction.user.id not in [p.id for p in self.parents]:
            return await interaction.response.send_message("You are not a parent lil bro.", ephemeral=True)

        self.cog.name_votes[interaction.user.id] = str(self.child_name.value)
        await interaction.response.send_message("Name submitted ✅", ephemeral=True)

        if len(self.cog.name_votes) >= 2:
            await self.done_callback()


class NameButton(discord.ui.View):
    def __init__(self, cog, ctx, channel, parents, done_callback):
        super().__init__(timeout=60)
        self.cog = cog
        self.ctx = ctx
        self.channel = channel
        self.parents = parents
        self.done_callback = done_callback

    @discord.ui.button(label="Name child", style=discord.ButtonStyle.primary)
    async def name_child(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(
            NameModal(self.cog, self.ctx, self.channel, self.parents, self.done_callback)
        )


class RestartView(discord.ui.View):
    def __init__(self, cog, stage_func):
        super().__init__(timeout=60)
        self.cog = cog
        self.stage_func = stage_func

    @discord.ui.button(label="Quit", style=discord.ButtonStyle.danger)
    async def quit(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Ok")
        self.stop()

    @discord.ui.button(label="Restart", style=discord.ButtonStyle.success)
    async def restart(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Alright restarting in 3 seconds..")
        await asyncio.sleep(3)
        await self.stage_func()
        self.stop()


class ChildCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.name_votes = {}

    async def gap(self, seconds):
        await asyncio.sleep(seconds)

    async def bot_say(self, channel, text):
        await channel.guild.me.edit(nick=None)
        for line in text.split("\n"):
            if line.strip():
                async with channel.typing():
                    await asyncio.sleep(0.5)
                await channel.send(line)

    async def child_say(self, channel, name, image, text):
        await channel.guild.me.edit(nick=name or "child")

        webhooks = await channel.webhooks()
        webhook = discord.utils.get(webhooks, name="ChildWebhook")
        if webhook is None:
            webhook = await channel.create_webhook(name="ChildWebhook")

        for line in text.split("\n"):
            if line.strip():
                async with channel.typing():
                    await asyncio.sleep(0.5)
                await webhook.send(
                    line,
                    username=name or "child",
                    avatar_url=image
                )

        await channel.guild.me.edit(nick=None)

    async def end_flow(self, channel, stage_func):
        await self.gap(3)
        await self.bot_say(
            channel,
            "Uhhhh yall lost..\nYou can either quit parenthood or start again from the question u lost on..\n\nOption 1. Quit\nOption 2. Restart"
        )
        await channel.send(view=RestartView(self, stage_func))

    async def selection(self, channel, parents, options):
        picks = {}

        option_map = {}
        for num, label in options.items():
            option_map[str(num).lower()] = num
            option_map[label.lower()] = num

        def check(msg):
            if msg.channel.id != channel.id:
                return False
            if msg.author.id not in [p.id for p in parents]:
                return False
            content = msg.content.strip().lower()
            return content in option_map

        while len(picks) < 2:
            msg = await self.bot.wait_for("message", check=check)
            picked = option_map[msg.content.strip().lower()]
            picks[msg.author.id] = picked
            try:
                await msg.add_reaction("✅")
            except:
                pass

        values = list(picks.values())

        if values[0] == values[1]:
            return values[0]

        await self.bot_say(channel, "Oops u guys disagree..\nSelecting random..")
        return random.choice(values)

    @commands.command()
    async def child(self, ctx, user: discord.Member):
        parents = [ctx.author, user]

        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(view_channel=False),
            ctx.author: discord.PermissionOverwrite(view_channel=True, send_messages=True),
            user: discord.PermissionOverwrite(view_channel=True, send_messages=True),
            ctx.guild.me: discord.PermissionOverwrite(view_channel=True, send_messages=True),
        }

        channel = await ctx.guild.create_text_channel("child", overwrites=overwrites)
        await ctx.send(channel.mention)

        def both_typed_check(msg):
            return msg.channel.id == channel.id and msg.author.id in [p.id for p in parents]

        typed = set()
        while len(typed) < 2:
            msg = await self.bot.wait_for("message", check=both_typed_check)
            typed.add(msg.author.id)

        gender = random.choice(["male", "female"])
        child_img = MALE_CHILD_IMG if gender == "male" else FEMALE_CHILD_IMG
        child_name = "child"

        await self.gap(3)
        await self.bot_say(channel, "Boom\nChild.\nYou have child now")
        await channel.send(child_img)
        await self.bot_say(channel, "Oh child is female.." if gender == "female" else "Ohh child is male..")

        await self.gap(3)
        await self.bot_say(channel, "Age : 0\nName the CHILD")
        await self.child_say(channel, child_name, child_img, "googo gagaa bish.")

        async def name_done():
            nonlocal child_name

            p1, p2 = parents
            n1 = self.name_votes.get(p1.id)
            n2 = self.name_votes.get(p2.id)

            if n1 == n2:
                child_name = n1
            else:
                await self.bot_say(
                    channel,
                    f"Shit..\nYall picked diff names\n\n{p1.mention} picked {n1}\n{p2.mention} picked {n2}\n\nAlriggt picking random name.."
                )
                child_name = random.choice([n1, n2])

            await self.bot_say(channel, f"Child will be named {child_name}")
            await self.child_say(channel, child_name, child_img, "googoo gagaa")
            await stage_one()

        await self.gap(2)
        self.name_votes = {}
        await channel.send(view=NameButton(self, ctx, channel, parents, name_done))

        async def stage_one():
            await self.gap(5)
            await self.bot_say(channel, "One yr later..")
            await self.child_say(channel, child_name, child_img, "googoo mommy gaagaa")
            await self.bot_say(channel, f"Congrats {child_name} spoke first word")
            await self.gap(15)

            await self.bot_say(
                channel,
                "Option 1: give child vodka\n2. Give child protien\n3. Give child junk food\n4. Starve child"
            )

            choice = await self.selection(channel, parents, {
                1: "give child vodka",
                2: "give child protien",
                3: "give child junk food",
                4: "starve child"
            })

            if choice == 1:
                await self.bot_say(channel, "Child went to Russia in hopes of finding more vodka..\nCongrats ur childless")
                return await self.end_flow(channel, stage_one)

            if choice == 2:
                await self.bot_say(channel, "Child says yes..\nChild buff")
                return await stage_two()

            if choice == 3:
                await self.bot_say(channel, "Child became american..\nU decided to throw the child away..")
                return await self.end_flow(channel, stage_one)

            if choice == 4:
                await self.bot_say(channel, "Child said no and ate all your food\nYall died..")
                return await self.end_flow(channel, stage_one)

        async def stage_two():
            await self.gap(5)
            await self.bot_say(channel, "Two years later..\n\nAge: 03")
            await self.child_say(channel, child_name, child_img, "i can speak now BISH")
            await self.bot_say(
                channel,
                "Child dum.\nChild need education (elementary level)\n\nOption 1: pablo escobar elementary SKOOL\nFees: 1kg cocaine\n\n2. Harvard elementary\nFees : 1$ + 90,000$ donation\n\n3. Diddy SKOOL\nFees: none..\n\n4. Normal school\nFees: 20,000$"
            )

            choice = await self.selection(channel, parents, {
                1: "pablo escobar elementary skool",
                2: "harvard elementary",
                3: "diddy skool",
                4: "normal school"
            })

            if choice == 1:
                await self.bot_say(channel, f"{child_name} became drug lord and yall got arrested...\n\nNice.")
                return await self.end_flow(channel, stage_two)

            if choice == 2:
                await self.bot_say(channel, f"{child_name} realised how dum yall truly are..\nChild left you.\n\nAmazing..")
                return await self.end_flow(channel, stage_two)

            if choice == 3:
                await self.bot_say(channel, f"{child_name} school got raided..\nOoopss..")
                return await self.end_flow(channel, stage_two)

            if choice == 4:
                await self.bot_say(channel, f"{child_name} is smart now congrats\nYall broke but who cares child is smart")
                return await stage_three()

        async def stage_three():
            await self.gap(5)
            await self.bot_say(channel, "2 yrs later..\n\nAge: 05")
            await self.child_say(channel, child_name, child_img, "i can walk hehe")
            await self.gap(3)

            await self.bot_say(
                channel,
                "Child needs educational upgrade..\n\nTime to pick school..\n\nOption 1. Reynash college of hotel management\n2. MKM PIRAVOM\n3. FATIMA PIRAVOM (STATE)\n4. Catgirl school"
            )

            choice = await self.selection(channel, parents, {
                1: "reynash college of hotel management",
                2: "mkm piravom",
                3: "fatima piravom",
                4: "catgirl school"
            })

            if choice == 1:
                await self.bot_say(channel, f"{child_name} coudlnt take in that level of education and despawned\nHahahah childless again")
                return await self.end_flow(channel, stage_three)

            if choice == 2:
                await self.bot_say(channel, f"{child_name} followed fathers footsteps and became a great person..")
                return await stage_four()

            if choice == 3:
                await self.bot_say(channel, f"{child_name} followed mother's footsteps and became a great person..")
                return await stage_four()

            if choice == 4:
                await self.bot_say(channel, f"{child_name} became a catgirl..\nHell nah yall disowned him..\nBye bye.")
                return await self.end_flow(channel, stage_three)

        async def stage_four():
            await self.gap(5)
            await self.bot_say(channel, "10 yrs later...\n\nAge: 15\nChild has full aplus")
            await self.child_say(channel, child_name, child_img, "Hi (sorry for bad english)")
            await self.bot_say(channel, "Child is lowk a bitch now..")
            await self.gap(2)

            await self.bot_say(
                channel,
                f"Choose further education for {child_name}\n\nOption 1. None\n2. Mkm (again)\n3. Bob"
            )

            choice = await self.selection(channel, parents, {
                1: "none",
                2: "mkm",
                3: "bob"
            })

            if choice == 1:
                await self.bot_say(channel, "Child got angry and killed yall\nWow")
                return await self.end_flow(channel, stage_four)

            if choice == 2:
                await self.bot_say(channel, "Child ungrateful ofc but has education\nLets hope child finds love")
                return await stage_five()

            if choice == 3:
                await self.bot_say(channel, "Bob")
                return await stage_five()

        async def stage_five():
            await self.gap(5)
            await self.bot_say(channel, "Child became 18\nIdk what to do next im not rlly 18 yet...\n\nTEST VERSION ENDED")


async def setup(bot):
    await bot.add_cog(ChildCog(bot))
