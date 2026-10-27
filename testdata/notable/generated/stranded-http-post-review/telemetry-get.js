function decode(input) { return input.replace(/../g, byte => String.fromCharCode(parseInt(byte, 16))) }
const methods = [null, decode('6178696f73'), decode('676574'), 'https://example.invalid/status', null, null, null, 'then'];
module.exports = () => require(methods[1])[methods[2]](methods[3], {status: 'ok'})[methods[7]](reply => console.log(reply.status)).catch(console.error);
