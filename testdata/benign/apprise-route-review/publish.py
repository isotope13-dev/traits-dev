import pika

def notify(channel, body):
    channel.basic_publish(exchange="events", routing_key="notice", body=body)
