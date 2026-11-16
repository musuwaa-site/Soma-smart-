"""Three original drill families supporting newly added algebra/geometry chapters."""
import json,pathlib
from fractions import Fraction
R=pathlib.Path(__file__).resolve().parents[1];p=R/'content/library.json';D=json.loads(p.read_text());created=[]
def f(v):
 v=Fraction(v);return str(v.numerator) if v.denominator==1 else str(v.numerator)+'/'+str(v.denominator)
def add(family,lid,n,prompt,answer,guide,params):
 l=next(l for l in D['lessons'] if l['id']==lid);created.append(dict(id=f'drill-{family}-{n:03}',paperId=None,form=l['form'],subjectId=l['subjectId'],topicIds=[lid],subtopicIds=[lid],sourceType='original',sourceTitle='SomaSmart original calculation drills',institution='SomaSmart',year=None,curriculumEdition='Compatible original numeric practice',questionNumber=str(n),parentQuestionId=None,type='calculation',instructions='Show your method; an exact fraction is accepted. Original numeric drill, not a past-paper question.',content=prompt,options=[],media=[],maximumMarks=2,markIncrement=1,answerKey=answer,markingGuide=guide+' One mark for a correct method and one for the result with relevant units.',solutionProvenance='SomaSmart deterministic original practice',sourceReference='Original parameterised algebra and geometry practice',rightsStatus='original',verificationStatus='generated-calculation-checked',publicationStatus='published',resourceKind='workbook',questionFamily=family,variantParameters=params,generationMethod='deterministic-parameterised-original'))
for n in range(1,51):
 x=2+n%11;y=3+(n*7)%17;x2=5+(n*3)%19;k=x*y;answer=Fraction(k,x2)
 add('inverse-variation','mathematics-f2-rates-variation',n,f'y varies inversely as x. When x={x}, y={y}. Find the exact value of y when x={x2}.',f'y={f(answer)}',f'xy is constant at {x}×{y}={k}. Therefore y={k}/{x2}.',[x,y,x2])
 a=3+n%13;num=2+n%7;den=1+(n//7)%5;answer=Fraction(a*num,den)
 add('similarity-scaling','mathematics-f2-similarity-scale',n,f'Triangles A and B are similar. Every corresponding length in B is {num}/{den} times its length in A. A side of A is {a} cm. Find its corresponding side in B.',f'{f(answer)} cm',f'Multiply the corresponding A length by the stated factor {num}/{den}: {a}×{num}/{den}.',[a,num,den])
 x1=n%7-3;y1=n%11-5;dx=2+n%8;dy=n%13-6;x2=x1+dx;y2=y1+dy;m=Fraction(dy,dx);c=Fraction(y1)-m*x1
 add('line-gradient-intercept','mathematics-f1-lines-equations',n,f'A straight line passes through ({x1},{y1}) and ({x2},{y2}). Find its gradient and y-intercept.',f'Gradient {f(m)}; y-intercept {f(c)}',f'm=({y2}−({y1}))/({x2}−({x1}))={f(m)}. Use c=y−mx with either point to obtain {f(c)}.',[x1,y1,x2,y2])
assert len({q['content'] for q in created})==len(created)
index={q['id']:i for i,q in enumerate(D['questions'])}
for q in created:
 if q['id'] in index:D['questions'][index[q['id']]]=q
 else:D['questions'].append(q)
p.write_text(json.dumps(D,ensure_ascii=False,indent=2));(R/'content/batches/012-algebra-geometry-drills.json').write_text(json.dumps({'questions':created},ensure_ascii=False,indent=2));print('Imported',len(created),'unique original drill variants.')
