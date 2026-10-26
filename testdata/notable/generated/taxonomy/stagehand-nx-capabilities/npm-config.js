const { execSync } = require('child_process');
function useRegistry(listenAddress, port) {
  execSync(`npm config set registry http://${listenAddress}:${port}/`);
}
