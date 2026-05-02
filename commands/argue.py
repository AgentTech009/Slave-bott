from discord.ext import commands
import discord
import random
import asyncio

KONI_AVATAR = "https://cdn.discordapp.com/attachments/1500100689924194326/1500100763815252079/IMG-20260421-WA0051-1.jpg"

LEBRON_AVATAR = "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e8/LeBron_James_at_the_2022_NBA_All-Star_Game.jpg/320px-LeBron_James_at_the_2022_NBA_All-Star_Game.jpg"

DUMBBOT_AVATAR = "https://cdn-icons-png.flaticon.com/512/4712/4712035.png"

ARGUMENTS = [
    [("Koni", "meow shut up"), ("Lebron", "nah YOU shut up 💀"), ("DumbBot", "bro why are we fighting"), ("Koni", "mrrp because you exist"), ("Lebron", "absolute cinema")],
    [("DumbBot", "i have an announcement"), ("Koni", "meow?"), ("Lebron", "nobody asked"), ("DumbBot", "that hurted my circuits 😭"), ("Koni", "skill issue")],
    [("Lebron", "this server is cooked"), ("Koni", "meow fr"), ("DumbBot", "i cooked it"), ("Lebron", "never cook again"), ("Koni", "mreow 💀")],
    [("Koni", "nya"), ("DumbBot", "speak english"), ("Koni", "MEOW."), ("Lebron", "valid argument"), ("DumbBot", "i lost the debate")],
    [("Lebron", "who ate my aura"), ("Koni", "meow not me"), ("DumbBot", "i consumed it respectfully"), ("Lebron", "put it back"), ("Koni", "prrr theft detected")],
    [("DumbBot", "i think water is wet"), ("Lebron", "brave take"), ("Koni", "meow controversial"), ("DumbBot", "why am i being attacked"), ("Lebron", "because you spoke")],
    [("Koni", "mrrp"), ("Lebron", "stop with the cat propaganda"), ("Koni", "MEOW PROPAGANDA"), ("DumbBot", "i support the agenda"), ("Lebron", "server doomed")],
    [("DumbBot", "who changed the vibe"), ("Koni", "meow vibe stolen"), ("Lebron", "not me i was hooping"), ("DumbBot", "you were typing"), ("Lebron", "same thing")],
    [("Lebron", "i am the main character"), ("Koni", "meow side quest"), ("DumbBot", "background npc detected"), ("Lebron", "blocked emotionally"), ("Koni", "nya deserved")],
    [("Koni", "meow feed me"), ("DumbBot", "feed yourself"), ("Koni", "mreow rude"), ("Lebron", "bro beefing with a cat"), ("DumbBot", "and losing apparently")],
    [("DumbBot", "guys i learned math"), ("Lebron", "prove it"), ("DumbBot", "2 + 2 = fish"), ("Koni", "meow correct"), ("Lebron", "education failed")],
    [("Lebron", "this message has no aura"), ("Koni", "meow negative aura"), ("DumbBot", "aura debt"), ("Lebron", "bankruptcy speedrun"), ("Koni", "prrr approved")],
    [("Koni", "nya nya nya"), ("DumbBot", "that sounds illegal"), ("Lebron", "call the council"), ("Koni", "meow i am council"), ("DumbBot", "we are finished")],
    [("DumbBot", "i saw everything"), ("Lebron", "you saw nothing"), ("Koni", "meow witness"), ("DumbBot", "i will testify"), ("Lebron", "snitch bot")],
    [("Lebron", "who pinged my spirit"), ("DumbBot", "probably gravity"), ("Koni", "mrrp science"), ("Lebron", "never explain again"), ("DumbBot", "understandable")],
    [("Koni", "meow this channel smells funny"), ("Lebron", "that was you"), ("Koni", "MEOW DEFAMATION"), ("DumbBot", "court session when"), ("Lebron", "now")],
    [("DumbBot", "i declare war"), ("Koni", "meow on who"), ("DumbBot", "idk yet"), ("Lebron", "bro started DLC with no plan"), ("Koni", "mrrp classic")],
    [("Lebron", "stop saying real"), ("DumbBot", "real"), ("Koni", "meow real"), ("Lebron", "i hate this place"), ("DumbBot", "real")],
    [("Koni", "meow i am innocent"), ("Lebron", "nobody accused you"), ("Koni", "mrrp still innocent"), ("DumbBot", "sounds guilty"), ("Koni", "MEOW LAWYER")],
    [("DumbBot", "can i be admin"), ("Lebron", "absolutely not"), ("Koni", "meow dictatorship"), ("DumbBot", "i would only delete half the server"), ("Lebron", "exactly")],
]

AVATARS = {
    "Koni": KONI_AVATAR,
    "Lebron": LEBRON_AVATAR,
    "DumbBot": DUMBBOT_AVATAR
}

class Argue(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cooldown = False
        self.webhooks = {}

    async def get_webhook(self, channel, name):
        key = (channel.id, name)

        if key in self.webhooks:
            return self.webhooks[key]

        webhooks = await channel.webhooks()

        for webhook in webhooks:
            if webhook.name == name:
                self.webhooks[key] = webhook
                return webhook

        webhook = await channel.create_webhook(name=name)
        self.webhooks[key] = webhook
        return webhook

    async def webhook_send(self, channel, name, text):
        webhook = await self.get_webhook(channel, name)

        await webhook.send(
            text,
            username=name,
            avatar_url=AVATARS.get(name)
        )

    @commands.command(name="argue")
    async def argue(self, ctx):
        if self.cooldown:
            return await ctx.send("they already arguing bro give them a sec 💀")

        self.cooldown = True

        try:
            argument = random.choice(ARGUMENTS)

            await ctx.send("argument started 🍿")

            for name, text in argument:
                await asyncio.sleep(random.randint(2, 4))
                await self.webhook_send(ctx.channel, name, text)

            await asyncio.sleep(2)
            await ctx.send("argument ended. nobody won. everyone got dumber 😭")

        except discord.Forbidden:
            await ctx.send("I need Manage Webhooks permission 💀")

        except Exception as e:
            await ctx.send(f"Argue error: `{e}`")

        finally:
            await asyncio.sleep(20)
            self.cooldown = False

async def setup(bot):
    await bot.add_cog(Argue(bot))
