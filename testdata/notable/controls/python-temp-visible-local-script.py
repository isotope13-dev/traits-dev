from os import system
from sys import executable
from tempfile import NamedTemporaryFile


def open_local_report():
    with NamedTemporaryFile(mode='w', suffix='.py', delete=False) as script:
        script.write(\"print('local report')\")
    system(f'\"{executable}\" \"{script.name}\"')
