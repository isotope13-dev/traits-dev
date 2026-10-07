#!/bin/bash
sfdisk --delete "$node_dev"
dd if=/dev/zero of="$node_dev"
cat > lvm.yaml <<'YAML'
apiVersion: lvm.topolvm.io/v1alpha1
kind: LVMCluster
YAML
