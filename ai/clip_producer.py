'''
This script will attach and listen for
bot messages (temporary location for testing) and will
generate a 10 second clip of the channel where "hype" occurred
'''
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

import threading

from queue import Queue

from talis import config
from talis import log
from talis import VideoProducer
from talis.kafka import QueueConsumer
from talis.processor import JsonProcessor

if __name__ == "__main__":
    try:
        spam_message_queue = Queue()
        stop_event = threading.Event()

        json_processor = JsonProcessor()

        consumer = QueueConsumer(
            spam_message_queue,
            stop_event,
            json_processor,
            topic=config.get('topic', config.get('KAFKA_BOT_MESSAGE_TOPIC')),
            bootstrap_servers=config.get('KAFKA_BOOTSTRAP_HOST'),
            auto_offset_reset=config.get('auto_offset_reset', 'latest')
        )
        consumer.start()
        video_producer = VideoProducer(
            spam_message_queue,
            json_processor
        )
        video_producer.setDaemon(True)
        video_producer.start()
    except:
        stop_event.set()
        raise
