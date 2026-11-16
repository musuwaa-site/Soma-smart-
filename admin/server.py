"""Separate owner-only authoring server. Student build contains no admin credentials.
Bind localhost; use a TLS reverse proxy for remote access. No default password.
"""
from http.server import ThreadingHTTPServer,BaseHTTPRequestHandler
from http.cookies import SimpleCookie
import os,json,secrets,time,pathlib,sys,hashlib,hmac,tempfile,threading
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]/'scripts'))
from validate import validate,ROOT
SESSIONS={};FAILURES={};LOCK=threading.Lock();WORK=ROOT/'admin/workspace';WORK.mkdir(exist_ok=True)
def atomic(path,data):
 path=pathlib.Path(path);fd,name=tempfile.mkstemp(dir=path.parent)
 try:
  with os.fdopen(fd,'w') as f:json.dump(data,f,ensure_ascii=False,indent=2);f.flush();os.fsync(f.fileno())
  os.replace(name,path)
 finally:
  if os.path.exists(name):os.unlink(name)
def publish(data):
 errors=validate(data)
 if errors:raise ValueError('\n'.join(errors))
 atomic(ROOT/'content/library.json',data)
class Handler(BaseHTTPRequestHandler):
 def log_message(self,fmt,*args):pass
 def reply(self,status,data,ctype='application/json',cookie=None):
  body=data.encode() if isinstance(data,str) else json.dumps(data).encode();self.send_response(status);self.send_header('Content-Type',ctype);self.send_header('Cache-Control','no-store');self.send_header('X-Content-Type-Options','nosniff');self.send_header('Content-Security-Policy',"default-src 'self'; script-src 'self'; style-src 'self'; frame-ancestors 'none'")
  if cookie:self.send_header('Set-Cookie',cookie)
  self.send_header('Content-Length',str(len(body)));self.end_headers();self.wfile.write(body)
 def session(self):
  c=SimpleCookie();c.load(self.headers.get('Cookie',''));token=c.get('soma_owner');s=SESSIONS.get(token.value if token else '')
  return s if s and s['expires']>time.time() else None
 def do_GET(self):
  if self.path in ['/','/admin.js','/admin.css']:
   filename={'/':'index.html','/admin.js':'admin.js','/admin.css':'admin.css'}[self.path];ctype={'/':'text/html','/admin.js':'text/javascript','/admin.css':'text/css'}[self.path];return self.reply(200,(ROOT/'admin'/filename).read_text(),ctype)
  s=self.session()
  if not s:return self.reply(401,{'error':'Owner authentication required'})
  if self.path=='/api/content':
   p=WORK/'draft.json';return self.reply(200,{'csrf':s['csrf'],'content':json.loads((p if p.exists() else ROOT/'content/library.json').read_text())})
  if self.path=='/api/sources':return self.reply(200,[json.loads(p.read_text()) for p in (ROOT/'acquisition/documents').glob('*/source.json')])
  return self.reply(404,{'error':'Not found'})
 def do_POST(self):
  # Same-origin required even on login, blocking cross-site cookie/session tricks.
  origin=self.headers.get('Origin');host=self.headers.get('Host')
  if origin and origin not in ['http://'+host,'https://'+host]:return self.reply(403,{'error':'Origin rejected'})
  try:
   length=int(self.headers.get('Content-Length','0'))
   if length>8_000_000:return self.reply(413,{'error':'Payload too large'})
   payload=json.loads(self.rfile.read(length))
   if self.path=='/api/login':
    peer=self.client_address[0];now=time.time();recent=[t for t in FAILURES.get(peer,[]) if now-t<300]
    if len(recent)>=10:return self.reply(429,{'error':'Too many attempts; retry in five minutes'})
    expected=os.environ.get('SOMASMART_ADMIN_PASSWORD','');given=payload.get('password','')
    if not expected or not hmac.compare_digest(hashlib.sha256(given.encode()).digest(),hashlib.sha256(expected.encode()).digest()):FAILURES[peer]=recent+[now];return self.reply(401,{'error':'Invalid owner password'})
    token=secrets.token_urlsafe(32);SESSIONS[token]={'expires':now+3600,'csrf':secrets.token_urlsafe(32)};secure='; Secure' if os.getenv('SOMASMART_ADMIN_SECURE')=='1' else ''
    return self.reply(200,{'ok':True},cookie=f'soma_owner={token}; HttpOnly; SameSite=Strict; Path=/; Max-Age=3600{secure}')
   s=self.session()
   if not s:return self.reply(401,{'error':'Owner authentication required'})
   if not hmac.compare_digest(self.headers.get('X-CSRF-Token',''),s['csrf']):return self.reply(403,{'error':'CSRF token required'})
   if self.path=='/api/draft':atomic(WORK/'draft.json',payload);return self.reply(200,{'ok':True})
   if self.path=='/api/publish':
    with LOCK:publish(payload)
    return self.reply(200,{'ok':True,'message':'Source content validated and updated. Run npm run build and release checks before distributing.'})
   return self.reply(404,{'error':'Not found'})
  except (ValueError,KeyError,TypeError) as e:return self.reply(400,{'error':str(e)})
if __name__=='__main__':
 if len(os.environ.get('SOMASMART_ADMIN_PASSWORD',''))<16:raise SystemExit('Set SOMASMART_ADMIN_PASSWORD to a unique password of at least 16 characters.')
 print('Owner authoring: http://127.0.0.1:8765');ThreadingHTTPServer(('127.0.0.1',8765),Handler).serve_forever()
