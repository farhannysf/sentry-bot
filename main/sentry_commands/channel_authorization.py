import re
from utility import retrieveDB_data, checkChannel


async def channel_authorizationLogic(ctx, firestore, db, operation, channel):
    guildId = str(ctx.message.guild.id)

    channel_fetch = retrieveDB_data(db, option="channel-list", title=guildId)

    if operation:
        if channel:
            channel_init_DB = db.collection("channel-list").document(str(guildId))

            try:
                channelSelect = int(re.search(r"\d+", channel).group())

            except:
                return await ctx.send(
                    "Please input the correct channel format, e.g. `#example`."
                )

            channelVerify = await checkChannel(
                db, firestore, channelSelect, str(guildId)
            )

            if operation == "authorize":
                if channelVerify:
                    return await ctx.send(f"<#{channelSelect}> is already authorized")

                data = {str(channelSelect): str(channelSelect)}
                channel_init_DB.update(data)
                return await ctx.send(
                    f"**Updated authorized channel list.**\n <#{channelSelect}> `is now authorized`"
                )

            if operation == "revoke":
                if not channelVerify:
                    return await ctx.send(f"<#{channelSelect}> is not yet authorized")

                data = {str(channelSelect): firestore.DELETE_FIELD}
                channel_init_DB.update(data)
                return await ctx.send(
                    f"**Updated authorized channel list.**\n `Revoked access from` <#{channelSelect}>"
                )

    if channel_fetch is None:
        authorizedChannels = ""

    else:
        authorizedChannels = "\n".join(
            "<#{}>".format(key) for key, value in channel_fetch.items()
        )

    usageMessage = f"\n**Usage:**\n\n`!sentry channel authorize [#channel]`\n`!sentry channel revoke [#channel]`\n\n**Authorized Channels:**\n\n{authorizedChannels}"

    return await ctx.send(usageMessage)