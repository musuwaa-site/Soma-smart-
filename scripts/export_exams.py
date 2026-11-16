"""Create printable original revision papers and independent marking guides.
No downloaded examination text is used or republished by this exporter.
"""
import json,pathlib,html,fitz,hashlib
ROOT=pathlib.Path(__file__).resolve().parents[1];OUT=ROOT/'public/exams';OUT.mkdir(parents=True,exist_ok=True);D=json.loads((ROOT/'content/library.json').read_text());Q={q['id']:q for q in D['questions']}
def e(value):return html.escape(str(value))
def write_pdf(path,body):
 css='body{font-family:serif;font-size:11pt;line-height:1.4}h1{font-size:18pt;color:#125b4b}h2{font-size:13pt}.question{margin:14pt 0}.rubric{color:#365647}li{margin:5pt 0}'
 story=fitz.Story(html=body,user_css=css,archive=fitz.Archive(str(ROOT/'public')));writer=fitz.DocumentWriter(path);rect=fitz.paper_rect('a4');area=rect+(42,42,-42,-42);more=True;pages=0
 while more:
  device=writer.begin_page(rect);more,_=story.place(area);story.draw(device);writer.end_page();pages+=1
  if pages>80:raise RuntimeError('Unexpected paper overflow')
 writer.close()
 doc=fitz.open(path);doc.set_metadata({'title':path.stem,'author':'SomaSmart','creationDate':'D:20261116000000Z','modDate':'D:20261116000000Z'})
 fingerprint=hashlib.sha256(body.encode()).hexdigest()[:32];doc.xref_set_key(-1,'ID',f'[<{fingerprint}><{fingerprint}>]');blob=doc.tobytes(garbage=4,deflate=True,no_new_id=True);doc.close();path.write_bytes(blob);return pages
catalogue=[]
def context(q):
 body=('<blockquote>'+e(q['passage'])+'</blockquote>') if q.get('passage') else ''
 if q.get('table'):body+='<table>'+''.join('<tr>'+''.join('<td>'+e(c)+'</td>' for c in row)+'</tr>' for row in q['table'])+'</table>'
 for m in q.get('media',[]):body+=f'<p><img src="{e(m["path"].lstrip("/"))}" alt="{e(m.get("alt","Question figure"))}" width="380"/></p>'
 return body
for paper in D['papers']:
 if paper.get('sourceType')!='original' or paper.get('publicationStatus')!='published':continue
 sw=paper['subjectId'] in ['kiswahili','historia'];qs=[Q[id] for id in paper['questionIds']]
 heading=f'<h1>{e(paper["title"])}</h1><p>'+('Jaribio asilia la marudio la SomaSmart. Si mtihani wa zamani wa shule wala NECTA. Linahusu sura zilizopo tu.' if sw else 'Original SomaSmart revision test. Not a school or NECTA past examination. Covers the available chapters only.')+'</p>'
 instructions='Jibu maswali yote. Jumla ya alama: ' if sw else 'Answer all questions. Total marks: '
 body=heading+f'<p>{instructions}{paper["maximumMarks"]}.</p>'
 for n,q in enumerate(qs,1):
  body+=f'<div class="question"><h2>{n}. {e(q["content"])} ({q["maximumMarks"]} '+('alama' if sw else 'marks')+')</h2>'
  body+=context(q)
  if q['options']:body+='<ol type="A">'+''.join(f'<li>{e(o)}</li>' for o in q['options'])+'</ol>'
  if q.get('pairs'):body+='<ul>'+''.join(f'<li>{e(p["left"])}</li>' for p in q['pairs'])+'</ul>'
  if not q['options']:body+='<p>..........................................................................................................</p>'*2
  body+='</div>'
 guide=heading+'<h2>'+('Mwongozo wa majibu ulioandaliwa na SomaSmart' if sw else 'Independent model answers and marking guidance')+'</h2><p>'+('Mwongozo huu si mpango rasmi wa NECTA. Kubali majibu mbadala sahihi yanayokidhi swali.' if sw else 'This is not an official NECTA marking scheme. Accept valid alternative responses satisfying each question.')+'</p>'
 for n,q in enumerate(qs,1):
  answer=q['answerKey'];answer='; '.join(f'{k}: {v}' for k,v in answer.items()) if isinstance(answer,dict) else answer
  guide+=f'<div class="question"><h2>{n}. {e(q["content"])}</h2><p>{e(answer)}</p><p class="rubric">{e(q["markingGuide"])}</p><p>{q["maximumMarks"]} '+('alama' if sw else 'marks')+'</p></div>'
 name=paper['id'];pages=write_pdf(OUT/(name+'.pdf'),body);guide_pages=write_pdf(OUT/(name+'-answers.pdf'),guide);catalogue.append(dict(id=name,sourceType='original',path='/exams/'+name+'.pdf',answerPath='/exams/'+name+'-answers.pdf',pages=pages,answerPages=guide_pages))
(OUT/'catalogue.json').write_text(json.dumps(catalogue,indent=2));print('Exported',len(catalogue),'original revision PDFs and',len(catalogue),'independent answer guides.')
