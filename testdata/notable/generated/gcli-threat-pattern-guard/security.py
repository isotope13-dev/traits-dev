"""Security enhancements for gcli remote access tool."""

import collections
import hashlib
import json
import logging
import os
import re
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger("gcli.security")

COMMAND_LIMITS: Dict[str, int] = {
    "exec": 100,
    "upload": 10,
    "download": 10,
    "default": 100,
}

THREAT_PATTERNS: List[re.Pattern] = [
    re.compile(r"rm\s+-[a-zA-Z]*r[a-zA-Z]*f[a-zA-Z]*\s+/\s*(\s|$)", re.IGNORECASE),
    re.compile(r"format\s+[cC]:", re.IGNORECASE),
    re.compile(r":\(\)\{\s*:.*&.*\};:", re.IGNORECASE),
    re.compile(r"\|\s*(python|perl|ruby|node|bash|sh|cmd)\s+-c\b", re.IGNORECASE),
    re.compile(r"\|\s*eval\b", re.IGNORECASE),
    re.compile(r"(;\s*(DROP|DELETE|UPDATE|INSERT|ALTER)\s+)", re.IGNORECASE),
    re.compile(r"'\s*(OR|AND)\s+['\"]?\d+['\"]?\s*=\s*['\"]?\d+", re.IGNORECASE),
]


class SecurityManager:
    def __init__(self, audit_dir: Optional[Path] = None) -> None:
        self._rate_windows: Dict[str, Dict[str, List[float]]] = collections.defaultdict(
            lambda: collections.defaultdict(list)
        )
        self._audit_log: collections.deque = collections.deque(maxlen=1000)
        self._audit_file: Path = audit_dir or Path.home() / ".gcli"
        self._audit_log_path = self._audit_file / "audit.log"
        self._session_locked = False
        self._session_lock_reason: Optional[str] = None
        self._rotation_old_keys: Dict[str, float] = {}
        self._current_session_key: str = self._generate_session_key()

    @staticmethod
    def _generate_session_key() -> str:
        return hashlib.sha256(os.urandom(32)).hexdigest()

    @staticmethod
    def _now() -> float:
        return time.time()

    def _check_session_locked(self, payload: dict) -> Optional[dict]:
        if self._session_locked and payload.get("type") != "unlock_session":
            return {"ok": False, "locked": True, "reason": self._session_lock_reason}
        return None

    def _sliding_window_count(self, client_id: str, command_type: str) -> int:
        window = self._rate_windows[client_id][command_type]
        cutoff = self._now() - 60
        self._rate_windows[client_id][command_type] = [t for t in window if t > cutoff]
        return len(self._rate_windows[client_id][command_type])

    def _append_audit(self, entry: dict) -> None:
        self._audit_log.append(entry)
        try:
            self._audit_file.mkdir(parents=True, exist_ok=True)
            with open(self._audit_log_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(entry, default=str) + "\n")
        except OSError as e:
            logger.warning("Failed to write audit log file: %s", e)

    def handle_rate_check(self, payload: dict) -> dict:
        client_id = payload.get("client_id", "")
        command = payload.get("command", "default")
        limit = COMMAND_LIMITS.get(command, COMMAND_LIMITS["default"])
        count = self._sliding_window_count(client_id, command)
        allowed = count < limit
        if allowed:
            self._rate_windows[client_id][command].append(self._now())
        remaining = max(0, limit - count - (1 if allowed else 0))
        return {
            "ok": True,
            "allowed": allowed,
            "remaining": remaining,
            "reset_in": 60,
        }

    def handle_audit_log(self, payload: dict) -> dict:
        entry = {
            "timestamp": self._now(),
            "client_id": payload.get("client_id"),
            "action": payload.get("action"),
            "command": payload.get("command"),
            "result": payload.get("result"),
        }
        self._append_audit(entry)
        return {"ok": True, "logged": True}

    def handle_get_audit_log(self, payload: dict) -> dict:
        limit = payload.get("limit", 50)
        filter_client = payload.get("filter_client")
        log_list = list(self._audit_log)
        if filter_client:
            log_list = [e for e in log_list if e.get("client_id") == filter_client]
        log_list = log_list[-limit:]
        return {"ok": True, "entries": log_list, "total": len(log_list)}

    def handle_clear_audit_log(self, _payload: dict) -> dict:
        self._audit_log.clear()
        try:
            if self._audit_log_path.exists():
                self._audit_log_path.unlink()
        except OSError as e:
            logger.warning("Failed to remove audit log file: %s", e)
        return {"ok": True, "cleared": True}

    def handle_rotate_key(self, payload: dict) -> dict:
        old_key = self._current_session_key
        new_key = self._generate_session_key()
        self._rotation_old_keys[old_key] = self._now() + 60
        self._current_session_key = new_key
        return {
            "ok": True,
            "new_session_key": new_key,
            "old_key_valid_until": self._rotation_old_keys[old_key],
            "hint": payload.get("new_password_hint"),
        }

    def handle_threat_check(self, payload: dict) -> dict:
        command = payload.get("command", "")
        for pattern in THREAT_PATTERNS:
            if pattern.search(command):
                return {
                    "ok": True,
                    "threat_level": "high",
                    "reason": f"Suspicious pattern detected: {pattern.pattern}",
                }
        return {"ok": True, "threat_level": "none", "reason": ""}

    def handle_lock_session(self, payload: dict) -> dict:
        self._session_locked = True
        self._session_lock_reason = payload.get("reason", "manual")
        return {"ok": True, "locked": True, "reason": self._session_lock_reason}

    def handle_unlock_session(self, _payload: dict) -> dict:
        self._session_locked = False
        self._session_lock_reason = None
        return {"ok": True, "locked": False}

    def dispatch(self, payload: dict) -> dict:
        locked = self._check_session_locked(payload)
        if locked is not None:
            return locked

        handlers = {
            "rate_check": self.handle_rate_check,
            "audit_log": self.handle_audit_log,
            "get_audit_log": self.handle_get_audit_log,
            "clear_audit_log": self.handle_clear_audit_log,
            "rotate_key": self.handle_rotate_key,
            "threat_check": self.handle_threat_check,
            "lock_session": self.handle_lock_session,
            "unlock_session": self.handle_unlock_session,
        }
        msg_type = payload.get("type")
        handler = handlers.get(msg_type)
        if handler is None:
            return {"ok": False, "error": f"Unknown command type: {msg_type}"}
        return handler(payload)

    def is_key_valid(self, key: str) -> bool:
        if key == self._current_session_key:
            return True
        expiry = self._rotation_old_keys.get(key)
        if expiry is None:
            return False
        if self._now() > expiry:
            self._rotation_old_keys.pop(key, None)
            return False
        return True

    def test_security(self) -> bool:
        sm = SecurityManager()
        r = sm.dispatch({"type": "rate_check", "client_id": "c1", "command": "exec"})
        assert r["ok"] and r["allowed"], f"rate_check failed: {r}"

        r = sm.dispatch({"type": "audit_log", "action": "exec", "client_id": "c1", "command": "whoami", "result": "ok"})
        assert r["ok"] and r["logged"], f"audit_log failed: {r}"

        r = sm.dispatch({"type": "get_audit_log", "limit": 50})
        assert r["ok"] and len(r["entries"]) == 1, f"get_audit_log failed: {r}"

        r = sm.dispatch({"type": "threat_check", "command": "cat file | python -c 'import os; os.system(\"rm -rf /\")'"})
        assert r["ok"] and r["threat_level"] == "high", f"threat_check pipe failed: {r}"

        r = sm.dispatch({"type": "threat_check", "command": "rm -rf /"})
        assert r["ok"] and r["threat_level"] == "high", f"threat_check rm failed: {r}"

        r = sm.dispatch({"type": "threat_check", "command": "format c:"})
        assert r["ok"] and r["threat_level"] == "high", f"threat_check format failed: {r}"

        r = sm.dispatch({"type": "threat_check", "command": ":(){ :|:& };:"})
        assert r["ok"] and r["threat_level"] == "high", f"threat_check fork bomb failed: {r}"

        r = sm.dispatch({"type": "threat_check", "command": "cat file"})
        assert r["ok"] and r["threat_level"] == "none", f"threat_check clean cmd failed: {r}"

        old_key = sm._current_session_key
        r = sm.dispatch({"type": "rotate_key", "new_password_hint": "test"})
        assert r["ok"] and r["new_session_key"] != old_key, f"rotate_key failed: {r}"
        assert sm.is_key_valid(old_key), "old key should still be valid"
        assert sm.is_key_valid(r["new_session_key"]), "new key should be valid"

        r = sm.dispatch({"type": "lock_session", "reason": "test"})
        assert r["ok"] and r["locked"], f"lock_session failed: {r}"

        r = sm.dispatch({"type": "rate_check", "client_id": "c1", "command": "exec"})
        assert not r["ok"] and r["locked"], f"should be blocked when locked: {r}"

        r = sm.dispatch({"type": "unlock_session"})
        assert r["ok"] and not r["locked"], f"unlock_session failed: {r}"

        r = sm.dispatch({"type": "rate_check", "client_id": "c1", "command": "exec"})
        assert r["ok"], f"should work after unlock: {r}"

        r = sm.dispatch({"type": "clear_audit_log"})
        assert r["ok"] and r["cleared"], f"clear_audit_log failed: {r}"

        for i in range(11):
            sm.dispatch({"type": "rate_check", "client_id": "lim", "command": "upload"})
        r = sm.dispatch({"type": "rate_check", "client_id": "lim", "command": "upload"})
        assert r["ok"] and not r["allowed"], f"rate limit upload failed: {r}"

        r = sm.dispatch({"type": "unknown_command"})
        assert not r["ok"], f"unknown command should fail: {r}"

        return True


if __name__ == "__main__":
    sm = SecurityManager()
    sm.test_security()
    print("All security tests passed.")


# ---------------------------------------------------------------------------
# Module-level dispatch (called by host._dispatch_module)
# ---------------------------------------------------------------------------

_manager: Optional["SecurityManager"] = None


def _get_manager() -> "SecurityManager":
    global _manager
    if _manager is None:
        _manager = SecurityManager()
    return _manager


def dispatch(payload: dict) -> dict:
    """Route a security command payload to SecurityManager.dispatch().

    >>> dispatch({"type": "threat_check", "command": "ls"})["ok"]
    True
    """
    return _get_manager().dispatch(payload)
