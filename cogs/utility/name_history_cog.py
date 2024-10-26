import discord
from discord.ext import commands
from utils.database import fetch_name_history
from utils.error_handler import error_handler
from utils.permissions import has_permissions_to_send_messages

class NameHistoryCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.local_cache = bot.local_cache

    @commands.command(name='namehistory')
    @error_handler
    @has_permissions_to_send_messages()
    async def name_history(self, ctx, user: discord.User = None):
        if user is None:
            user = ctx.author
        name_history = self.fetch_name_history(user.id)
        if name_history:
            await ctx.send(f"Here's the name history for {user.name}: {', '.join(name_history)}")
        else:
            await ctx.send(f"Sorry, I couldn't find any name history for {user.name}.")

    def fetch_name_history(self, user_id):
        return fetch_name_history(user_id, self.local_cache)

def setup(bot):
    bot.add_cog(NameHistoryCog(bot))
