// CommonJS appends .js when resolving these extensionless module names.
const BaseDelay = require("../delay.base");
const DelayFactory = require("../delay.factory");
const SkipFirstDelay = require("./skip-first.delay");

module.exports = { BaseDelay, DelayFactory, SkipFirstDelay };
