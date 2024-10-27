import discord
from discord.ext import commands

def error_handler(func):
    async def wrapper(*args, **kwargs):
        ctx = args[0]
        try:
            await func(*args, **kwargs)
        except commands.CommandNotFound:
            await ctx.send("Sorry, I didn't understand that command.")
        except commands.MissingRequiredArgument:
            await ctx.send("It looks like you're missing a required argument.")
        except commands.BadArgument:
            await ctx.send("There was an issue with one of the arguments you provided.")
        except commands.CommandInvokeError:
            await ctx.send("There was an error while executing the command.")
        except Exception as e:
            await ctx.send(f"An unexpected error occurred: {e}")
    return wrapper
