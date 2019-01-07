import pika
import random
import string
def random_word(length):
    return ''.join(random.choice(string.lowercase) for i in range(length))

class RabbitMQBinding:

    def __init__(self):
        self.uri = "amqp://guest:guest@127.0.0.1:5672/"
        
        self.exchange_uplink = 'data'
        self.exchange_downlink = 'cmd'
        self.downlink_queue = 'obi_tcp_adapter.cmd'+ random_word(10)


        self.parameters = pika.URLParameters(self.uri)
        self.connection = pika.BlockingConnection(self.parameters)
        self.channel = self.connection.channel()

    def connect(self):
        self.uplink_channel = self.channel
        self.uplink_channel.exchange_declare(exchange=self.exchange_uplink, exchange_type='topic')

    def publish(self, topic, msg):
        self.connect()
        self.uplink_channel.basic_publish(exchange=self.exchange_uplink,
                                            routing_key=topic,
                                            body=msg,
                                            properties=pika.BasicProperties(content_type='text/plain',
                                                                            delivery_mode=2)
                                            )
