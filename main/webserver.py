from datetime import datetime
from settings import glyph_URL
from httptools.parser.errors import HttpParserInvalidURLError as invalidURL
from sanic import Sanic
from sanic.log import logger as webLogger
from sanic.exceptions import NotFound as error404
from sanic.exceptions import MethodNotSupported as invalidMethod
from sanic.response import json
from discord.errors import NotFound
from ip_validator import validate_ip
from request_validator import validate_args, validate_json
from utility import checkChannel, checkUser, check_existingProject

cn = "exoduspi.com"
currentDate = str(datetime.now().date())
tls = {"cert": f"{cn}-{currentDate}.crt", "key": f"{cn}-{currentDate}.key"}

# Initialize Sanic web server
async def sanic_webserver(exit, devState, client, firestore, db, discordEmbed):
    app = Sanic(__name__)

    querystring_schema = {
        "id": {"type": "string", "required": True},
        "mention": {"type": "string", "required": False},
    }
    json_schema = {
        "id": {"type": "string", "required": True},
        "project": {"type": "string", "required": True},
        "project_name": {"type": "string", "required": True},
        "project_slug": {"type": "string", "required": True},
        "logger": {"nullable": True, "type": "string", "required": True},
        "level": {"type": "string", "required": True},
        "culprit": {"type": "string", "required": True},
        "message": {"type": "string", "required": True},
        "url": {"type": "string", "required": True},
        "triggering_rules": {"required": True},
        "event": {"type": "dict", "required": True},
    }

    probeResponse = {"error": "Access Forbidden"}

    @app.exception(error404)
    async def ignore404(request, exception):
        errorLog = {
            "message": str(exception),
            "ip": str(request.ip),
            "url": str(request.url),
            "body": str(request.body),
        }
        webLogger.error(errorLog)
        return json(probeResponse, status=400)

    @app.exception(invalidMethod)
    async def error400(request, exception):
        webLogger.error(
            {
                "message": str(exception),
                "ip": str(request.ip),
                "url": str(request.url),
            }
        )
        return json(probeResponse, status=400)

    async def invalidURL_handler(request, invalidURL):
        return json(probeResponse, status=400)

    app.error_handler.add(Exception(invalidURL), invalidURL_handler)

    @app.route("/sentry-bot/channel", methods=["POST"])
    @validate_ip(devState)
    @validate_args(querystring_schema)
    @validate_json(json_schema)
    async def postAlert(request):
        queries = dict(request.args)
        try:
            channel = int(queries["id"][0])
        except ValueError:
            errorLog = {"error": {"message": "Channel ID must be a string of integer"}}
            webLogger.error(errorLog)
            return json(errorLog, status=400)

        discordChannel = client.get_channel(channel)
        errorLog = {"error": {"message": "Unauthorized channel", "channel": channel}}

        if not discordChannel:
            webLogger.error(errorLog)
            return json(errorLog, status=401)

        guildId = discordChannel.guild.id
        channelVerify = await checkChannel(db, firestore, str(channel), str(guildId))
        if not channelVerify:
            webLogger.error(errorLog)
            return json(errorLog, status=401)

        mention = None
        if "mention" in queries:
            try:
                mention = int(queries["mention"][0])
            except ValueError:
                errorLog = {
                    "error": {"message": "Mention ID must be a string of integer"}
                }
                webLogger.error(errorLog)
                return json(errorLog, status=400)

            try:
                discordUser = await client.fetch_user(mention)
            except NotFound:
                errorLog = {
                    "error": {"message": "User does not exist", "user": mention}
                }
                webLogger.error(errorLog)
                return json(errorLog, status=401)

        try:
            payload = request.json
            payload = {k: "None" if not v else v for k, v in payload.items()}
            project = payload["project"]
            title = payload["event"]["title"]
            logger = payload["logger"]
            level = payload["level"]
            culprit = payload["culprit"]
            message = payload["message"]
            url = payload["url"]
            timestamp = payload["event"]["timestamp"]
            utcTime = datetime.utcfromtimestamp(timestamp).strftime("%d-%m-%Y %H:%M:%S")
            embed = discordEmbed(
                title="***SENTRY ALERT***", description=f"{project}", color=0xE74C3C
            )
            embed.add_field(name="Title", value=f"`{title}`", inline=True)
            embed.add_field(name="Logger", value=f"`{logger}`", inline=True)
            embed.add_field(name="Level", value=f"`{level}`", inline=True)
            embed.add_field(name="Culprit", value=f"`{culprit}`", inline=True)
            embed.add_field(name="Message", value=f"`{message}`", inline=True)
            embed.add_field(name="URL", value=url, inline=True)
            embed.add_field(name="Timestamp (UTC)", value=f"`{utcTime}`", inline=True)
            embed.set_thumbnail(url=glyph_URL)

            if mention:
                discordMention = discordUser.mention
                userVerify = await checkUser(db, firestore, str(mention), str(guildId))

                if not userVerify:
                    errorLog = {
                        "error": {
                            "message": "User is not registered to any project",
                            "id": mention,
                        }
                    }
                    webLogger.error(errorLog)
                    return json(errorLog, status=401)

                existingProject = await check_existingProject(
                    db, str(mention), str(project), str(guildId)
                )

                if existingProject:
                    errorLog = {
                        "error": {
                            "message": "User is already registered to other project",
                            "id": mention,
                            "project": existingProject,
                        }
                    }
                    webLogger.error(errorLog)
                    return json(errorLog, status=401)

                await discordChannel.send(discordMention, embed=embed)

            else:
                await discordChannel.send(embed=embed)

            alertStatus = {"success": "200"}
            return json(alertStatus)

        except Exception as e:
            webLogger.error(
                {
                    "error": {
                        "message": "An internal error have occurred while processing request",
                        "error": e,
                        "ip": request.ip,
                        "url": request.url,
                        "body": request.body,
                    }
                }
            )
            return json(
                {"error": {"message": "An internal error have occurred:"}}, status=500
            )

    try:
        return await app.create_server(
            host="0.0.0.0",
            port=8080,
            return_asyncio_server=True,
            access_log=True,
            ssl=tls,
        ), webLogger.info(tls)

    except FileNotFoundError:
        webLogger.error("TLS certificate expired: App rebuild is required")
        exit()
    except Exception as e:
        webLogger.error(
            {
                "error": {
                    "message": "Error during Sanic webserver initialization",
                    "error": e,
                }
            }
        )
        exit()