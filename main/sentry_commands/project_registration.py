from utility import checkChannel, retrieveDB_data, checkUser
from settings import unauthorized_channelMessage, glyph_URL


async def project_registrationLogic(
    ctx, discordEmbed, firestore, db, operation, project_name
):
    channelId = str(ctx.message.channel.id)
    guildId = str(ctx.message.guild.id)
    userId = str(ctx.author.id)

    channelVerify = await checkChannel(db, firestore, channelId, guildId)

    if channelVerify:
        registered_project = ""
        user_projects = retrieveDB_data(db, option="user-projects", title=guildId)
        user_projectsDB = db.collection("user-projects").document(str(guildId))
        userVerify = await checkUser(db, firestore, str(userId), str(guildId))
        if userVerify:
            registered_project = user_projects[str(userId)]

        usageMessage = f"`!sentry project register project-name-slug`\n------\n`!sentry project revoke`\n------"
        embed = discordEmbed(
            title="***SENTRY PROJECT REGISTRATION***",
            description="Register a Sentry project to your Discord user ID and enable mention alert",
            color=0xE74C3C,
        )
        
        embed.set_thumbnail(url=glyph_URL)
        embed.add_field(name="Usage", value=usageMessage)
        embed.add_field(
            name="Registered Project", value=f"{registered_project}\n------"
        )

        if operation == "revoke":
            if not userVerify:
                return await ctx.send("You have no project to be revoked")

            data = {str(userId): firestore.DELETE_FIELD}
            user_projectsDB.update(data)
            return await ctx.send(f"Revoked Sentry project: `{user_projects[userId]}`")

        if operation == "register":
            if project_name is None:
                return await ctx.send(embed=embed)

            updb_dict = user_projectsDB.get().to_dict()
            existingProject = [
                key for key, value in updb_dict.items() if value == str(project_name)
            ]

            if len(existingProject) > 0:
                return await ctx.send(
                    f"Sentry project: `{project_name}` is already registered to <@!{existingProject[0]}>"
                )

            else:
                data = {str(userId): str(project_name)}
                user_projectsDB.update(data)
                return await ctx.send(f"Registered Sentry project: `{project_name}`")

        else:
            return await ctx.send(embed=embed)
    else:
        return await ctx.send(unauthorized_channelMessage)
