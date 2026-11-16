"""Attach complete original reading materials to standalone exercise records."""
import json,pathlib
R=pathlib.Path(__file__).resolve().parents[1];p=R/'content/library.json';d=json.loads(p.read_text())
indices={'kiswahili-f1-01':2,'english-f1-01':1,'english-f2-inference-summary':1,'kiswahili-f2-insha-muhtasari':2,'kiswahili-f1-kusoma-kamusi':1,'english-f1-information-letters':1}
lessons={l['id']:l for l in d['lessons']};n=0
for q in d['questions']:
 if q['sourceType']!='original' or q.get('passage'):continue
 for lid,index in indices.items():
  if lid in q['topicIds']:
   q['passage']=lessons[lid]['paragraphs'][index];n+=1;break
p.write_text(json.dumps(d,ensure_ascii=False,indent=2));print('Attached full reading context to',n,'original exercise records.')
