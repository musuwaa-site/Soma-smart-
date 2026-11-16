import urllib.request,pathlib,json,re
from html.parser import HTMLParser
from urllib.parse import urljoin
from documents import acquire,extract
class Links(HTMLParser):
 def __init__(self):super().__init__();self.links=[]
 def handle_starttag(self,tag,attrs):
  if tag=='a':
   for k,v in attrs:
    if k=='href':self.links.append(v)
p=pathlib.Path('acquisition');url='https://maktaba.tetea.org/resources/form-1-2/'
raw=urllib.request.urlopen(url,timeout=40).read();(p/'tetea-form12.html').write_bytes(raw);parser=Links();parser.feed(raw.decode());links=[urljoin(url,u) for u in parser.links];candidates=list(dict.fromkeys(u for u in links if '.pdf' in u.lower()));(p/'exam-candidates.json').write_text(json.dumps([{'url':u,'sourcePage':url,'rightsStatus':'unresolved','reviewStatus':'located-not-verified'} for u in candidates],indent=2));print('Actual PDF candidates',len(candidates));print(json.dumps(candidates[:20]),flush=True)
# First vertical extraction batch; no automatic third-party publication.
selected=[]
for subject in ['Chemistry','Physics','Biology','Math','English','Kiswahili','Geography']:
 match=next((u for u in candidates if '/past-papers/' in u and '/'+subject.lower()+'/' in u.lower() and 'solution' not in u.lower()),None)
 if match:selected.append(match)
for u in selected:
 try:
  f=acquire(u,'candidate-paper',u.rsplit('/',1)[-1]);print(u,extract(f),flush=True)
 except Exception as e:print(u,str(e),flush=True)
# Chemistry official URL contains an apostrophe; HTMLParser preserves it.
s=(p/'syllabi-page-2.html').read_text();parser=Links();parser.feed(s)
for u in parser.links:
 if 'CHEMISTRY' in u.upper() and '.pdf' in u.lower():
  try:f=acquire(u,'official-syllabus',u.rsplit('/',1)[-1]);print(u,extract(f),flush=True)
  except Exception as e:print(u,str(e),flush=True)
