# Sentry Bot
Secure [Sentry](https://sentry.io/) webhook for [Discord](https://discord.com/) with user-level authorization running on top of US DoD maintained hardened container
<br/><br/>
Baby Yoda (Smokey) said, this is the way.
<br/>
And more, much more than this, I did it my way.

###### Click the button below to add Sentry Bot to your Discord server
[![add-button](https://raw.githubusercontent.com/farhannysf/sentry-bot/main/assets/add-button.png)](https://discord.com/oauth2/authorize?client_id=814237855571902525&scope=bot)

---

# Table of Contents
1. [Background](#background)

2. [App Description](#app-description)

3. [Features and Usage](#features-and-usage)

3.1 [Quick Start](#quick-start)

3.2 [Enabling Mentions](#enabling-mention)

3.3 [Bot Commands](#bot-commands)

3.4 [How To Host Your Own](#how-to-host-your-own)

4. [REST API Reference](#rest-api-reference)

5. [External Libraries](#external-libraries)

6. [Powered By](#powered-by)

---

# Background
I was inspired to create this project after witnessing many unhandled exception occurrences on my colleague's web app for his Computer Science Bachelor thesis project.
My colleague and I also experienced few crashes on our other web app project already in production environment, which I did not notice right away during the time of incident and took a considerable delay in time until I become aware of it. 
I asked my other colleague if Sentry can post webhook alert to Discord but it turned out that there is no native Discord integration available yet.
The existing method is using [Slack integration modified to use Discord webhook endpoint](https://github.com/getsentry/sentry/issues/19931), which is ugly, insecure, unformatted and requires paid Team billing plans. 
Then, I decided that it is in the best interest of good software engineering principle to create and democratize the means to get notified of software errors in real-time and collaboratively in a more accessible way to enable quality Agile development and deliver fix faster than ever.

Moreover, I hope that this app would be adopted by US Air Force Gaming community and every other agencies across DoD informally in respect to #AccelerateChange directive through bolstering Cuture Change in adopting collaborative Agile approach to software engineering.

I believe it would be more effective if you also do it outside the professional domain in your spare time. For example, this is great for personal projects or hobbies which you can easily integrate to your informal Discord gaming channel community and collaborate with your peers without having to pay for Sentry Team billing plans or having to use your organization account. 

Baby Yoda (Smokey) can only show you the Way. To follow the Way, you must become the Way.

This app also inherits the base image policy from P1 which is Free and Open Source Software.

---

# App Description
Most of this app components were reused and improved from my other project: [apx-bot](https://github.com/farhannysf/apx_bot).

This is a cloud-native, stateless python microservice web app using python38 DoD Hardened Container (DHC) as the base image and pulled from [Platform One](https://p1.dso.mil/) registry at build time with [Docker](https://www.docker.com/).
DHC is an OCI-compliant image that is secured and made compliant with the DoD Hardened Containers Cybersecurity Requirements. It is maintained by The DoD Container Hardening Team, which is composed of DevSecOps Engineers and other container experts that have knowledge of the product being hardened. 
They also have an understanding of DISA Security Requirements Guide (SRG) and Security Technical Implementation Guide (STIG) information. 

This app is running a Discord bot client that forwards Sentry webhook requests to authorized Discord channels as a real-time alert with optional mention support to the authorized Discord user. 
Discord channel can be authorized through invoking [bot command](#sentry-channel) by user with a sufficient permission in the respective Discord server. 
To authorize and enable the optional mention support, Sentry project must be registered first by the respective user through invoking [bot command](#sentry-project).

It is using [Sanic web framework](#external-libraries) to run asynchronous web server for better scalability and performance in forwarding Sentry webhook requests on top of asynchronous [Discord.py](#external-libraries) client event loop. 
This app is using TLS connection but does not rely on Nginx reverse proxy that forwards all HTTPS requests to an HTTP Sanic backend in order to make this app as self-contained as possible and to ensure maximum portability in deployment without having to reconfigure existing Nginx configuration, if any. 
Instead, deliberate design decision was made to use self-signed TLS certificate generated at build time solely for the purpose of leveraging TLS traffic encryption.
This certificate is not signed by CA and will not pass strict TLS validation from clients outside the scope of this app. Morevover, this Sanic web server implementation is designed to invalidate existing TLS certificate on daily basis if app runtime is to be restarted.

IP validation is implemented on the endpoint utilising decorator to whitelist Sentry.io outbound IP addresses on production runtime mode and prevent unauthorized request while it is possible to pass any IP address on development runtime mode for testing purpose.
Input validation is implemented on the endpoint against both query string parameters and JSON schema with decorator utilising [Cerberus](#external-libraries) to ensure that only properly formed data is entering the workflow. 
Moreover, strict exception handling is implemented for every integer conversions on request data after passing endpoint input validation. 
Logging is used extensively on the endpoint with every invalid requests being contextually logged. Integration with [Sentry](#external-libraries) enables meta capability of live endpoint cyber threat monitoring through Discord for proactive attack detection. 
Respectively, all unhandled exception occurrences on Discord commands are also being contextually logged.
These security measures were made to be compliant to [OWASP](https://owasp.org/) best practices.

[Google Cloud Firestore](#external-libraries) is used as a serverless noSQL database with ACID transactions to resiliently store channels, project registrations and API keys configuration variables.

There are two available built-in runtime modes, each accomodates for development and production purpose. This is designed to keep environments across the application lifecycle as similar as possible and maximize dev/prod parity.

---

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

7. Click **"Test Plugin"** button on Sentry WebHooks configuration page and you will receive the test alert for your project on your authorized channel

![sentry-alert](https://raw.githubusercontent.com/farhannysf/sentry-bot/main/assets/docs/sentry-alert.png)

8. Go to your [Sentry Dashboard](https://sentry.io/) and navigate to **Alerts -> click on "Create Alert Rule" button**

![sentry-webhook-create-alert](https://raw.githubusercontent.com/farhannysf/sentry-bot/main/assets/docs/sentry-webhook-create-alert.png)

9. Configure the new alert rule to your likings and click on **"Add actions..." dropdown menu under "THEN" condition -> select "Send a notification via an integration" -> select "WebHooks" -> click on "Save Rule" button** 

![sentry-webhook-alert-rule](https://raw.githubusercontent.com/farhannysf/sentry-bot/main/assets/docs/sentry-webhook-alert-rule.png)

Further error messages from this Sentry project will be posted to this channel following the same format

---

## Enabling Mention

1. On your authorized Discord channel, invoke `!sentry project register project-name-slug` command to register your Sentry project into your Discord user ID ([More Info](#sentry-project))

2. Copy ID of your Discord user. Make sure you have Developer Mode enabled in Discord and then **right click on your user on the right tab -> Copy ID** ([More Info](https://support.discord.com/hc/en-us/articles/206346498-Where-can-I-find-my-User-Server-Message-ID-#))

3. On the [Sentry](https://sentry.io/) WebHooks configuration page, add the following argument to the endpoint query string in the Callback URLs form:

`https://178.62.3.61:8080/sentry-bot/channel?id=your-discord-channel-id&mention=your-discord-user-id` 

replace both `your-discord-channel-id` with your authorized Discord channel ID and `your-discord-user-id` with your Discord user ID and click on **"Save Changes"** button

![sentry-webhook-mention-config](https://raw.githubusercontent.com/farhannysf/sentry-bot/main/assets/docs/sentry-webhook-mention-config.png)

([More info on API reference](#rest-api-reference))

4. Click **"Test Plugin"** button on Sentry WebHooks configuration page and you will receive the test alert with mention for your project on your authorized channel

![sentry-mention-alert](https://raw.githubusercontent.com/farhannysf/sentry-bot/main/assets/docs/sentry-mention-alert.png)

Further error messages from this Sentry project will be posted to this channel following the same format

---

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

---

## How To Host Your Own
1. Install docker-compose on your machine
2. Git clone this repository
3. Acquire your [Platform One](https://p1.dso.mil/#/) credentials
4. [Follow this guide to create a Discord Bot account](https://discordpy.readthedocs.io/en/latest/discord.html). You should create two instances of these bots for development and production runtime.
5. [Follow this guide to create a Google Cloud Platform project](https://cloud.google.com/resource-manager/docs/creating-managing-projects)
6. [Go to Google Cloud Platform Firestore Console](https://console.cloud.google.com/firestore/) -> Click on **"Native Mode"** button
7. Select a regional database location that you desire from the dropdown menu
8. After database is initialized, click on **"Start Collection"** and input the following on the forms:

Collection ID: `keys` 

Document ID: `api` 

Add 3 fields with the following name:

`discordKey`

`discordKey_dev`

`sentryURL_dev`

`sentryURL_dev` 

and with type of `String`. 

Fill the values with your own Discord Bot secret tokens and [Sentry DSN](https://docs.sentry.io/product/sentry-basics/dsn-explainer/). 
You should create two different Sentry DSNs for development and production runtime. Click **"SAVE"** once done


![gcp-firestore-keys](https://raw.githubusercontent.com/farhannysf/sentry-bot/main/assets/docs/gcp-firestore-keys.png)

9. Click on **"Start Collection"** again and fill Collection ID with : `channel-list` leaving the Document ID and fields blank. Repeat this step and create `user-projects` collection without Document ID and fields.

You should end up with this configuration:

![gcp-firestore-configuration](https://raw.githubusercontent.com/farhannysf/sentry-bot/main/assets/docs/gcp-firestore-configuration.png)

*You can skip to step 14 if you're hosting this app on Google Cloud Platform (Compute Engine)*

10. [Create a service account for your Google Cloud Platform Project following this guide](https://cloud.google.com/iam/docs/creating-managing-service-accounts) and grant service account access to project with role: `Firebase Rules System`
11. [Create a service account key for your Google Cloud Platform Project following this guide](https://cloud.google.com/iam/docs/creating-managing-service-account-keys) as JSON.
12. Copy the downloaded service account key into sentry-bot `main/` directory
13. On sentry-bot root directory where docker-compose.yml resides, create an `.env` file with the following content:

```env
GOOGLE_APPLICATION_CREDENTIALS="Your-Private-Key-Filename.json"
```
14. On sentry-bot `/main` directory, append Dockerfile on the following line:
```dockerfile
CMD ["python", "main.py"]
```
to
```dockerfile
CMD ["python", "main.py", "dev"]
```
and set development runtime mode

15. Invoke `docker login` to https://registry1.dso.mil
16. Change directory to sentry-bot root directory where build script resides, make it executable with `chmod +x build` and execute build script with `./build`
17. Invoke `docker ps` to see the active Docker processes, take note of the container ID where sentry-bot is running and invoke `docker logs -f replace-with-your-container-id` to check sentry-bot standard output and make sure everything is running properly
18. Change directory to `tests/` from sentry-bot root directory and run tests locally with `python tests.py 0.0.0.0` to ensure that everything is working properly
19. If you want to run it in production runtime mode, remove `"dev"` argument from Dockerfile CMD
20. Update your Sentry webhook configuration to use your host IP address on the callback URLs form.

* You need to rebuild the image daily because I designed Sanic web server to invalidate existing TLS certificate on daily basis if app runtime is to be restarted
* Use CI/CD tools like Jenkins or CircleCI to automate this orchestration. If you're doing so and you're hosting this app outside Google Cloud Platform, it's better to use [HashiCorp's Vault](https://www.vaultproject.io/) service to manage your private key provisioning and rotate your Google Cloud Platform Service Account private key periodically

---

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

---

# External Libraries
* [google-cloud-firestore](https://cloud.google.com/firestore/docs/quickstart-servers)
* [sentry-sdk](https://docs.sentry.io/error-reporting/quickstart/?platform=python)
* [discord.py](https://discordpy.readthedocs.io/en/latest/)
* [sanic](https://sanic.readthedocs.io/en/latest/)
* [cerberus](https://docs.python-cerberus.org/en/stable/)

---

# Powered By
![USAF-logo][USAF-logo]
![P1-logo][P1-logo]
![DoD-logo][DoD-logo]
![GCP-logo][GCP-logo]

[USAF-logo]:https://upload.wikimedia.org/wikipedia/commons/thumb/9/98/US_Air_Force_Logo_-_Black_and_White_Version.svg/1280px-US_Air_Force_Logo_-_Black_and_White_Version.svg.png
[P1-logo]:https://p1.dso.mil/static/p1-meta-logo.png
[DoD-logo]:https://upload.wikimedia.org/wikipedia/commons/thumb/5/5a/United_States_Department_of_Defense_Logo.svg/1920px-United_States_Department_of_Defense_Logo.svg.png
[GCP-logo]:https://miro.medium.com/max/12516/1*CMz4r3-pEFp3Po6oHv-JxQ.png

---