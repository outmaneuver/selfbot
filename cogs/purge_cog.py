import discord
from discord.ext import commands
from utils.rate_limiter import RateLimiter
import asyncio

class PurgeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.rate_limiter = RateLimiter()

    @commands.command(name='purge')
    async def purge(self, ctx, channel_id: int = None, delay: float = 1.0):
        if channel_id is None:
            channel = ctx.channel
        else:
            channel = self.bot.get_channel(channel_id)

        if channel is None:
            await ctx.send("Invalid channel ID.")
            return

        def is_selfbot_message(message):
            return message.author == self.bot.user

        async for message in channel.history(limit=None):
            if is_selfbot_message(message):
                await self.rate_limiter.wait()
                await message.delete()
                await asyncio.sleep(delay)

def setup(bot):
    bot.add_cog(PurgeCog(bot))
