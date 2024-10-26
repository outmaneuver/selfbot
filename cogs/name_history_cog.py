import discord
from discord.ext import commands

class NameHistoryCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='namehistory')
    async def name_history(self, ctx, user: discord.User):
        # Fetch name history from the database
        name_history = self.fetch_name_history(user.id)
        if name_history:
            await ctx.send(f"Name history for {user.name}: {', '.join(name_history)}")
        else:
            await ctx.send(f"No name history found for {user.name}")

    def fetch_name_history(self, user_id):
        # Implement the logic to fetch name history from the database
        # This is a placeholder implementation
        return ["OldName1", "OldName2", "OldName3"]

def setup(bot):
    bot.add_cog(NameHistoryCog(bot))
