// Positive: a standard-base64 blob is decoded and handed to a require-enabled Function.
const payload = Buffer.from('Y29uc29sZS5sb2coMSk=', 'base64').toString('utf8');
const run = new Function('require', payload);
run(require);
