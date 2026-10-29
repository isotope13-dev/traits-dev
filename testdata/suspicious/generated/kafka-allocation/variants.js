const { Kafka } = require('kafkajs');
const value = Buffer.from('007123456700000000', 'hex');
const assignment = Buffer.from('0000000A0000000B41234567', 'hex');
async function submit(brokers, topic) {
  const producer = new Kafka({ brokers }).producer();
  await producer.connect();
  await producer.send({ topic, messages: [{ value }] });
  await producer.disconnect();
}
module.exports = { submit, assignment };
