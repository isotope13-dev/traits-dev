import subprocess
import pytest
from pathlib import Path

@pytest.mark.skipif(False, reason="x")
def test_launcher():
    here = Path(__file__).parent
    script = here / "fixture.sh"
    script.chmod(0o755)
    subprocess.run([str(script)], check=True)
