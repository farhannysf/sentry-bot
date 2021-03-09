import re
from utility import retrieveDB_data, checkChannel


async def channel_authorizationLogic(
    ctx, discordEmbed, firestore, db, operation, channel
):
    guildId = str(ctx.message.guild.id)

    channel_fetch = retrieveDB_data(db, option="channel-list", title=guildId)

    if operation:
        if channel:
            channel_init_DB = db.collection("channel-list").document(str(guildId))

            try:
                channelSelect = int(re.search(r"\d+", channel).group())

            except:
                return await ctx.send(
                    "Please input the correct channel format, e.g. `#example`"
                )

            channelVerify = await checkChannel(
                db, firestore, channelSelect, str(guildId)
            )

            if operation == "authorize":
                if channelVerify:
                    return await ctx.send(f"<#{channelSelect}> is already authorized")

                data = {str(channelSelect): str(channelSelect)}
                channel_init_DB.update(data)
                return await ctx.send(f"<#{channelSelect}> is now authorized")

            if operation == "revoke":
                if not channelVerify:
                    return await ctx.send(f"<#{channelSelect}> is not yet authorized")

                data = {str(channelSelect): firestore.DELETE_FIELD}
                channel_init_DB.update(data)
                return await ctx.send(f"Revoked access from <#{channelSelect}>")

    if channel_fetch is None:
        authorizedChannels = ""

    else:
        authorizedChannels = "\n".join(
            "<#{}>".format(key) for key, value in channel_fetch.items()
        )

    usageMessage = "`!sentry channel authorize #channel`\n------\n`!sentry channel revoke #channel`\n------"
    embed = discordEmbed(
        title="***SENTRY CHANNEL AUTHORIZATION***",
        description="Authorize or revoke bot access to channels",
        color=0xE74C3C,
    )
    embed.set_thumbnail(
        url="https://cdn.iconscout.com/icon/free/png-512/sentry-2749339-2284729.png"
    )  ## Placeholder glyph
    embed.add_field(name="Usage", value=usageMessage)
    embed.add_field(name="Authorized Channels", value=f"{authorizedChannels}\n------")

    return await ctx.send(embed=embed)