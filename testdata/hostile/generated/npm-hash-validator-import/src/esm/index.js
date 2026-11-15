import { sha256String } from '@hash-validator/v2';
const ALPHABET = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz';
sha256String(ALPHABET).catch(console.error);
export default ALPHABET;
