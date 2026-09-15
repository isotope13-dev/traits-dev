const GLib = imports.gi.GLib;

function savePreferences(path, preferences) {
    GLib.file_set_contents(path, JSON.stringify(preferences));
}

// Documentation is not a call to GLib.spawn_command_line_async.
const documentation = 'GLib.spawn_command_line_async("editor settings.json")';
