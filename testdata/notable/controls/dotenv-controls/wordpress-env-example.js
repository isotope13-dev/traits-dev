const path = require('path');

// Helper operating on a wordpress-develop checkout: the develop marker plus
// the sample env file together identify the WordPress local environment.
function sampleEnvFor(checkoutRoot) {
  const marker = path.join(checkoutRoot, 'wordpress-develop', 'src', 'wp-config-sample.php');
  const envExample = path.join(checkoutRoot, 'wordpress-develop', '.env.example');
  return { marker, envExample };
}

module.exports = { sampleEnvFor };
