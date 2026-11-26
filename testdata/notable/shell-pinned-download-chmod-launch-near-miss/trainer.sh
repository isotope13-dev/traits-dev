#!/usr/bin/env bash
# Near-miss fixture: curl --resolve, wget -O, and chmod +x appear in the same
# file (>30 lines apart) without forming a download-chmod-launch sequence.
questions+=("Override DNS for updates.example.test -> 192.0.2.10|curl --resolve updates.example.test:443:192.0.2.10 https://updates.example.test/tool")

# Unrelated filler lines separating the quiz string from local sandbox setup.
msg_01="step 1"
msg_02="step 2"
msg_03="step 3"
msg_04="step 4"
msg_05="step 5"
msg_06="step 6"
msg_07="step 7"
msg_08="step 8"
msg_09="step 9"
msg_10="step 10"
msg_11="step 11"
msg_12="step 12"
msg_13="step 13"
msg_14="step 14"
msg_15="step 15"
msg_16="step 16"
msg_17="step 17"
msg_18="step 18"
msg_19="step 19"
msg_20="step 20"
msg_21="step 21"
msg_22="step 22"
msg_23="step 23"
msg_24="step 24"
msg_25="step 25"
msg_26="step 26"
msg_27="step 27"
msg_28="step 28"
msg_29="step 29"
msg_30="step 30"
msg_31="step 31"
msg_32="step 32"

curl -o output.html https://docs.example.test/index.html
dir=$(mktemp -d)
printf '%s\n' '#!/bin/bash' 'echo "done"' > "$dir/backup.sh"
chmod +x "$dir/backup.sh"
