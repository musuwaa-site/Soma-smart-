"""Bundle complete owner-authorized papers and associated source answer guides.
PDF bytes are preserved; every page is rendered without cropping or summarising questions.
"""
import json,pathlib,hashlib,shutil,fitz
ROOT=pathlib.Path(__file__).resolve().parents[1];p=ROOT/'content/library.json';d=json.loads(p.read_text());docs=[];folders={x.name:x for x in (ROOT/'acquisition/documents').iterdir() if (x/'source.json').exists()};metadata={id:json.loads((f/'source.json').read_text()) for id,f in folders.items()}
subjects={'BasicMath':'mathematics','Chemistry':'chemistry','Physics':'physics','Biology':'biology','English':'english','Kiswahili':'kiswahili','Geography':'geography','BusinessStudies':'business','HistoriaYaTanzaniaNaMaadili':'historia'}
def bundle(m,kind='source-document'):
 folder=folders[m['id']];raw=(folder/'original.pdf').read_bytes();assert hashlib.sha256(raw).hexdigest()==m['sha256'],'Source bytes changed.';assert m.get('rightsStatus')=='cleared' and m.get('rightsEvidence'),'Owner authorization must be retained.'
 id=('guide-' if kind=='source-marking-guide' else 'source-')+m['id'];out=ROOT/'public/source-papers'/id;out.mkdir(parents=True,exist_ok=True)
 if not (out/'original.pdf').exists():shutil.copyfile(folder/'original.pdf',out/'original.pdf')
 pdf=fitz.open(stream=raw,filetype='pdf');pages=[]
 for n,page in enumerate(pdf,1):
  name=f'page-{n:03}.jpg'
  if not (out/name).exists():page.get_pixmap(matrix=fitz.Matrix(1.45,1.45)).save(out/name,jpg_quality=80)
  pages.append('/source-papers/'+id+'/'+name)
 return dict(id=id,sha256=m['sha256'],sourcePdf='/source-papers/'+id+'/original.pdf',pageImages=pages,pageCount=len(pages),sourceReference=m.get('url'),rightsStatus='cleared',rightsEvidence=m['rightsEvidence'],contentMode=kind)
for id,m in sorted(metadata.items()):
 if m['category']!='candidate-paper':continue
 title=m['sourceTitle'];form=m.get('form');sid=m.get('subjectId')
 if form!=1:
  sid=next((v for k,v in subjects.items() if title.startswith(k+'-F2-2025') or title.startswith(k+'-F2-Vocational-2025')),None);form=2
 if sid not in {x['id'] for x in d['subjects']}:continue
 source=bundle(m);subject=next(s['name'] for s in d['subjects'] if s['id']==sid);stream='vocational' if 'Vocational' in title else 'legacy-general' if form==2 else 'school-current-attribution';paper=next((x for x in d['papers'] if x.get('sourceSha256')==m['sha256']),None);year=m.get('year',2025 if form==2 else None);year_basis=m.get('yearBasis','Printed source/year filename');issuer=m.get('institution','NECTA (archive attribution and printed source)' if form==2 else 'Issuing institution not confirmed')
 source.update(title=m.get('sourceTitle') if form==1 else f'{subject} • Form Two • 2025'+(' • Vocational' if stream=='vocational' else ''),form=form,subjectId=sid,year=year,yearBasis=year_basis,sourceType=m.get('sourceType','necta' if form==2 else 'school'),institution=issuer,curriculumStream=stream,publicationStatus='published',questionTranscriptionStatus='selected-questions-integrated' if paper else 'not-yet-structured',interactivePaperId=paper['id'] if paper else None,note='Complete original pages, with all questions, subparts, diagrams and instructions preserved.'+(' Vocational-stream source: use matching topics.' if stream=='vocational' else '')+(' Year is archive attribution where the paper header does not state it.' if 'archive' in str(year_basis).lower() else ''))
 associated=m.get('associatedSourceId')
 if associated and associated in metadata and metadata[associated].get('category')=='marking-resource':
  guide=metadata[associated];assert guide.get('associatedSourceId')==m['id'],'Paper/guide association must match the source listing.';source['answerGuide']={**bundle(guide,'source-marking-guide'),'title':'Source-provided answer guide','provenance':guide.get('solutionProvenance','Issuing district/archive-provided marking resource; not an official NECTA scheme'),'associatedSourceId':m['id'],'associationEvidence':guide.get('sourcePage',guide.get('url'))}
 docs.append(source)
existing={x['id']:i for i,x in enumerate(d.get('sourceDocuments',[]))};d.setdefault('sourceDocuments',[])
for item in docs:
 if item['id'] in existing:d['sourceDocuments'][existing[item['id']]]=item
 else:d['sourceDocuments'].append(item)
p.write_text(json.dumps(d,ensure_ascii=False,indent=2));(ROOT/'content/batches/008-offline-source-library.json').write_text(json.dumps({'sourceDocuments':docs},ensure_ascii=False,indent=2));print('Bundled',len(docs),'complete papers;',sum(x['pageCount'] for x in docs),'paper pages;',sum('answerGuide' in x for x in docs),'complete answer guides.')
