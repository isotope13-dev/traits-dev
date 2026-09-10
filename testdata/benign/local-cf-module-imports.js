import './cf-env.js';
import { configuration } from './cf.js';
const legacy = require('../cf.js');
export const settings = { configuration, legacy };
