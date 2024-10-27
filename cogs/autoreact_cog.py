import discord
from discord.ext import commands
from utils.rate_limiter import RateLimiter
import asyncio

class AutoReactCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.user_reactions = {}
        self.rate_limiter = RateLimiter()

    @commands.command(name='react')
    async def react(self, ctx, user_ids: commands.Greedy[int], *emojis):
        if not user_ids:
            user_ids = [ctx.author.id]

        for user_id in user_ids:
            if user_id not in self.user_reactions:
                self.user_reactions[user_id] = set()
            self.user_reactions[user_id].update(emojis)

        await ctx.send(f"Auto-react enabled for users: {', '.join(map(str, user_ids))} with emojis: {', '.join(emojis)}")

    @commands.command(name='reactstop')
    async def react_stop(self, ctx, user_id: int):
        if user_id in self.user_reactions:
            del self.user_reactions[user_id]
            await ctx.send(f"Auto-react disabled for user: {user_id}")
        else:
            await ctx.send(f"No auto-react found for user: {user_id}")

    @commands.command(name='reactlist')
    async def react_list(self, ctx):
        if self.user_reactions:
            response = "Auto-react enabled for the following users:\n"
            for user_id, emojis in self.user_reactions.items():
                response += f"User ID: {user_id}, Emojis: {', '.join(emojis)}\n"
            await ctx.send(f"```{response}```")
        else:
            await ctx.send("No users have auto-react enabled.")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id in self.user_reactions:
            for emoji in self.user_reactions[message.author.id]:
                await self.rate_limiter.wait()
                await message.add_reaction(emoji)

def setup(bot):
    bot.add_cog(AutoReactCog(bot))
