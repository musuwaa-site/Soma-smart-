import json,urllib.request,re,sys
from documents import acquire,extract
rows=json.load(open('acquisition/official.json')); urls=[u for r in rows[:2] for u in r.get('links',[]) if any(k in u.upper() for k in ['PHYSICS','MATHEMATICS','KISWAHILI','HISTORIA','CURRICULUM'])]
# Follow the real next page, not guessed document URLs.
for pg in [2,3]:
 url=f'https://www.tie.go.tz/publications/syllabus-for-lower-secondary-academics?page={pg}'
 try:
  raw=urllib.request.urlopen(url,timeout=25).read();open(f'acquisition/syllabi-page-{pg}.html','wb').write(raw)
  for u in re.findall(r'href\s*=\s*[\"\']([^\"\']+)',raw.decode(errors='replace')):
   if '.pdf' in u.lower() and any(k in u.upper() for k in ['CHEMISTRY','BIOLOGY','GEOGRAPHY','BUSINESS','ENGLISH LANGUAGE']):urls.append(u)
 except Exception as e:print(url,str(e),flush=True)
for url in dict.fromkeys(urls):
 try:
  folder=acquire(url,'official-syllabus' if 'CURRICULUM' not in url.upper() else 'official-curriculum',url.rsplit('/',1)[-1]);print(url,extract(folder),flush=True)
 except Exception as e:print(url,str(e),flush=True)
