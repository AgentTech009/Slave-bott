import discord
from discord.ext import commands
import asyncio
import random

# Optional: set to a channel ID if .date should only work there
DATE_COMMAND_CHANNEL_ID = None

FRENCH_GUY_PFP = "https://cdn.discordapp.com/attachments/1500472877210927197/1500472967065243708/IMG_20260503_172432.jpg?ex=69f88fd8&is=69f73e58&hm=85414fb9f7a316237a61efaef30e93785a9074d137c2c120affe5dcd4656dd93&"
WAITRESS_PFP = "https://cdn.discordapp.com/attachments/1500472877210927197/1500472966750801962/IMG_20260503_172534.jpg?ex=69f88fd8&is=69f73e58&hm=1f468c4fbebef050e14baee1aa47a9c1b0af40eabf7e2e8f34310bedc116a13c&"
ROCK_PFP = "https://cdn.discordapp.com/attachments/1500472877210927197/1500472966377640067/images-1.jpg?ex=69f88fd8&is=69f73e58&hm=652e0ae389d9030d6748869ece76c42de8732924f1390dad59622d9294ff0846&"
TAXI_PFP = "https://cdn.discordapp.com/attachments/1500472877210927197/1500472966138433596/images-2.jpg?ex=69f88fd8&is=69f73e58&hm=4579cbcaef50e7f12ff09e8d92a90cf2f078465a4e2e823c14083416640e85e8&"

RESTAURANT_IMG = "https://cdn.discordapp.com/attachments/1500472877210927197/1500472965857546240/images-3.jpg?ex=69f88fd8&is=69f73e58&hm=d23d2603416fdf634de2329418798fcc6bdbecb9b18ade0134c3693bdfcbf608&"
TABLE_IMG = "https://cdn.discordapp.com/attachments/1500472877210927197/1500472960719261716/images-4.jpg?ex=69f88fd7&is=69f73e57&hm=b98a3923c8ccc984c00e4255ada9572b8e8ade7e55923d4cc40467aeb44e25ee&"
MENU_IMG = "https://cdn.discordapp.com/attachments/1500472877210927197/1500472959653908681/IMG_20260503_173009.jpg?ex=69f88fd7&is=69f73e57&hm=940f7a43cb63229c7719edf4a8ffad97411b979e7d92f447f7d2c9a542b28f64&"
PROTEIN_IMG = "https://cdn.discordapp.com/attachments/1500472877210927197/1500472958831951922/images-7.jpg?ex=69f88fd6&is=69f73e56&hm=aa92e8a7196f1c27cd39d8c72ae04ad500a06bc2ecaa89c394b5b5c2a71753e9&"
ICECREAM_IMG = "https://cdn.discordapp.com/attachments/1500472877210927197/1500472959222153316/images-5.jpg?ex=69f88fd6&is=69f73e56&hm=bd08067d9f5d199d05792f4fad39ca6049d1ddcab593b80ab5d61dea0ae2a843&"
BILL_IMG = "https://cdn.discordapp.com/attachments/1500472877210927197/1500472960383979681/IMG_20260503_173230.jpg?ex=69f88fd7&is=69f73e57&hm=f2413bc7733a6bf1864b63193716bf083594d5a7664c1d08870e99822cfc1398&"
DECLINED_IMG = "https://cdn.discordapp.com/attachments/1500472877210927197/1500472958521446470/images-8.jpg?ex=69f88fd6&is=69f73e56&hm=e708feb064fabb3b51b5110a7faa35e8ec1aca0a6917be4b025ecb5054fe29c6&"
FACE_CARD_IMG = "https://cdn.discordapp.com/attachments/1500472877210927197/1500472959947640934/images-6.jpg?ex=69f88fd7&is=69f73e57&hm=505ba4fde0977c35ab63db638d1d9c0fce3230b6d05e9a43137e6192e2285ee1&"
OUTSIDE_IMG = "https://cdn.discordapp.com/attachments/1500472877210927197/1500472958198747286/images-9.jpg?ex=69f88fd6&is=69f73e56&hm=edc75e9262e483b597f2a3ce8852eecc9caa49cb1e99447a5fc05eb22287bad1&"
TAXI_IMG = "https://cdn.discordapp.com/attachments/1500472877210927197/1500472957938569276/images-10.jpg?ex=69f88fd6&is=69f73e56&hm=64225e45a164e0c9880c5752544b1e66f5cc4f0a2f5432524fed36e2f2bdf51a&"
EIFEL_IMG = "https://cdn.discordapp.com/attachments/1500472877210927197/1500472957602893935/eiffel-tower-night.jpg?ex=69f88fd6&is=69f73e56&hm=cf3c28b806062424ad22816e5351716aae26c64c999d9b2e346ca84bbc1efc24&"


class DateButtonView(discord.ui.View):
    def __init__(self, allowed_ids, options, timeout=300):
        super().__init__(timeout=timeout)
        self.allowed_ids = allowed_ids
        self.answers = {}
        self.done = asyncio.Event()

        for label, value, style in options:
            btn = discord.ui.Button(label=label, style=style)
            btn.callback = self.make_callback(value)
            self.add_item(btn)

    def make_callback(self, value):
        async def callback(interaction: discord.Interaction):
            if interaction.user.id not in self.allowed_ids:
                return await interaction.response.send_message("This date is not for you gang 💀", ephemeral=True)

            self.answers[interaction.user.id] = value
            await interaction.response.send_message("Choice locked ✅", ephemeral=True)

            if len(self.answers) >= len(self.allowed_ids):
                self.done.set()

        return callback


class DateCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.active_users = set()

    async def get_webhook(self, channel, name):
        hooks = await channel.webhooks()
        for hook in hooks:
            if hook.name == name:
                return hook
        return await channel.create_webhook(name=name)

    async def speak(self, channel, name, avatar, content=None, image=None, view=None):
        hook = await self.get_webhook(channel, name)

        if image:
            content = f"{content}\n{image}" if content else image

        return await hook.send(
            content=content,
            username=name,
            avatar_url=avatar,
            view=view,
            wait=True,
            allowed_mentions=discord.AllowedMentions(users=True)
        )

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
            ),
        }

        return await guild.create_text_channel(
            name=name,
            overwrites=overwrites,
            category=category
        )

    async def wait_until_both_talk(self, channel, p1, p2, reason_text):
        talked = set()

        await self.speak(
            channel,
            "le weightress",
            WAITRESS_PFP,
            f"{reason_text}\n\nBoth of you type literally anything here so I know you are present. Random yapping after this will be ignored unless I ask for it."
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
            f"{user.mention} say this exact sentence or we are washing dishes till 2042:\n`lemme scan my face card`"
        )

        def check(msg):
            return (
                msg.channel.id == channel.id
                and msg.author.id == user.id
                and msg.content.strip() == "lemme scan my face card"
            )

        await self.bot.wait_for("message", check=check)

    async def cleanup_later(self, *channels):
        await asyncio.sleep(15)
        for ch in channels:
            try:
                await ch.delete()
            except:
                pass

    @commands.command(name="date")
    async def date(self, ctx, partner: discord.Member = None):
        if DATE_COMMAND_CHANNEL_ID and ctx.channel.id != DATE_COMMAND_CHANNEL_ID:
            return

        if partner is None:
            return await ctx.send("Use `.date @user`")

        if partner.bot or partner.id == ctx.author.id:
            return await ctx.send("Pick a real person bro 😭")

        if ctx.author.id in self.active_users or partner.id in self.active_users:
            return await ctx.send("One of you is already in a date. Scandalous.")

        self.active_users.add(ctx.author.id)
        self.active_users.add(partner.id)

        restaurant = None
        outside = None
        tower = None

        try:
            requester = ctx.author
            allowed = {requester.id, partner.id}

            accept_view = DateButtonView(
                {partner.id},
                [
                    ("Accept date", "accept", discord.ButtonStyle.success),
                    ("Reject date", "reject", discord.ButtonStyle.danger),
                ],
                timeout=120
            )

            await self.speak(
                ctx.channel,
                "French guy",
                FRENCH_GUY_PFP,
                f"{partner.mention}, bonjour. {requester.mention} has requested one extremely suspicious fancy date.\n\n"
                "Click **Accept date** to enter romance lore.\n"
                "Click **Reject date** to publicly destroy bro.",
                view=accept_view
            )

            try:
                await asyncio.wait_for(accept_view.done.wait(), timeout=120)
            except asyncio.TimeoutError:
                return await self.speak(ctx.channel, "French guy", FRENCH_GUY_PFP, "No answer. Date cancelled. Pain.")

            if accept_view.answers.get(partner.id) != "accept":
                return await self.speak(ctx.channel, "French guy", FRENCH_GUY_PFP, "Rejected. Bro got cooked medium rare.")

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
                f"Magnifique. {requester.mention} {partner.mention}, kindly move to {restaurant.mention}.\n"
                "The restaurant is ready and the staff is only mildly unstable."
            )

            await self.speak(
                restaurant,
                "French guy",
                FRENCH_GUY_PFP,
                f"Welcome to **le restront**.\nTonight you will experience luxury, protein, emotional damage and maybe tax fraud.",
                image=RESTAURANT_IMG
            )

            await self.wait_until_both_talk(
                restaurant,
                requester,
                partner,
                "Please confirm your existence before I show you the seat."
            )

            no_count = 0

            while True:
                seat_view = DateButtonView(
                    allowed,
                    [
                        ("Yes this seat is okay", "yes", discord.ButtonStyle.success),
                        ("No this seat sucks", "no", discord.ButtonStyle.danger),
                    ],
                    timeout=300
                )

                await self.speak(
                    restaurant,
                    "le weightress",
                    WAITRESS_PFP,
                    "Here is your romantic table. Is this seat okay?\n\nBoth of you must choose. You may say no only 5 total times before I throw you into the street.",
                    image=TABLE_IMG,
                    view=seat_view
                )

                await seat_view.done.wait()

                if all(v == "yes" for v in seat_view.answers.values()):
                    break

                no_count += list(seat_view.answers.values()).count("no")

                if no_count >= 5:
                    await self.speak(
                        restaurant,
                        "le weightress",
                        WAITRESS_PFP,
                        "ENOUGH. Five no's. OUT. Go eat air."
                    )
                    await self.cleanup_later(restaurant)
                    return

                await self.speak(
                    restaurant,
                    "le weightress",
                    WAITRESS_PFP,
                    f"Wrong opinion detected. No count: `{no_count}/5`.\nI will ask again. Pick better this time."
                )

            await self.speak(
                restaurant,
                "le weightress",
                WAITRESS_PFP,
                "Finally. Sit down before the chair union complains."
            )

            menu_view = DateButtonView(
                allowed,
                [
                    ("Protein", "protein", discord.ButtonStyle.success),
                    ("Fat", "fat", discord.ButtonStyle.danger),
                ],
                timeout=300
            )

            await self.speak(
                restaurant,
                "le weightress",
                WAITRESS_PFP,
                "Here is tonight's legendary menu.\n\nYou have two options: **Protein** or **Fat**.\nChoose wisely. The kitchen is being supervised by a bald gym deity.",
                image=MENU_IMG,
                view=menu_view
            )

            await menu_view.done.wait()

            if "fat" in menu_view.answers.values():
                await self.speak(
                    restaurant,
                    "Dwayne Rock Jhonson",
                    ROCK_PFP,
                    "NO. ABSOLUTELY NOT. FAT HAS BEEN CANCELLED.\nYou are getting protein. Be grateful.",
                )

            await self.speak(
                restaurant,
                "le weightress",
                WAITRESS_PFP,
                "Order locked: **Protein**.\n\nYour food will arrive in **1 minute**. You may talk now. I will return when the protein has finished emotionally preparing."
            )

            await asyncio.sleep(60)

            eat_view = DateButtonView(
                allowed,
                [
                    ("I ate", "ate", discord.ButtonStyle.success),
                ],
                timeout=600
            )

            await self.speak(
                restaurant,
                "le weightress",
                WAITRESS_PFP,
                "Your protein meal has arrived. It has more gains than your entire bloodline.\n\nWhen both of you are done eating click **I ate**.",
                image=PROTEIN_IMG,
                view=eat_view
            )

            await eat_view.done.wait()

            ice_view = DateButtonView(
                allowed,
                [
                    ("I finished ice cream", "done", discord.ButtonStyle.success),
                ],
                timeout=600
            )

            await self.speak(
                restaurant,
                "le weightress",
                WAITRESS_PFP,
                "Dessert time. Ice cream has arrived because even protein warriors need joy.\n\nClick **I finished ice cream** when both of you are done.",
                image=ICECREAM_IMG,
                view=ice_view
            )

            await ice_view.done.wait()

            pay_view = DateButtonView(
                allowed,
                [
                    ("She pays", "she", discord.ButtonStyle.danger),
                    ("I pay", "me", discord.ButtonStyle.success),
                ],
                timeout=300
            )

            await self.speak(
                restaurant,
                "le weightress",
                WAITRESS_PFP,
                "The bill has arrived.\n\nWho is paying? Choose carefully. Society is watching.",
                image=BILL_IMG,
                view=pay_view
            )

            await pay_view.done.wait()

            if pay_view.answers.get(partner.id) == "she" or "she" in pay_view.answers.values():
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
                f"{requester.mention}, your turn. Pay the bill like the financially questionable gentleman you are."
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
                "Accepted. Annoyingly handsome payment method approved. You may leave.",
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
                f"The restaurant arc is complete. Kindly move to {outside.mention} before the waitress changes her mind."
            )

            await self.speak(
                outside,
                "French guy",
                FRENCH_GUY_PFP,
                "You are now outside. The night is cold. The vibes are expensive.",
                image=OUTSIDE_IMG
            )

            await self.wait_until_both_talk(
                outside,
                requester,
                partner,
                "Both of you type anything here and the taxi driver will arrive."
            )

            taxi_view = DateButtonView(
                allowed,
                [
                    ("Aifil Tawar", "tower", discord.ButtonStyle.success),
                    ("House", "house", discord.ButtonStyle.danger),
                ],
                timeout=300
            )

            await self.speak(
                outside,
                "le taxi driver",
                TAXI_PFP,
                "Where are we going?\n\nFirst valid choice decides the destination. Pick wisely because I drive like a side quest NPC.",
                image=TAXI_IMG,
                view=taxi_view
            )

            while not taxi_view.answers:
                await asyncio.sleep(0.5)

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
                "Destination locked: **Aifal Tawar**.\nDrive time: **30 seconds**.\nTalk in the taxi while I violate every traffic law in France."
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
                f"We are here. Get out. Kindly move to {tower.mention}. I do not accept emotional baggage as payment."
            )

            await self.speak(
                tower,
                "le taxi driver",
                TAXI_PFP,
                "Welcome to **Aifal Tawar**.\nYou have **5 minutes** to talk, be cute, stare at pixels and pretend this is Paris.",
                image=EIFEL_IMG
            )

            await asyncio.sleep(300)

            end_view = DateButtonView(
                allowed,
                [
                    ("Kiss and end the date", "kiss", discord.ButtonStyle.success),
                    ("End with no kiss", "no_kiss", discord.ButtonStyle.danger),
                ],
                timeout=300
            )

            await self.speak(
                tower,
                "French guy",
                FRENCH_GUY_PFP,
                "The date is ending.\n\nBoth of you must choose the ending.\nIf anyone chooses **no kiss**, the bald romance guardian will interfere.",
                view=end_view
            )

            await end_view.done.wait()

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

            await asyncio.sleep(10)

            await self.speak(
                tower,
                "le taxi driver",
                TAXI_PFP,
                "Date complete. I am leaving. Please do not summon me again unless there is petrol money."
            )

        finally:
            self.active_users.discard(ctx.author.id)
            if partner:
                self.active_users.discard(partner.id)


async def setup(bot):
    await bot.add_cog(DateCog(bot))
