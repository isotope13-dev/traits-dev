// Positive control: genuine REST collection URL segments must still match
// the endpoint tokens after the relative-require guard.
const groupsUrl = 'https://graph.microsoft.com/v1.0/groups';
const domainsUrl = 'https://graph.microsoft.com/v1.0/domains';
const orgUrl = 'https://graph.microsoft.com/v1.0/organization';
module.exports = { groupsUrl, domainsUrl, orgUrl };
