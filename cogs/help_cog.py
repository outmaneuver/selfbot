import discord
from discord.ext import commands
from utils.error_handler import error_handler

class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='help')
    @error_handler
    async def help_command(self, ctx, *input):
        prefix = self.bot.command_prefix
        version = "1.0"
        author = os.getenv("AUTHOR")

        if not input:
            # No input, show all categories and commands
            embed = discord.Embed(title="Help", description=f"Use `{prefix}help <category>` to get more information on a category.", color=discord.Color.blue())
            cogs_desc = ''
            for cog in self.bot.cogs:
                cogs_desc += f'`{cog}` {self.bot.cogs[cog].__doc__}\n'
            embed.add_field(name='Categories', value=cogs_desc, inline=False)
            await ctx.send(embed=embed)
        elif len(input) == 1:
            # One input, show commands in the category
            cog = self.bot.get_cog(input[0])
            if cog:
                embed = discord.Embed(title=f"{input[0]} - Commands", description=cog.__doc__, color=discord.Color.blue())
                for command in cog.get_commands():
                    embed.add_field(name=f"`{prefix}{command.name}`", value=command.help, inline=False)
                await ctx.send(embed=embed)
            else:
                await ctx.send(f"Category `{input[0]}` not found.")
        else:
            await ctx.send("Invalid input. Use `!help` to see all categories.")

def setup(bot):
    bot.add_cog(HelpCog(bot))
