// Counter-shape: names the collaborator service in a comment, but performs
// no lookup and collects no identity. The conjunction gates the verdict.
const COLLABORATOR_DOCS = "https://oastify.com";

function describe() {
  return `point callbacks at ${COLLABORATOR_DOCS}`;
}

module.exports = { describe };
