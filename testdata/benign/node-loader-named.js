import { register as addLoader } from 'node:module';
addLoader('./loader.mjs', import.meta.url);
