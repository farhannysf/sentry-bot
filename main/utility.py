def retrieveDB_data(db, option, title):
    data_ref = db.collection(option).document(title)
    docs = data_ref.get()
    return docs.to_dict()


async def initDB(db, objectList, objectDb, firestore):
    if objectList is None:
        data = {"create": "create"}
        objectDb.set(data)
        objectDb.update({"create": firestore.DELETE_FIELD})
        return


async def checkChannel(db, firestore, channelId, guildId):
    channel_fetch = retrieveDB_data(db, option="channel-list", title=str(guildId))
    channel_DB_init = db.collection("channel-list").document(str(guildId))
    await initDB(db, channel_fetch, channel_DB_init, firestore)
    try:
        channelVerify = channel_fetch[f"{channelId}"]
    except (KeyError, TypeError):
        return
    return channelVerify


async def checkUser(db, firestore, userId, guildId):
    user_projects = retrieveDB_data(db, option="user-projects", title=str(guildId))
    user_projectsDB = db.collection("user-projects").document(str(guildId))
    await initDB(db, user_projects, user_projectsDB, firestore)
    try:
        userVerify = user_projects[str(userId)]
    except (KeyError, TypeError):
        return
    return userVerify


async def check_existingProject(db, mention, project, guildId):
    user_projects = retrieveDB_data(db, option="user-projects", title=str(guildId))
    userProject = user_projects[str(mention)]

    if str(userProject) != str(project):
        return userProject

    return