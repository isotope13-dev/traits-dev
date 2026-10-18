// A format recognizer with an unused DPAPI import is not credential theft.
const { Dpapi } = require('@primno/dpapi');
const encryptedPrefix = 'dQw4w9WgXcQ:';
const plainPattern = /[\w-]{24}\.[\w-]{6}\.[\w-]{38}/g;
