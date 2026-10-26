// CI-environment detection, as in env-ci/size-plugin style libraries and
// GitHub Actions bundles: identify which CI vendor is running and which
// project it is building. Reading these identity variables alone sends
// nothing anywhere; exfiltration needs a separate transfer trait.
const repo =
  process.env.GITHUB_REPOSITORY ||
  process.env.CI_PROJECT_PATH ||
  process.env.CIRCLE_PROJECT_USERNAME + '/' + process.env.CIRCLE_PROJECT_REPONAME;
console.log(`building ${repo}`);
