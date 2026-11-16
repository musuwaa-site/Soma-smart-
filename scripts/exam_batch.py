import json,pathlib,urllib.request,concurrent.futures,datetime
from documents import acquire,extract
P=pathlib.Path('acquisition');rows=json.loads((P/'exam-candidates.json').read_text());links=[r['url'] for r in rows if '/past-papers/' in r['url'] and not any(s in r['url'].lower() for s in ['solution','answer','marking'])];subjects=['chemistry','physics','biology','math','english','kiswahili','geography','business-studies','historia-ya-tanzania-na-maadili'];selected=[next(u for u in links if '/'+s+'/' in u) for s in subjects]
# Fix overbroad first discovery selection: syllabus references are not papers.
for f in (P/'documents').glob('*/source.json'):
 d=json.loads(f.read_text())
 if '/syllabi/' in d['url']:d['category']='archive-syllabus-reference';f.write_text(json.dumps(d,indent=2))
# Investigate real candidate URLs independently, recording HTTP checks, not content verification.
def check(url):
 r={'url':url,'sourcePage':'https://maktaba.tetea.org/resources/form-1-2/','rightsStatus':'unresolved','verificationStatus':'not-content-verified','checkedAt':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 try:
  response=urllib.request.urlopen(urllib.request.Request(url,method='HEAD'),timeout=20);r.update(httpStatus=response.status,contentType=response.headers.get('Content-Type'),status='reachable')
 except Exception as e:r.update(status='failed',error=str(e))
 return r
with concurrent.futures.ThreadPoolExecutor(max_workers=12) as pool:
 checks=list(pool.map(check,links[:360]))
(P/'candidate-checks.json').write_text(json.dumps(checks,indent=2));print('Checked',len(checks),'real paper URLs;',sum(r['status']=='reachable' for r in checks),'reachable',flush=True)
for u in selected:
 try:
  f=acquire(u,'candidate-paper',u.rsplit('/',1)[-1]);print(u,extract(f),flush=True)
 except Exception as e:print(u,str(e),flush=True)
