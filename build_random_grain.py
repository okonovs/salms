from pathlib import Path
import math
root = Path(__file__).resolve().parent
source = (root/'Phase1.setting').read_text()
# Stateless, independent deterministic streams. Seed is fixed at 17 for this prototype.
index = '(floor((time-comp.RenderStart)/4)+17)'
def random_expr(channel):
    v = f'(sin({index}*12.9898+{channel}*78.233)*43758.5453)'
    return f'({v}-floor({v}))'
w = f'0.18+0.40*{random_expr(1)}'
h = f'0.18+0.44*{random_expr(2)}'
x = f'0.01+SalmsRectangle.Width/2+(0.98-SalmsRectangle.Width)*{random_expr(3)}'
y = f'0.01+SalmsRectangle.Height/2+(0.98-SalmsRectangle.Height)*{random_expr(4)}'
source = source.replace('Center = Input { Value = { 0.5, 0.5 } }',f'Center = Input {{ Expression = "Point({x},{y})" }}',1)
source = source.replace('Width = Input { Value = 0.35 }',f'Width = Input {{ Expression = "{w}" }}',1)
source = source.replace('Height = Input { Value = 0.4 }',f'Height = Input {{ Expression = "{h}" }}',1)
grain = '''  SalmsFilmGrain = FilmGrain {
   Inputs = {
    Input = Input { SourceOp = "SalmsBlur", Source = "Output" },
    Blend = Input { Value = 0.5 }
   },
   ViewInfo = OperatorInfo { Pos = { 275, 65 } }
  },
'''
source = source.replace('  SalmsRectangle = RectangleMask {',grain+'  SalmsRectangle = RectangleMask {')
source = source.replace('Background = Input { SourceOp = "SalmsBlur", Source = "Output" }','Background = Input { SourceOp = "SalmsFilmGrain", Source = "Output" }')
(root/'Random4_Grain.setting').write_text(source)
# Check temporal holding and bounds independently of Resolve expression evaluation.
def state(frame):
    i=frame//4+17
    def r(c):
        v=math.sin(i*12.9898+c*78.233)*43758.5453
        return v-math.floor(v)
    w,h=.18+.40*r(1),.18+.44*r(2)
    return .01+w/2+(.98-w)*r(3),.01+h/2+(.98-h)*r(4),w,h
for frame in range(10000):
    x,y,w,h=state(frame)
    assert state(frame)==state(frame-frame%4)
    assert .18<=w<=.58 and .18<=h<=.62
    assert x-w/2>=.01-1e-12 and x+w/2<=.99+1e-12
    assert y-h/2>=.01-1e-12 and y+h/2<=.99+1e-12
    if frame and frame%4==0: assert state(frame)!=state(frame-1)
(root/'tests/random4-math.txt').write_text('PASS: 10000 frames, four-frame holds, jumps at boundaries, width/height bounds, one-percent image margins.\nResolve import and rendered output: pending user verification.\n')
print('Created Random4_Grain.setting; 10000-frame math checks passed.')
