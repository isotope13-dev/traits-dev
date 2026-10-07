// Connectivity-check control: famous public DNS resolvers used as
// reachability targets. The resolver exclusion must keep this silent.
const TARGETS = [
  { host: '223.5.5.5', port: 443 }, // AliDNS
  { host: '119.29.29.29', port: 443 }, // DNSPod
  { host: '1.1.1.1', port: 443 }, // Cloudflare
  { host: '8.8.8.8', port: 443 }, // Google
  { host: '9.9.9.9', port: 443 }, // Quad9
];
module.exports = TARGETS;
