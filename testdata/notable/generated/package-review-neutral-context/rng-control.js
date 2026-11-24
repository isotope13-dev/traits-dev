const crypto = require('crypto');
export function sign(data) { return crypto.createHmac('sha256', key).update(data).digest(); }
