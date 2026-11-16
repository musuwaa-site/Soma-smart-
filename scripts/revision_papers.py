"""Assemble labelled original mixed-topic revision papers from unique existing items.
References do not increase distinct-question totals or authentic-paper counts.
"""
import json,pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1];p=ROOT/'content/library.json';d=json.loads(p.read_text());papers=[]
for form in [1,2]:
 for s in d['subjects']:
  bank=[q for q in d['questions'] if q['form']==form and q['subjectId']==s['id'] and q['sourceType']=='original' and q['publicationStatus']=='published'];topics=list(dict.fromkeys(t for q in bank for t in q['topicIds']));selected=[]
  # First include an objective item where available, then distribute across chapters.
  objective=next((q for q in bank if q['type']=='mcq'),None)
  if objective:selected.append(objective)
  for step in range(20):
   for topic in topics:
    items=[q for q in bank if topic in q['topicIds'] and q['id'] not in {x['id'] for x in selected}]
    if items:selected.append(items[0])
    if len(selected)==12:break
   if len(selected)==12:break
  assert len(selected)==12
  papers.append(dict(id=f'original-revision-f{form}-{s["id"]}-01',form=form,subjectId=s['id'],sourceType='original',title=f'SomaSmart • {s["name"]} • Form {form} revision test 1',institution='SomaSmart',sourceReference='Original SomaSmart revision collection, not a school or NECTA examination',year=2026,curriculumEdition='TIE 2023, partial scope',rightsStatus='original',verificationStatus='author-reviewed',publicationStatus='published',questionIds=[q['id'] for q in selected],maximumMarks=sum(q['maximumMarks'] for q in selected),instructions='Answer all questions. Objective items are automatically marked; use the independently authored guidance to self-mark written responses. This revision test covers only the available published chapters.'))
for paper in papers:
 existing=next((i for i,x in enumerate(d['papers']) if x['id']==paper['id']),None)
 if existing is None:d['papers'].append(paper)
 else:d['papers'][existing]=paper
p.write_text(json.dumps(d,ensure_ascii=False,indent=2));(ROOT/'content/batches/004-original-revision-papers.json').write_text(json.dumps({'papers':papers},ensure_ascii=False,indent=2));print('Assembled',len(papers),'original revision papers; no genuine-paper attribution.')
