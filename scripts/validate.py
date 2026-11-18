import json,pathlib,math,re,hashlib
from source_integrity import text_hash
ROOT=pathlib.Path(__file__).resolve().parents[1]
CLEAR={'cleared','public-domain','open-license'}
def validate(d):
 errors=[];ids=set(); lesson_ids={l['id'] for l in d['lessons']};paper_ids={p['id'] for p in d['papers']}; subject_ids={s['id'] for s in d['subjects']}
 for collection in ['subjects','lessons','questions','books','papers','glossary']:
  seen=set()
  for x in d[collection]:
   if not x.get('id') or x['id'] in seen:errors.append(f'{collection}: missing or duplicate id {x.get("id")}')
   if not isinstance(x.get('id'),str) or not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9._-]{0,179}',x.get('id','')):errors.append(f'{collection}: unsafe identifier')
   seen.add(x.get('id'))
 for q in d['questions']:
  if q.get('sourceTextSha256') and text_hash(q)!=q['sourceTextSha256']:errors.append(f'{q["id"]}: original source transcription changed')
  if q.get('publicationStatus')!='published':continue
  if q.get('sourceTextSha256'):
   source=next((s for s in d.get('sourceDocuments',[]) if s.get('id')==q.get('sourceDocumentId')),None)
   if not source or source.get('publicationStatus')!='published' or source.get('sha256')!=q.get('sourceSha256') or source.get('form')!=q.get('form') or source.get('subjectId')!=q.get('subjectId'):errors.append(f'{q["id"]}: mismatched or quarantined source')
   elif any(not isinstance(p,int) or p<1 or p>source['pageCount'] or not any(m.get('path')==source['pageImages'][p-1] for m in q.get('media',[])) for p in q.get('sourcePages',[])):errors.append(f'{q["id"]}: incomplete original source-page references')
  if q.get('sourceType')!='original' and (q.get('rightsStatus') not in CLEAR or q.get('verificationStatus')!='verified' or q.get('paperId') not in paper_ids or not q.get('sourceReference')):errors.append(f'{q["id"]}: source not cleared/verified')
  if q.get('sourceType')=='original' and (q.get('rightsStatus')!='original' or q.get('paperId')):errors.append(f'{q["id"]}: original provenance invalid')
  if q.get('form') not in [1,2] or q.get('subjectId') not in subject_ids:errors.append(f'{q["id"]}: invalid form/subject')
  if not q.get('topicIds') or any(t not in lesson_ids for t in q['topicIds']):errors.append(f'{q["id"]}: invalid topic mapping')
  if not (q.get('content') or q.get('sourceParts')) or not q.get('answerKey') or not q.get('markingGuide'):errors.append(f'{q["id"]}: missing answer or rubric')
  m=q.get('maximumMarks');inc=q.get('markIncrement')
  if not isinstance(m,(float,int)) or not isinstance(inc,(float,int)) or not math.isfinite(m) or not math.isfinite(inc) or m<=0 or inc<=0 or abs(m/inc-round(m/inc))>1e-8:errors.append(f'{q["id"]}: invalid marking increments')
  if q.get('type') not in ['mcq','matching','short','calculation','essay']:errors.append(f'{q["id"]}: unsupported question type')
  if q.get('type')=='mcq' and (q['answerKey'] not in q['options'] or len(set(q['options']))!=len(q['options']) or len(q['options'])<2):errors.append(f'{q["id"]}: invalid options')
  if q.get('acceptedAnswerKeys') is not None:
   keys=q['acceptedAnswerKeys']
   if q['type']!='mcq' or not isinstance(keys,list) or not keys or q['answerKey'] not in keys or any(k not in q['options'] for k in keys):errors.append(f'{q["id"]}: invalid alternative answer keys')
  if q.get('acceptedMatchingAnswers') is not None:
   keys=q['acceptedMatchingAnswers']
   if q['type']!='matching' or not isinstance(keys,dict) or any(k not in q['answerKey'] or not isinstance(v,list) or q['answerKey'][k] not in v or any(a not in q['options'] for a in v) for k,v in keys.items()):errors.append(f'{q["id"]}: invalid matching alternatives')
  if q.get('type')=='matching':
   pairs=q.get('pairs',[]);key=q.get('answerKey',{})
   if not isinstance(key,dict) or not pairs or {p.get('id') for p in pairs}!=set(key) or any(v not in q.get('options',[]) for v in key.values()) or len(key)*inc!=m:errors.append(f'{q["id"]}: invalid matching structure')
  for media in q.get('media',[]):
   path=ROOT/'public'/media['path'].lstrip('/')
   if not path.is_file():errors.append(f'{q["id"]}: missing media {path}')
  if q.get('parentQuestionId') and q['parentQuestionId'] not in {x['id'] for x in d['questions']}:errors.append(f'{q["id"]}: orphan group')
 for document in d.get('sourceDocuments',[]):
  if document.get('publicationStatus')!='published':continue
  path=ROOT/'public'/document.get('sourcePdf','').lstrip('/')
  if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest()!=document.get('sha256'):errors.append(f'{document.get("id")}: missing or changed source PDF')
  if document.get('rightsStatus') not in CLEAR or not document.get('rightsEvidence'):errors.append(f'{document.get("id")}: missing owner permission record')
  pages=document.get('pageImages',[])
  if not pages or len(pages)!=document.get('pageCount'):errors.append(f'{document.get("id")}: incomplete source pages')
  for page in pages:
   if not (ROOT/'public'/page.lstrip('/')).is_file():errors.append(f'{document.get("id")}: missing source page')
  if document.get('answerGuide'):
   guide=document['answerGuide'];gp=ROOT/'public'/guide['sourcePdf'].lstrip('/')
   if not gp.is_file() or hashlib.sha256(gp.read_bytes()).hexdigest()!=guide['sha256']:errors.append(f'{document["id"]}: missing or changed answer guide')
   if len(guide.get('pageImages',[]))!=guide.get('pageCount'):errors.append(f'{document["id"]}: incomplete answer guide pages')
   for page in guide.get('pageImages',[]):
    if not (ROOT/'public'/page.lstrip('/')).is_file():errors.append(f'{document["id"]}: missing guide page')

 for paper in d['papers']:
  if paper.get('publicationStatus')!='published':continue
  items=[next((q for q in d['questions'] if q['id']==id),None) for id in paper.get('questionIds',[])]
  if not items or any(q is None for q in items) or len({q['id'] for q in items if q})!=len(items):errors.append(f'{paper["id"]}: empty, missing or duplicate paper items');continue
  if any(q['form']!=paper['form'] or q['subjectId']!=paper['subjectId'] or q['publicationStatus']!='published' for q in items):errors.append(f'{paper["id"]}: incompatible paper items')
  if paper.get('sourceType')=='original' and (paper.get('rightsStatus')!='original' or any(q['sourceType']!='original' for q in items)):errors.append(f'{paper["id"]}: false original provenance')
  if paper.get('sourceType')!='original' and (paper.get('rightsStatus') not in CLEAR or paper.get('verificationStatus')!='verified'):errors.append(f'{paper["id"]}: uncleared source paper')
  if paper.get('sourceType')!='original' and (not paper.get('rightsEvidence') or any(q['sourceType']=='original' or q.get('paperId')!=paper['id'] for q in items)):errors.append(f'{paper["id"]}: missing rights evidence or false authentic attribution')
  if paper.get('maximumMarks')!=sum(q['maximumMarks'] for q in items):errors.append(f'{paper["id"]}: incorrect paper total')
 activity_by_id={a['id']:a for a in d.get('curriculum',{}).get('activities',[])}
 for l in d['lessons']:
  for ref in l.get('curriculumRefs',[]):
   activity=activity_by_id.get(ref.get('activityId'))
   if not activity or activity['form']!=l['form'] or activity['subjectId']!=l['subjectId'] or activity['pdfPages']!=ref.get('pdfPages'):errors.append(f'{l["id"]}: invalid curriculum reference')

  if not l.get('paragraphs') or not l.get('examples'):errors.append(f'{l["id"]}: empty lesson')
  if l.get('diagram') and not (ROOT/'public'/l['diagram'].lstrip('/')).is_file():errors.append(f'{l["id"]}: missing diagram')
 for b in d['books']:
  if b.get('completionStatus')=='complete':
   required=[x for x in d.get('curriculum',{}).get('subtopics',[]) if x.get('form')==b['form'] and x.get('subjectId')==b['subjectId']]
   if not b.get('curriculumVerified') or not required or any(x.get('coverageStatus')!='complete' for x in required):errors.append(f'{b["id"]}: completion claim lacks verified subtopic coverage')

  if not b.get('lessonIds') or any(x not in lesson_ids for x in b['lessonIds']):errors.append(f'{b["id"]}: empty/invalid book')
  elif any(next(l for l in d['lessons'] if l['id']==id)['form']!=b['form'] or next(l for l in d['lessons'] if l['id']==id)['subjectId']!=b['subjectId'] for id in b['lessonIds']):errors.append(f'{b["id"]}: book contains an incompatible chapter')
 return errors
if __name__=='__main__':
 import sys
 errors=validate(json.load(open(sys.argv[1] if len(sys.argv)>1 else ROOT/'content/library.json')))
 print('\n'.join(errors) if errors else 'Content integrity passed');sys.exit(bool(errors))
