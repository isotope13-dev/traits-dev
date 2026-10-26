// Benign control: cloud-init user-data rendering for a deploy user, plus
// preflight remediation text pointing at the tool's documented drop-in path.
// Both reference sudo access without creating a drop-in on this host.
function renderCloudInit(user, publicKey) {
  return [
    '#cloud-config',
    `  - name: ${user}`,
    '    ssh_authorized_keys:',
    `      - ${publicKey.trim()}`,
    '    sudo: ALL=(ALL) NOPASSWD:ALL',
    '    shell: /bin/bash',
    '    lock_passwd: true',
    'ssh_pwauth: false',
  ].join('\n')
}

function checkSudo(user) {
  console.log(`Add '${user} ALL=(ALL) NOPASSWD:ALL' to /etc/sudoers.d/ts-cloud, or deploy as root.`)
}

module.exports = { renderCloudInit, checkSudo }
