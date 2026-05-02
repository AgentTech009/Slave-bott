from discord.ext import commands
import discord
import random
import asyncio

KONI_AVATAR = "https://cdn.discordapp.com/attachments/1500100689924194326/1500100763815252079/IMG-20260421-WA0051-1.jpg"

LEBRON_AVATAR = "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e8/LeBron_James_at_the_2022_NBA_All-Star_Game.jpg/320px-LeBron_James_at_the_2022_NBA_All-Star_Game.jpg"

NORMAL_THREATS = [
    [
        "🚨 HYDRATION ALERT 🚨",
        "{user} you have been selected",
        "drink water NOW",
        "this is not a suggestion",
        "i am watching you"
    ],
    [
        "{user} your organs filed a complaint",
        "reason: neglect",
        "requested item: water",
        "approve immediately"
    ],
    [
        "{user} hydration police here 🚔",
        "step away from dehydration",
        "drink with your hands visible"
    ],
    [
        "{user} your cells are screaming",
        "they want WATER"
    ],
    [
        "{user} your vibe is dry",
        "fix it biologically"
    ]
]

AGGRESSIVE_NO = [
    "{user} DID YOU JUST SAY NO?",
    "wrong answer 💀",
    "hydration refusal detected",
    "activating annoying mode",
    "{user} drink water.",
    "not later.",
    "NOW.",
    "your kidneys are filing paperwork",
    "your aura is evaporating",
    "you are not a raisin",
    "do NOT become a raisin",
    "{user} apologize to your organs"
]

KONI_PHASE = [
    "meow.",
    "{user} drink water",
    "mrrp dehydration detected",
    "nya this is unacceptable",
    "meow meow threat level silly",
    "prrr drink or perish socially"
]

LEBRON_PHASE = [
    "hydration legacy on the line",
    "{user} has no water aura",
    "fourth quarter hydration check",
    "drink water or get benched",
    "this is not goat behavior",
    "legacy points deducted"
]

FINAL_PHASE = [
    "⚠️ FINAL HYDRATION ESCALATION ⚠️",
    "{user} has refused basic liquid survival",
    "the council is disappointed",
    "Koni is disappointed",
    "Lebron is disappointed",
    "{user} drink water and type `done`",
    "or forever be known as Dry Mode"
]

class Drink(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.active = set()

    async def get_webhook(self, channel, name):
        webhooks = await channel.webhooks()

        for webhook in webhooks:
            if webhook.name == name:
                return webhook

        return await channel.create_webhook(name=name)

    async def webhook_send(self, channel, name, avatar, text):
        webhook = await self.get_webhook(channel, name)
        await webhook.send(
            text,
            username=name,
            avatar_url=avatar
        )

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        content = message.content.lower()

        if "make" not in content or "drink water" not in content:
            return

        if not message.mentions:
            return

        target = message.mentions[0]

        if target.id in self.active:
            return await message.channel.send(
                f"{target.mention} is already under hydration investigation 💀"
            )

        self.active.add(target.id)

        try:
            sequence = random.choice(NORMAL_THREATS)

            for msg in sequence:
                await asyncio.sleep(random.randint(1, 2))
                await message.channel.send(msg.format(user=target.mention))

            await asyncio.sleep(1)
            await message.channel.send(
                f"{target.mention} type `done` when you drink water. Type `no` if you want the boss fight 💧"
            )

            def check(m):
                return (
                    m.author.id == target.id
                    and m.channel.id == message.channel.id
                    and m.content.lower() in ["done", "no"]
                )

            try:
                reply = await self.bot.wait_for("message", timeout=60, check=check)

                if reply.content.lower() == "done":
                    return await message.channel.send(
                        f"{target.mention} hydration successful. disaster avoided ✅"
                    )

                for msg in AGGRESSIVE_NO:
                    await asyncio.sleep(1)
                    await message.channel.send(msg.format(user=target.mention))

                await asyncio.sleep(2)
                await message.channel.send("summoning witnesses...")

                for msg in random.sample(KONI_PHASE, 4):
                    await asyncio.sleep(1)
                    await self.webhook_send(
                        message.channel,
                        "Koni",
                        KONI_AVATAR,
                        msg.format(user=target.mention)
                    )

                for msg in random.sample(LEBRON_PHASE, 4):
                    await asyncio.sleep(1)
                    await self.webhook_send(
                        message.channel,
                        "Lebron",
                        LEBRON_AVATAR,
                        msg.format(user=target.mention)
                    )

                for msg in FINAL_PHASE:
                    await asyncio.sleep(1)
                    await message.channel.send(msg.format(user=target.mention))

                try:
                    final = await self.bot.wait_for("message", timeout=45, check=check)

                    if final.content.lower() == "done":
                        await message.channel.send(
                            f"{target.mention} finally hydrated. took you long enough 💀"
                        )
                    else:
                        await message.channel.send(
                            f"{target.mention} has chosen Dry Mode. tragic ending 🏜️"
                        )

                except asyncio.TimeoutError:
                    await message.channel.send(
                        f"{target.mention} ignored the council. Dry Mode confirmed 🏜️"
                    )

            except asyncio.TimeoutError:
                await message.channel.send(
                    f"{target.mention} ignored hydration court. guilty by silence 💀"
                )

        finally:
            self.active.discard(target.id)

async def setup(bot):
    await bot.add_cog(Drink(bot))
