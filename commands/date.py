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
    def __init__(self, allowed_ids, timeout=120):
        super().__init__(timeout=timeout)
        self.allowed_ids = set(allowed_ids)
        self.answers = {}
        self.done = asyncio.Event()
        self.message = None

        accept = discord.ui.Button(label="Accept date", style=discord.ButtonStyle.success)
        reject = discord.ui.Button(label="Reject date", style=discord.ButtonStyle.danger)

        accept.callback = self.accept_callback
        reject.callback = self.reject_callback

        self.add_item(accept)
        self.add_item(reject)

    async def accept_callback(self, interaction: discord.Interaction):
        await self.handle_click(interaction, "accept")

    async def reject_callback(self, interaction: discord.Interaction):
        await self.handle_click(interaction, "reject")

    async def handle_click(self, interaction, value):
        if interaction.user.id not in self.allowed_ids:
            await interaction.response.defer()
            return

        if interaction.user.id in self.answers:
            await interaction.response.defer()
            return

        await interaction.response.defer()
        self.answers[interaction.user.id] = value
        self.done.set()

    async def disable_buttons(self):
        for item in self.children:
            item.disabled = True

        if self.message:
            try:
                await self.message.edit(view=self)
            except Exception:
                pass


class DateCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.active_users = set()

    async def get_webhook(self, channel, name):
        try:
            webhooks = await channel.webhooks()
            for webhook in webhooks:
                if webhook.name == name:
                    return webhook
        except Exception:
            pass

        return await channel.create_webhook(name=name)

    async def type_wait(self, channel):
        async with channel.typing():
            await asyncio.sleep(random.uniform(0.5, 1.0))

    async def send_webhook(self, channel, name, avatar, content):
        await self.type_wait(channel)
        webhook = await self.get_webhook(channel, name)

        try:
            return await webhook.send(
                content=content,
                username=name,
                avatar_url=avatar,
                wait=True,
                allowed_mentions=discord.AllowedMentions(users=True)
            )
        except (discord.NotFound, discord.HTTPException):
            webhook = await channel.create_webhook(name=name)
            return await webhook.send(
                content=content,
                username=name,
                avatar_url=avatar,
                wait=True,
                allowed_mentions=discord.AllowedMentions(users=True)
            )

    async def speak(self, channel, name, avatar, content=None, image=None):
        last_msg = None

        if image:
            last_msg = await self.send_webhook(channel, name, avatar, image)

        if content:
            parts = [p.strip() for p in content.split("\n") if p.strip()]
            for part in parts:
                last_msg = await self.send_webhook(channel, name, avatar, part)

        return last_msg

    async def persona_reply(self, msg, content="okey"):
        try:
            await msg.reply(content, mention_author=False)
        except Exception:
            await msg.channel.send(content)

    async def button_msg(self, channel, text, view):
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

    async def wait_for_phrase(self, channel, user, phrases, timeout=300, ack=True):
        phrases = [p.lower() for p in phrases]

        def check(msg):
            return (
                msg.channel.id == channel.id
                and msg.author.id == user.id
                and not msg.author.bot
                and any(p in msg.content.lower() for p in phrases)
            )

        try:
            msg = await asyncio.wait_for(self.bot.wait_for("message", check=check), timeout=timeout)
        except asyncio.TimeoutError:
            return None

        if ack:
            await self.persona_reply(msg, "okey")

        return msg

    async def wait_text_choices(
        self,
        channel,
        users,
        choices,
        ask_name,
        ask_avatar,
        mode="both",
        timeout=300,
        ack=True
    ):
        allowed_ids = {u.id for u in users}
        answers = {}
        missing_pinged = set()

        def check(msg):
            return (
                msg.channel.id == channel.id
                and not msg.author.bot
                and msg.author.id in allowed_ids
                and msg.author.id not in answers
                and msg.content.lower().strip() in choices
            )

        while True:
            try:
                msg = await asyncio.wait_for(self.bot.wait_for("message", check=check), timeout=timeout)
            except asyncio.TimeoutError:
                return answers

            value, label = choices[msg.content.lower().strip()]
            answers[msg.author.id] = value

            if ack:
                await self.persona_reply(msg, "okey")

            if mode == "first":
                return answers

            await asyncio.sleep(0.2)

            if len(answers) >= len(allowed_ids):
                return answers

            for user in users:
                if user.id not in answers and user.id not in missing_pinged:
                    missing_pinged.add(user.id)
                    await self.speak(channel, ask_name, ask_avatar, f"what abt {user.mention}")

    async def wait_menu_choices(self, channel, users, timeout=300):
        allowed_ids = {u.id for u in users}
        answers = {}
        missing_pinged = set()

        def check(msg):
            return (
                msg.channel.id == channel.id
                and not msg.author.bot
                and msg.author.id in allowed_ids
                and msg.author.id not in answers
                and msg.content.lower().strip() in ["fat", "protien", "protein"]
            )

        while len(answers) < len(allowed_ids):
            try:
                msg = await asyncio.wait_for(self.bot.wait_for("message", check=check), timeout=timeout)
            except asyncio.TimeoutError:
                return answers

            choice = msg.content.lower().strip()

            if choice == "fat":
                answers[msg.author.id] = "protein"
                await self.speak(channel, "Dwayne Rock Jhonson", ROCK_PFP, "FAT??!!")
                await self.speak(channel, "Dwayne Rock Jhonson", ROCK_PFP, "HELL NAH BROTHER.")
                await self.speak(channel, "Dwayne Rock Jhonson", ROCK_PFP, "WE NEED PROTIEN FOR THE GAINS.")
                await self.speak(channel, "Dwayne Rock Jhonson", ROCK_PFP, f"{msg.author.mention} ur order is now **PROTIEN**.")
            else:
                answers[msg.author.id] = "protein"
                await self.persona_reply(msg, "okey")

            await asyncio.sleep(0.2)

            if len(answers) >= len(allowed_ids):
                return answers

            for user in users:
                if user.id not in answers and user.id not in missing_pinged:
                    missing_pinged.add(user.id)
                    await self.speak(channel, "le weightress", WAITRESS_PFP, f"what abt {user.mention}")

        return answers

    async def wait_special_payment_phrase(self, channel, user):
        await self.speak(
            channel,
            "le weightress",
            WAITRESS_PFP,
            f"{user.mention} uhhh...\nthe machine said **nuh uh**.\nr we ready to wash plates?"
        )

        def check(msg):
            return (
                msg.channel.id == channel.id
                and msg.author.id == user.id
                and not msg.author.bot
                and "face card" in msg.content.lower()
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
        allowed_users = [requester, partner]

        self.active_users.add(requester.id)
        self.active_users.add(partner.id)

        try:
            accept_view = DateButtonView({partner.id}, timeout=120)

            await self.speak(
                ctx.channel,
                "French guy",
                FRENCH_GUY_PFP,
                f"{partner.mention} bonjor baguette.\n{requester.mention} has requested one **fancy restront date**.\naccept = romance lore\nreject = emotional tax fraud"
            )

            await self.button_msg(ctx.channel, "date request buttons:", accept_view)

            try:
                await asyncio.wait_for(accept_view.done.wait(), timeout=120)
            except asyncio.TimeoutError:
                return await self.speak(ctx.channel, "French guy", FRENCH_GUY_PFP, "no answer. date evaporated.")

            await accept_view.disable_buttons()

            if accept_view.answers.get(partner.id) != "accept":
                return await self.speak(ctx.channel, "French guy", FRENCH_GUY_PFP, "rejected. bro became soup.")

            restaurant = await self.make_private_channel(ctx.guild, "le-restront", requester, partner, ctx.channel.category)

            await self.speak(ctx.channel, "French guy", FRENCH_GUY_PFP, f"{requester.mention} {partner.mention}\nle restront has spawned: {restaurant.mention}\nmove ur pixels.")

            await self.speak(
                restaurant,
                "French guy",
                FRENCH_GUY_PFP,
                "welcum to **le restront**.\ntonight we serve romance, protien, and silly little money problems.",
                image=RESTAURANT_IMG
            )

            await self.wait_until_both_talk_silent(restaurant, requester, partner)

            no_count = 0

            while True:
                await self.speak(
                    restaurant,
                    "le weightress",
                    WAITRESS_PFP,
                    f"i have picked the best seat for you guys i totally wont be watching you from inside the walls...\nseat ok or u wanna inspect furniture like ikea employee?\nType `yes` or `no`\nno counter: `{no_count}/5`",
                    image=TABLE_IMG
                )

                seat_answers = await self.wait_text_choices(
                    restaurant,
                    allowed_users,
                    {
                        "yes": ("yes", "yes"),
                        "y": ("yes", "yes"),
                        "no": ("no", "no"),
                        "n": ("no", "no")
                    },
                    "le weightress",
                    WAITRESS_PFP,
                    mode="both",
                    timeout=300,
                    ack=True
                )

                if len(seat_answers) < 2:
                    return await self.speak(restaurant, "le weightress", WAITRESS_PFP, "too slow. chair got bored. date cancelled.")

                if all(v == "yes" for v in seat_answers.values()):
                    break

                no_count += list(seat_answers.values()).count("no")

                if no_count >= 5:
                    return await self.speak(restaurant, "le weightress", WAITRESS_PFP, "5 NO'S???\noutside. no food. chair wins.")

                await self.speak(restaurant, "le weightress", WAITRESS_PFP, f"ok picky furniture inspector.\nagain.\nno counter: `{no_count}/5`")

            await self.speak(restaurant, "le weightress", WAITRESS_PFP, "finally. sit. chair has accepted u.")

            await self.speak(
                restaurant,
                "le weightress",
                WAITRESS_PFP,
                "heres the menu we have a loto options you can see .\nwe have **protien** and **FAT**.\nchef made 2 items then got tired.\nType `protien` or `fat`",
                image=MENU_IMG
            )

            menu_answers = await self.wait_menu_choices(restaurant, allowed_users, timeout=300)

            if len(menu_answers) < 2:
                return await self.speak(restaurant, "le weightress", WAITRESS_PFP, "menu timeout. chef left. tragic.")

            await self.speak(
                restaurant,
                "le weightress",
                WAITRESS_PFP,
                "order locked: **protien**.\nfood takes **1 minute** because the egg is doing character development.\nyap while kitchen does kitchen things."
            )

            await asyncio.sleep(60)

            await self.speak(
                restaurant,
                "le weightress",
                WAITRESS_PFP,
                "FOOD ARRIVD.\nthis plate has protien and uhm protien .\nType `done` when u finish eating",
                image=PROTEIN_IMG
            )

            eat_answers = await self.wait_text_choices(
                restaurant,
                allowed_users,
                {
                    "done": ("done", "done"),
                    "ate": ("done", "done"),
                    "finished": ("done", "done")
                },
                "le weightress",
                WAITRESS_PFP,
                mode="both",
                timeout=600,
                ack=False
            )

            if len(eat_answers) < 2:
                return await self.speak(restaurant, "le weightress", WAITRESS_PFP, "food got cold. date died of slow typing.")

            await self.speak(
                restaurant,
                "le weightress",
                WAITRESS_PFP,
                "time for desert.\nice creem arrived with eyeballs. very fancy.\nType `done` when finished.",
                image=ICECREAM_IMG
            )

            ice_answers = await self.wait_text_choices(
                restaurant,
                allowed_users,
                {
                    "done": ("done", "done"),
                    "finished": ("done", "done")
                },
                "le weightress",
                WAITRESS_PFP,
                mode="both",
                timeout=600,
                ack=False
            )

            if len(ice_answers) < 2:
                return await self.speak(restaurant, "le weightress", WAITRESS_PFP, "ice creem melted. so did the relationship.")

            await self.speak(
                restaurant,
                "le weightress",
                WAITRESS_PFP,
                "BILL TIME.\nthis paper has too many zeroes.\nwho pay.\nType `me` or `she`.\nfirst answer decides.",
                image=BILL_IMG
            )

            pay_answers = await self.wait_text_choices(
                restaurant,
                allowed_users,
                {
                    "me": ("me", "me"),
                    "i pay": ("me", "me"),
                    "she": ("she", "she"),
                    "her": ("she", "she")
                },
                "le weightress",
                WAITRESS_PFP,
                mode="first",
                timeout=300,
                ack=False
            )

            if not pay_answers:
                return await self.speak(restaurant, "le weightress", WAITRESS_PFP, "nobody paid. police arc unlocked.")

            if list(pay_answers.values())[0] == "she":
                await self.speak(restaurant, "Dwayne Rock Jhonson", ROCK_PFP, f"*BONK* {partner.mention}\nprincesses do not pay.\nwallet goes back in pocket.")

            await self.speak(restaurant, "le weightress", WAITRESS_PFP, f"{requester.mention} card pls.\nbe brave. we gonna get through ts")

            card_msg = await self.wait_for_phrase(restaurant, requester, ["card"], timeout=300, ack=False)

            if card_msg is None:
                return await self.speak(restaurant, "le weightress", WAITRESS_PFP, "no card. no money. no oxygen.")

            await asyncio.sleep(2)

            await self.speak(
                restaurant,
                "le weightress",
                WAITRESS_PFP,
                "DECLINED???\nmy brother in baguette... the machine just giggled.",
                image=DECLINED_IMG
            )

            await self.wait_special_payment_phrase(restaurant, requester)

            await self.speak(restaurant, "le weightress", WAITRESS_PFP, "wait...\nscanning face card..\ncomputer is blushing hold on.")

            await asyncio.sleep(3)

            await self.speak(restaurant, "le weightress", WAITRESS_PFP, "APPROVED.\nseggsy bf you got there mam", image=FACE_CARD_IMG)

            outside = await self.make_private_channel(ctx.guild, "le-outside", requester, partner, ctx.channel.category)

            await self.speak(restaurant, "French guy", FRENCH_GUY_PFP, f"hi.\ngo outside before weightress charges oxygen: {outside.mention}")

            await self.speak(outside, "French guy", FRENCH_GUY_PFP, "a taxi will be here soon.\ni touch kids ngl", image=OUTSIDE_IMG)

            await self.wait_until_both_talk_silent(outside, requester, partner)

            await self.speak(
                outside,
                "le taxi driver",
                TAXI_PFP,
                "hi im taxi driver.\nwhere we going.\nType `aifil tawar` or `house`.\nfirst answer decides because democracy got tired.",
                image=TAXI_IMG
            )

            taxi_answers = await self.wait_text_choices(
                outside,
                allowed_users,
                {
                    "aifil tawar": ("tower", "aifil tawar"),
                    "eiffel tower": ("tower", "aifil tawar"),
                    "tower": ("tower", "aifil tawar"),
                    "house": ("house", "house"),
                    "home": ("house", "house")
                },
                "le taxi driver",
                TAXI_PFP,
                mode="first",
                timeout=300,
                ack=False
            )

            if not taxi_answers:
                return await self.speak(outside, "le taxi driver", TAXI_PFP, "no destination. taxi exploded emotionally.")

            if list(taxi_answers.values())[0] == "house":
                await self.speak(outside, "Dwayne Rock Jhonson", ROCK_PFP, "HOUSE?\nHELL NAH BROTHER.\nthis is a date not bedtime.\ntaxi go to aifil tawar.")

            await self.speak(outside, "le taxi driver", TAXI_PFP, "destination: **aifil tawar**.\ndrive time: **30 seconds**.\npls dong fuhh in my taxi")

            await asyncio.sleep(30)

            tower = await self.make_private_channel(ctx.guild, "aifal-tower", requester, partner, ctx.channel.category)

            await self.speak(outside, "le taxi driver", TAXI_PFP, f"we here.\nget out my car and go be romantic over there: {tower.mention}")

            await self.speak(tower, "le taxi driver", TAXI_PFP, "welcome to **aifal tawar**.\nu got **5 minutes**.\nesplore the area and try not to die", image=EIFEL_IMG)

            await asyncio.sleep(300)

            await self.speak(tower, "French guy", FRENCH_GUY_PFP, "final boss choice.\nchoose ending.\nType `kiss` or `no kiss`.\nno kiss ending exists but it is suspicious.")

            end_answers = await self.wait_text_choices(
                tower,
                allowed_users,
                {
                    "kiss": ("kiss", "kiss"),
                    "no kiss": ("no_kiss", "no kiss"),
                    "no": ("no_kiss", "no kiss")
                },
                "French guy",
                FRENCH_GUY_PFP,
                mode="both",
                timeout=300,
                ack=False
            )

            if len(end_answers) < 2:
                return await self.speak(tower, "French guy", FRENCH_GUY_PFP, "ending timeout. romance buffer crashed.")

            if "no_kiss" in end_answers.values():
                await self.speak(tower, "Dwayne Rock Jhonson", ROCK_PFP, "NO KISS?\nTHE FBI IS DISAPPOINTED .\nromance ending has been force updated.")

            await self.speak(tower, "French guy", FRENCH_GUY_PFP, f"{requester.mention} and {partner.mention} ended le date with kiss.\nABSOLOUTE CINEMA. protien. fancy payment aura. peak fiction.")

        finally:
            self.active_users.discard(requester.id)
            self.active_users.discard(partner.id)


async def setup(bot):
    await bot.add_cog(DateCog(bot))
