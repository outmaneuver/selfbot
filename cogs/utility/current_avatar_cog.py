import discord
from discord.ext import commands
from utils.permissions import has_permissions_to_send_images

class CurrentAvatarCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='currentav')
    @has_permissions_to_send_images()
    async def current_avatar(self, ctx, user: discord.User = None):
        if user is None:
            user = ctx.author
        await ctx.send(f"Hey there! Here's the current avatar for {user.name}: {user.avatar_url}")

def setup(bot):
    bot.add_cog(CurrentAvatarCog(bot))
