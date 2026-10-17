import os
import subprocess


def test_converter_fixture_runs_as_executable(tmp_path):
    script = tmp_path / "convert.py"
    script.write_text('with open(path, "wb") as out:\n    out.write(data)\n')
    os.chmod(script, 0o755)
    subprocess.run([str(script)], check=True)
