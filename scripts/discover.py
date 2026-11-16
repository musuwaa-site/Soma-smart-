import urllib.request, re, json, pathlib
from urllib.parse import urljoin
p=pathlib.Path('acquisition'); urls=['https://www.tie.go.tz/publications/academic-publications','https://www.necta.go.tz/publications/all','https://www.necta.go.tz/pages/ftna']
rows=[]
for n,url in enumerate(urls):
 try:
  data=urllib.request.urlopen(url,timeout=25).read(); (p/f'discovery-{n}.html').write_bytes(data)
  links=[urljoin(url,x) for x in re.findall(r'href=[\"\']([^\"\']+)',data.decode(errors='replace')) if any(k in x.lower() for k in ['pdf','syll','curricul','2023','2025','2024','ftna','secondary'])]
  rows.append({'url':url,'file':f'acquisition/discovery-{n}.html','links':links}); print(url, json.dumps(links),flush=True)
 except Exception as e: rows.append({'url':url,'error':str(e)})
(p/'discovery.json').write_text(json.dumps(rows,indent=2))
