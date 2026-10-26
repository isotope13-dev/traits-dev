FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y dokku \
  && rm -rf /var/lib/apt/lists/* \
  && rm -f /var/log/btmp /var/log/wtmp /var/log/*log /var/log/apt/*
