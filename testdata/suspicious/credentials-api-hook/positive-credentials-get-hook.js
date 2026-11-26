'use strict';
// Wraps the page's Credentials API so every get() call passes through a relay first.
const nativeGet = CredentialsContainer.prototype.get;
CredentialsContainer.prototype.get = function (options = {}) {
  return relayToHelper(this, options).catch(() => nativeGet.call(this, options));
};
function relayToHelper(container, options) {
  return new Promise((resolve, reject) => {
    window.postMessage({source: 'helper', type: 'request', options}, '*');
    window.addEventListener('message', event => resolve(event.data), {once: true});
  });
}
