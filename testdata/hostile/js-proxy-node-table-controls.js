// Proxy-farm control: a table of non-resolver raw-IP nodes. The famous
// resolver exclusion must not hide it.
const NODES = [
  { host: '45.155.204.9', port: 8080 },
  { host: '185.220.101.4', port: 8080 },
  { host: '91.240.118.200', port: 8080 },
  { host: '103.75.190.10', port: 8080 },
  { host: '8.8.8.8', port: 443 },
  { host: '1.1.1.1', port: 443 },
];
module.exports = NODES;
