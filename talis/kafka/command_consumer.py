import json

from talis.kafka.queue_consumer import QueueConsumer

class CommandConsumer(QueueConsumer):

    def __init__(self, commands, queue, data_processor, stop_event, *args, **kwargs):
        super().__init__(queue, data_processor, stop_event, *args, **kwargs)
        self.commands = commands

    def run(self):
        while not self.stop_event.is_set():
            for msg in self.consumer:
                data = self.data_processor.parse(msg.value)
                command = data.get('message')
                if command in self.commands.keys():
                    response = self.commands[command]
                    data = {
                        'channel' : data.get('channel'),
                        'message' : response
                    }
                    self.queue.put_nowait(bytes(self.data_processor.format(data), 'utf-8'))
                    self.processed += 1
            if self.stop_event.is_set():
                break
