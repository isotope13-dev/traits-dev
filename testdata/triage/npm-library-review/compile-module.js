const Module = require('module');
const child = new Module('plugin.js', module);
child._compile(source, 'plugin.js');
