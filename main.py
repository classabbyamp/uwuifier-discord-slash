"""
uwuifier-discord-slash
---
Copyright 2021 classabbyamp, 0x5c
Released under the terms of the BSD 3-Clause license.
"""


from typing import Union

import uwuify
import discord
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext

from data import secrets


bot = commands.Bot(command_prefix="uwuifier ")
slash = SlashCommand(bot, sync_commands=True)
exit_code = 1


@slash.slash(name="uwuify", description="Genewates uwu-text fow youw message")
async def _uwu(ctx: SlashContext, message: str):
    await ctx.send(uwuify.uwu(message, flags=uwuify.SMILEY | uwuify.YU))


async def add_react(msg: discord.Message, react: Union[discord.Emoji, discord.Reaction, discord.PartialEmoji, str]):
    try:
        await msg.add_reaction(react)
    except discord.Forbidden:
        idpath = (f"{msg.guild.id}/" if msg.guild else "") + str(msg.channel.id)
        print(f"[!!] Missing permissions to add reaction in '{idpath}'!")


@bot.command(name="restart", aliases=["rs"])
@commands.is_owner()
async def _restart_bot(ctx: commands.Context):
    """Restarts the bot."""
    global exit_code
    await add_react(ctx.message, "✅")
    print(f"[**] Restarting! Requested by {ctx.author}.")
    exit_code = 42  # Signals to the wrapper script that the bot needs to be restarted.
    await bot.logout()


@bot.command(name="shutdown", aliases=["shut"])
@commands.is_owner()
async def _shutdown_bot(ctx: commands.Context):
    """Shuts down the bot."""
    global exit_code
    await add_react(ctx.message, "✅")
    print(f"[**] Shutting down! Requested by {ctx.author}.")
    exit_code = 0  # Signals to the wrapper script that the bot should not be restarted.
    await bot.logout()


@bot.event
async def on_ready():
    print(f"Logged in as: {bot.user} - {bot.user.id}")
    print("------")


try:
    bot.run(secrets.token)

except discord.LoginFailure as ex:
    # Miscellaneous authentications errors: borked token and co
    raise SystemExit("Error: Failed to authenticate: {}".format(ex))

except discord.ConnectionClosed as ex:
    # When the connection to the gateway (websocket) is closed
    raise SystemExit("Error: Discord gateway connection closed: [Code {}] {}".format(ex.code, ex.reason))

except ConnectionResetError as ex:
    # More generic connection reset error
    raise SystemExit("ConnectionResetError: {}".format(ex))


# --- Exit ---
# Codes for the wrapper shell script:
# 0 - Clean exit, don't restart
# 1 - Error exit, [restarting is up to the shell script]
# 42 - Clean exit, do restart

raise SystemExit(exit_code)
