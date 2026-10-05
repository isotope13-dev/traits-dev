// Benign control for solana-config-yml-name: a CI workflow generator naming
// CircleCI's own `.circleci/config.yml`. No Solana connection exists, so the
// trait must stay silent here.
const ciWorkflowInputs = {
  circleci: ".circleci/config.yml",
};
