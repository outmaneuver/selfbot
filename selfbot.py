import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from utils.command_handler import CommandHandler
from utils.error_handler import error_handler

load_dotenv()

class SelfBot(CommandHandler):
    def __init__(self):
        super().__init__()

    @error_handler
    async def on_command_error(self, ctx, error):
        await super().on_command_error(ctx, error)

    async def on_guild_join(self, guild):
        for member in guild.members:
            self.database_manager.store_user_info(member)

    async def on_member_update(self, before, after):
        if before.name != after.name or before.avatar != after.avatar or before.display_name != after.display_name:
            self.database_manager.store_user_info(after)

    async def on_ready(self):
        print(f'Logged in as {self.user}')
        await self.load_custom_activity_settings()
        for guild in self.guilds:
            for member in guild.members:
                self.database_manager.store_user_info(member)

if __name__ == "__main__":
    bot = SelfBot()
    bot.run(os.getenv("TOKEN"))
