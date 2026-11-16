"""Deterministic original numeric practice, explicitly separate from past papers.
Each stored variant has unique input data, an exact answer and method feedback.
These are drill variants, not additional curriculum topics or authentic exam parts.
"""
from fractions import Fraction
from math import gcd
import json,pathlib
R=pathlib.Path(__file__).resolve().parents[1];p=R/'content/library.json';D=json.loads(p.read_text());created=[]
def f(x):
 x=Fraction(x);return str(x.numerator) if x.denominator==1 else f'{x.numerator}/{x.denominator}'
def put(family,lid,params,prompt,answer,guide):
 lesson=next(l for l in D['lessons'] if l['id']==lid);id=f'drill-{family}-'+ '-'.join(str(v).replace('-','n') for v in params)
 created.append(dict(id=id,paperId=None,form=lesson['form'],subjectId=lesson['subjectId'],topicIds=[lid],subtopicIds=[lid],sourceType='original',sourceTitle='SomaSmart original calculation drills',institution='SomaSmart',year=None,curriculumEdition='Compatible original calculation practice; coverage remains partial',questionNumber=str(len(created)+1),parentQuestionId=None,type='calculation',instructions='Show the method. Give an exact fraction where appropriate; these are original numeric practice variants, not past-examination questions.',content=prompt,options=[],media=[],maximumMarks=2,markIncrement=1,answerKey=answer,markingGuide=guide+' Award one mark for a valid method and one for a correct final result with required units.',solutionProvenance='SomaSmart deterministic original practice; answer calculated from the stored input values',sourceReference='Original parameterised calculation drill collection',rightsStatus='original',verificationStatus='generated-calculation-checked',publicationStatus='published',resourceKind='workbook',questionFamily=family,variantParameters=list(params),generationMethod='deterministic-parameterised-original'))
# Parameters deliberately vary difficulty, signs and dimensions; no item is copied from a source paper.
count=0
for a in range(2,12):
 for b in range(-9,11):
  x=(a*7+b*3)%23-11;c=a*x+b;term=f'+ {b}' if b>=0 else f'− {abs(b)}'
  put('linear-equations','mathematics-f1-lines-equations',(a,b,x),f'Solve {a}x {term} = {c}. Show the inverse operations.',f'x = {x}',f'Subtract {b} from both sides to obtain {a}x = {c-b}; divide by {a}. Check by substitution.');count+=1
  if count==100:break
 if count==100:break
count=0
for a in range(1,10):
 for b in range(2,12):
  if gcd(a,b)!=1:continue
  unit=(a*5+b*3)%19+2;total=(a+b)*unit*1000
  put('ratio-sharing','mathematics-f1-01',(a,b,unit),f'Divide TSh {total:,} between A and B in the ratio {a}:{b}. Give both shares.',f'A: TSh {a*unit*1000:,}; B: TSh {b*unit*1000:,}',f'Total ratio terms = {a+b}; one share = {total}/{a+b} = {unit*1000}. Multiply by {a} and {b}.');count+=1
  if count==100:break
 if count==100:break
# The coprime ratio pairs above produce fewer than 100; they remain the actual count, never padded.
count=0
for base in range(2,8):
 for m in range(-2,6):
  for n in range(1,5):
   r=(base+m+n)%5;e=m+n-r;value=Fraction(base)**e
   put('index-laws','mathematics-f2-quadratics',(base,m,n,r),f'Express ({base}^{m} × {base}^{n}) ÷ {base}^{r} as one power, then evaluate exactly.',f'{base}^{e} = {f(value)}',f'For the same nonzero base, add multiplication exponents and subtract the division exponent: {m}+{n}−{r}={e}. A negative power gives a reciprocal.');count+=1
   if count==100:break
  if count==100:break
 if count==100:break
count=0
for volume in range(5,30):
 for density in [Fraction(3,2),Fraction(2),Fraction(5,2),Fraction(3)]:
  mass=volume*density
  put('density','physics-f1-01',(volume,density.numerator,density.denominator),f'A solid has mass {f(mass)} g and volume {volume} cm³. Calculate its density in g/cm³ and kg/m³.',f'{f(density)} g/cm³; {f(density*1000)} kg/m³',f'Use density=mass/volume: {f(mass)}/{volume}={f(density)} g/cm³. Multiply by 1000 for kg/m³.');count+=1
count=0
for speed in range(3,8):
 for time in range(60,160,5):
  rest=15+((speed+time)//5%8)*15;distance=speed*time;answer=Fraction(distance,time+rest)
  put('journey-speed','physics-f2-01',(speed,time,rest),f'A cyclist travels {distance} m in {time} s, then rests for {rest} s. Find the average speed over the whole elapsed time.',f'{f(answer)} m/s',f'Total elapsed time={time}+{rest}={time+rest} s; divide total distance {distance} m by that time. Include the rest.');count+=1
count=0
for resistance in range(2,12):
 for voltage in range(3,13):
  current=Fraction(voltage,resistance);power=voltage*current
  put('electricity','physics-f2-current-electricity',(voltage,resistance),f'In a theoretical circuit, {voltage} V is applied across a {resistance} Ω resistor. Find its current and electrical power.',f'I = {f(current)} A; P = {f(power)} W',f'I=V/R={voltage}/{resistance} A. Then P=VI={voltage}×({f(current)})={f(power)} W.');count+=1
count=0
for force in range(40,240,10):
 for denominator in [10,20,25,50,100]:
  area=Fraction(1,denominator);pressure=force/area
  put('pressure','physics-f1-forces',(force,denominator),f'A normal force of {force} N acts on an area of 1/{denominator} m². Calculate the pressure.',f'{f(pressure)} Pa',f'p=F/A={force}/(1/{denominator})={f(pressure)} N/m².');count+=1
count=0
for force in range(5,15):
 for distance in range(2,12):
  time=(force+distance)%9+2;work=force*distance;power=Fraction(work,time)
  put('work-power','physics-f1-forces',(force,distance,time),f'A constant {force} N force moves a load {distance} m along its direction in {time} s. Calculate work done and average power.',f'W = {work} J; P = {f(power)} W',f'Work=force×distance={force}×{distance}={work} J. Power=work/time={work}/{time} W.');count+=1
# Atomic-count practice uses valid isotope proton/neutron relationships, not invented official papers.
count=0
for z in range(1,21):
 for extra in range(5):
  neutrons=z+extra;A=z+neutrons
  put('atomic-counts','chemistry-f2-atoms',(z,A),f'A neutral atom has atomic number {z} and mass number {A}. State its proton, neutron and electron numbers.',f'Protons {z}; neutrons {neutrons}; electrons {z}',f'Protons=Z={z}; neutrons=A−Z={A}−{z}={neutrons}; neutrality gives {z} electrons. These are counting examples, not a claim that every isotope shown is naturally stable.');count+=1
# Validate uniqueness before import and preserve unrelated authored records.
assert len({q['id'] for q in created})==len(created)
assert len({q['content'] for q in created})==len(created)
existing={q['id']:i for i,q in enumerate(D['questions'])}
for q in created:
 if q['id'] in existing:D['questions'][existing[q['id']]]=q
 else:D['questions'].append(q)
for b in D['books']:
 if b['kind']=='workbook':b['mixedTestQuestionIds']=[q['id'] for q in D['questions'] if q['form']==b['form'] and q['subjectId']==b['subjectId'] and q.get('resourceKind')=='workbook']
p.write_text(json.dumps(D,ensure_ascii=False,indent=2));(R/'content/batches/011-original-calculation-drills.json').write_text(json.dumps({'questions':created},ensure_ascii=False,indent=2));print('Imported',len(created),'unique original numeric drill variants in',len({q['questionFamily'] for q in created}),'families. These never count as authentic source questions.')
