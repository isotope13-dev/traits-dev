// Negative control: relative module paths are not URL endpoint segments.
// None of the endpoint collection tokens may fire on this file.
const groups = require('./groups');
const domains = require('../domains');
const organization = require('./organization');
module.exports = { groups, domains, organization };
