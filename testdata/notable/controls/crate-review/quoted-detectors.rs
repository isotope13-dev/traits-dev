fn compressed_source_example() -> &'static str {
    "import zlib\nimport base64\nexec(zlib.decompress(base64.b64decode(payload)))\n"
}

fn request_command_example() -> &'static str {
    "String cmd = request.getParameter(\"cmd\"); Runtime.getRuntime().exec(cmd);"
}
