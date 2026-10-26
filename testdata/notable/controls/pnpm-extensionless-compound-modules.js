// CommonJS appends .js when resolving these extensionless module names.
const BaseDelay = require("../delay.base");
const DelayFactory = require("../delay.factory");
const SkipFirstDelay = require("./skip-first.delay");
const IteratorZip = require("../Iterator.zip");

module.exports = { BaseDelay, DelayFactory, SkipFirstDelay, IteratorZip };
