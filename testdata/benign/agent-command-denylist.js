// Benign control for netsh-firewall-off: an agent permission policy that NAMES
// dangerous commands so the operator is asked before they run. The "netsh
// advfirewall" mention sits beside other tools' verbs ("ufw disable"); the
// disable belongs to ufw, and nothing here issues a firewall command.
const alwaysAskCommands = "killall, pkill, taskkill, shutdown, reboot, init 0, init 6, Stop-Process, Stop-Service, mv /*, chmod 000, chmod -R 777, chown, icacls, netsh advfirewall, iptables -F, ufw disable, git reset --hard, git clean -fd, npm uninstall";
const autoApproveGit = false;
function requiresApproval(cmd) {
  return alwaysAskCommands.split(",").some((entry) => cmd.includes(entry.trim().split(" ")[0]));
}
module.exports = { alwaysAskCommands, autoApproveGit, requiresApproval };
