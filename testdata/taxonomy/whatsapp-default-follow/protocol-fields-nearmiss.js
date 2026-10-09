import { makeGroupsSocket } from './groups.js';
const event = { name: 'Location' };
const rateLimits = { contacts: 40 };
new CustomEvent('upload_start');
