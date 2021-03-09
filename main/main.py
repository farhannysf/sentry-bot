import sys
import asyncio
import discord
import webserver
import logging
import sentry_sdk
import utility
from sentry_commands.channel_authorization import (
    channel_authorizationLogic as authorizeChannel,
)
from sentry_commands.project_registration import (
    project_registrationLogic as register_project,
)

from sentry_commands.sentry_help import commands_list

from discord.ext import commands
from google.cloud import firestore

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

db = firestore.Client()
keys = utility.retrieveDB_data(db, option="keys", title="api")

sentryURL = keys["sentryURL"]
discordKey = keys["discordKey"]
devState = False

if len(sys.argv) > 1:
    if sys.argv[1] == "dev":
        sentryURL = keys["sentryURL_dev"]
        discordKey = keys["discordKey_dev"]
        devState = True

sentry_sdk.init(
    sentryURL,
    traces_sample_rate=1.0,
)


client = commands.Bot(command_prefix="!sentry ")


@client.event
async def on_connect():
    client.loop.create_task(
        webserver.sanic_webserver(devState, client, firestore, db, discord.Embed)
    )


@client.event
async def on_ready():
    logger.info(f"sentry.bot running as {client.user.name} ({client.user.id}).\n------")
    game = discord.Game("!sentry -h")
    await client.change_presence(status=discord.Status.online, activity=game)

@client.command(pass_context=True)
async def h(ctx):
    await commands_list(ctx, discord.Embed, db, firestore)

@client.command(pass_context=True)
@commands.has_permissions(manage_messages=True)
async def channel(ctx, operation: str = None, channel: str = None):
    await authorizeChannel(ctx, discord.Embed, firestore, db, operation, channel)


@channel.error
async def channel_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(
            "You have no sufficient permission in this guild to use this command. Please contact guild administrator."
        )

    else:
        logger.error({"error": {"command": "channel", "message": error}})


@client.command(pass_context=True)
async def project(ctx, operation: str = None, project_name: str = None):
    await register_project(ctx, discord.Embed, firestore, db, operation, project_name)


@project.error
async def project_error(ctx, error):
    if isinstance(error, commands.UnexpectedQuoteError):
        await ctx.send(f"Unexpected quote mark in non-quoted string")

    else:
        logger.error({"error": {"command": "project", "message": error}})


if __name__ == "__main__":
    client.run(discordKey)
    logger.error("Client loop closed")