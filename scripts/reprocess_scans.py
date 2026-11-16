import pathlib,json
from documents import extract
P=pathlib.Path('acquisition/documents')
for p in P.glob('*/source.json'):
 d=json.loads(p.read_text())
 if '/syllabi/' in d['url']:
  d['category']='archive-syllabus-reference';p.write_text(json.dumps(d,indent=2))
 if d['sourceTitle'] in ['Chemistry-F2-2025.pdf','BasicMath-F2-2025.pdf']:
  print(d['sourceTitle'],extract(p.parent),flush=True)
