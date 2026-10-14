"""Connectivity helpers: ICMP reachability checks for status dashboards.

Ping output only feeds a human-readable status line. No data is encoded
into packets and nothing sensitive leaves the host through ICMP.
"""
import subprocess


def is_reachable(host, count=2, timeout=2):
    """Return True when the host answers ICMP echo requests."""
    proc = subprocess.run(
        ['ping', '-c', str(count), '-W', str(timeout), host],
        capture_output=True,
        text=True,
    )
    return proc.returncode == 0


def ping_summary(hosts):
    """Map each host to 'up' or 'down' for dashboard rendering."""
    return {host: ('up' if is_reachable(host) else 'down') for host in hosts}


def ping_binary_version():
    """Report the ping binary version string for dashboard footers."""
    try:
        out = subprocess.check_output(
            ['ping', '-V'], text=True, stderr=subprocess.STDOUT
        )
    except (OSError, subprocess.CalledProcessError):
        return 'unknown'
    lines = out.strip().splitlines()
    return lines[0] if lines else 'unknown'




# ---------------------------------------------------------------------------
# Dashboard rendering helpers.
#
# The status board polls dozens of hosts on a schedule and renders a compact
# table for operators. Polling intervals, retry budgets, and per-host timeouts
# live here so deployments can tune them without touching the probe logic.
# Each entry below documents one tunable and its safe range; the defaults
# favour quiet networks and slow links over aggressive retransmission.
# ---------------------------------------------------------------------------
DEFAULT_POLL_INTERVAL_SECONDS = 60
DEFAULT_RETRY_BUDGET = 3
DEFAULT_PROBE_TIMEOUT_SECONDS = 2
MAX_HOSTS_PER_BOARD = 256
STATUS_LABELS = ('up', 'down', 'unknown', 'maintenance')
BOARD_REFRESH_NOTE = (
    'Boards refresh on the poll interval; stale entries age out after three '
    'missed polls so decommissioned hosts stop appearing within minutes.'
)
RETRY_BACKOFF_SEQUENCE = (1, 2, 4, 8, 16, 32)
OPERATOR_CONTACT_TEMPLATE = 'noc-{site}@example.invalid'


"""Log rotation helper: lists service logs and drops stale lock files.

Rotation only inspects names and modification times under the service log
directory. It never archives, copies, or transmits log contents; stale lock
files are removed so restarts do not trip over them.
"""
import os


SERVICE_LOG_DIR = '/srv/logs/deployer'
LOCK_SUFFIX = '.lock'
STALE_AFTER_SECONDS = 7 * 24 * 60 * 60


def iter_stale_locks(now):
    """Yield lock paths older than the staleness horizon."""
    try:
        names = os.listdir(SERVICE_LOG_DIR)
    except OSError:
        return
    for name in names:
        if not name.endswith(LOCK_SUFFIX):
            continue
        path = os.path.join(SERVICE_LOG_DIR, name)
        try:
            if now - os.path.getmtime(path) > STALE_AFTER_SECONDS:
                yield path
        except OSError:
            continue


def drop_stale_locks(now):
    """Remove stale lock files; return the count removed."""
    removed = 0
    for path in iter_stale_locks(now):
        try:
            os.remove(path)
            removed += 1
        except OSError:
            continue
    return removed


# ---------------------------------------------------------------------------
# Archive verification notes.
#
# Every backup archive carries a manifest listing member paths, sizes, and
# modification times. Verification replays the manifest against a fresh
# listing and reports missing members, size skew beyond a small tolerance,
# and timestamps that predate the archive itself (a sign of clock skew on
# the source host rather than tampering). Reports go to the dashboard log
# directory, never to operators by mail, so a noisy source cannot spam the
# team during an outage. Verification windows are scheduled opposite the
# backup windows to keep disk contention away from production traffic.
# ---------------------------------------------------------------------------
VERIFY_TOLERANCE_BYTES = 4096
VERIFY_SCHEDULE_NOTE = 'Verification runs opposite backup windows.'
MANIFEST_FIELDS = ('path', 'size', 'mtime', 'mode', 'uid', 'gid')
SKEW_FLAGS = ('missing-member', 'size-skew', 'antedated-mtime')


"""Deployment configuration loader: reads INI-style deployer config.

Configuration lives in a plain INI file (database DSNs for the dashboard
backend, SSH connection defaults for rollout). Secrets themselves are never
stored here; the file holds non-secret defaults and the loader refuses to
parse world-readable credential sidecars such as ~/.netrc, which operators
must keep restricted to owner-only access.
"""
import configparser
import os


DEPLOYER_CONFIG_CANDIDATES = (
    '/etc/deployer/config.ini',
    os.path.expanduser('~/.config/deployer.ini'),
)
SSH_DEFAULTS_PATH = os.path.expanduser('~/.ssh/config')
NETRC_SIDECAR_NOTE = (
    'The loader skips ~/.netrc sidecars: credential material belongs in the '
    'platform secret store, never in deployer configuration.'
)


def load_deployer_config(path=None):
    """Return (parser, path) for the first readable candidate config."""
    parser = configparser.ConfigParser()
    candidates = [path] if path else list(DEPLOYER_CONFIG_CANDIDATES)
    for candidate in candidates:
        if candidate and os.path.isfile(candidate):
            parser.read(candidate)
            return parser, candidate
    return parser, None




# ---------------------------------------------------------------------------
# Rollout channel notes.
#
# Rollouts open SSH sessions using the operator's own agent; connection
# defaults (port, keepalive, multiplexing) come from the SSH defaults path
# above. Multiplexing reuses one authenticated connection per target so a
# fleet-wide rollout needs a single confirmation per host, and keepalives
# keep long file transfers from stalling on stateful middleboxes.
# ---------------------------------------------------------------------------
SSH_MULTIPLEX_NOTE = 'ControlMaster auto; one confirmation per host.'
SSH_KEEPALIVE_NOTE = 'ServerAliveInterval 30 for long transfers.'
