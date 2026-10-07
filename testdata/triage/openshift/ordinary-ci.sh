#!/bin/bash
curl -fO https://raw.githubusercontent.com/example/project/refs/heads/main/helper.sh
chmod +x helper.sh
./helper.sh
export PATH=$HOME/.tools/bin:$PATH
cat > capture.yaml <<'YAML'
apiVersion: apps/v1
kind: DaemonSet
spec:
  template:
    spec:
      containers:
      - command: ["chroot", "/host", "tcpdump"]
        securityContext:
          privileged: true
      volumes:
      - hostPath:
          path: /
YAML
chroot /host tcpdump -i eth0
