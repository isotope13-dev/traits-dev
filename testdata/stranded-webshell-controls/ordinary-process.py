import subprocess
import importlib
runner = importlib.import_module("subprocess")
result = subprocess.run(["/usr/bin/printf", "hello"], stdout=subprocess.DEVNULL, start_new_session=True)
status = result.returncode
exit_code = status
