"""Scan controls statically; never execute the PowerShell fixtures."""
import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
OLD = "objectives/persistence/login/scheduled-task/cmdlet::schtask-system-startup-persistence"
NEW = "micro-behaviors/os/autorun/task-trigger::system-startup-task-settings"
PREFIX = "micro-behaviors/os/autorun/scheduled::"
ATOMS = {PREFIX + name for name in (
    "register-scheduledtask", "scheduledtask-system-principal",
    "schtask-runlevel-highest", "schtask-trigger-at-startup",
)}
ACL = {"micro-behaviors/fs/acl::icacls-grant-command",
       "micro-behaviors/fs/acl::icacls-inheritance-command"}
FIREWALL = {"micro-behaviors/os/security/firewall::new-netfirewallrule",
            "micro-behaviors/os/security/firewall::get-netfirewallrule"}
ATTACK = {
    "objectives/command-and-control/backdoor/dispatch/eval::scheduled-socket-command-backdoor-attempt",
    "objectives/persistence/login/ssh/backdoor::administrator-ssh-key-with-command-backdoor",
    "objectives/persistence/system/service/install::excluded-service-with-command-backdoor",
}
STARTUP = '''
$principal = New-ScheduledTaskPrincipal -UserID "SYSTEM" -LogonType ServiceAccount -RunLevel Highest
$action = New-ScheduledTaskAction -Execute 'Powershell.exe' -Argument '-NoProfile -File C:\\Tools\\maintenance.ps1'
$trigger = New-ScheduledTaskTrigger -AtStartup
Register-ScheduledTask -Action $action -Trigger $trigger -Principal $principal -TaskName 'Maintenance'
'''


def scan(path):
    result = subprocess.run(
        [os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(ROOT),
         "--format", "json", str(path)], capture_output=True, text=True,
    )
    assert result.returncode == 0, result.stderr
    report = json.loads(result.stdout)
    return {t["id"]: t for f in report["files"] for t in f.get("traits", [])}


def check(label, traits, required=(), forbidden=(), benign=False):
    assert set(required) <= traits.keys(), (label, set(required) - traits.keys())
    assert not (set(forbidden) | {OLD}) & traits.keys(), label
    if benign:
        assert not any(t["crit"] >= 4 for t in traits.values()), label
    if NEW in traits:
        assert traits[NEW]["crit"] == 3, label
    print("PASS", label)


with tempfile.TemporaryDirectory(prefix=".ddtrace-controls-", dir=ROOT) as temporary:
    directory = Path(temporary)
    # Rename the real upstream provisioning fixture to exclude path-based effects.
    real = directory / "renamed.ps1"
    real.write_bytes((HERE / "ec2-ssh.ps1").read_bytes())
    check("upstream EC2 SSH provisioning", scan(real), ATOMS | ACL | FIREWALL | {NEW}, benign=True)

    cases = {
        "maintenance": (STARTUP, True),
        "no-startup": (STARTUP.replace("-AtStartup", "-Daily -At 12:00"), False),
        "no-highest": (STARTUP.replace("-RunLevel Highest", "-RunLevel Limited"), False),
        "no-system": (STARTUP.replace('"SYSTEM"', '"RegularUser"'), False),
        "no-registration": ("\n".join(line for line in STARTUP.splitlines()
                                       if not line.startswith("Register-ScheduledTask")), False),
    }
    for name, (source, matches) in cases.items():
        path = directory / (name + ".ps1")
        path.write_text(source)
        check(name, scan(path), {NEW} if matches else (), () if matches else {NEW}, benign=True)

    near = directory / "reference-only.ps1"
    near.write_text('''
# icacls.exe $path /grant "Administrators:F" /inheritance:r
$help = "New-NetFirewallRule -Name Example"
$query = "Get-NetFirewallRule -Name Example"
icacls.exe $path
''')
    check("ACL display and firewall references", scan(near), forbidden=ACL | FIREWALL, benign=True)

    attack_source = (ROOT / "testdata/taxonomy/concealed-task-resource-review/concealed-task-key-service.ps1").read_text()
    for name, source, required in (
        ("existing concealed backdoor", attack_source, ATTACK),
        ("backdoor with privileged boot task", attack_source + STARTUP, ATTACK | ATOMS | {NEW}),
    ):
        path = directory / (name.replace(" ", "-") + ".ps1")
        path.write_text(source)
        check(name, scan(path), required)
