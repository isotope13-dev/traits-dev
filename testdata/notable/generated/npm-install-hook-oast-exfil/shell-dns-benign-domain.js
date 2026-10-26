const { exec } = require("child_process");
// Counter-shape: shell identity plus a DNS lookup, but at a plain domain
// with no collaborator service. The OAST endpoint gates the verdict.
exec(
  "echo \"$(whoami)@$(hostname)\"; nslookup example.com >/dev/null 2>&1 || true;",
  (error) => {
    if (error) {
      return;
    }
  },
);
