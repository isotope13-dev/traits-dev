const runtime = require('./runtime.js');
const parent = require('../../core');
const packageSubpath = require('package/.settings');
const hiddenDirectory = require('../.cache/runtime.js');
module.exports = { runtime, parent, packageSubpath, hiddenDirectory };
