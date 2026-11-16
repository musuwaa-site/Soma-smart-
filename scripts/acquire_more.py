import urllib.request,re,pathlib,json,hashlib,datetime
from urllib.parse import urljoin
p=pathlib.Path('acquisition'); rows=[]
urls=['https://www.tie.go.tz/publications/syllabus-for-lower-secondary-academics','https://www.tie.go.tz/publications/curriculum-for-lower-secondary-academic','https://onlinesys.necta.go.tz/cira/ftna/2023/','https://onlinesys.necta.go.tz/cira/ftna/2022/','https://necta.go.tz/exam_formarts/FTNA.pdf']
for i,url in enumerate(urls):
 row={'id':f'official-{i}','url':url,'checkedAt':datetime.datetime.now(datetime.timezone.utc).isoformat(),'rightsStatus':'unresolved','publicationStatus':'draft'}
 try:
  raw=urllib.request.urlopen(url,timeout=25).read(); pdf=raw.startswith(b'%PDF'); fn=p/f'official-{i}.{ "pdf" if pdf else "html"}'; fn.write_bytes(raw)
  row.update(status='acquired',file=str(fn),sha256=hashlib.sha256(raw).hexdigest(),kind='assessment-format' if pdf else 'source-page')
  if not pdf:row['links']=[urljoin(url,x) for x in re.findall(r'href\s*=\s*[\"\']([^\"\']+)',raw.decode(errors='replace')) if '.pdf' in x.lower()]
 except Exception as e:row.update(status='failed',error=str(e))
 rows.append(row);print(json.dumps(row),flush=True)
(p/'official.json').write_text(json.dumps(rows,indent=2))
