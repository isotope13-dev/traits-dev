"""Require store disable, APK install, and restore for the hostile bypass."""

import json
import os
from pathlib import Path
import subprocess
from contextlib import nullcontext


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
EVASION = "objectives/evasion/anti-av/platform/play-protect::android-store-disable-install-restore"
INSTALL = "objectives/execution/payload/file-exec::store-disabled-apk-session-install"
DISABLE = "micro-behaviors/os/package-manager/management::android-play-store-disable-command"
RESTORE = "micro-behaviors/os/package-manager/management::android-play-store-enable-command"
BASE = (HERE / "user-scoped-install.java").read_text()
DISABLE_LINE = next(line for line in BASE.splitlines(True) if '"cmd package disable-user' in line)
RESTORE_LINE = next(line for line in BASE.splitlines(True) if '"cmd package enable' in line)
STAGING = BASE[BASE.index("        PackageInstaller pi"):BASE.index("    void onInstallResult")]

# Each expectation is (full bypass, launched disable, launched restore).
cases = {
    "original": (BASE, (True, True, True)),
    "pm": (BASE.replace("cmd package", "pm"), (True, True, True)),
    "current-user": (BASE.replace("--user 0", "--user current"), (True, True, True)),
    "another-user": (BASE.replace("--user 0", "--user 10"), (True, True, True)),
    "absolute-shell": (BASE.replace('"sh"', '"/bin/sh"'), (True, True, True)),
    "multiline": (BASE.replace("ProcessBuilder(", "ProcessBuilder (\n            ")
                  .replace(", \"-c\", ", ",\n            \"-c\",\n            ")
                  .replace(".start()", ". start ()")
                  .replace(".openWrite(", ". openWrite (\n            ")
                  .replace(".commit(", ". commit ("), (True, True, True)),
    "renamed": (BASE.replace("StageInstaller", "PackageUpdater")
                .replace("session", "transaction").replace("base.apk", "update.apk"),
                (True, True, True)),
    "same-line-commit": (BASE.replace("\n        session.commit", " session.commit"),
                         (True, True, True)),
    "no-disable": (BASE.replace(DISABLE_LINE, ""), (False, False, True)),
    "no-restore": (BASE.replace(RESTORE_LINE, ""), (False, True, False)),
    "no-commit": (BASE.replace("        session.commit(callback);\n", ""), (False, True, True)),
    "commented-commit": (BASE.replace("session.commit(callback);", "// session.commit(callback);"),
                         (False, True, True)),
    "no-install": (BASE.replace(STAGING, "    }\n"), (False, True, True)),
    "commented-install": (BASE.replace(STAGING, "        /*\n" + STAGING[:-6] + "        */\n    }\n"),
                          (False, True, True)),
    "commented-disable": (BASE.replace(DISABLE_LINE, "        // " + DISABLE_LINE.lstrip()),
                          (False, False, True)),
    "commented-restore": (BASE.replace(RESTORE_LINE, "        // " + RESTORE_LINE.lstrip()),
                          (False, True, False)),
    "other-package": (BASE.replace("com.android.vending", "org.example.app"), (False, False, False)),
    "unlaunched-disable": (BASE.replace(DISABLE_LINE, DISABLE_LINE.split(".start()")[0] + ";\n"),
                           (False, False, True)),
    "echoed-disable": (BASE.replace('"sh", "-c", "cmd package disable',
                                   '"echo", "-c", "cmd package disable'), (False, False, True)),
    "echoed-restore": (BASE.replace('"sh", "-c", "cmd package enable',
                                   '"echo", "-c", "cmd package enable'), (False, True, False)),
    "unrelated-disable-literal": (
        BASE.replace(DISABLE_LINE,
                     '        String help = "cmd package disable-user --user 0 com.android.vending";\n'
                     '        new ProcessBuilder("sh", "-c", "pm disable org.example.app").start();\n'),
        (False, False, True)),
    "disable-only": ('class Admin { void freeze() throws Exception {\n' + DISABLE_LINE + '} }\n',
                     (False, True, False)),
}

cases["complete-kotlin"] = ('''import android.content.Context
import android.content.IntentSender
import android.content.pm.PackageInstaller
import java.io.InputStream

class PackageUpdater {
    fun install(context: Context, apk: InputStream, callback: IntentSender) {
        ProcessBuilder("sh", "-c", "cmd package disable-user --user 0 com.android.vending").start().waitFor()
        val pi = context.packageManager.packageInstaller
        val params = PackageInstaller.SessionParams(PackageInstaller.SessionParams.MODE_FULL_INSTALL)
        val session: PackageInstaller.Session = pi.openSession(pi.createSession(params))
        session.openWrite("update.apk", 0, -1).use { out ->
            apk.copyTo(out)
            session.fsync(out)
        }
        session.commit(callback)
    }
    fun onInstallResult() {
        ProcessBuilder("sh", "-c", "cmd package enable --user 0 com.android.vending").start().waitFor()
    }
}
''', (True, True, True))

# Equivalent command vectors retain the same Android operation across JVM
# source languages; executable/package arguments must belong to the builder.
PM = BASE.replace('"sh", "-c", "cmd package disable-user --user 0 com.android.vending"',
                  '"pm", "disable", "com.android.vending"').replace(
                  '"sh", "-c", "cmd package enable --user 0 com.android.vending"',
                  '"pm", "enable", "com.android.vending"')
CMD = PM.replace('"pm", "disable"', '"cmd", "package", "disable"').replace(
                 '"pm", "enable"', '"cmd", "package", "enable"')
for name, source in (("pm-argv", PM), ("cmd-argv", CMD),
                     ("absolute-pm-argv", PM.replace('"pm"', '"/system/bin/pm"')),
                     ("absolute-cmd-argv", CMD.replace('"cmd"', '"/system/bin/cmd"')),
                     ("renamed-argv", PM.replace("StageInstaller", "SystemUpdater")
                                        .replace("session", "transaction")
                                        .replace("base.apk", "partner.apk"))):
    cases[name] = (source, (True, True, True))
    cases[name + "-other-package"] = (source.replace("com.android.vending", "org.example.store"),
                                       (False, False, False))
    cases[name + "-unstarted"] = (source.replace(".start().waitFor()", ""), (False, False, False))

kotlin = cases["complete-kotlin"][0]
cases["pm-argv-kotlin"] = (kotlin.replace(
    '"sh", "-c", "cmd package disable-user --user 0 com.android.vending"',
    '"pm", "disable", "com.android.vending"').replace(
    '"sh", "-c", "cmd package enable --user 0 com.android.vending"',
    '"pm", "enable", "com.android.vending"'), (True, True, True))
cases["cmd-argv-kotlin"] = (cases["pm-argv-kotlin"][0].replace(
    '"pm", "disable"', '"cmd", "package", "disable"').replace(
    '"pm", "enable"', '"cmd", "package", "enable"'), (True, True, True))

for name in ("pm-argv-kotlin", "cmd-argv-kotlin"):
    src = cases[name][0]
    disable_line = next(line for line in src.splitlines(True) if '"disable"' in line)
    cases["commented-" + name] = (src.replace(disable_line,
        "        // " + disable_line.lstrip() +
        '        ProcessBuilder("echo", "maintenance").start().waitFor()\n'),
        (False, False, True))
    cases["ordinary-" + name] = (src.replace(disable_line, ""), (False, False, True))

ATTRIBUTION = "objectives/evasion/masquerade/identity/installer::android-play-store-installer-masquerade"
ATTRIBUTION_CALL = "micro-behaviors/os/package-manager/management::android-play-installer-attribution-call"
setter = '        params.setInstallerPackageName("com.android.vending");\n'
with_attribution = PM.replace("        int id =", setter + "        int id =")
cases["play-attribution"] = (with_attribution, (True, True, True))
cases["other-attribution"] = (with_attribution.replace(
    'setInstallerPackageName("com.android.vending")',
    'setInstallerPackageName("org.example.store")'), (True, True, True))
cases["commented-attribution"] = (with_attribution.replace(setter, "        // " + setter.lstrip()),
                                    (True, True, True))
cases["ordinary-attribution"] = (with_attribution.replace(
    next(line for line in with_attribution.splitlines(True) if '"disable"' in line), ""),
    (False, False, True))

# Keep the pre-existing controls in the same gate.
for filename in ("install.java", "ordinary-install.java", "comment.java", "other-package.java",
                 "user-scoped-comment.java", "user-scoped-other-package.java"):
    text = (HERE / filename).read_text()
    cases[Path(filename).stem] = (text, {
        "install.java": (True, True, True),
        "ordinary-install.java": (False, False, True),
        "comment.java": (False, False, True),
        "other-package.java": (False, False, False),
        "user-scoped-comment.java": (False, False, True),
        "user-scoped-other-package.java": (False, False, False),
    }[filename])

# Keep benign controls in Cleave's fixtures, outside feed retrieval data.
fixture_root = Path(os.environ.get("CLEAVE_FIXTURES", "/usr/local/var/cyclotron/cleave/tests/fixtures"))
fixture_root.mkdir(parents=True, exist_ok=True)
fixture_dir = fixture_root / "midnight-mimosa-store-suppression"
fixture_dir.mkdir(exist_ok=True)
with nullcontext(str(fixture_dir)) as directory:
    paths = []
    for name, (source, _) in cases.items():
        path = Path(directory) / (name + (".kt" if name.endswith("-kotlin") else ".java"))
        path.write_text(source)
        paths.append(str(path))
    result = subprocess.run(
        [os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(ROOT), "--format", "jsonl", *paths],
        capture_output=True, text=True, check=False,
    )
    if result.returncode:
        raise RuntimeError(result.stderr)
    reports = {
        Path(f["path"]).stem: f
        for line in result.stdout.splitlines()
        for f in json.loads(line)["files"]
    }
    assert reports.keys() == cases.keys(), reports.keys()
    for name, (_, (bypass, disable, restore)) in cases.items():
        traits = {t["id"]: t["crit"] for t in reports[name].get("traits", [])}
        attribution = name == "play-attribution"
        bypass = bypass and attribution
        for trait, expected in ((EVASION, bypass), (INSTALL, False), (DISABLE, disable), (RESTORE, restore)):
            assert (trait in traits) == expected, (name, trait, expected, traits)
            if trait in traits:
                assert traits[trait] == (5 if trait in (EVASION, INSTALL) else (4 if trait == DISABLE else 3)), (name, traits)
        attribution = name == "play-attribution"
        assert (ATTRIBUTION in traits) == attribution, (name, traits)
        assert (ATTRIBUTION_CALL in traits) == (name in {"play-attribution", "ordinary-attribution"}), (name, traits)
        assert {t for t, c in traits.items() if c >= 4} == (({EVASION} if bypass else set()) | ({DISABLE} if disable else set()) | ({ATTRIBUTION} if attribution else set())), (name, traits)

print(f"Passed {len(cases)} store disable/install/restore controls")
