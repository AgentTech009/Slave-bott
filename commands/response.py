from discord.ext import commands
import json
import os

DATA_FILE = "responses.json"

def load_responses():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as f:
            json.dump({}, f)

    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_responses(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

class RespondTo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.responses = load_responses()

    @commands.command(name="respondto")
    async def respondto(self, ctx, trigger, *, response):
        trigger = trigger.lower()

        self.responses[trigger] = response
        save_responses(self.responses)

        await ctx.send(f"Saved response for `{trigger}`")

    @commands.command(name="delresponse")
    async def delresponse(self, ctx, trigger):
        trigger = trigger.lower()

        if trigger not in self.responses:
            return await ctx.send("That trigger does not exist.")

        del self.responses[trigger]
        save_responses(self.responses)

        await ctx.send(f"Deleted response for `{trigger}`")

    @commands.command(name="responses")
    async def responses_list(self, ctx):
        if not self.responses:
            return await ctx.send("No custom responses saved.")

        text = "\n".join([f"`{k}` → {v}" for k, v in self.responses.items()])
        await ctx.send(text[:1900])

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        msg = message.content.lower()

        for trigger, response in self.responses.items():
            if trigger in msg:
                await message.channel.send(response)
                break

async def setup(bot):
    await bot.add_cog(RespondTo(bot))