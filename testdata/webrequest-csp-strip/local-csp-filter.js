const responseHeaders = headers.responseHeaders.filter(h =>
  h.name.toLowerCase() !== 'content-security-policy');
