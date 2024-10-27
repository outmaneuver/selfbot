import discord
from discord.ext import commands

class ReactStopCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='reactstop')
    async def react_stop(self, ctx, user_id: int):
        autoreact_cog = self.bot.get_cog('AutoReactCog')
        if autoreact_cog:
            if user_id in autoreact_cog.user_reactions:
                del autoreact_cog.user_reactions[user_id]
                await ctx.send(f"Auto-react disabled for user: {user_id}")
            else:
                await ctx.send(f"No auto-react found for user: {user_id}")
        else:
            await ctx.send("AutoReactCog is not loaded.")

def setup(bot):
    bot.add_cog(ReactStopCog(bot))
