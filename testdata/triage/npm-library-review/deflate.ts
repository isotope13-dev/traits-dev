import pako from 'pako';
const result = pako.deflate(new TextEncoder().encode(diagram));
