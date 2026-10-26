# -*- coding: utf-8 -*-
"""vetter_rules.py — 与 yotta-security-audit/scripts/audit_rules.py 的同步副本（勿手改）。

本文件由 YottaSkills 仓库 tools/sync-vetter-rules.py 自动生成；
修改规则请改 yotta-security-audit/scripts/audit_rules.py，然后重新运行同步。
"""


import re
from collections import namedtuple

# 单条规则：规则号 / 检测器名 / 严重级 / 正则源码 / 描述 / 置信度(0-100)
Rule = namedtuple("Rule", ["id", "detector", "severity", "pattern", "description", "confidence"])

MAX_LINE_LEN = 500

# 严重级从低到高（用于排序与 exit code 语义：0=干净/仅 low，1=medium，2=high，3=critical，4=错误）
SEVERITY_ORDER = ("info", "low", "medium", "high", "critical")

# 严重级 → 数值（exit code 语义）
SEVERITY_VALUE = {"info": 0, "low": 0, "medium": 1, "high": 2, "critical": 3}

PATTERN_RULES = [
    # ── DownloadExec 下载即执行 ───────────────────────────────────────────
    Rule("DEX-001", "DownloadExec", "critical",
         r"(?i)\bcurl\b[^\n|;]{0,120}\|\s*(?:ba)?sh\b",
         "curl 下载内容通过管道交给 shell 执行", 95),
    Rule("DEX-002", "DownloadExec", "critical",
         r"(?i)\bwget\b[^\n|;]{0,120}\|\s*(?:ba)?sh\b",
         "wget 下载内容通过管道交给 shell 执行", 95),
