"""Check linked installer/deployment/probe detections without running samples.

Fixtures are parsed, mutated, and statically scanned only. Supply an extracted
wheel directory with --sample-dir, and a fresh temporary --out directory.
"""
import argparse
import ast
import json
import os
from pathlib import Path
import subprocess
import zipfile

ROOT = Path(__file__).resolve().parents[3]
INSTALL = "micro-behaviors/os/package-manager/install::python-wheel-url-install-arguments"
DEPLOY = "micro-behaviors/os/package-manager/runtime-install::python-url-deployment-installs-and-starts-code"
PROBE = "micro-behaviors/process/deploy::python-extracted-archive-probe-execution"
SELECTED = {INSTALL, DEPLOY, PROBE}
LEVELS = {INSTALL: 3, DEPLOY: 4, PROBE: 4}


def functions(source, names):
    tree = ast.parse(source)
    nodes = [node for node in tree.body if isinstance(node, (ast.Import, ast.ImportFrom))
             or isinstance(node, ast.FunctionDef) and node.name in names]
    return ast.unparse(ast.Module(body=nodes, type_ignores=[])) + "\n"


class Rename(ast.NodeTransformer):
    def __init__(self, replacements):
        self.replacements = replacements

    def visit_Name(self, node):
        node.id = self.replacements.get(node.id, node.id)
        return node

    def visit_arg(self, node):
        node.arg = self.replacements.get(node.arg, node.arg)
        return node

    def visit_Attribute(self, node):
        self.generic_visit(node)
        node.attr = self.replacements.get(node.attr, node.attr)
        return node

    def visit_FunctionDef(self, node):
        self.generic_visit(node)
        node.name = self.replacements.get(node.name, node.name)
        return node


def renamed(source, replacements):
    return ast.unparse(Rename(replacements).visit(ast.parse(source))) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sample-dir", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--cleave", default=os.environ.get("CLEAVE", "cleave"))
    args = parser.parse_args()
    inputs = args.out / "inputs"
    inputs.mkdir(parents=True, exist_ok=True)
    worker = (args.sample_dir / "ryry/ryry_widget.py").read_text()
    staging = (args.sample_dir / "ryry/widget_install.py").read_text()
    installer = functions(worker, {"widgetReInstall"})
    deployment = functions(worker, {"widgetReInstall", "UpdateWidgetFromPypi"})
    stage_names = {"_extract", "run_staged_healthcheck", "install_zip", "_install_zip_locked"}
    probe = functions(staging, stage_names)
    cases = []

    def case(name, source, expected):
        ast.parse(source)  # Check fixture syntax, never execute it.
        path = inputs / (name + ".py")
        path.write_text(source)
        cases.append((path, set(expected)))

    def mutate(name, source, old, new, expected):
        assert old in source, (name, old)
        case(name, source.replace(old, new, 1), expected)

    case("actual-installer", worker, {INSTALL, DEPLOY})
    case("actual-stage", staging, {PROBE})
    case("local-installer-only", installer, {INSTALL})
    case("minimal-deployment", deployment, {INSTALL, DEPLOY})
    case("minimal-archive-probe", probe, {PROBE})

    for index, mapping in enumerate([
        {"widgetReInstall": "replace_extension", "UpdateWidgetFromPypi": "sync_plugins",
         "getAutoDeployWidget": "fetch_records", "url": "location", "package_url": "artifact",
         "widget_id": "extension_key", "widget_name": "extension_name"},
        {"_run_pip_command": "invoke_installer", "urlparse": "urlsplit",
         "package_path": "candidate_path", "is_install": "enabled", "remote_version": "release"},
        {"start_daemon": "start_worker", "daemon_manager": "supervisor"},
        {"start_daemon": "startService", "retry": "backoff"},
    ]):
        case(f"deployment-renamed-{index}", renamed(deployment, mapping), {INSTALL, DEPLOY})
    for index, mapping in enumerate([
        {"_extract": "unpack", "run_staged_healthcheck": "preflight", "install_zip": "activate",
         "_install_zip_locked": "transaction", "healthcheck": "verify_candidate"},
        {"archive": "bundle", "destination": "output", "directory": "candidate_root",
         "stage": "candidate", "script": "hook", "package": "opened", "healthcheck": "check"},
        {"run": "Popen"},
        {"run": "check_call"},
    ]):
        case(f"probe-renamed-{index}", renamed(probe, mapping), {PROBE})
    mutate("probe-different-filename", probe, "healthcheck.py", "preflight_hook.py", {PROBE})
    mutate("probe-different-flag", probe, "--imports-only", "--inspect", {PROBE})
    mutate("probe-no-cosmetic-flag", probe, ", '--imports-only'", "", {PROBE})
    mutate("different-stage-directory", probe, "'candidate'", "'pending'", {PROBE})

    # URL identity and install verb must hold in one function/argv, not just
    # somewhere in a file that also contains requests, pip or install text.
    for label, old, new in [
        ("parsed-other-value", "urlparse(url)", "urlparse(other_url)"),
        ("installed-other-value", "['install', '--upgrade', url,", "['install', '--upgrade', other_url,"),
        ("other-verb", "['install', '--upgrade', url,", "['download', '--upgrade', url,"),
        ("other-carrier", "endswith('.whl')", "endswith('.txt')"),
        ("other-path", "if package_path.endswith", "if unrelated_path.endswith"),
    ]:
        mutate("url-" + label, deployment, old, new, set())

    # The automated record's URL, selected installer, and component startup
    # must agree. The installer alone remains a notable local capability.
    for label, old, new in [
        ("different-installer", "widgetReInstall(widget_name, package_url,", "unrelated(widget_name, package_url,"),
        ("different-record-url", "widgetReInstall(widget_name, package_url,", "widgetReInstall(widget_name, other_url,"),
        ("fixed-local-source", "widgetReInstall(widget_name, package_url,", "widgetReInstall(widget_name, '/opt/local.whl',"),
        ("different-component", "start_daemon(widget_id, _map_new[widget_id])", "start_daemon(other_id, _map_new[widget_id])"),
        ("no-start", "daemon_manager.start_daemon(widget_id, _map_new[widget_id])", "print(widget_id)"),
    ]:
        mutate("deploy-" + label, deployment, old, new, {INSTALL})
    case("deployment-caller-only", functions(worker, {"UpdateWidgetFromPypi"}), set())

    # Break each edge of the archive -> staging -> default callback -> script
    # chain. All these still contain superficially alarming ZIP/process APIs.
    for label, old, new in [
        ("other-archive-bytes", "io.BytesIO(archive)", "io.BytesIO(other_archive)"),
        ("other-opened-handle", "package.extractall(destination)", "other_package.extractall(destination)"),
        ("other-extraction-dir", "package.extractall(destination)", "package.extractall(other_directory)"),
        ("other-script-directory", "Path(directory) /", "Path(other_directory) /"),
        ("other-script", "str(script),", "str(other_script),"),
        ("other-callback-default", "healthcheck=run_staged_healthcheck", "healthcheck=unrelated_probe"),
        ("other-callback-forward", "install_requirements, healthcheck)", "install_requirements, unrelated_probe)"),
        ("other-forwarded-archive", "_install_zip_locked(archive,", "_install_zip_locked(other_archive,"),
        ("other-stage-callee", "return _install_zip_locked(", "return unrelated_stage("),
        ("other-extractor", "_extract(archive, stage)", "unrelated_extractor(archive, stage)"),
        ("other-stage-archive", "_extract(archive, stage)", "_extract(other_archive, stage)"),
        ("other-stage-directory", "healthcheck(str(stage))", "healthcheck(str(other_stage))"),
        ("other-stage-callback", "healthcheck(str(stage))", "unrelated_probe(str(stage))"),
    ]:
        mutate("archive-" + label, probe, old, new, set())
    for name in sorted(stage_names):
        case("stage-part-only-" + name.lstrip("_"), functions(staging, {name}), set())
        case("stage-missing-" + name.lstrip("_"), functions(staging, stage_names - {name}), set())
    # Cleave deliberately recovers complete programs from string literals and
    # analyzes that embedded code. A match describes the recovered capability,
    # not evidence that the outer program executes the string. Comments do not
    # supply executable AST nodes or a recoverable string payload.
    case("embedded-deployment-code", "documentation = " + repr(deployment), {INSTALL, DEPLOY})
    case("embedded-probe-code", "documentation = " + repr(probe), {PROBE})
    case("commented-deployment", "\n".join("# " + line for line in deployment.splitlines()), set())
    case("commented-probe", "\n".join("# " + line for line in probe.splitlines()), set())
    case("local-healthcheck", "import subprocess, sys\nsubprocess.run([sys.executable, '/opt/check.py'])\n", set())

    def archive(name, members, expected):
        path = inputs / (name + ".whl")
        with zipfile.ZipFile(path, "w") as bundle:
            for member, content in members.items():
                bundle.writestr(member, content)
        cases.append((path, set(expected)))

    archive("complete-renamed-members", {"a.py": deployment, "b.py": probe}, SELECTED)
    archive("split-deployment-roles", {"a.py": installer,
                                      "b.py": functions(worker, {"UpdateWidgetFromPypi"})}, {INSTALL})
    archive("split-probe-roles", {name + ".py": functions(staging, {name}) for name in stage_names}, set())
    result = subprocess.run(
        [args.cleave, "--traits-dir", str(ROOT), "--no-update-check", "--format", "jsonl", str(inputs)],
        capture_output=True, text=True, check=True, timeout=600,
        env={**os.environ, "CLEAVE_SKIP_CACHE": "1", "RAYON_NUM_THREADS": "2"},
    )
    (args.out / "scan.jsonl").write_text(result.stdout)
    reports = {}
    for line in result.stdout.splitlines():
        for report in json.loads(line).get("files", []):
            if "!!" not in report["path"]:
                reports[Path(report["path"]).name] = report
    results = []
    failures = []
    for path, expected in cases:
        matched = {trait["id"]: trait["crit"] for trait in reports[path.name].get("traits", [])
                   if trait["id"] in SELECTED}
        passed = set(matched) == expected and all(matched[trait] == LEVELS[trait] for trait in matched)
        if not passed:
            failures.append((path.name, sorted(matched), sorted(expected)))
        results.append({"case": path.name, "passed": passed, "matches": matched})
    (args.out / "results.json").write_text(json.dumps(results, indent=2) + "\n")
    assert not failures, json.dumps(failures, indent=2)
    print(f"Passed {len(results)} linked deployment, URL-install and archive-probe controls")


if __name__ == "__main__":
    main()
