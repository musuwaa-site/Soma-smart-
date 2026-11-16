"""Upsert complete source transcriptions with independent scoring and text locks.
Never synthesize missing source wording, keys, or mark allocations.
"""
import json,pathlib,hashlib,re,sys,copy
from validate import validate
from apply_source_corrections import apply
from source_integrity import text_hash
R=pathlib.Path(__file__).resolve().parents[1]
def merge(data,files):
 data=apply(copy.deepcopy(data));sources={d['sha256']:d for d in data.get('sourceDocuments',[])};report=[]
 def upsert(kind,row):
  i=next((i for i,x in enumerate(data[kind]) if x['id']==row['id']),None)
  if i is None:data[kind].append(row)
  else:data[kind][i]=row
 for path in files:
  asset=json.loads(path.read_text());paper=copy.deepcopy(asset['paper']);qs=copy.deepcopy(asset['questions']);source=sources[paper['sourceSha256']]
  assert source['publicationStatus']=='published' and source['form']==paper['form'] and source['subjectId']==paper['subjectId'],(path,'Source subject/form is quarantined or mismatched')
  assert hashlib.sha256((R/'public'/source['sourcePdf'].lstrip('/')).read_bytes()).hexdigest()==paper['sourceSha256']
  for l in asset.get('supplementalLessons',[]):
   assert l['form']==paper['form'] and l['subjectId']==paper['subjectId'];assert len(l['paragraphs'])>=3 and len(l['examples'])>=3
   l.update(topicId=l['id'],language=l.get('language','en'),glossary=l.get('glossary',[]),diagram=l.get('diagram'),curriculumStatus='supplemental-legacy-prerequisite',publicationStatus='published',completionStatus='supplemental-revision');upsert('lessons',l)
   for b in data['books']:
    if b['subjectId']==l['subjectId'] and b['form']==l['form'] and l['id'] not in b['lessonIds']:b['lessonIds'].append(l['id'])
  assert len({q['id'] for q in qs})==len(qs),'Duplicate source record ID'
  for q in qs:
   q['type']={'short-answer':'short','short_answer':'short','written':'short'}.get(q['type'],q['type'])
   assert q['paperId']==paper['id'] and q['form']==paper['form'] and q['subjectId']==paper['subjectId']
   assert q['sourceSha256']==source['sha256'] and q['sourcePdf']==source['sourcePdf']
   assert q.get('content') and q.get('sourcePages') and all(1<=p<=source['pageCount'] for p in q['sourcePages'])
   q.setdefault('media',[])
   for page in q['sourcePages']:
    if not any(m.get('path')==source['pageImages'][page-1] for m in q['media']):q['media'].append(dict(path=source['pageImages'][page-1],alt=f'Complete unchanged original source page {page}.',role='source-page'))
   q['sourceTextSha256']=text_hash(q);q['transcriptionBatch']=path.name;q['sourceDocumentId']=source['id']
   q['mainQuestionNumber']=str(q.get('mainQuestionNumber') or re.match(r'\d+',str(q['questionNumber']))[0])
   marking=q.get('sourceMarkingResource',{})
   if isinstance(marking,dict):marking=marking.get('sourcePdf') or marking.get('pdf')
   guide=q.get('answerGuidePdf') or q.get('sourceMarkingGuidePdf') or q.get('markingSourcePdf') or marking
   if guide:q['answerGuidePdf']=guide
   if q.get('publicationStatus')=='published':
    assert q.get('verificationStatus')=='verified' and q.get('maximumMarks') and q.get('markIncrement') and q.get('marksProvenance') and q.get('answerKey') and q.get('markingGuide'),(q['id'],'Missing verified scoring data')
    assert q.get('rightsStatus')=='cleared' and q.get('rightsEvidence')
  # A shared passage/dependent group must never be partly admitted to scored selection.
  groups={}
  for q in qs:groups.setdefault(q.get('groupId') or q['id'],[]).append(q)
  for group in groups.values():
   if any(q.get('publicationStatus')!='published' for q in group):
    for q in group:
     if q.get('publicationStatus')=='published':q.update(publicationStatus='draft',verificationStatus='held-group',sourceIssue='A linked item is unresolved; preserve the complete group outside scored tests.')
  for q in qs:upsert('questions',q)
  published=[q for q in qs if q['publicationStatus']=='published'];all_ids=[q['id'] for q in qs]
  declared_complete=bool(paper.get('completePaper'))
  paper.update(questionIds=[q['id'] for q in published],allTranscribedQuestionIds=all_ids,draftQuestionIds=[q['id'] for q in qs if q['publicationStatus']!='published'],maximumMarks=sum(q['maximumMarks'] for q in published),transcriptionComplete=True,completeScoredPaper=declared_complete and len(published)==len(qs),completePaper=declared_complete and len(published)==len(qs),sourceDocumentId=source['id'],publicationScope='complete-paper' if declared_complete and len(published)==len(qs) else 'selected-questions')
  if paper.get('completePaper') and paper.get('sourceMaximumMarks') is not None:assert paper['maximumMarks']==paper['sourceMaximumMarks'],(paper['id'],'Complete paper mark total mismatch')
  paper['publicationStatus']='published' if published else 'draft'
  if published:paper['verificationStatus']='verified'
  upsert('papers',paper)
  source.update(interactivePaperId=paper['id'] if published else None,questionTranscriptionStatus='complete-transcription',transcribedRecords=len(qs),scoredRecords=len(published),completeScoredPaper=paper['completeScoredPaper'])
  report.append(dict(paperId=paper['id'],transcribed=len(qs),scored=len(published),marks=paper['maximumMarks'],completeScoredPaper=paper['completeScoredPaper']))
 for support in sorted((R/'content/batches').glob('*source-revision-support.json')):
  for q in json.loads(support.read_text()).get('questions',[]):
   assert q['sourceType']=='original' and q['paperId'] is None and q['rightsStatus']=='original'
   upsert('questions',q)
 data['version']='0.6.0';errors=validate(data)
 if errors:raise ValueError('\n'.join(errors))
 return data,report
if __name__=='__main__':
 files=[pathlib.Path(x) for x in sys.argv[1:]] if len(sys.argv)>1 else sorted((R/'content/batches').glob('interactive-*.json'))
 p=R/'content/library.json';d,report=merge(json.loads(p.read_text()),files);p.write_text(json.dumps(d,ensure_ascii=False,indent=2));(R/'content/interactive-conversion-report.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
