import discord
from discord.ext import commands

def has_permissions_to_send_messages():
    async def predicate(ctx):
        if not ctx.channel.permissions_for(ctx.author).send_messages:
            await ctx.author.send("You do not have permission to send messages in this channel.")
            return False
        return True
    return commands.check(predicate)

def has_permissions_to_send_images():
    async def predicate(ctx):
        if not ctx.channel.permissions_for(ctx.author).attach_files:
            await ctx.author.send("You do not have permission to send images in this channel.")
            return False
        return True
    return commands.check(predicate)

def has_permissions_to_use_external_emojis():
    async def predicate(ctx):
        if not ctx.channel.permissions_for(ctx.author).use_external_emojis:
            await ctx.author.send("You do not have permission to use external emojis in this channel.")
            return False
        return True
    return commands.check(predicate)
