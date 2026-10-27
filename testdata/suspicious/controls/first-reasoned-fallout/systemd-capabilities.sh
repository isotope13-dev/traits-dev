cat <<EOF > /etc/systemd/system/demo.service
[Service]
CapabilityBoundingSet=CAP_SYS_PTRACE CAP_DAC_OVERRIDE
AmbientCapabilities=CAP_SYS_PTRACE CAP_DAC_OVERRIDE
EOF
