"""Integrate original chapter assets without replacing existing student progress IDs.
Exact repeated original prompts share a record instead of inflating inventory counts.
"""
import json,pathlib,sys,hashlib,re
R=pathlib.Path(__file__).resolve().parents[1];p=R/'content/library.json';D=json.loads(p.read_text());activities={x['id']:x for x in D.get('curriculum',{}).get('activities',[])}
files=[pathlib.Path(x) for x in sys.argv[1:]] if len(sys.argv)>1 else sorted((R/'content/batches').glob('agent-*-books.json'))+sorted((R/'content/batches').glob('agent-*-completion.json'))
def upsert(collection,row):
 index=next((i for i,x in enumerate(D[collection]) if x['id']==row['id']),None)
 if index is None:D[collection].append(row)
 else:D[collection][index]=row

def signature(q):return json.dumps([' '.join(q['content'].split()).casefold(),q.get('passage',''),q.get('options',[])],ensure_ascii=False,sort_keys=True)
known={signature(q):q for q in D['questions'] if q['sourceType']=='original'};added=0;shared=0;chapters=0
for file in files:
 asset=json.loads(file.read_text());rows=asset.get('chapters',[])
 for c in rows:
  lid=c['id'];assert c['form'] in [1,2] and c['subjectId'] in {s['id'] for s in D['subjects']};assert len(c['paragraphs'])>=4 and len(c['examples'])>=3 and len(c['questions'])>=15 and len(c['workbookQuestions'])>=3,(file,lid,'Incomplete asset')
  refs=[]
  for id in c.get('curriculumActivityIds',[]):
   a=activities[id];assert a['form']==c['form'] and a['subjectId']==c['subjectId'];refs.append(dict(activityId=id,sourceId=a['sourceId'],pdfPages=a['pdfPages'],scope='partial-support'))
  l={k:c[k] for k in ['id','subjectId','form','title','language','objectives','paragraphs','examples']};l.update(topicId=lid,glossary=[g['term'] for g in c.get('glossary',[])],diagram=c.get('diagram'),diagramAlt=c.get('diagramAlt',''),summary=c.get('summary',c['paragraphs'][0].split('. ')[0]+'.'),curriculumRefs=refs,curriculumStatus='source-referenced-partial',publicationStatus='published',completionStatus='expanded-chapter',authoringBatch=file.name)
  l['examples']=[' — '.join(str(x[k]) for k in ['title','problem','solution'] if x.get(k)) if isinstance(x,dict) else x for x in l['examples']]
  upsert('lessons',l);chapters+=1
  for n,g in enumerate(c.get('glossary',[]),1):upsert('glossary',dict(id=f'{lid}-term-{n}',lessonId=lid,term=g['term'],definition=g['definition']))
  for kind,items in [('textbook',c['questions']),('workbook',c['workbookQuestions'])]:
   for n,source in enumerate(items,1):
    q=dict(source);id=lid+('-asset-q-' if kind=='textbook' else '-asset-wb-')+str(n);options=q.get('options',[])
    if q.get('type')=='mcq' and q['answerKey'] not in options and q['answerKey'] in ['A','B','C','D','E','F']:
     index=ord(q['answerKey'])-ord('A');assert index<len(options);q['answerKey']=options[index]
    if q.get('type')=='mcq':assert q['answerKey'] in options,(id,'No matching answer option')
    media=list(q.get('media',[]))
    if c.get('diagram') and not any(m['path']==c['diagram'] for m in media):media.append({'path':c['diagram'],'alt':c.get('diagramAlt',c['title']+' original schematic.')})
    q.update(id=id,paperId=None,form=c['form'],subjectId=c['subjectId'],topicIds=[lid],subtopicIds=[lid],sourceType='original',sourceTitle='SomaSmart original revision workbook' if kind=='workbook' else 'SomaSmart original practice',institution='SomaSmart',year=None,curriculumEdition='TIE 2023; referenced original learning content',curriculumRefs=refs,questionNumber=str(n),parentQuestionId=None,instructions=q.get('instructions',''),options=options,media=media,maximumMarks=q.get('maximumMarks',1 if q.get('type')=='mcq' else 2),markIncrement=q.get('markIncrement',1),solutionProvenance='SomaSmart independently authored',sourceReference='Original educational chapter asset '+file.name,rightsStatus='original',verificationStatus='original-authored',publicationStatus='published',resourceKind=kind)
    sig=signature(q);old=known.get(sig)
    if old and old['id']!=id:
     old['topicIds']=list(dict.fromkeys(old['topicIds']+[lid]));old['subtopicIds']=list(dict.fromkeys(old['subtopicIds']+[lid]));shared+=1;continue
    upsert('questions',q);known[sig]=next(x for x in D['questions'] if x['id']==id);added+=1
for b in D['books']:
 b['lessonIds']=[l['id'] for l in D['lessons'] if l['form']==b['form'] and l['subjectId']==b['subjectId']]
 if b['kind']=='workbook':
  bank=[q for q in D['questions'] if q['form']==b['form'] and q['subjectId']==b['subjectId'] and q.get('resourceKind')=='workbook'];groups=[[q['id'] for q in bank if lid in q['topicIds']] for lid in b['lessonIds']];selection=[]
  while len(selection)<20 and any(groups):
   for group in groups:
    while group and group[0] in selection:group.pop(0)
    if group:selection.append(group.pop(0))
    if len(selection)==20:break
  b['mixedTestQuestionIds']=selection
D['version']='0.5.0';p.write_text(json.dumps(D,ensure_ascii=False,indent=2));print('Integrated',chapters,'chapters;',added,'asset assessment records;',shared,'exact repeated prompts shared rather than recounted.')
