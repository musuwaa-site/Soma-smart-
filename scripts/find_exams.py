import urllib.request,re,json,pathlib
from urllib.parse import urljoin
P=pathlib.Path('acquisition');rows=[]
urls=['https://maktaba.tetea.org/','https://www.necta.go.tz/publications/ftna','https://www.tie.go.tz/publications/syllabus-for-lower-secondary-academics?page=2']
for n,url in enumerate(urls):
 r={'url':url,'kind':'source-page','rightsStatus':'unresolved'}
 try:
  raw=urllib.request.urlopen(url,timeout=25).read();(P/f'exam-search-{n}.html').write_bytes(raw);links=[urljoin(url,u) for u in re.findall(r'href\s*=\s*[\"\']([^\"\']+)',raw.decode(errors='replace'))];r.update(status='acquired-page',links=links);print(url,json.dumps([x for x in links if any(k in x.lower() for k in ['form','ftna','chem','pdf','exam'])]),flush=True)
 except Exception as e:r.update(status='failed',error=str(e));print(url,str(e),flush=True)
 rows.append(r)
(P/'exam-search.json').write_text(json.dumps(rows,indent=2))
