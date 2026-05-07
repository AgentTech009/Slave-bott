import discord
from discord.ext import commands
import asyncio
import random

MALE_CHILD_IMG = "https://cdn.discordapp.com/attachments/1500472877210927197/1501944584349941801/images-14.jpg?ex=69fdea65&is=69fc98e5&hm=7844c88fa5c1b1603b30ad22edd748d01cdd6f29f75fae1a9cfbbe4af077822f&"
FEMALE_CHILD_IMG = "https://cdn.discordapp.com/attachments/1500472877210927197/1501944584349941801/images-14.jpg?ex=69fdea65&is=69fc98e5&hm=7844c88fa5c1b1603b30ad22edd748d01cdd6f29f75fae1a9cfbbe4af077822f&"


class NameModal(discord.ui.Modal, title="Name the child"):
    child_name = discord.ui.TextInput(
        label="Secret child name",
        placeholder="Type name here...",
        max_length=30
    )

    def __init__(self, view, user_id):
        super().__init__()
        self.view_ref = view
        self.user_id = user_id

    async def on_submit(self, interaction: discord.Interaction):
        self.view_ref.names[self.user_id] = str(self.child_name.value).strip()
        await interaction.response.send_message("Name locked 🔒", ephemeral=True)

        if len(self.view_ref.names) >= 2:
            self.view_ref.stop()


class NameView(discord.ui.View):
    def __init__(self, users):
        super().__init__(timeout=120)
        self.users = users
        self.names = {}

    @discord.ui.button(label="Secretly name child", style=discord.ButtonStyle.primary)
    async def name_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id not in [u.id for u in self.users]:
            return await interaction.response.send_message("Not ur child lil bro 💀", ephemeral=True)

        if interaction.user.id in self.names:
            return await interaction.response.send_message("You already picked.", ephemeral=True)

        await interaction.response.send_modal(NameModal(self, interaction.user.id))


class EndView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=120)
        self.choice = None

    @discord.ui.button(label="Quit", style=discord.ButtonStyle.danger)
    async def quit_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.choice = "quit"
        await interaction.response.send_message("Ok")
        self.stop()

    @discord.ui.button(label="Restart", style=discord.ButtonStyle.success)
    async def restart_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.choice = "restart"
        await interaction.response.send_message("Alright restarting in 3 seconds..")
        self.stop()


class Child(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def set_bot_nick(self, guild, name=None):
        me = guild.me
        try:
            await me.edit(nick=name)
        except discord.Forbidden:
            pass
        except discord.HTTPException:
            pass

    async def bot_type(self, channel, seconds=1.1):
        await self.set_bot_nick(channel.guild, None)
        async with channel.typing():
            await asyncio.sleep(seconds)

    async def child_type(self, channel, child_name):
        await self.set_bot_nick(channel.guild, child_name or "child")
        async with channel.typing():
            await asyncio.sleep(random.uniform(1, 1.2))
        await self.set_bot_nick(channel.guild, None)

    async def send_bot(self, channel, text=None, image=None, delay=True):
        if delay:
            await self.bot_type(channel)
        if image:
            await channel.send(image)
        if text:
            for line in text.split("\n"):
                if line.strip():
                    await channel.send(line.strip())
                    await asyncio.sleep(random.uniform(1, 1.2))

    async def send_child(self, channel, webhook, child_name, avatar, text):
        await self.child_type(channel, child_name)
        await webhook.send(
            text,
            username=child_name or "child",
            avatar_url=avatar
        )

    async def gap(self, seconds):
        await asyncio.sleep(seconds)

    async def wait_both_talk(self, channel, users):
        spoken = set()

        def check(msg):
            return (
                msg.channel.id == channel.id
                and msg.author.id in [u.id for u in users]
                and not msg.author.bot
            )

        while len(spoken) < 2:
            msg = await self.bot.wait_for("message", check=check)
            spoken.add(msg.author.id)

    async def end_screen(self, channel):
        await self.gap(3)
        await self.send_bot(
            channel,
            "Uhh yall lost..\nYou can either quit parenthood or start again from the question u lost on..",
        )

        view = EndView()
        await channel.send("Choose wisely 🍼", view=view)
        await view.wait()

        if view.choice == "restart":
            await asyncio.sleep(3)
            return "restart"

        return "quit"

    async def selection(self, channel, users, options):
        """
        options format:
        [
            {"num": "1", "label": "give child vodka", "trigger": "vodka"},
            ...
        ]
        """

        msg = "**Pick one option.**\n"
        msg += "Type only the trigger word by itself.\n\n"

        for opt in options:
            msg += f"**{opt['num']}. {opt['label']}**\n"
            msg += f"Trigger: `{opt['trigger']}`\n\n"

        await self.send_bot(channel, msg)

        picked = {}
        triggers = {o["trigger"].lower(): o for o in options}
        nums = {o["num"]: o for o in options}

        def check(m):
            if m.channel.id != channel.id:
                return False
            if m.author.id not in [u.id for u in users]:
                return False
            if m.author.bot:
                return False

            content = m.content.strip().lower()
            return content in triggers or content in nums

        while len(picked) < 2:
            msg = await self.bot.wait_for("message", check=check)
            if msg.author.id in picked:
                continue

            content = msg.content.strip().lower()
            option = triggers.get(content) or nums.get(content)

            picked[msg.author.id] = option
            try:
                await msg.add_reaction("✅")
            except:
                pass

            await asyncio.sleep(1)

        picks = list(picked.values())

        if picks[0]["num"] == picks[1]["num"]:
            return picks[0]["num"]

        await self.send_bot(
            channel,
            "Oops u guys disagree..\nSelecting random.."
        )

        chosen = random.choice(picks)
        await self.send_bot(channel, f"*selects random from the two picked options*\nSelected: **{chosen['label']}**")
        return chosen["num"]

    async def stage_food(self, channel, users, child_name, webhook, avatar):
        await self.gap(5)
        await self.send_bot(channel, "One yr later..")
        await self.send_child(channel, webhook, child_name, avatar, "googoo mommy gaagaa")
        await self.gap(1.5)
        await self.send_bot(channel, f"Congrats {child_name} spoke first word")
        await self.gap(3)

        choice = await self.selection(channel, users, [
            {"num": "1", "label": "give child vodka", "trigger": "vodka"},
            {"num": "2", "label": "Give child protien", "trigger": "protien"},
            {"num": "3", "label": "Give child junk food", "trigger": "junk"},
            {"num": "4", "label": "Starve child", "trigger": "starve"},
        ])

        if choice == "1":
            await self.send_bot(channel, "Child went to Russia in hopes of finding more vodka..\nCongrats ur childless")
            return await self.end_screen(channel)

        if choice == "2":
            await self.send_bot(channel, "Child says yes..\nChild buff")
            return "continue"

        if choice == "3":
            await self.send_bot(channel, "Child became american..\nU decided to throw the child away..")
            return await self.end_screen(channel)

        if choice == "4":
            await self.send_bot(channel, "Child said no and ate all your food\nYall died..")
            return await self.end_screen(channel)

    async def stage_elementary(self, channel, users, child_name):
        await self.gap(5)
        await self.send_bot(
            channel,
            f"Two years later..\n\nAge: 03\n\n{child_name}: i can speak now BISH\n\nChild dum.\nChild need education"
        )
        await self.gap(1.5)

        choice = await self.selection(channel, users, [
            {"num": "1", "label": "pablo escobar elementary SKOOL | Fees: 1kg cocaine", "trigger": "pablo"},
            {"num": "2", "label": "Harvard elementary | Fees: 1$ + 90,000$ donation", "trigger": "harvard"},
            {"num": "3", "label": "Diddy SKOOL | Fees: none..", "trigger": "diddy"},
            {"num": "4", "label": "Normal school | Fees: 20,000$", "trigger": "normal"},
        ])

        if choice == "1":
            await self.send_bot(channel, f"{child_name} became drug lord and yall got arrested...\n\nNice.")
            return await self.end_screen(channel)

        if choice == "2":
            await self.send_bot(channel, f"{child_name} realised how dum yall truly are..\nChild left you.\n\nAmazing..")
            return await self.end_screen(channel)

        if choice == "3":
            await self.send_bot(channel, "School got raided...\nOoopss..")
            return await self.end_screen(channel)

        if choice == "4":
            await self.send_bot(channel, f"{child_name} is smart now congrats\nYall broke but who cares child is smart")
            return "continue"

    async def stage_school_upgrade(self, channel, users, child_name):
        await self.gap(5)
        await self.send_bot(channel, f"2 yrs later..\n\nAge: 05\n\n{child_name}: i can walk hehe")
        await self.gap(3)
        await self.send_bot(channel, "Child needs educational upgrade..\n\nTime to pick school..")

        choice = await self.selection(channel, users, [
            {"num": "1", "label": "Reynash college of hotel management", "trigger": "reynash"},
            {"num": "2", "label": "MKM PIRAVOM", "trigger": "mkm"},
            {"num": "3", "label": "FATIMA PIRAVOM", "trigger": "fatima"},
            {"num": "4", "label": "Catgirl school", "trigger": "catgirl"},
        ])

        if choice == "1":
            await self.send_bot(channel, f"{child_name} couldnt take in that level of education and despawned\nHahahah childless again")
            return await self.end_screen(channel)

        if choice == "2":
            await self.send_bot(channel, f"{child_name} followed fathers footsteps and became a great person..")
            return "continue"

        if choice == "3":
            await self.send_bot(channel, f"{child_name} followed mother's footsteps and became a great person..")
            return "continue"

        if choice == "4":
            await self.send_bot(channel, f"{child_name} became a catgirl..\nHell nah yall disowned him..\nBye bye.")
            return await self.end_screen(channel)

    async def stage_fifteen(self, channel, users, child_name):
        await self.gap(5)
        await self.send_bot(
            channel,
            f"10 yrs later...\n\nAge: 15\nChild has full aplus\n{child_name}: Hi sorry for bad english\nChild is lowk a bitch now.."
        )
        await self.gap(2)

        await self.send_bot(channel, f"Choose further education for {child_name}")

        choice = await self.selection(channel, users, [
            {"num": "1", "label": "None", "trigger": "none"},
            {"num": "2", "label": "Mkm again", "trigger": "mkm"},
            {"num": "3", "label": "Bob", "trigger": "bob"},
        ])

        if choice == "1":
            await self.send_bot(channel, f"{child_name} got angry and killed yall\nWow")
            return await self.end_screen(channel)

        if choice == "2":
            await self.send_bot(channel, f"{child_name} ungrateful ofc but has education\nLets hope child finds love")
            return "continue"

        if choice == "3":
            await self.send_bot(channel, "Bob")
            return "continue"

    async def stage_eighteen(self, channel, child_name):
        await self.gap(5)
        await self.send_bot(
            channel,
            f"{child_name} became 18\nIdk what to do next im not rlly 18 yet...\n\nCongrats.\nYour child survived somehow.\nBad parenting but plot armor carried 💀"
        )
        return "done"

    @commands.command(name="child")
    async def child(self, ctx, partner: discord.Member):
        if partner.bot:
            return await ctx.send("Bots cant parent bro what is this factory settings family 💀")

        parent1 = ctx.author
        parent2 = partner
        users = [parent1, parent2]

        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(view_channel=False),
            parent1: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True),
            parent2: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True),
            ctx.guild.me: discord.PermissionOverwrite(view_channel=True, send_messages=True, manage_channels=True, manage_webhooks=True),
        }

        channel = await ctx.guild.create_text_channel(
            name="child",
            overwrites=overwrites,
            category=ctx.channel.category
        )

        await ctx.send(channel.mention)

        await self.wait_both_talk(channel, users)
        await asyncio.sleep(3)

        gender = random.choice(["male", "female"])
        avatar = MALE_CHILD_IMG if gender == "male" else FEMALE_CHILD_IMG

        webhook = await channel.create_webhook(name="child")

        await self.send_bot(channel, "Boom\nChild.\nYou have child now", image=avatar)
        await self.gap(2)

        if gender == "female":
            await self.send_bot(channel, "Oh child is female..")
        else:
            await self.send_bot(channel, "Ohh child is male..")

        await self.gap(2)
        await self.send_bot(channel, "Age : 0\nName the CHILD")
        await self.gap(1)

        await self.send_child(channel, webhook, "child", avatar, "googo gagaa bish.")

        await self.gap(2)

        name_view = NameView(users)
        await channel.send("Both parents secretly pick a name 🍼", view=name_view)
        await name_view.wait()

        if len(name_view.names) < 2:
            await self.send_bot(channel, "Yall didnt name the child in time.\nChild evaporated.")
            return

        name1 = name_view.names[parent1.id]
        name2 = name_view.names[parent2.id]

        if name1.lower() == name2.lower():
            child_name = name1
            await self.send_bot(channel, f"Both picked **{child_name}**\nRare teamwork moment.")
        else:
            await self.send_bot(
                channel,
                f"Shit..\nYall picked diff names\n\n{parent1.mention} picked {name1}\n{parent2.mention} picked {name2}\n\nAlright picking random name.."
            )
            child_name = random.choice([name1, name2])
            await self.send_bot(channel, f"*picks a random name from those two options*\nChild will be named {child_name}")

        await self.send_child(channel, webhook, child_name, avatar, "googoo gagaa")

        stages = [
            lambda: self.stage_food(channel, users, child_name, webhook, avatar),
            lambda: self.stage_elementary(channel, users, child_name),
            lambda: self.stage_school_upgrade(channel, users, child_name),
            lambda: self.stage_fifteen(channel, users, child_name),
            lambda: self.stage_eighteen(channel, child_name),
        ]

        index = 0

        while index < len(stages):
            result = await stages[index]()

            if result == "continue":
                index += 1
            elif result == "restart":
                continue
            elif result == "quit":
                break
            elif result == "done":
                break

        try:
            await webhook.delete()
        except:
            pass

        await self.set_bot_nick(ctx.guild, None)


async def setup(bot):
    await bot.add_cog(Child(bot))
