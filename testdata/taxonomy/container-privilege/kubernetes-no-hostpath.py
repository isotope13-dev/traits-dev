manifest = {
    "metadata": {"namespace": "kube-system"},
    "spec": {"containers": [{"securityContext": {"privileged": True}}],
             "volumes": [{"emptyDir": {}}]},
}
url = "/api/v1/namespaces/kube-system/pods"
