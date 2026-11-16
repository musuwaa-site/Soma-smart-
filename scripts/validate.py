import json,pathlib,math
ROOT=pathlib.Path(__file__).resolve().parents[1]
CLEAR={'cleared','public-domain','open-license'}
def validate(d):
 errors=[];ids=set(); lesson_ids={l['id'] for l in d['lessons']};paper_ids={p['id'] for p in d['papers']}; subject_ids={s['id'] for s in d['subjects']}
 for collection in ['subjects','lessons','questions','books','papers','glossary']:
  seen=set()
  for x in d[collection]:
   if not x.get('id') or x['id'] in seen:errors.append(f'{collection}: missing or duplicate id {x.get("id")}')
   seen.add(x.get('id'))
 for q in d['questions']:
  if q.get('publicationStatus')!='published':continue
  if q.get('sourceType')!='original' and (q.get('rightsStatus') not in CLEAR or q.get('verificationStatus')!='verified' or q.get('paperId') not in paper_ids or not q.get('sourceReference')):errors.append(f'{q["id"]}: source not cleared/verified')
  if q.get('sourceType')=='original' and (q.get('rightsStatus')!='original' or q.get('paperId')):errors.append(f'{q["id"]}: original provenance invalid')
  if q.get('form') not in [1,2] or q.get('subjectId') not in subject_ids:errors.append(f'{q["id"]}: invalid form/subject')
  if not q.get('topicIds') or any(t not in lesson_ids for t in q['topicIds']):errors.append(f'{q["id"]}: invalid topic mapping')
  if not q.get('content') or not q.get('answerKey') or not q.get('markingGuide'):errors.append(f'{q["id"]}: missing answer or rubric')
  m=q.get('maximumMarks');inc=q.get('markIncrement')
  if not isinstance(m,(float,int)) or not isinstance(inc,(float,int)) or not math.isfinite(m) or not math.isfinite(inc) or m<=0 or inc<=0 or abs(m/inc-round(m/inc))>1e-8:errors.append(f'{q["id"]}: invalid marking increments')
  if q.get('type') not in ['mcq','matching','short','calculation','essay']:errors.append(f'{q["id"]}: unsupported question type')
  if q.get('type')=='mcq' and (q['answerKey'] not in q['options'] or len(set(q['options']))!=len(q['options']) or len(q['options'])<2):errors.append(f'{q["id"]}: invalid options')
  if q.get('type')=='matching':
   pairs=q.get('pairs',[]);key=q.get('answerKey',{})
   if not isinstance(key,dict) or not pairs or {p.get('id') for p in pairs}!=set(key) or any(v not in q.get('options',[]) for v in key.values()) or len(key)*inc!=m:errors.append(f'{q["id"]}: invalid matching structure')
  for media in q.get('media',[]):
   path=ROOT/'public'/media['path'].lstrip('/')
   if not path.is_file():errors.append(f'{q["id"]}: missing media {path}')
  if q.get('parentQuestionId') and q['parentQuestionId'] not in {x['id'] for x in d['questions']}:errors.append(f'{q["id"]}: orphan group')
 for l in d['lessons']:
  if not l.get('paragraphs') or not l.get('examples'):errors.append(f'{l["id"]}: empty lesson')
  if l.get('diagram') and not (ROOT/'public'/l['diagram'].lstrip('/')).is_file():errors.append(f'{l["id"]}: missing diagram')
 for b in d['books']:
  if not b.get('lessonIds') or any(x not in lesson_ids for x in b['lessonIds']):errors.append(f'{b["id"]}: empty/invalid book')
 return errors
if __name__=='__main__':
 import sys
 errors=validate(json.load(open(sys.argv[1] if len(sys.argv)>1 else ROOT/'content/library.json')))
 print('\n'.join(errors) if errors else 'Content integrity passed');sys.exit(bool(errors))
