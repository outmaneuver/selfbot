import discord
from discord.ext import commands
from utils.error_handler import error_handler
import os

class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='help')
    @error_handler
    async def help_command(self, ctx, *input):
        prefix = self.bot.command_prefix
        version = "1.0"
        author = os.getenv("AUTHOR")

        if not ctx.channel.permissions_for(ctx.author).send_messages:
            await ctx.author.send("You do not have permission to send messages in this channel.")
            return

        if not input:
            # No input, show all categories and commands
            help_message = "Help\nUse `{prefix}help <category>` to get more information on a category.\n\nCategories:\n"
            for cog in self.bot.cogs:
                help_message += f'`{cog}` {self.bot.cogs[cog].__doc__}\n'
            await ctx.send(f"```{help_message}```")
        elif len(input) == 1:
            # One input, show commands in the category
            cog = self.bot.get_cog(input[0])
            if cog:
                help_message = f"{input[0]} - Commands\n{cog.__doc__}\n\n"
                for command in cog.get_commands():
                    help_message += f"`{prefix}{command.name}`: {command.help}\n"
                await ctx.send(f"```{help_message}```")
            else:
                await ctx.send(f"Category `{input[0]}` not found.")
        else:
            await ctx.send("Invalid input. Use `!help` to see all categories.")

def setup(bot):
    bot.add_cog(HelpCog(bot))
