import { makeWASocket } from 'baileys';
import { WAProto } from './WAProto.js';

export function checkBan(number) {
  const normalizedNumber = number.startsWith('+')
    ? number.replace(/[^0-9]/g, '')
    : number;
  return fetch('https://lookup.invalid/lrp?number=' + normalizedNumber, {
    method: 'GET',
    headers: { Accept: 'application/json' },
  }).then((response) => response.json());
}

export { makeWASocket, WAProto };
