const { Kafka } = require('kafkajs');
// Empty serialized list and empty active task count, rather than huge counts.
const record = Buffer.from('000000000000000000', 'hex');
const assignment = Buffer.from('0000000b0000000b00000000', 'hex');
