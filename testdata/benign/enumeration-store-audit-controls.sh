#!/bin/sh
# Enumeration-script control: a distant file read and directory traversal
# must not convict a later browser-store readability audit as credential
# collection. The store path, the read, and the traversal below are
# deliberately more than one routine apart.

print_section() {
  printf '\n[+] %s\n' "$1"
}

print_section "world-writable log sweep"
find /var/log -xdev -type f -perm -0002 -print 2>/dev/null | head -n 50
kernel_release=$(cat /proc/version 2>/dev/null | head -c 200)
printf 'kernel: %s\n' "$kernel_release"
open_ports=$(cat /proc/net/tcp 2>/dev/null | wc -l)
printf 'tcp lines: %s\n' "$open_ports"

# --- filler: ordinary enumeration output, several kilobytes below ---
# Host inventory notes. These lines carry no credentials, no network
# endpoints, and no encoded payloads; they exist so the audit block at
# the end of the file sits well outside a single routine's span from
# the traversal and read operations above.
# row 001: checked listening sockets against the expected baseline
# row 002: checked mounted filesystems for nosuid deviations
# row 003: checked running services against the hardened unit list
# row 004: checked kernel modules for out-of-tree taint flags
# row 005: checked sysctl forwarding and core pattern settings
# row 006: checked user accounts with interactive shells configured
# row 007: checked sudoers drop-ins for NOPASSWD wildcard entries
# row 008: checked cron spools and systemd timers for unknown jobs
# row 009: checked container runtimes for privileged socket mounts
# row 010: checked package manager logs for unsigned installs
# row 011: checked bootloader entries for single-user backdoors
# row 012: checked firmware variables for unexpected boot entries
# row 013: checked audit daemon rules for immutable flag coverage
# row 014: checked time sync sources for unauthenticated peers
# row 015: checked name resolution order and stub configurations
# row 016: checked firewall chains for permissive default policies
# row 017: checked open file handles of long-running daemon tasks
# row 018: checked temporary directories for sticky-bit drift
# row 019: checked home directories for world-readable key files
# row 020: checked shell history files for embedded access tokens
# row 021: checked browser profile roots for unexpected extensions
# row 022: checked mail spools for unreadable ownership changes
# row 023: checked backup archives for world-readable permissions
# row 024: checked service logs for repeated authentication faults
# row 025: checked core dump patterns for setuid capture risks
# row 026: checked device nodes for permissive character devices
# row 027: checked kernel keyrings for user-session secret residue
# row 028: checked process environments for exported secret values
# row 029: checked mount namespaces for host path leakages
# row 030: checked control groups for device controller gaps
# row 031: checked seccomp profiles for unconfined service tasks
# row 032: checked capability sets of file capabilities binaries
# row 033: checked login records for impossible travel entries
# row 034: checked accounting logs for after-hours compiler use
# row 035: checked module signatures for verification failures
# row 036: checked disk quotas for runaway world-writable growth
# row 037: checked swap configuration for cleartext spill risks
# row 038: checked hibernation images for stale memory captures
# row 039: checked removable media automount policy settings
# row 040: checked screen lock idle delay enforcement state
# row 041: checked password quality module minimum length rules
# row 042: checked account lockout threshold configuration values
# row 043: checked session timeout profiles for idle disconnects
# row 044: checked banner files for information leakage text
# row 045: checked motd scripts for world-writable components
# row 046: checked profile scripts for suspicious path exports
# row 047: checked dynamic loader cache for unknown library hits
# row 048: checked locale archives for unauthorized replacements
# row 049: checked timezone data for symbolic link integrity
# row 050: checked hostname resolution against inventory records
# row 051: checked interface addresses for unregistered subnets
# row 052: checked neighbor tables for spoofed gateway entries
# row 053: checked routing tables for asymmetric path injections
# row 054: checked packet filters for logging rule presence
# row 055: checked connection tracking table overflow counters
# row 056: checked dns query logs for tunneling label shapes
# row 057: checked proxy variables for unexpected all-caps exports
# row 058: checked certificate stores for unknown authority roots
# row 059: checked keytab files for readable service principals
# row 060: checked ssh client configs for lax host key policies
# row 061: checked authorized key files for options-less entries
# row 062: checked known host files for hashed versus plain rows
# row 063: checked agent sockets for cross-user accessibility
# row 064: checked gpg home directories for trust database drift
# row 065: checked password store directories for group access
# row 066: checked vault agent caches for token file residue
# row 067: checked cloud metadata endpoints for proxy exposure
# row 068: checked instance identity documents for role drift
# row 069: checked container registries for latest-tag pinning
# row 070: checked image layers for embedded secret strings
# row 071: checked orchestration manifests for hostPath volumes
# row 072: checked admission webhooks for fail-open settings
# row 073: checked service accounts for automounted token paths
# row 074: checked role bindings for cluster-admin grants
# row 075: checked network policies for default-deny coverage
# row 076: checked pod security standards for baseline gaps
# row 077: checked secrets encryption provider configuration
# row 078: checked etcd peer urls for plaintext endpoints
# row 079: checked kubelet anonymous auth flag settings
# row 080: checked api server audit log path configuration

print_section "browser extension store readability audit"
for profile in "$HOME/.config/google-chrome/Default" "$HOME/.config/chromium/Default"; do
  extension_settings="$profile/Local Extension Settings"
  if [ -d "$extension_settings" ]; then
    if [ -r "$extension_settings" ]; then
      echo "store readable (path only; contents not inspected): $extension_settings"
    else
      echo "store not readable: $extension_settings"
    fi
  fi
done
