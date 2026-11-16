import pathlib,json
from documents import extract
for p in pathlib.Path('acquisition/documents').glob('*/source.json'):
 d=json.loads(p.read_text())
 if d['category']=='candidate-paper':
  e=json.loads((p.parent/'extraction.json').read_text())
  if any(x.get('ocrUsed') for x in e['pages']):continue
  print(d['sourceTitle'],extract(p.parent),flush=True)
