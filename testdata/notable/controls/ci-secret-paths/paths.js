const path = require('path');
const jenkins = path.join(process.env.JENKINS_HOME, 'secrets', 'initialAdminPassword');
const runner = path.join(process.env.HOME, '.gitlab-runner', 'config.toml');
module.exports = {jenkins, runner};
