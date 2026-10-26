import sys
from fontTools.fontBuilder import FontBuilder
from fontTools.pens.ttGlyphPen import TTGlyphPen
UPM = 16384
N = 9
SCALE = 0.5
DX = 33
fb = FontBuilder(UPM, isTTF=True)
names = ['.notdef', 'leaf'] + [f'c{i}' for i in range(N - 1)] + ['A']
fb.setupGlyphOrder(names)
fb.setupCharacterMap({ord('A'): 'A'})
p = TTGlyphPen(None)
p.moveTo((0, 0))
p.lineTo((DX, 0))
p.lineTo((DX, 40))
p.lineTo((0, 40))
p.closePath()
p.moveTo((20, 1))
p.lineTo((20, 39))
p.closePath()
glyf = {'leaf': p.glyph()}
p = TTGlyphPen(None)
p.moveTo((0, 0))
p.lineTo((1, 0))
p.lineTo((1, 1))
p.closePath()
glyf['.notdef'] = p.glyph()
gs = dict.fromkeys(names)
prev = 'leaf'
for name in names[2:]:
    p = TTGlyphPen(gs)
    p.addComponent(prev, (SCALE, 0, 0, SCALE, 0, 0))
    glyf[name] = p.glyph()
    prev = name
fb.setupGlyf(glyf)
fb.setupHorizontalMetrics({n: (100, 0) for n in names})
fb.setupHorizontalHeader(ascent=100, descent=-100)
fb.setupOS2()
fb.setupNameTable({'familyName': 'T', 'styleName': 'R'})
fb.setupPost()
fb.font['maxp'].maxComponentDepth = N
fb.font.recalcBBoxes = True
for g in glyf.values():
    g.xMin = g.yMin = 0
    g.xMax = DX
    g.yMax = 40
fb.font['head'].xMin = 0
fb.font['head'].xMax = DX
fb.font['head'].yMin = 0
fb.font['head'].yMax = 40
fb.save(sys.argv[1] if len(sys.argv) > 1 else 'trigger.ttf')
