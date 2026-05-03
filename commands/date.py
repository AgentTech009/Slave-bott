import discord
from discord.ext import commands
import asyncio

DATE_COMMAND_CHANNEL_ID = None

# PASTE YOUR IMAGE LINKS HERE
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
    def __init__(self, allowed_ids, options, mode="both", timeout=300):
        super().__init__(timeout=timeout)
        self.allowed_ids = set(allowed_ids)
        self.mode = mode
        self.answers = {}
        self.done = asyncio.Event()

        for label, value, style in options:
            button = discord.ui.Button(label=label, style=style)
            button.callback = self.make_callback(value)
            self.add_item(button)

    def make_callback(self, value):
        async def callback(interaction: discord.Interaction):
            if interaction.user.id not in self.allowed_ids:
                return await interaction.response.send_message(
                    "This date is not for you gang 💀",
                    ephemeral=True
                )

            if self.mode == "first" and self.answers:
                return await interaction.response.send_message(
                    "Too late. Someone already picked 😭",
                    ephemeral=True
                )

            self.answers[interaction.user.id] = value

            await interaction.response.send_message("Choice locked ✅", ephemeral=True)

            if self.mode == "first":
                self.done.set()

            if self.mode == "both" and len(self.answers) >= len(self.allowed_ids):
                self.done.set()

        return callback


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

    async def speak(self, channel, name, avatar, content=None, image=None):
        webhook = await self.get_webhook(channel, name)

        if image:
            content = f"{content}\n{image}" if content else image

        return await webhook.send(
            content=content,
            username=name,
            avatar_url=avatar,
            wait=True,
            allowed_mentions=discord.AllowedMentions(users=True)
        )

    async def button_msg(self, channel, text, view):
        return await channel.send(content=text, view=view)

    async def make_private_channel(self, guild, name, p1, p2, category=None):
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            p1: discord.PermissionOverwrite(
                view_channel=True,
                send_messages=True,
                read_message_history=True
            ),
            p2: discord.PermissionOverwrite(
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

        return await guild.create_text_channel(
            name=name,
            overwrites=overwrites,
            category=category
        )

    async def wait_until_both_talk(self, channel, p1, p2, text):
        talked = set()

        await self.speak(
            channel,
            "le weightress",
            WAITRESS_PFP,
            f"{text}\n\nBoth of you type any message here once. Normal chat after that will be ignored unless I ask."
        )

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
            f"{user.mention}, say this exact sentence:\n`lemme scan my face card`"
        )

        def check(msg):
            return (
                msg.channel.id == channel.id
                and msg.author.id == user.id
                and msg.content.strip() == "lemme scan my face card"
            )

        await self.bot.wait_for("message", check=check)

    @commands.command(name="date")
    async def date(self, ctx, partner: discord.Member = None):
        if DATE_COMMAND_CHANNEL_ID and ctx.channel.id != DATE_COMMAND_CHANNEL_ID:
            return

        if partner is None:
            return await ctx.send("Use `.date @user`")

        if partner.bot or partner.id == ctx.author.id:
            return await ctx.send("Pick a real person bro 😭")

        if ctx.author.id in self.active_users or partner.id in self.active_users:
            return await ctx.send("One of you is already in a date.")

        requester = ctx.author
        allowed = {requester.id, partner.id}

        self.active_users.add(requester.id)
        self.active_users.add(partner.id)

        try:
            accept_view = DateButtonView(
                {partner.id},
                [
                    ("Accept date", "accept", discord.ButtonStyle.success),
                    ("Reject date", "reject", discord.ButtonStyle.danger)
                ],
                mode="both",
                timeout=120
            )

            await self.speak(
                ctx.channel,
                "French guy",
                FRENCH_GUY_PFP,
                f"{partner.mention}, bonjour. {requester.mention} has requested one extremely suspicious fancy date.\n\n"
                "Click **Accept date** to enter romance lore.\n"
                "Click **Reject date** to publicly destroy bro."
            )

            button_message = await self.button_msg(ctx.channel, "Choose below:", accept_view)

            try:
                await asyncio.wait_for(accept_view.done.wait(), timeout=120)
            except asyncio.TimeoutError:
                return await self.speak(ctx.channel, "French guy", FRENCH_GUY_PFP, "No answer. Date cancelled. Pain.")

            try:
                await button_message.delete()
            except:
                pass

            if accept_view.answers.get(partner.id) != "accept":
                return await self.speak(ctx.channel, "French guy", FRENCH_GUY_PFP, "Rejected. Bro got cooked.")

            restaurant = await self.make_private_channel(
                ctx.guild,
                "le-restront",
                requester,
                partner,
                category=ctx.channel.category
            )

            await self.speak(
                ctx.channel,
                "French guy",
                FRENCH_GUY_PFP,
                f"Magnifique. {requester.mention} {partner.mention}, kindly move to {restaurant.mention}."
            )

            await self.speak(
                restaurant,
                "French guy",
                FRENCH_GUY_PFP,
                "Welcome to **le restront**.\nTonight includes luxury, protein, romance and financial crime.",
                image=RESTAURANT_IMG
            )

            await self.wait_until_both_talk(
                restaurant,
                requester,
                partner,
                "Confirm your existence before I show you the seat."
            )

            no_count = 0

            while True:
                seat_view = DateButtonView(
                    allowed,
                    [
                        ("Yes this seat is okay", "yes", discord.ButtonStyle.success),
                        ("No this seat sucks", "no", discord.ButtonStyle.danger)
                    ],
                    mode="both",
                    timeout=300
                )

                await self.speak(
                    restaurant,
                    "le weightress",
                    WAITRESS_PFP,
                    "Here is your romantic table. Is this seat okay?\n\nBoth must choose. You can say no only 5 total times before I throw you out.",
                    image=TABLE_IMG
                )

                btn = await self.button_msg(restaurant, "Seat choice:", seat_view)
                await seat_view.done.wait()

                try:
                    await btn.delete()
                except:
                    pass

                if all(v == "yes" for v in seat_view.answers.values()):
                    break

                no_count += list(seat_view.answers.values()).count("no")

                if no_count >= 5:
                    await self.speak(
                        restaurant,
                        "le weightress",
                        WAITRESS_PFP,
                        "ENOUGH. Five no's. OUT. Go eat oxygen."
                    )
                    return

                await self.speak(
                    restaurant,
                    "le weightress",
                    WAITRESS_PFP,
                    f"No count: `{no_count}/5`.\nI ask again. Choose correctly this time before I become a villain."
                )

            await self.speak(
                restaurant,
                "le weightress",
                WAITRESS_PFP,
                "Finally. Sit down before the chair resigns."
            )

            menu_view = DateButtonView(
                allowed,
                [
                    ("Protein", "protein", discord.ButtonStyle.success),
                    ("Fat", "fat", discord.ButtonStyle.danger)
                ],
                mode="both",
                timeout=300
            )

            await self.speak(
                restaurant,
                "le weightress",
                WAITRESS_PFP,
                "Here is tonight's menu.\nOptions: **Protein** or **Fat**.\nChoose wisely. The bald protein guardian is watching.",
                image=MENU_IMG
            )

            btn = await self.button_msg(restaurant, "Pick your food:", menu_view)
            await menu_view.done.wait()

            try:
                await btn.delete()
            except:
                pass

            if "fat" in menu_view.answers.values():
                await self.speak(
                    restaurant,
                    "Dwayne Rock Jhonson",
                    ROCK_PFP,
                    "NO. FAT HAS BEEN CANCELLED.\nYou are getting protein. Be grateful."
                )

            await self.speak(
                restaurant,
                "le weightress",
                WAITRESS_PFP,
                "Order locked: **Protein**.\n\nFood arrives in **1 minute**. You may talk now. I will return when the protein is emotionally ready."
            )

            await asyncio.sleep(60)

            eat_view = DateButtonView(
                allowed,
                [("I ate", "ate", discord.ButtonStyle.success)],
                mode="both",
                timeout=600
            )

            await self.speak(
                restaurant,
                "le weightress",
                WAITRESS_PFP,
                "Your protein meal has arrived. It has more gains than your bloodline.\n\nClick **I ate** when both of you are done.",
                image=PROTEIN_IMG
            )

            btn = await self.button_msg(restaurant, "Eating confirmation:", eat_view)
            await eat_view.done.wait()

            try:
                await btn.delete()
            except:
                pass

            ice_view = DateButtonView(
                allowed,
                [("I finished ice cream", "done", discord.ButtonStyle.success)],
                mode="both",
                timeout=600
            )

            await self.speak(
                restaurant,
                "le weightress",
                WAITRESS_PFP,
                "Dessert time. Ice cream has arrived because even protein soldiers need happiness.\n\nClick when done.",
                image=ICECREAM_IMG
            )

            btn = await self.button_msg(restaurant, "Dessert confirmation:", ice_view)
            await ice_view.done.wait()

            try:
                await btn.delete()
            except:
                pass

            pay_view = DateButtonView(
                allowed,
                [
                    ("She pays", "she", discord.ButtonStyle.danger),
                    ("I pay", "me", discord.ButtonStyle.success)
                ],
                mode="first",
                timeout=300
            )

            await self.speak(
                restaurant,
                "le weightress",
                WAITRESS_PFP,
                "The bill has arrived.\n\nWho is paying? First choice decides. Choose carefully.",
                image=BILL_IMG
            )

            btn = await self.button_msg(restaurant, "Payment choice:", pay_view)
            await pay_view.done.wait()

            try:
                await btn.delete()
            except:
                pass

            if list(pay_view.answers.values())[0] == "she":
                await self.speak(
                    restaurant,
                    "Dwayne Rock Jhonson",
                    ROCK_PFP,
                    f"*BONK* {partner.mention} princesses do not pay. Sit down."
                )

            await self.speak(
                restaurant,
                "le weightress",
                WAITRESS_PFP,
                f"{requester.mention}, your turn. Pay like a financially suspicious gentleman."
            )

            await asyncio.sleep(2)

            await self.speak(
                restaurant,
                "le weightress",
                WAITRESS_PFP,
                "Card declined.\nI am calm. I am professional. I am about to throw a fork.",
                image=DECLINED_IMG
            )

            await self.wait_exact_face_card(restaurant, requester)

            await self.speak(
                restaurant,
                "le weightress",
                WAITRESS_PFP,
                "Scanning face card..."
            )

            await asyncio.sleep(3)

            await self.speak(
                restaurant,
                "le weightress",
                WAITRESS_PFP,
                "Accepted. Face card approved. You may leave before I change my mind.",
                image=FACE_CARD_IMG
            )

            outside = await self.make_private_channel(
                ctx.guild,
                "le-outside",
                requester,
                partner,
                category=ctx.channel.category
            )

            await self.speak(
                restaurant,
                "French guy",
                FRENCH_GUY_PFP,
                f"Restaurant arc complete. Move to {outside.mention}."
            )

            await self.speak(
                outside,
                "French guy",
                FRENCH_GUY_PFP,
                "You are outside. The night is cold. The vibes are expensive.",
                image=OUTSIDE_IMG
            )

            await self.wait_until_both_talk(
                outside,
                requester,
                partner,
                "Both of you type anything and the taxi driver will arrive."
            )

            taxi_view = DateButtonView(
                allowed,
                [
                    ("Aifil Tawar", "tower", discord.ButtonStyle.success),
                    ("House", "house", discord.ButtonStyle.danger)
                ],
                mode="first",
                timeout=300
            )

            await self.speak(
                outside,
                "le taxi driver",
                TAXI_PFP,
                "Where are we going?\nFirst valid choice decides.",
                image=TAXI_IMG
            )

            btn = await self.button_msg(outside, "Pick destination:", taxi_view)
            await taxi_view.done.wait()

            try:
                await btn.delete()
            except:
                pass

            first_choice = list(taxi_view.answers.values())[0]

            if first_choice == "house":
                await self.speak(
                    outside,
                    "Dwayne Rock Jhonson",
                    ROCK_PFP,
                    "NO. You are not going home. Romance requires architecture. Go to Aifal Tawar."
                )

            await self.speak(
                outside,
                "le taxi driver",
                TAXI_PFP,
                "Destination locked: **Aifal Tawar**.\nDrive time: **30 seconds**. Talk while I commit French traffic crimes."
            )

            await asyncio.sleep(30)

            tower = await self.make_private_channel(
                ctx.guild,
                "aifal-tower",
                requester,
                partner,
                category=ctx.channel.category
            )

            await self.speak(
                outside,
                "le taxi driver",
                TAXI_PFP,
                f"We are here. Get out. Move to {tower.mention}."
            )

            await self.speak(
                tower,
                "le taxi driver",
                TAXI_PFP,
                "Welcome to **Aifal Tawar**.\nYou have **5 minutes** to talk and do whatever romantic nonsense you want.",
                image=EIFEL_IMG
            )

            await asyncio.sleep(300)

            end_view = DateButtonView(
                allowed,
                [
                    ("Kiss and end the date", "kiss", discord.ButtonStyle.success),
                    ("End with no kiss", "no_kiss", discord.ButtonStyle.danger)
                ],
                mode="both",
                timeout=300
            )

            await self.speak(
                tower,
                "French guy",
                FRENCH_GUY_PFP,
                "The date is ending.\nBoth must choose the ending.\nIf anyone picks no kiss, the protein guardian interferes."
            )

            btn = await self.button_msg(tower, "Choose ending:", end_view)
            await end_view.done.wait()

            try:
                await btn.delete()
            except:
                pass

            if "no_kiss" in end_view.answers.values():
                await self.speak(
                    tower,
                    "Dwayne Rock Jhonson",
                    ROCK_PFP,
                    "NO. Bad ending rejected. KISS ENDING HAS BEEN FORCEFULLY INSTALLED."
                )

            await self.speak(
                tower,
                "French guy",
                FRENCH_GUY_PFP,
                f"{requester.mention} and {partner.mention} ended the date with a kiss.\n\nCinema. Protein. Financial recovery. 10/10."
            )

        finally:
            self.active_users.discard(requester.id)
            self.active_users.discard(partner.id)


async def setup(bot):
    await bot.add_cog(DateCog(bot))
