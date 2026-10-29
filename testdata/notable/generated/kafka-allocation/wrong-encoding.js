const { Kafka } = require('kafkajs');
const record = Buffer.from('007fffffff00000000', 'utf8');
const assignment = Buffer.from('0000000b0000000b7fffffff', 'utf8');
