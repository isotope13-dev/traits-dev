const tracing = require('tracing');
const crypto_1 = require('crypto');
const child_process_1 = require('child_process');
const trace = (0, tracing.fork)('span');
const generateId = (0, crypto_1.randomUUID);
const fork = child_process_1.fork;
const example = '(0, child_process_1.fork)(modulePath)';
// (0, crypto_1.randomUUID)();
