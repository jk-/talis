# Talis

***Author: Jon Kirkpatrick***

A Microservice'd Twitch Chat Bot that utilizes Docker, Kafka and Zookeeper.

The general idea of the Bot was the ability to attach and detach "services" to the bot, at will, and dynamically, without destroying, disconnected and restarting the bot. The bot is highly fault-tolerant, in that the attached services have no "connection" or "knowledge" of the bot, and the bot has no knowledge of the services.

This is the next general step into creating a hive mind AI that can attach and disconnect micro-ai services at will.

Twitch Message Producer is the primary script ran inside of the python docker container. This producer connects to Twitch's IRC server and joins the specified channel located in your .env file. This produce pipes the chat messages into a Kafka topic, assigned in the .env file.

Bot.py is the bot that interacts with chat. This bot starts off with no attachments and listens on the topic "bot_messages". It awaits commands from other services.

AI/spam.py is an example service that attaches to the Kafka Topic "twitch_messages" and processes and calculates unique messages in a N-range bin log of recent messages. It will send a message to "bot_messages" on kafka with what text message the bot should send to chat.


### To run:

1. Get an oAuth token for your bot/user using the twitch password generator
2. place the entire oauth:<token> text in the .oauth file
3. update the channel name in the .env folder
4. Run these commands:

```
python -m virtualenv env
source env/bin/activate
pip install -r requirements.txt
docker-compose up --build -d
```

*** To see if the bot worked: ***

```
docker logs -f talis_app
```

You should see messages piping out to your console.

*** To test if kafka is receiving the messages: ***
```
python ai/consumer_test.py
```

You may to change a few "flags" in the twitch_message_producer and ai/* scripts. I manually change certain flags to tell the script if im running on local or in docker.

## Todo:
- [ ] private message response and @ responsesHub
- [ ] ai/consumer_to_file.py  --> data/twitch_messages.txt (compress please)
