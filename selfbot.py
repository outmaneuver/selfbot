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

if __name__ == "__main__":
    bot = SelfBot()
    bot.run(os.getenv("TOKEN"))
