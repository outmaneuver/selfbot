import pytest
from discord.ext import commands
from selfbot import SelfBot

@pytest.fixture
def bot():
    bot = SelfBot()
    return bot

@pytest.mark.asyncio
async def test_on_ready(bot):
    await bot.on_ready()
    assert bot.user is not None

@pytest.mark.asyncio
async def test_on_member_update(bot):
    member_before = commands.Member(data={"id": 1, "name": "OldName", "avatar": "old_avatar", "display_name": "OldDisplayName"}, guild=None, state=None)
    member_after = commands.Member(data={"id": 1, "name": "NewName", "avatar": "new_avatar", "display_name": "NewDisplayName"}, guild=None, state=None)
    await bot.on_member_update(member_before, member_after)
    # Add assertions to verify the behavior

@pytest.mark.asyncio
async def test_on_command_error(bot):
    ctx = commands.Context(prefix="!", message=None, bot=bot)
    error = commands.CommandNotFound("Test command not found")
    await bot.on_command_error(ctx, error)
    # Add assertions to verify the behavior
