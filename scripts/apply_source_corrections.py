"""Correct source attribution without modifying any original examination bytes."""
import json,pathlib
R=pathlib.Path(__file__).resolve().parents[1]
def apply(data):
 corrections=json.loads((R/'content/source-corrections.json').read_text())
 for doc in data.get('sourceDocuments',[]):
  fix=corrections.get(doc['id'])
  if not fix:continue
  doc.setdefault('archiveAttribution', {k:doc.get(k) for k in ['title','subjectId','institution','year']})
  if fix.get('removeAnswerGuide') and doc.get('answerGuide'):doc['quarantinedGuideAssociation']=doc.pop('answerGuide')
  doc.update({k:v for k,v in fix.items() if k!='removeAnswerGuide'})
 return data
if __name__=='__main__':
 p=R/'content/library.json';d=apply(json.loads(p.read_text()));p.write_text(json.dumps(d,ensure_ascii=False,indent=2));print('Applied source attribution corrections; original PDFs unchanged.')
