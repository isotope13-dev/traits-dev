import os, subprocess, pathlib

def test_script(tmp_path):
    script_file = tmp_path / "test_script.sh"
    script_file.write_text("#!/bin/sh\necho hi\n")
    script_file.chmod(0o755)
    script = os.path.join(os.path.dirname(__file__), 'test_script.sh')
    output = subprocess.check_output(script, text=True)
    assert output
