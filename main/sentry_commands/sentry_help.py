from utility import checkChannel
from settings import unauthorized_channelMessage


async def commands_list(ctx, discordEmbed, db, firestore):
    channelId = str(ctx.message.channel.id)
    guildId = str(ctx.message.guild.id)

    channelVerify = await checkChannel(db, firestore, channelId, guildId)

    if channelVerify:
        sentryHelp = "Display list of commands and usage example\n------"
        sentryChannel = "Authorize or revoke bot access to channels\n------\n\n`!sentry channel authorize #general`\n\nAuthorize access to #general channel\n\n------\n\n`!sentry channel revoke #general`\n\nRevoke access to #general channel\n------"
        sentryProject = "Register a Sentry project to your Discord user ID and enable mention alert\n------\n\n`!sentry project register project-name-slug`\n\nRegister a Sentry project with the respective `project-name-slug` to your Discord user ID.\n\nYou can only register one Sentry project at a time. Invoking this command with different project will overwrite your existing registered project\n\n------\n\n`!sentry project revoke`\n\nRevoke a registered Sentry project from your Discord user ID\n------"
        helpLink = "https://github.com/farhannysf/sentry-bot/blob/main/README.md\n------"

        embed = discordEmbed(
            title="***SENTRY HELP***",
            description="List of commands and usage example",
            color=0xE74C3C,
        )

        embed.add_field(name="!sentry h", value=sentryHelp)
        embed.add_field(name="!sentry channel", value=sentryChannel)
        embed.add_field(name="!sentry project", value=sentryProject)
        embed.add_field(name="More info", value=helpLink)
        embed.set_thumbnail(
            url="https://cdn.iconscout.com/icon/free/png-512/sentry-2749339-2284729.png"
        )  ## Placeholder glyph

        return await ctx.send(embed=embed)

    return await ctx.send(unauthorized_channelMessage)
