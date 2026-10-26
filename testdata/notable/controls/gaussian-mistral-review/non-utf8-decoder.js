// new TextDecoder() uses UTF-8; this decoder explicitly selects UTF-16.
export const decoder = new TextDecoder('utf-16le');
export const text = decoder.decode(bytes);
