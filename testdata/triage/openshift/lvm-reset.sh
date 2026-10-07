#!/bin/bash
sfdisk --delete "$node_dev"
dd if=/dev/zero of="$node_dev" bs=1M count=1
cat > lvm.yaml <<'YAML'
apiVersion: lvm.topolvm.io/v1alpha1
kind: LVMCluster
YAML
