#!/bin/bash
if [[ "${GRANT_SUDO}" == "1" || "${GRANT_SUDO}" == "yes" ]]; then
    echo "${NB_USER} ALL=(ALL) NOPASSWD:ALL" >/etc/sudoers.d/notebook
fi
