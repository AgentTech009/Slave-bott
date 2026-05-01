from discord.ext import commands
import urllib.request
import urllib.error
import json
import os
import asyncio

def get_key():
    return os.getenv("GROQ_API_KEY")

def ask_groq(api_key, question):
    url = "https://api.groq.com/openai/v1/chat/completions"

    data = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {"role": "user", "content": question}
        ]
    }

    body = json.dumps(data).encode("utf-8")

    req = urllib.request.Request(
        url,
        data=body,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
            "User-Agent": "Mozilla/5.0"
        },
        method="POST"
    )

    with urllib.request.urlopen(req, timeout=60) as response:
        result = json.loads(response.read().decode())

    return result["choices"][0]["message"]["content"]

class Ask(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.api_key = get_key()

    @commands.command(name="ask")
    async def ask(self, ctx, *, question):
        if not self.api_key:
            return await ctx.send("Groq API key missing. Add `GROQ_API_KEY` in Railway variables.")

        msg = await ctx.send("Thinking...")

        try:
            answer = await asyncio.to_thread(ask_groq, self.api_key, question)

            if len(answer) > 1900:
                answer = answer[:1900] + "..."

            await msg.edit(content=answer)

        except urllib.error.HTTPError as e:
            error_text = e.read().decode("utf-8")
            await msg.edit(content=f"Groq error:\n```{error_text[:1500]}```")

        except Exception as e:
            await msg.edit(content=f"Error: `{e}`")

async def setup(bot):
    await bot.add_cog(Ask(bot))
