import queue
import threading

# config and logs
from talis import config
from talis import log

# threads
from talis import TwitchChat
from talis.kafka import QueueConsumer
from talis.kafka import CommandConsumer
from talis.kafka import DequeueProducer
from talis.processor import JsonProcessor

if __name__ == "__main__":
    config.add_oauth()
    log.info("=== Twitch Bot Started ===")

    chat_queue = queue.Queue()
    bot_message_queue = queue.Queue()
    stop_event = threading.Event()

    json_processor = JsonProcessor()

    bot_message_consumer = QueueConsumer(
        bot_message_queue,
        stop_event,
        json_processor,
        topic=config.get("KAFKA_BOT_MESSAGE_TOPIC"),
        auto_offset_reset="latest",
        bootstrap_servers=config.get("KAFKA_BOOTSTRAP_HOST")
    )
    bot_message_consumer.setDaemon(True)

    twitch_chat_dequeue = DequeueProducer(
        chat_queue,
        json_processor,
        bootstrap_servers=config.get('KAFKA_BOOTSTRAP_HOST'),
        topic=config.get('KAFKA_TOPIC')
    )
    twitch_chat_dequeue.setDaemon(True)

    twitch_chat_producer = TwitchChat(
        config.get('TWITCH_NICK'),
        config.get('TWITCH_OAUTH_TOKEN'),
        config.get('TWITCH_CHANNEL'),
        chat_queue,
        bot_message_queue,
        stop_event,
        verbose=True
    )
    twitch_chat_producer.connect()

    try:
        twitch_chat_producer.start()
        twitch_chat_dequeue.start()
        bot_message_consumer.start()
    except (KeyboardInterrupt, SystemExit):
        stop_event.set()
        raise
    except:
        stop_event.set()
        raise
