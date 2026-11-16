"""Export all current original manuscripts as deterministic EPUB 3 books.
Partial manuscripts are explicitly labelled partial; this never changes completion flags.
"""
import json,pathlib,zipfile,html,hashlib
ROOT=pathlib.Path(__file__).resolve().parents[1];OUT=ROOT/'public/books';OUT.mkdir(parents=True,exist_ok=True)
D=json.loads((ROOT/'content/library.json').read_text());lessons={l['id']:l for l in D['lessons']};subjects={s['id']:s for s in D['subjects']}
def e(value):return html.escape(str(value))
def answer(q):
 value=q['answerKey']
 return '; '.join(f'{k}: {v}' for k,v in value.items()) if isinstance(value,dict) else str(value)
def page(title,body,lang):return f'<?xml version="1.0" encoding="UTF-8"?><html xmlns="http://www.w3.org/1999/xhtml" lang="{lang}" xml:lang="{lang}"><head><title>{e(title)}</title><link rel="stylesheet" type="text/css" href="../style.css"/></head><body>{body}</body></html>'
def write(z,name,data,stored=False):
 info=zipfile.ZipInfo(name,(2026,11,16,0,0,0));info.compress_type=zipfile.ZIP_STORED if stored else zipfile.ZIP_DEFLATED;z.writestr(info,data.encode() if isinstance(data,str) else data)
exports=[]
for b in D['books']:
 lang=subjects[b['subjectId']]['language'];status='Partial development manuscript — not a complete syllabus textbook.' if lang=='en' else 'Muswada wa maendeleo usiokamilika — si kitabu chenye mtaala wote.'
 title=b['title']+' (partial manuscript)';files={};nav=[];images={};spine=[]
 intro=f'<h1>{e(title)}</h1><p>{e(status)}</p><p>Original SomaSmart content • {e(D["version"])} • Form {b["form"]}</p><p>{e(b.get("introduction","Jifunze maelezo, mifano na mazoezi katika sura zinazofuata." if lang=="sw" else "Read explanations, examples and exercises in the chapters below."))}</p>'
 files['text/introduction.xhtml']=page(title,intro,lang);nav.append(('text/introduction.xhtml','About this manuscript'));spine.append('text/introduction.xhtml')
 for n,lid in enumerate(b['lessonIds']):
  l=lessons[lid];qs=[q for q in D['questions'] if lid in q['topicIds'] and q['sourceType']=='original' and q['publicationStatus']=='published' and ((q.get('resourceKind')=='workbook')==(b['kind']=='workbook'))]
  body=f'<h1>{e(l["title"])}</h1>'
  if b['kind']=='textbook':
   body+='<h2>Learning objectives</h2><ul>'+''.join(f'<li>{e(x)}</li>' for x in l['objectives'])+'</ul>'+''.join(f'<p>{e(x)}</p>' for x in l['paragraphs'])
   if l.get('diagram'):
    source=ROOT/'public'/l['diagram'].lstrip('/');name='images/'+source.name;images[name]=source.read_bytes();body+=f'<figure><img src="../{name}" alt="{e(l.get("diagramAlt",l["title"]+" schematic"))}"/><figcaption>Original schematic; not to scale.</figcaption></figure>'
   body+='<h2>Worked examples</h2>'+''.join(f'<section><h3>Example {i+1}</h3><p>{e(x)}</p></section>' for i,x in enumerate(l['examples']))
   terms=[g for g in D['glossary'] if g['lessonId']==lid];body+='<h2>Glossary</h2><dl>'+''.join(f'<dt>{e(g["term"])}</dt><dd>{e(g["definition"])}</dd>' for g in terms)+'</dl>'
  else:body+=f'<p>{e(l["summary"])}</p><p>'+('Jaribu shughuli kwa kujitegemea kabla ya kuangalia majibu. Tumia mwongozo kurekebisha hoja au hatua pungufu.' if lang=='sw' else 'Attempt the tasks independently before turning to the model answers. Use the rubric to review incomplete reasoning.')+'</p>'
  body+='<h2>Practice activities</h2><ol>'+''.join(f'<li><p>{e(q["content"])}</p>'+('<p>'+e(' / '.join(q['options']))+'</p>' if q['options'] else '')+'</li>' for q in qs)+'</ol>'
  body+='<h2>Model answers and feedback</h2><ol>'+''.join(f'<li><p>{e(answer(q))}</p><p>{e(q["markingGuide"])}</p></li>' for q in qs)+'</ol>'
  name=f'text/chapter-{n+1:03}.xhtml';files[name]=page(l['title'],body,lang);nav.append((name,l['title']));spine.append(name)
 if b['kind']=='workbook':
  p=next(x for x in D['papers'] if x['form']==b['form'] and x['subjectId']==b['subjectId'] and x['sourceType']=='original');qs=[next(q for q in D['questions'] if q['id']==id) for id in p['questionIds']];body=f'<h1>Mixed revision test</h1><p>{e(p["instructions"])}</p><p>{p["maximumMarks"]} marks. This is an original SomaSmart test, not a past examination.</p><ol>'+''.join(f'<li><p>{e(q["content"])}</p><p>{e(" / ".join(q["options"]))}</p><p>{q["maximumMarks"]} marks</p></li>' for q in qs)+'</ol><h2>Model answers and rubrics</h2><ol>'+''.join(f'<li><p>{e(answer(q))}</p><p>{e(q["markingGuide"])}</p></li>' for q in qs)+'</ol>';name='text/mixed-test.xhtml';files[name]=page('Mixed revision test',body,lang);nav.append((name,'Mixed revision test'));spine.append(name)
 nav_body='<h1>Contents</h1><nav xmlns:epub="http://www.idpf.org/2007/ops" epub:type="toc" id="toc"><ol>'+''.join(f'<li><a href="../{href}">{e(label)}</a></li>' for href,label in nav)+'</ol></nav>';files['text/nav.xhtml']=page('Contents',nav_body,lang)
 files['style.css']='body{font-family:serif;line-height:1.6;margin:1em}h1,h2,h3{color:#125b4b}img{max-width:100%}dt{font-weight:bold}li{margin-bottom:1em}p{orphans:2;widows:2}'
 manifest=[];identifiers={}
 for i,name in enumerate(files):
  id=f'item-{i}';identifiers[name]=id;media='application/xhtml+xml' if name.endswith('.xhtml') else 'text/css';prop=' properties="nav"' if name=='text/nav.xhtml' else '';manifest.append(f'<item id="{id}" href="{name}" media-type="{media}"{prop}/>')
 for i,name in enumerate(images):manifest.append(f'<item id="image-{i}" href="{name}" media-type="image/svg+xml"/>')
 uid='urn:sha256:'+hashlib.sha256((b['id']+json.dumps(files,sort_keys=True)).encode()).hexdigest();package=f'<?xml version="1.0" encoding="UTF-8"?><package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="book-id"><metadata xmlns:dc="http://purl.org/dc/elements/1.1/"><dc:identifier id="book-id">{uid}</dc:identifier><dc:title>{e(title)}</dc:title><dc:creator>SomaSmart</dc:creator><dc:language>{lang}</dc:language><dc:rights>Original SomaSmart educational content; third-party examination text is excluded.</dc:rights><meta property="dcterms:modified">2026-11-16T00:00:00Z</meta></metadata><manifest>'+''.join(manifest)+'</manifest><spine>'+''.join(f'<itemref idref="{identifiers[name]}"/>' for name in spine)+'</spine></package>'
 with zipfile.ZipFile(OUT/(b['id']+'.epub'),'w') as z:
  write(z,'mimetype','application/epub+zip',True);write(z,'META-INF/container.xml','<?xml version="1.0"?><container xmlns="urn:oasis:names:tc:opendocument:xmlns:container" version="1.0"><rootfiles><rootfile full-path="EPUB/package.opf" media-type="application/oebps-package+xml"/></rootfiles></container>');write(z,'EPUB/package.opf',package)
  for name,body in files.items():write(z,'EPUB/'+name,body)
  for name,body in images.items():write(z,'EPUB/'+name,body)
 exports.append(dict(id=b['id'],path='/books/'+b['id']+'.epub',completionStatus=b['completionStatus'],chapterCount=len(b['lessonIds'])))
(OUT/'catalogue.json').write_text(json.dumps(exports,ensure_ascii=False,indent=2));print('Exported',len(exports),'readable EPUB manuscripts; all completion states retained.')
