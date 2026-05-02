from discord.ext import commands
import discord
import random
import asyncio

KONI_AVATAR = "https://cdn.discordapp.com/attachments/1500100689924194326/1500100763815252079/IMG-20260421-WA0051-1.jpg"
LEBRON_AVATAR = "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e8/LeBron_James_at_the_2022_NBA_All-Star_Game.jpg/320px-LeBron_James_at_the_2022_NBA_All-Star_Game.jpg"
DUMBBOT_AVATAR = "https://cdn-icons-png.flaticon.com/512/4712/4712035.png"

BOT_PROFILES = {
    "Koni": KONI_AVATAR,
    "Lebron": LEBRON_AVATAR,
    "DumbBot": DUMBBOT_AVATAR
}

ARGUMENTS = [
    [
        ("DumbBot", "i think i’m becoming wise"),
        ("Lebron", "you said fish is math"),
        ("Koni", "meow wise fish"),
        ("DumbBot", "exactly"),
        ("Lebron", "pain")
    ],
    [
        ("Koni", "meow shut up"),
        ("Lebron", "nah YOU shut up 💀"),
        ("DumbBot", "bro why are we fighting"),
        ("Koni", "mrrp because you exist"),
        ("Lebron", "absolute cinema")
    ],
    [
        ("Lebron", "this server is cooked"),
        ("Koni", "meow fr"),
        ("DumbBot", "i cooked it"),
        ("Lebron", "never cook again"),
        ("Koni", "mreow 💀")
    ]
]

class Argue(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cooldown = False
        self.webhooks = {}

    async def get_or_create_webhook(self, channel, name):
        cache_key = f"{channel.id}-{name}"

        if cache_key in self.webhooks:
            return self.webhooks[cache_key]

        existing_webhooks = await channel.webhooks()

        for webhook in existing_webhooks:
            if webhook.name == name:
                self.webhooks[cache_key] = webhook
                return webhook

        new_webhook = await channel.create_webhook(name=name)
        self.webhooks[cache_key] = new_webhook
        return new_webhook

    async def send_webhook_message(self, channel, name, text):
        avatar_url = BOT_PROFILES.get(name)

        webhook = await self.get_or_create_webhook(channel, name)

        await webhook.send(
            content=text,
            username=name,
            avatar_url=avatar_url,
            allowed_mentions=discord.AllowedMentions.none(),
            wait=True
        )

    @commands.command(name="argue")
    async def argue(self, ctx):
        if self.cooldown:
            return await ctx.send("they already arguing bro give them a sec 💀")

        self.cooldown = True

        try:
            await ctx.send("argument started 🍿")

            argument = random.choice(ARGUMENTS)

            for name, text in argument:
                await asyncio.sleep(random.randint(2, 4))
                await self.send_webhook_message(ctx.channel, name, text)

            await asyncio.sleep(2)
            await ctx.send("argument ended. nobody won. everyone got dumber 😭")

        except discord.Forbidden:
            await ctx.send("I need **Manage Webhooks** permission 💀")

        except Exception as e:
            await ctx.send(f"Argue error: `{e}`")

        finally:
            await asyncio.sleep(20)
            self.cooldown = False

async def setup(bot):
    await bot.add_cog(Argue(bot))
