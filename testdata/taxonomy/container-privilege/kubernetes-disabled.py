manifest = {
    "metadata": {"namespace": "kube-system"},
    "spec": {"containers": [{"securityContext": {"privileged": False}}],
             "volumes": [{"hostPath": {"path": "/"}}]},
}
url = "/api/v1/namespaces/kube-system/pods"
