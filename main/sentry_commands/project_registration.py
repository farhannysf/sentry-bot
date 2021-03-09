from utility import checkChannel, retrieveDB_data, checkUser
from settings import unauthorized_channelMessage


async def project_registrationLogic(ctx, firestore, db, operation, project_name):
    channelId = str(ctx.message.channel.id)
    guildId = str(ctx.message.guild.id)
    userId = str(ctx.author.id)

    channelVerify = await checkChannel(db, firestore, channelId, guildId)

    if channelVerify:
        registered_project = None
        user_projects = retrieveDB_data(db, option="user-projects", title=guildId)
        user_projectsDB = db.collection("user-projects").document(str(guildId))
        userVerify = await checkUser(db, firestore, str(userId), str(guildId))
        if userVerify:
            registered_project = user_projects[str(userId)]

        usageMessage = f"\n**Usage:**\n\n`!sentry project register project-name-slug\n!sentry project revoke`\n\n**Registered project:**\n\n{registered_project}"

        if operation == "revoke":
            if not userVerify:
                return await ctx.send("You have no project to be revoked")

            data = {str(userId): firestore.DELETE_FIELD}
            user_projectsDB.update(data)
            return await ctx.send(f"Revoked `{user_projects[userId]}`")

        if operation == "register":
            if project_name is None:
                return await ctx.send(usageMessage)

            updb_dict = user_projectsDB.get().to_dict()
            existingProject = [
                key for key, value in updb_dict.items() if value == str(project_name)
            ]

            if len(existingProject) > 0:
                return await ctx.send(
                    f"{project_name} already registered by <@!{existingProject[0]}>"
                )

            else:
                data = {str(userId): str(project_name)}
                user_projectsDB.update(data)
                return await ctx.send(f"Registered `{project_name}`")

        else:
            return await ctx.send(usageMessage)
    else:
        return await ctx.send(unauthorized_channelMessage)
