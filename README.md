# sentry-bot (Docs still WIP)
Secure [Sentry](https://sentry.io/) webhook for [Discord](https://discord.com/) with user-level authorization running on top of US DoD maintained hardened container
<br/><br/>
Baby Yoda (Smokey) said, this is the way.
<br/>
And more, much more than this, I did it my way.

###### Click the button below to add Sentry Bot to your Discord server
[![add-button](https://raw.githubusercontent.com/farhannysf/sentry-bot/main/assets/add-button.png)](https://discord.com/oauth2/authorize?client_id=814237855571902525&scope=bot)

# Background
I was inspired to create this project after witnessing many unhandled exception occurence on my colleague's web app for his Computer Science Bachelor thesis project.
My colleague and I also experienced few crashes on our other web app project already in production environment, which I did not notice right away during the time of incident and took a considerable delay in time until I become aware of it. 
I asked my other colleague if Sentry can post webhook alert to Discord but it turned out that there is no native Discord integration available yet.
The existing method is using Slack integration modified to use Discord webhook endpoint, which is ugly, unformatted and requires paid Team billing plans. 
Then, I decided that it is in the best interest of good software engineering principle to create and democratize the mean to get notified of software errors in real-time and collaboratively in a more accessible way to enable quality Agile development and deliver fix faster than ever.

Moreover, I hope that this app would be adopted by US Air Force Gaming community and every other agencies across DoD informally in respect to #AccelerateChange directive through bolstering Cuture Change in adopting collaborative Agile approach to software engineering, which I believe would be more effective
if you also do it outside the professional domain in your spare time. For example, this is great for personal projects or hobbies which you can easily integrate to your informal Discord gaming channel community and collaborate with your peers without having to pay for Sentry Team billing plans or having to use your organization account. 

Baby Yoda (Smokey) can only show you the Way. To follow the Way, you must become the Way.

This app also inherits the base image policy from P1 which is Free and Open Source Software.

# Features and Usage
## Quick Start
1. [Invite Sentry Bot to your Discord server](#click-the-button-below-to-add-sentry-bot-to-your-discord-server) 
2. Authorize desired channel in your Discord server by invoking `!sentry authorize #channel` command ([More Info](#sentry-channel))
3. Copy ID of the authorized channel. Make sure you have Developer Mode enabled in Discord and then **right click on desired channel -> Copy ID** ([More Info](https://support.discord.com/hc/en-us/articles/206346498-Where-can-I-find-my-User-Server-Message-ID-#))

4. Go to your [Sentry Dashboard](https://sentry.io/) and navigate to **Settings -> Integrations** page and search for webhook

![sentry-settings](https://raw.githubusercontent.com/farhannysf/sentry-bot/main/assets/docs/sentry-settings.png)

5. Select **"WebHooks"** integration and click on **"Add to Project"** button

![sentry-webhook](https://raw.githubusercontent.com/farhannysf/sentry-bot/main/assets/docs/sentry-webhook.png)

6. On the WebHooks configuration page, copy the following endpoint URL to the Callback URLs form: 
 
`https://178.62.3.61:8080/sentry-bot/channel?id=your-discord-channel-id` 

replace `your-discord-channel-id` with your previously authorized Discord channel ID, click on **"Save Changes"** button and **"Enable Plugin"**

![sentry-webhook-config](https://raw.githubusercontent.com/farhannysf/sentry-bot/main/assets/docs/sentry-webhook-config.png)

([More info on API reference](#rest-api-reference))

7. Click **Test Plugin** button on Sentry WebHooks configuration page and you will receive the test alert for your project on your authorized channel

![sentry-alert](https://raw.githubusercontent.com/farhannysf/sentry-bot/main/assets/docs/sentry-alert.png)

8. Go to your [Sentry Dashboard](https://sentry.io/) and navigate to **Alerts -> click on "Create Alert Rule" button**

![sentry-webhook-create-alert](https://raw.githubusercontent.com/farhannysf/sentry-bot/main/assets/docs/sentry-webhook-create-alert.png)

9. Configure the new alert rule to your likings and click on **"Add actions..." dropdown menu under "THEN" condition -> select "Send a notification via an integration" -> select "WebHooks" -> click on "Save Rule" button** 

![sentry-webhook-alert-rule](https://raw.githubusercontent.com/farhannysf/sentry-bot/main/assets/docs/sentry-webhook-alert-rule.png)

Further error messages from this Sentry project will be posted to this channel following the same format

## Enabling Mention

1. On your authorized Discord channel, invoke `!sentry project register project-name-slug` command to register your Sentry project into your Discord user ID ([More Info](#sentry-project))

2. Copy ID of your Discord user. Make sure you have Developer Mode enabled in Discord and then **right click on your user on the right tab -> Copy ID** ([More Info](https://support.discord.com/hc/en-us/articles/206346498-Where-can-I-find-my-User-Server-Message-ID-#))

3. On the [Sentry](https://sentry.io/) WebHooks configuration page, add the following argument to the endpoint URL in the Callback URLs form:

`https://178.62.3.61:8080/sentry-bot/channel?id=your-discord-channel-id&mention=your-discord-user-id` 

replace both `your-discord-channel-id` with your authorized Discord channel ID and `your-discord-user-id` with your Discord user ID and click on "Save Changes" button

![sentry-webhook-mention-config](https://raw.githubusercontent.com/farhannysf/sentry-bot/main/assets/docs/sentry-webhook-mention-config.png)

([More info on API reference](#rest-api-reference))

4. Click **Test Plugin** button on Sentry WebHooks configuration page and you will receive the test alert with mention for your project on your authorized channel

![sentry-mention-alert](https://raw.githubusercontent.com/farhannysf/sentry-bot/main/assets/docs/sentry-mention-alert.png)

Further error messages from this Sentry project will be posted to this channel following the same format

## Bot Commands
### !sentry h
Display list of commands and usage example

![sentry-help-command](https://raw.githubusercontent.com/farhannysf/sentry-bot/main/assets/docs/sentry-help-command.png)
<br/><br/>

### !sentry channel
Authorize or revoke bot access to channels.

`!sentry channel authorize #general`
Authorize access to #general channel

`!sentry channel revoke #general`
Revoke access to #general channel

![sentry-channel-command](https://raw.githubusercontent.com/farhannysf/sentry-bot/main/assets/docs/sentry-channel-command.png)
<br/><br/>

### !sentry project
Register a Sentry project to your Discord user ID and enable mention alert

`!sentry project register project-name-slug`
Register a Sentry project with the respective project-name-slug to your Discord user ID. 

You can only register one Sentry project at a time. 
Invoking this command with different project will overwrite your existing registered project

`!sentry project revoke`
Revoke a registered Sentry project from your Discord user ID

![sentry-project-command](https://raw.githubusercontent.com/farhannysf/sentry-bot/main/assets/docs/sentry-project-command.png)

# REST API Reference
## Endpoint path
`https://178.62.3.61:8080/sentry-bot/channel`
## Query parameters
### id
Type: `String`

Required: `Yes`

Description: `Authorized Discord channel ID`

Example: `https://178.62.3.61:8080/sentry-bot/channel?id=819187565546176513`
### mention
Type: `String`

Required: `Optional`

Description: `Discord user ID registered to this project`

Example: `https://178.62.3.61:8080/sentry-bot/channel?id=819187565546176513&mention=814237855571902525`


# External Libraries used
* [google-cloud-firestore](https://cloud.google.com/firestore/docs/quickstart-servers)
* [sentry-sdk](https://docs.sentry.io/error-reporting/quickstart/?platform=python)
* [discord.py](https://discordpy.readthedocs.io/en/latest/)
* [sanic](https://sanic.readthedocs.io/en/latest/)
* [cerberus](https://docs.python-cerberus.org/en/stable/)

# Powered by
![alt text][USAF-logo]
![alt text][P1-logo]
![alt text][DoD-logo]
![alt text][GCP-logo]

[USAF-logo]:https://upload.wikimedia.org/wikipedia/commons/thumb/9/98/US_Air_Force_Logo_-_Black_and_White_Version.svg/1280px-US_Air_Force_Logo_-_Black_and_White_Version.svg.png
[P1-logo]:https://p1.dso.mil/static/p1-meta-logo.png
[DoD-logo]:https://upload.wikimedia.org/wikipedia/commons/thumb/5/5a/United_States_Department_of_Defense_Logo.svg/1920px-United_States_Department_of_Defense_Logo.svg.png
[GCP-logo]:https://miro.medium.com/max/12516/1*CMz4r3-pEFp3Po6oHv-JxQ.png