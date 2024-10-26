import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import importlib
from utils.database import determine_database
from utils.user_info import store_user_info

load_dotenv()

class SelfBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=os.getenv("PREFIX"))
        self.local_db_conn, self.mongo_client, self.mysql_conn, self.redis_client = determine_database()
        self.load_cogs()

    def load_cogs(self):
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                cog_name = filename[:-3]
                cog_module = importlib.import_module(f'cogs.{cog_name}')
                self.add_cog(cog_module.setup(self))

    async def on_ready(self):
        print(f'Logged in as {self.user}')

    async def on_member_update(self, before, after):
        if before.name != after.name or before.avatar != after.avatar or before.display_name != after.display_name:
            store_user_info(after, self.local_db_conn, self.mongo_client, self.mysql_conn, self.redis_client)

    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send("Sorry, I didn't understand that command.")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("It looks like you're missing a required argument.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("There was an issue with one of the arguments you provided.")
        elif isinstance(error, commands.CommandInvokeError):
            await ctx.send("There was an error while executing the command.")
        else:
            await ctx.send("An unexpected error occurred. Please try again later.")

if __name__ == "__main__":
    bot = SelfBot()
    bot.run(os.getenv("TOKEN"))
