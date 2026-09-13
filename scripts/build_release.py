from pathlib import Path
import re, zipfile, json, math
root=Path(__file__).resolve().parent.parent
out=root/'dist';out.mkdir(exist_ok=True)
s=(root/'src/random-window-base.setting').read_text()
# Publish custom controller inputs from the master mask so expressions stay inside the macro.
controls=[
 ('BlurAmount','Blur Amount',12,0,100,'Image',False),
 ('GrainAmount','Film Grain Amount',.5,0,1,'Image',False),
 ('Grayscale','Grayscale',0,0,1,'Image',True),
 ('HoldFrames','Change Every Frames',4,1,240,'Rectangle',True),
 ('RandomSeed','Random Seed',17,0,100000,'Rectangle',True),
 ('MinArea','Minimum Area (%)',4,0.1,90,'Rectangle',False),
 ('MaxArea','Maximum Area (%)',18,0.1,90,'Rectangle',False),
 ('MinRatio','Minimum Shape Ratio (W/H)',0.25,0.1,10,'Rectangle',False),
 ('MaxRatio','Maximum Shape Ratio (W/H)',4,0.1,10,'Rectangle',False),
]
def ref(k):return 'SalmsRectangle.'+k
idx=f'(floor((time-comp.RenderStart)/max(1,floor({ref("HoldFrames")})))+floor({ref("RandomSeed")}))'
def rnd(c):
 v=f'(sin({idx}*12.9898+{c}*78.233)*43758.5453)'
 return f'({v}-floor({v}))'
def dim(axis,c):
 return ('sqrt(SalmsRectangle.SampleArea*SalmsRectangle.SampleRatio/SalmsRectangle.FrameAspect)'
         if axis == 'Width' else
         'sqrt(SalmsRectangle.SampleArea*SalmsRectangle.FrameAspect/SalmsRectangle.SampleRatio)')
area_a='max(0.001,min(0.90,SalmsRectangle.MinArea/100))'
area_b='max(0.001,min(0.90,SalmsRectangle.MaxArea/100))'
# Preserve sampled area; restrict shape range only when an extreme shape cannot fit.
fit_lo='(SalmsRectangle.SampleArea*SalmsRectangle.FrameAspect/0.9604)'
fit_hi='(0.9604*SalmsRectangle.FrameAspect/SalmsRectangle.SampleArea)'
hidden={
 'FrameAspect':'SalmsTimeline.Output.OriginalWidth/max(1,SalmsTimeline.Output.OriginalHeight)',
 'SampleArea':f'min({area_a},{area_b})+abs({area_a}-{area_b})*{rnd(1)}',
 'LowRatio':f'max({fit_lo},min({fit_hi},min(SalmsRectangle.MinRatio,SalmsRectangle.MaxRatio)))',
 'HighRatio':f'max({fit_lo},min({fit_hi},max(SalmsRectangle.MinRatio,SalmsRectangle.MaxRatio)))',
 'SampleRatio':f'exp(log(SalmsRectangle.LowRatio)+(log(SalmsRectangle.HighRatio)-log(SalmsRectangle.LowRatio))*{rnd(2)})',
}

x=f'0.01+SalmsRectangle.Width/2+(0.98-SalmsRectangle.Width)*{rnd(3)}'
y=f'0.01+SalmsRectangle.Height/2+(0.98-SalmsRectangle.Height)*{rnd(4)}'
start=s.index('  SalmsRectangle = RectangleMask {'); end=s.index('  SalmsSharpWindow = Merge {')
r=s[start:end]
for k,e in [('Center',f'Point({x},{y})'),('Width',dim('Width',1)),('Height',dim('Height',2))]:
 r=re.sub(rf'{k} = Input \{{ Expression = "[^"]*" \}}',f'{k} = Input {{ Expression = "{e}" }}',r,count=1)
r=r.replace('   Inputs = {','   Inputs = {\n'+''.join(f'    {k} = Input {{ Value = {v} }},\n' for k,_,v,*_ in controls),1)
r=r.replace('   Inputs = {', '   Inputs = {\n'+''.join(f'    {k} = Input {{ Expression = "{v}" }},\n' for k,v in hidden.items()),1)
uc=[f'    {k} = {{ LINKID_DataType = "Number", INPID_InputControl = "SliderControl", INP_External = false, INP_Visible = false }},' for k in hidden]
for k,label,v,lo,hi,page,integer in controls:
 ui='CheckboxControl' if k=='Grayscale' else 'SliderControl'
 uc.append(f'    {k} = {{ LINKS_Name = "{label}", LINKID_DataType = "Number", INPID_InputControl = "{ui}", INP_Default = {v}, INP_MinScale = {lo}, INP_MaxScale = {hi}, INP_MinAllowed = {lo}, INP_MaxAllowed = {hi}, INP_Integer = {str(integer).lower()}, INP_External = true, ICS_ControlPage = "{page}" }},')
r=r.replace('   ViewInfo =', '   UserControls = ordered() {\n'+'\n'.join(uc)+'\n   },\n   ViewInfo =')
s=s[:start]+r+s[end:]
s=s.replace('XBlurSize = Input { Value = 12 }','XBlurSize = Input { Expression = "SalmsRectangle.BlurAmount" }')
s=s.replace('Blend = Input { Value = 0.5 }','Blend = Input { Expression = "SalmsRectangle.GrainAmount" }')
# Grayscale is upstream of BOTH branches, border is downstream.
s=s.replace('SourceOp = "SalmsTimeline", Source = "Output"','SourceOp = "SalmsGrayscale", Source = "Output"')
s=s.replace('  SalmsBlur = Blur {','''  SalmsGrayscale = BrightnessContrast {
   Inputs = {
    Input = Input { SourceOp = "SalmsTimeline", Source = "Output" },
    Saturation = Input { Expression = "1-SalmsRectangle.Grayscale" }
   },
   ViewInfo = OperatorInfo { Pos = { 110, 0 } }
  },
  SalmsBlur = Blur {''')
# Desaturate the completed footage composite, including any colored grain.
# The border is added afterwards and retains its independent color.
s=s.replace('SourceOp = "SalmsGrayscale", Source = "Output"', 'SourceOp = "SalmsTimeline", Source = "Output"')
a=s.index('  SalmsGrayscale = BrightnessContrast {')
b=s.index('  SalmsBlur = Blur {',a)
s=s[:a]+s[a:b].replace('SourceOp = "SalmsTimeline"','SourceOp = "SalmsSharpWindow"')+s[b:]
s=s.replace('Background = Input { SourceOp = "SalmsSharpWindow", Source = "Output" }','Background = Input { SourceOp = "SalmsGrayscale", Source = "Output" }')
# Macro outputs final merge directly; Resolve supplies the timeline MediaOut.
body=s[s.index('  SalmsTimeline ='):s.index('  MediaOut1 =')].rstrip().rstrip(',')
published=[]
for k,label,v,lo,hi,page,integer in controls:
 published.append(f'   {k} = InstanceInput {{ SourceOp = "SalmsRectangle", Source = "{k}", Name = "{label}", Page = "{page}", Default = {v} }},')
for k,node,param,label,v,extra in [
 ('BorderWidth','SalmsOutline','BorderWidth','Border Width',.003,''),
 ('BorderRed','SalmsWhite','TopLeftRed','Border Color',1,'ControlGroup = 1,'),
 ('BorderGreen','SalmsWhite','TopLeftGreen','Green',1,'ControlGroup = 1,'),
 ('BorderBlue','SalmsWhite','TopLeftBlue','Blue',1,'ControlGroup = 1,'),
 ('BorderOpacity','SalmsWhite','TopLeftAlpha','Border Opacity',1,'')]:
 published.append(f'   {k} = InstanceInput {{ SourceOp = "{node}", Source = "{param}", Name = "{label}", Page = "Border", Default = {v}, {extra} }},')
macro='''{
 Tools = ordered() {
  SalmsRandomWindow = MacroOperator {
   NameSet = true,
   Inputs = ordered() {
'''+ '\n'.join(published)+'''
   },
   Outputs = { MainOutput1 = InstanceOutput { SourceOp = "SalmsBorder", Source = "Output" } },
   ViewInfo = GroupInfo { Pos = { 0, 0 } },
   Tools = ordered() {
'''+body+'''
   }
  }
 }
}
'''
setting=out/'Salms Random Window.setting';setting.write_text(macro)
package=out/'Salms Random Window.drfx'
with zipfile.ZipFile(package,'w',zipfile.ZIP_DEFLATED) as z:
 z.writestr('Edit/Generators/Salms/Salms Random Window.setting',macro)
with zipfile.ZipFile(package) as z:
 assert z.testzip() is None
 assert z.read(z.namelist()[0]).decode()==macro
# Every source reference must resolve to an internal tool (including published inputs).
nodes=set(re.findall(r'^\s*(\w+) = (?:MediaIn|Blur|FilmGrain|BrightnessContrast|RectangleMask|Background|Merge) \{',macro,re.M))
assert set(re.findall(r'SourceOp = "(\w+)"',macro))<=nodes
assert 'MediaOut1' not in macro
assert macro.count('floor((time-comp.RenderStart)')==8
assert 'Expression = "SalmsRectangle.Center"' in macro
(root/'tests').mkdir(exist_ok=True)
(root/'tests/package-checks.txt').write_text('PASS: ZIP integrity, standard Edit/Generators path, payload equality, internal SourceOp references, linked border, single macro output.\nResolve installation, Inspector display and rendering: pending live validation.\n')
print(package)
