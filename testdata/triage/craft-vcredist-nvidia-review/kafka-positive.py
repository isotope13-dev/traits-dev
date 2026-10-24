from confluent_kafka import Producer as MessageProducer

publisher = MessageProducer({"bootstrap.servers": "localhost:9092"})
publisher.produce("analytics", value=b'{"steps": [1, 2, 3]}')
publisher.flush()
