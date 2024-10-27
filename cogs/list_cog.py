import discord
from discord.ext import commands

class ListCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='list')
    async def list_command(self, ctx):
        autoreact_cog = self.bot.get_cog('AutoReactCog')
        if autoreact_cog:
            user_reactions = autoreact_cog.user_reactions
            if user_reactions:
                response = "Auto-react enabled for the following users:\n"
                for user_id, emojis in user_reactions.items():
                    response += f"User ID: {user_id}, Emojis: {', '.join(emojis)}\n"
                await ctx.send(f"```{response}```")
            else:
                await ctx.send("No users have auto-react enabled.")
        else:
            await ctx.send("AutoReactCog is not loaded.")

def setup(bot):
    bot.add_cog(ListCog(bot))
