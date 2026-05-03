import discord
from discord.ext import commands
import asyncio
import random

DATE_COMMAND_CHANNEL_ID = None

FRENCH_GUY_PFP = "https://cdn.discordapp.com/attachments/1500472877210927197/1500485689928585367/IMG_20260503_172432.jpg?ex=69f89bb2&is=69f74a32&hm=54e8301b787f2b14cbab8af8ffaaf82affa038e57d258ec4e4de3f843e19ae38&"
WAITRESS_PFP = "https://cdn.discordapp.com/attachments/1500472877210927197/1500485690251804943/IMG_20260503_172534.jpg?ex=69f89bb2&is=69f74a32&hm=cfd1ded3cfd73b3962ac94cc3bd2a9c7ea397ee222d86e27559f216e7e9ada24&"
ROCK_PFP = "https://cdn.discordapp.com/attachments/1500472877210927197/1500485690553663599/images-1.jpg?ex=69f89bb2&is=69f74a32&hm=286c96be0388932f09cefa9fc1ba5ece597974b5fbab5b8d20234a76021803a4&"
TAXI_PFP = "https://cdn.discordapp.com/attachments/1500472877210927197/1500485690964840650/images-2.jpg?ex=69f89bb2&is=69f74a32&hm=a58d97f879486b70a911b4febea22bd5bffef260b74597e07104b8618d2845ea&"

RESTAURANT_IMG = "https://cdn.discordapp.com/attachments/1500472877210927197/1500485691216367878/images-3.jpg?ex=69f89bb2&is=69f74a32&hm=fe3cbfb764752a764980e59c6ba5453cb8727b446e2680327f917de58e1c26ce&"
TABLE_IMG = "https://cdn.discordapp.com/attachments/1500472877210927197/1500485691493060688/images-4.jpg?ex=69f89bb2&is=69f74a32&hm=c760dae84c49249b44a61227472858cd74193dc5adc8b327283272b8f039b7a3&"
MENU_IMG = "https://cdn.discordapp.com/attachments/1500472877210927197/1500485691854032946/IMG_20260503_173009.jpg?ex=69f89bb2&is=69f74a32&hm=6c66bc20f824b1647acdb05820a463533f7e5777c6f1026f47e1ee5b4cc5bc4e&"
PROTEIN_IMG = "https://cdn.discordapp.com/attachments/1500472877210927197/1500485704705114375/images-7.jpg?ex=69f89bb5&is=69f74a35&hm=d27f738a15660d8da36930d0da310b4514c01403e4a16162df953f030a5717a1&"
ICECREAM_IMG = "https://cdn.discordapp.com/attachments/1500472877210927197/1500485692118143046/images-5.jpg?ex=69f89bb2&is=69f74a32&hm=a74f0750342ef3952c22cf50d103858c12e472fda1fbe028f1022adec4adbecf&"
BILL_IMG = "https://cdn.discordapp.com/attachments/1500472877210927197/1500485692478722118/IMG_20260503_173230.jpg?ex=69f89bb2&is=69f74a32&hm=2bd5c7b3661cb6b411952c402c887e93f853f9c9f6db34607c97f8a03d9bd890&"
DECLINED_IMG = "https://cdn.discordapp.com/attachments/1500472877210927197/1500485705011429427/images-8.jpg?ex=69f89bb5&is=69f74a35&hm=e6d47f47057d9d68e9e26b3f8fda417a09984699f890f675dca9c70c1e42c77f&"
FACE_CARD_IMG = "https://cdn.discordapp.com/attachments/1500472877210927197/1500485692789362818/images-6.jpg?ex=69f89bb2&is=69f74a32&hm=82d4bc32692e0de4824bba71448aedab0fd17d17c63fe6f6872a92e2d152110b&"
OUTSIDE_IMG = "https://cdn.discordapp.com/attachments/1500472877210927197/1500485705275543552/images-9.jpg?ex=69f89bb5&is=69f74a35&hm=5646225a361823e398103c2fed7739bf124e50a24f91b2e2611faffc7df48af6&"
TAXI_IMG = "https://cdn.discordapp.com/attachments/1500472877210927197/1500485705560752219/images-10.jpg?ex=69f89bb5&is=69f74a35&hm=a0344950f54bbb3c19e89a164294ae57f0d1f031fecb21b8d1f1b1150f0aba6c&"
EIFEL_IMG = "https://cdn.discordapp.com/attachments/1500472877210927197/1500485705917399103/eiffel-tower-night.jpg?ex=69f89bb5&is=69f74a35&hm=8716ae951e23070054945ddee117e960d55f50ae2c688182d4ac867cfb3b48eb&"


class DateButtonView(discord.ui.View):
    def __init__(self, cog, channel, allowed_ids, options, mode="both", wrong_values=None, timeout=300):
        super().__init__(timeout=timeout)
        self.cog = cog
        self.channel = channel
        self.allowed_ids = set(allowed_ids)
        self.mode = mode
        self.wrong_values = wrong_values or []
        self.answers = {}
        self.done = asyncio.Event()
        self.message = None

        for label, value, style in options:
            button = discord.ui.Button(label=label, style=style)
            button.callback = self.make_callback(label, value)
            self.add_item(button)

    def make_callback(self, label, value):
        async def callback(interaction: discord.Interaction):
            if interaction.user.id not in self.allowed_ids:
                await interaction.response.defer()
                return

            if interaction.user.id in self.answers:
                await interaction.response.defer()
                return

            if self.mode == "first" and self.answers:
                await interaction.response.defer()
                return

            await interaction.response.defer()

            self.answers[interaction.user.id] = value

            await self.cog.speak(
                self.channel,
                "le weightress",
                WAITRESS_PFP,
                f"{interaction.user.mention} picked **{label}**"
            )

            if value in self.wrong_values:
                await self.cog.speak(
                    self.channel,
                    "Dwayne Rock Jhonson",
                    ROCK_PFP,
                    f"*BONK* {interaction.user.mention}\nwrong choice detected. protein court finds u guilty."
                )

            if self.mode == "first":
                self.done.set()

            if self.mode == "both" and len(self.answers) >= len(self.allowed_ids):
                self.done.set()

        return callback

    async def disable_buttons(self):
        for item in self.children:
            item.disabled = True

        if self.message:
            try:
                await self.message.edit(view=self)
            except:
                pass


class DateCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.active_users = set()

    async def get_webhook(self, channel, name):
        webhooks = await channel.webhooks()

        for webhook in webhooks:
            if webhook.name == name:
                return webhook

        return await channel.create_webhook(name=name)

    async def type_wait(self, channel):
        async with channel.typing():
            await asyncio.sleep(random.randint(3, 5))

    async def speak(self, channel, name, avatar, content=None, image=None):
        webhook = await self.get_webhook(channel, name)

        if image:
            await self.type_wait(channel)
            await webhook.send(
                content=image,
                username=name,
                avatar_url=avatar,
                wait=True,
                allowed_mentions=discord.AllowedMentions(users=True)
            )

        if content:
            await self.type_wait(channel)
            return await webhook.send(
                content=content,
                username=name,
                avatar_url=avatar,
                wait=True,
                allowed_mentions=discord.AllowedMentions(users=True)
            )

    async def button_msg(self, channel, text, view):
        await self.type_wait(channel)
        msg = await channel.send(content=text, view=view)
        view.message = msg
        return msg

    async def make_private_channel(self, guild, name, p1, p2, category=None):
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            p1: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True),
            p2: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True),
            guild.me: discord.PermissionOverwrite(
                view_channel=True,
                send_messages=True,
                manage_channels=True,
                manage_webhooks=True,
                read_message_history=True
            )
        }

        return await guild.create_text_channel(name=name, overwrites=overwrites, category=category)

    async def wait_until_both_talk_silent(self, channel, p1, p2):
        talked = set()

        def check(msg):
            return (
                msg.channel.id == channel.id
                and msg.author.id in [p1.id, p2.id]
                and not msg.author.bot
            )

        while len(talked) < 2:
            msg = await self.bot.wait_for("message", check=check)
            talked.add(msg.author.id)

    async def wait_exact_face_card(self, channel, user):
        await self.speak(
            channel,
            "le weightress",
            WAITRESS_PFP,
            f"{user.mention} bro what now.\ncard went **nyoom denied**.\ndo somthin before i start billing ur bloodline."
        )

        def check(msg):
            return (
                msg.channel.id == channel.id
                and msg.author.id == user.id
                and msg.content.strip().lower() == "lemme scan my face card"
            )

        await self.bot.wait_for("message", check=check)

    @commands.command(name="date")
    async def date(self, ctx, partner: discord.Member = None):
        if DATE_COMMAND_CHANNEL_ID and ctx.channel.id != DATE_COMMAND_CHANNEL_ID:
            return

        if partner is None:
            return await ctx.send("use `.date @user` goofy")

        if partner.bot or partner.id == ctx.author.id:
            return await ctx.send("bro tried dating air 💀")

        if ctx.author.id in self.active_users or partner.id in self.active_users:
            return await ctx.send("one of u already in date jail")

        requester = ctx.author
        allowed = {requester.id, partner.id}

        self.active_users.add(requester.id)
        self.active_users.add(partner.id)

        try:
            accept_view = DateButtonView(
                self,
                ctx.channel,
                {partner.id},
                [
                    ("Accept date", "accept", discord.ButtonStyle.success),
                    ("Reject date", "reject", discord.ButtonStyle.danger)
                ],
                mode="both",
                wrong_values=["reject"],
                timeout=120
            )

            await self.speak(
                ctx.channel,
                "French guy",
                FRENCH_GUY_PFP,
                f"{partner.mention} bonjor baguette.\n{requester.mention} has requested one **fancy restront date**.\n\naccept = romance lore\nreject = emotional tax fraud"
            )

            await self.button_msg(ctx.channel, "date request buttons:", accept_view)

            try:
                await asyncio.wait_for(accept_view.done.wait(), timeout=120)
            except asyncio.TimeoutError:
                return await self.speak(ctx.channel, "French guy", FRENCH_GUY_PFP, "no answer. date evaporated like my will to live.")

            await accept_view.disable_buttons()

            if accept_view.answers.get(partner.id) != "accept":
                return await self.speak(ctx.channel, "French guy", FRENCH_GUY_PFP, "rejected. bro got grilled in le pan.")

            restaurant = await self.make_private_channel(ctx.guild, "le-restront", requester, partner, ctx.channel.category)

            await self.speak(
                ctx.channel,
                "French guy",
                FRENCH_GUY_PFP,
                f"{requester.mention} {partner.mention}\nle restront has spawned: {restaurant.mention}\nmove ur pixels."
            )

            await self.speak(
                restaurant,
                "French guy",
                FRENCH_GUY_PFP,
                "welcum to **le restront**.\ntonight we serve romance, protien, and bank account damage.",
                image=RESTAURANT_IMG
            )

            await self.wait_until_both_talk_silent(restaurant, requester, partner)

            no_count = 0

            while True:
                seat_view = DateButtonView(
                    self,
                    restaurant,
                    allowed,
                    [
                        ("yes seat gud", "yes", discord.ButtonStyle.success),
                        ("no chair ugly", "no", discord.ButtonStyle.danger)
                    ],
                    mode="both",
                    wrong_values=["no"],
                    timeout=300
                )

                await self.speak(
                    restaurant,
                    "le weightress",
                    WAITRESS_PFP,
                    f"here ur chair corner deluxe 5 star depression table.\nseat ok or u wanna act premium?\n\nno counter: `{no_count}/5`",
                    image=TABLE_IMG
                )

                await self.button_msg(restaurant, "seat buttons:", seat_view)
                await seat_view.done.wait()
                await seat_view.disable_buttons()

                if all(v == "yes" for v in seat_view.answers.values()):
                    break

                no_count += list(seat_view.answers.values()).count("no")

                if no_count >= 5:
                    await self.speak(
                        restaurant,
                        "le weightress",
                        WAITRESS_PFP,
                        "5 NO'S??? OUT.\nno date. no food. only pavement."
                    )
                    return

                await self.speak(
                    restaurant,
                    "le weightress",
                    WAITRESS_PFP,
                    f"ok picky royal family.\nasking again before i replace the chairs with emotional support bricks.\nno counter: `{no_count}/5`"
                )

            await self.speak(
                restaurant,
                "le weightress",
                WAITRESS_PFP,
                "finally. sit. do not breathe expensive air too hard."
            )

            await asyncio.sleep(2)

            menu_view = DateButtonView(
                self,
                restaurant,
                allowed,
                [
                    ("Protien", "protein", discord.ButtonStyle.success),
                    ("FAT", "fat", discord.ButtonStyle.danger)
                ],
                mode="both",
                wrong_values=["fat"],
                timeout=300
            )

            await self.speak(
                restaurant,
                "le weightress",
                WAITRESS_PFP,
                "menu time.\nwe have **protien** and **FAT**.\nthat is all because chef failed spelling class.",
                image=MENU_IMG
            )

            await self.button_msg(restaurant, "food buttons:", menu_view)
            await menu_view.done.wait()
            await menu_view.disable_buttons()

            if "fat" in menu_view.answers.values():
                await self.speak(
                    restaurant,
                    "Dwayne Rock Jhonson",
                    ROCK_PFP,
                    "FAT OPTION HAS BEEN REMOVED BY FEDERAL GYM LAW.\neveryone gets protien. cry into ur fork."
                )

            await self.speak(
                restaurant,
                "le weightress",
                WAITRESS_PFP,
                "order locked: **protien**.\nfood takes **1 minute** because the egg is doing character development.\nchat or stare awkwardly idc."
            )

            await asyncio.sleep(60)

            eat_view = DateButtonView(
                self,
                restaurant,
                allowed,
                [("i has eaten", "ate", discord.ButtonStyle.success)],
                mode="both",
                timeout=600
            )

            await self.speak(
                restaurant,
                "le weightress",
                WAITRESS_PFP,
                "FOOD ARRIVD.\nthis plate has more protien than my ex had excuses.\nclick when u finish chewing ur pixels.",
                image=PROTEIN_IMG
            )

            await self.button_msg(restaurant, "eat buttons:", eat_view)
            await eat_view.done.wait()
            await eat_view.disable_buttons()

            ice_view = DateButtonView(
                self,
                restaurant,
                allowed,
                [("ice creem finished", "done", discord.ButtonStyle.success)],
                mode="both",
                timeout=600
            )

            await self.speak(
                restaurant,
                "le weightress",
                WAITRESS_PFP,
                "dessert jumpscare.\nice creem arrived with eyeballs. very french. very legal.",
                image=ICECREAM_IMG
            )

            await self.button_msg(restaurant, "ice creem buttons:", ice_view)
            await ice_view.done.wait()
            await ice_view.disable_buttons()

            pay_view = DateButtonView(
                self,
                restaurant,
                allowed,
                [
                    ("she pay", "she", discord.ButtonStyle.danger),
                    ("i pay", "me", discord.ButtonStyle.success)
                ],
                mode="first",
                wrong_values=["she"],
                timeout=300
            )

            await self.speak(
                restaurant,
                "le weightress",
                WAITRESS_PFP,
                "BILL TIME.\nthis is not a bill this is a financial boss fight.\nwho pay.",
                image=BILL_IMG
            )

            await self.button_msg(restaurant, "payment buttons:", pay_view)
            await pay_view.done.wait()
            await pay_view.disable_buttons()

            await self.speak(
                restaurant,
                "le weightress",
                WAITRESS_PFP,
                f"{requester.mention} card pls.\nbe brave. be broke. be both."
            )

            await asyncio.sleep(3)

            await self.speak(
                restaurant,
                "le weightress",
                WAITRESS_PFP,
                "DECLINED???\nmy brother in baguette the machine just laughed.",
                image=DECLINED_IMG
            )

            await self.wait_exact_face_card(restaurant, requester)

            await self.speak(
                restaurant,
                "le weightress",
                WAITRESS_PFP,
                "wait...\nscanning face card rn...\ncomputer is blushing hold on."
            )

            await asyncio.sleep(3)

            await self.speak(
                restaurant,
                "le weightress",
                WAITRESS_PFP,
                "APPROVED.\nface card carried. bank account useless but face economy strong.",
                image=FACE_CARD_IMG
            )

            outside = await self.make_private_channel(ctx.guild, "le-outside", requester, partner, ctx.channel.category)

            await self.speak(
                restaurant,
                "French guy",
                FRENCH_GUY_PFP,
                f"restront arc complete.\ngo outside before weightress starts charging oxygen: {outside.mention}"
            )

            await self.speak(
                outside,
                "French guy",
                FRENCH_GUY_PFP,
                "outside moment.\nair is free for now.",
                image=OUTSIDE_IMG
            )

            await self.wait_until_both_talk_silent(outside, requester, partner)

            taxi_view = DateButtonView(
                self,
                outside,
                allowed,
                [
                    ("aifil tawar", "tower", discord.ButtonStyle.success),
                    ("house", "house", discord.ButtonStyle.danger)
                ],
                mode="first",
                wrong_values=["house"],
                timeout=300
            )

            await self.speak(
                outside,
                "le taxi driver",
                TAXI_PFP,
                "get in loser.\nwhere we going.\nfirst click decides because democracy got nerfed.",
                image=TAXI_IMG
            )

            await self.button_msg(outside, "taxi buttons:", taxi_view)
            await taxi_view.done.wait()
            await taxi_view.disable_buttons()

            if list(taxi_view.answers.values())[0] == "house":
                await self.speak(
                    outside,
                    "Dwayne Rock Jhonson",
                    ROCK_PFP,
                    "HOUSE???\nno. date needs monument. go look at metal triangle."
                )

            await self.speak(
                outside,
                "le taxi driver",
                TAXI_PFP,
                "destination: **aifil tawar**.\ndrive time: **30 seconds**.\nseatbelt optional. regret mandatory."
            )

            await asyncio.sleep(30)

            tower = await self.make_private_channel(ctx.guild, "aifal-tower", requester, partner, ctx.channel.category)

            await self.speak(
                outside,
                "le taxi driver",
                TAXI_PFP,
                f"we here.\nget out my car and go romance over there: {tower.mention}"
            )

            await self.speak(
                tower,
                "le taxi driver",
                TAXI_PFP,
                "welcome to **aifal tawar**.\nu got **5 minutes**.\nbe cute. be cringe. i am not watching. probably.",
                image=EIFEL_IMG
            )

            await asyncio.sleep(300)

            end_view = DateButtonView(
                self,
                tower,
                allowed,
                [
                    ("kiss and end date", "kiss", discord.ButtonStyle.success),
                    ("no kiss ending", "no_kiss", discord.ButtonStyle.danger)
                ],
                mode="both",
                wrong_values=["no_kiss"],
                timeout=300
            )

            await self.speak(
                tower,
                "French guy",
                FRENCH_GUY_PFP,
                "final boss choice.\nchoose ending.\nno kiss ending is available but also illegal."
            )

            await self.button_msg(tower, "ending buttons:", end_view)
            await end_view.done.wait()
            await end_view.disable_buttons()

            if "no_kiss" in end_view.answers.values():
                await self.speak(
                    tower,
                    "Dwayne Rock Jhonson",
                    ROCK_PFP,
                    "NO KISS???\nbad ending patched. forced update installed."
                )

            await self.speak(
                tower,
                "French guy",
                FRENCH_GUY_PFP,
                f"{requester.mention} and {partner.mention} ended le date with kiss.\ncinema. protien. face card economy. peak fiction."
            )

        finally:
            self.active_users.discard(requester.id)
            self.active_users.discard(partner.id)


async def setup(bot):
    await bot.add_cog(DateCog(bot))
