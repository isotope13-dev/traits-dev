"""Quote-pair chr() usage must not read as string concealment.

Guards objectives/anti-static/obfuscation/string/encoding::python-dense-chr-calls:
isolated chr(34)/chr(39) pairs (double/single quote literals, e.g. in codegen
templates) are not a concatenation chain. No obfuscation exists in this file.
"""


def quote_class():
    return 'href=[' + chr(34) + chr(39) + ']([^' + chr(34) + chr(39) + ']+)'


def image_class():
    return 'src=[' + chr(34) + chr(39) + ']([^' + chr(34) + chr(39) + ']+)'
