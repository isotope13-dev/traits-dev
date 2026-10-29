from kafka import KafkaProducer
from kafka.coordinator.protocol import ConsumerProtocolMemberAssignment

# Different count, version, spelling, and trailing content from the article.
record = bytes.fromhex("004000000112345678")
assignment = bytes.fromhex("000000030000000B70000005AABB")
legacy_assignment = bytes.fromhex("0000000170000005")

def submit(brokers, topic):
    producer = KafkaProducer(bootstrap_servers=brokers)
    return producer.send(topic, value=record)
