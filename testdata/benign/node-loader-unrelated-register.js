import * as moduleApi from 'node:module';
import { register } from './event-registry.js';
router.register('./loader.mjs', import.meta.url);
register('./loader.mjs', import.meta.url);
// moduleApi.register('./loader.mjs', import.meta.url);
