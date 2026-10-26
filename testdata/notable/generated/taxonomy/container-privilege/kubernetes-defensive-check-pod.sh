#!/bin/bash
# Defensive cluster-audit harness: spins up a transient hardened pod to
# collect host evidence, then tears it down. Exercises the same pod-spec
# markers as a privileged host-root escape without the attack intent.
set -euo pipefail
CHECK_NS="audit-checks"
CHECK_POD="audit-host-check-$$"
cleanup_check_pod() {
    kubectl delete pod "$CHECK_POD" -n "$CHECK_NS" --ignore-not-found=true --wait=false >/dev/null 2>&1 || true
}
trap cleanup_check_pod EXIT
kubectl apply --request-timeout=60s -f - >/dev/null <<EOF
apiVersion: v1
kind: Pod
metadata:
  name: ${CHECK_POD}
  namespace: ${CHECK_NS}
spec:
  automountServiceAccountToken: false
  restartPolicy: Never
  activeDeadlineSeconds: 600
  containers:
  - name: check
    image: ubuntu:24.04
    command: ["sleep", "480"]
    securityContext:
      privileged: true
    volumeMounts:
    - name: host-root
      mountPath: /host
  volumes:
  - name: host-root
    hostPath:
      path: /
      type: Directory
EOF
kubectl exec -i -n "$CHECK_NS" "$CHECK_POD" -- chroot /host bash -s <<'INNER'
sha256sum /etc/os-release
INNER
