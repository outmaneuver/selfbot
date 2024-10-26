import discord
from discord.ext import commands

class CurrentAvatarCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='currentav')
    async def current_avatar(self, ctx, user: discord.User):
        await ctx.send(f"Hey there! Here's the current avatar for {user.name}: {user.avatar_url}")

def setup(bot):
    bot.add_cog(CurrentAvatarCog(bot))
