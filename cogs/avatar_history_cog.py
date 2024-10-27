import discord
from discord.ext import commands
from utils.database import fetch_avatar_history
from utils.error_handler import error_handler
from utils.permissions import has_permissions_to_send_images

class AvatarHistoryCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.local_cache = bot.local_cache

    @commands.command(name='avhistory')
    @error_handler
    @has_permissions_to_send_images()
    async def avatar_history(self, ctx, user: discord.User = None):
        if user is None:
            user = ctx.author
        avatar_history = self.fetch_avatar_history(user.id)
        if avatar_history:
            await ctx.send(f"Here's the avatar history for {user.name}: {', '.join(avatar_history)}")
        else:
            await ctx.send(f"Sorry, I couldn't find any avatar history for {user.name}.")

    def fetch_avatar_history(self, user_id):
        return fetch_avatar_history(user_id, self.local_cache)

def setup(bot):
    bot.add_cog(AvatarHistoryCog(bot))
