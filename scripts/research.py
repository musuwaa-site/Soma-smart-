"""Fetch real source pages, recording failures without inventing acquisitions."""
import urllib.request, json, pathlib, re, datetime
from urllib.parse import urljoin
root=pathlib.Path(__file__).resolve().parents[1]; out=root/'acquisition'; out.mkdir(exist_ok=True)
urls=['https://www.tie.go.tz/','https://www.tie.go.tz/pages/secondary-education','https://www.necta.go.tz/','https://www.necta.go.tz/publications']
rows=[]
for i,url in enumerate(urls):
 row={'url':url,'checkedAt':datetime.datetime.now(datetime.timezone.utc).isoformat(),'rightsStatus':'unresolved','category':'official-source-page'}
 try:
  data=urllib.request.urlopen(url,timeout=30).read(); path=out/f'page-{i}.html'; path.write_bytes(data)
  row.update(status='acquired-page',file=str(path.relative_to(root)),links=[urljoin(url,x) for x in re.findall(r'href=[\"\']([^\"\']+)',data.decode(errors='replace')) if any(k in x.lower() for k in ['pdf','syll','curricul','ftna','publication','secondary'])])
 except Exception as e: row.update(status='failed',error=str(e))
 rows.append(row); print(json.dumps(row),flush=True)
(out/'research.json').write_text(json.dumps(rows,indent=2))
