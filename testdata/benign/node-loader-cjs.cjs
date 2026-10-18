const moduleApi = require('node:module');
moduleApi.register('./loader.mjs', __filename);
