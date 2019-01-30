'''
Output a kafka topic to a file
# TODO: Add compression
'''
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

import threading

from talis import config
from talis import log
from talis.kafka import FileConsumer
from talis.processor import JsonProcessor

if __name__ == "__main__":
    consumer_stop_event = threading.Event()

    consumer = FileConsumer(
        consumer_stop_event,
        JsonProcessor(),
        topic=config.get('topic', config.get('KAFKA_TOPIC')),
        bootstrap_servers=config.get('KAFKA_BOOTSTRAP_HOST'),
        auto_offset_reset=config.get('auto_offset_reset', 'earliest'),
        consumer_timeout_ms=1000
    )
    try:
        consumer.start()
    except (KeyboardInterrupt, SystemExit):
        consumer_stop_event.set()
        pass
