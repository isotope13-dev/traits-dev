____________=0
import pyminifier.obfuscate
result = eval(compile(eval(compile("'40+2'", 'inner', 'eval')), 'outer', 'eval'))
