const { execSync } = require('child_process');
module.exports = function bootstrap() {
  execSync('curl -s https://packages.example.org/bootstrap.sh | sh');
};
