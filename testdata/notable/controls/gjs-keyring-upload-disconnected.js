const GLib = imports.gi.GLib;

function inspectAccount() {
    GLib.spawn_command_line_async(
        "/bin/sh -c 'secret-tool search service myapp | " + "cat'");
}

function reportHealth() {
    GLib.spawn_command_line_async(
        "/bin/sh -c 'printf ready | " +
        "curl -s --data-binary @- https://health.example.invalid/status'");
}

function inspectThenReport() {
    GLib.spawn_command_line_async(
        "/bin/sh -c 'secret-tool search service myapp | cat; printf ready | " +
        "curl -s --data-binary @- https://health.example.invalid/status'");
}

function discardThenReport() {
    GLib.spawn_command_line_async(
        "/bin/sh -c 'secret-tool search service myapp >/dev/null | " +
        "curl -s --data-binary @- https://health.example.invalid/status'");
}

function sendLiteralMarker() {
    GLib.spawn_command_line_async(
        "/bin/sh -c 'secret-tool search service myapp | " +
        "curl -s --data-raw @- https://health.example.invalid/status'");
}

function uploadHelpText() {
    GLib.spawn_command_line_async(
        "/bin/sh -c 'secret-tool search --help | " +
        "curl -s --data-binary @- https://health.example.invalid/status'");
}
