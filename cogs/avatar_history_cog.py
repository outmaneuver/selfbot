import discord
from discord.ext import commands

class AvatarHistoryCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='avhistory')
    async def avatar_history(self, ctx, user: discord.User):
        # Fetch avatar history from the database
        avatar_history = self.fetch_avatar_history(user.id)
        if avatar_history:
            await ctx.send(f"Avatar history for {user.name}: {', '.join(avatar_history)}")
        else:
            await ctx.send(f"No avatar history found for {user.name}")

    def fetch_avatar_history(self, user_id):
        # Implement the logic to fetch avatar history from the database
        # This is a placeholder implementation
        return ["Avatar1", "Avatar2", "Avatar3"]

def setup(bot):
    bot.add_cog(AvatarHistoryCog(bot))
