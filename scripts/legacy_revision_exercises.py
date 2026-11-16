"""Original exercises for supplemental prerequisite chapters; no past-paper attribution."""
import pathlib,json
R=pathlib.Path(__file__).resolve().parents[1];p=R/'content/library.json';d=json.loads(p.read_text())
sets={
'mathematics-f2-number-revision':[
('Evaluate one half of ((24÷6+7)−(3×5−2)).','−1','First brackets: 4+7=11 and 15−2=13; difference −2, half −1.'),('Round 73,480 to the nearest thousand.','73,000','The final 480 is below 500.'),('A cost of 4000 becomes a selling price of 3500. Find percentage loss.','12.5%','Loss500; 500/4000×100.'),('Divide 42 kg in ratio 2:5. Give the larger share.','30 kg','Seven shares; each is 6 kg, larger is 5×6.'),('Evaluate one third of (18−27).','−3','18−27=−9 and one third is −3.'),('Round 286,750 to the nearest thousand.','287,000','750 is at least 500, so round up.')],
'mathematics-f2-geometry-review':[
('Two adjacent angles on a straight line include 38°. Find the other.','142°','180−38.'),('Expand 6r−3(2s−r).','9r−6s','Distribute −3, then collect r terms.'),('Triangle sides are x+2, x+4 and 8 with perimeter 24. Find x.','x=5','2x+14=24.'),('An angle is vertically opposite 117°. Find it.','117°','Vertically opposite angles are equal.'),('Simplify 2(a−3b)+4a+b.','6a−5b','Expand to 2a−6b+4a+b.'),('Find two numbers whose sum is 26 and difference is 8.','17 and 9','Add the equations to get the larger number.')],
'mathematics-f2-coordinate-review':[
('State the gradient and intercept of 3y=9x+12.','Gradient3; y-intercept4.','Divide every term by three.'),('Does (2,5) lie on y=3x−1?','Yes.','3×2−1=5.'),('Find m if y=mx+1 contains (4,9).','m=2','9=4m+1.'),('Find the y-intercept of 2y=8x−6.','−3','Rearrange to y=4x−3.'),('Find the gradient through (0,2) and (3,8).','2','(8−2)/(3−0).'),('A line is y=−2x+5. Find y when x=−1.','7','−2×(−1)+5=7.')]
}
for lid,items in sets.items():
 for n,(prompt,answer,guide) in enumerate(items,1):
  q=dict(id=f'{lid}-original-{n}',paperId=None,form=2,subjectId='mathematics',topicIds=[lid],subtopicIds=[lid],sourceType='original',sourceTitle='SomaSmart original prerequisite revision',institution='SomaSmart',year=None,curriculumEdition='Supplemental prerequisite revision',questionNumber=str(n),parentQuestionId=None,type='calculation',instructions='',content=prompt,options=[],media=[],maximumMarks=2,markIncrement=1,answerKey=answer,markingGuide=guide+' Two marks for correct method and result; one for a sound method with an arithmetic slip.',solutionProvenance='SomaSmart independently authored',sourceReference='Original supplemental revision exercises',rightsStatus='original',verificationStatus='author-reviewed',publicationStatus='published',resourceKind='textbook' if n<=3 else 'workbook')
  index=next((i for i,x in enumerate(d['questions']) if x['id']==q['id']),None)
  if index is None:d['questions'].append(q)
  else:d['questions'][index]=q
 for n,(term,definition) in enumerate({'prerequisite':'Earlier knowledge needed for a later task.','equivalent method':'A different valid approach producing the same mathematical result.','verification':'Checking a result against the original conditions.'}.items(),1):
  g=dict(id=lid+f'-term-{n}',lessonId=lid,term=term,definition=definition);index=next((i for i,x in enumerate(d['glossary']) if x['id']==g['id']),None)
  if index is None:d['glossary'].append(g)
  else:d['glossary'][index]=g
for b in d['books']:
 if b['kind']=='workbook':b['mixedTestQuestionIds']=[q['id'] for q in d['questions'] if q['form']==b['form'] and q['subjectId']==b['subjectId'] and q.get('resourceKind')=='workbook']
p.write_text(json.dumps(d,ensure_ascii=False,indent=2))
