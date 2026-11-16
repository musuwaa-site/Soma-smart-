import unittest,sys,pathlib,json,copy,tempfile,threading,urllib.request,urllib.error,http.cookiejar,os
ROOT=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'));sys.path.insert(0,str(ROOT/'admin'))
from validate import validate
from documents import extract
import server,fitz
class ContentTests(unittest.TestCase):
 def setUp(self):self.d=json.loads((ROOT/'content/library.json').read_text())
 def test_library_integrity(self):self.assertEqual(validate(self.d),[])
 def test_duplicate_rejected(self):
  self.d['questions'].append(self.d['questions'][0]);self.assertTrue(validate(self.d))
 def test_uncleared_source_rejected(self):
  self.d['questions'][0].update(sourceType='necta',rightsStatus='unresolved');self.assertTrue(validate(self.d))
 def test_damaged_marks_rejected(self):
  self.d['questions'][0]['markIncrement']=0;self.assertTrue(validate(self.d))
 def test_missing_media_rejected(self):
  self.d['questions'][0]['media']=[{'path':'/missing.png','alt':'Missing'}];self.assertTrue(validate(self.d))
 def test_extract_real_pdf_preserves_layout_and_review_state(self):
  # Synthetic fixture tests parser behaviour; never counted as an authentic paper.
  with tempfile.TemporaryDirectory() as d:
   p=pathlib.Path(d);doc=fitz.open();page=doc.new_page();page.insert_text((60,60),'1. Calculate the density of a 60 g object with volume 20 cm3.');doc.save(p/'original.pdf');doc.close();pages,n=extract(p);self.assertEqual(pages,1);self.assertEqual(n,1);q=json.loads((p/'extraction.json').read_text())['questions'][0];self.assertEqual(q['publicationStatus'],'draft');self.assertTrue((p/'page-1.png').exists())
class AdminTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  os.environ['SOMASMART_ADMIN_PASSWORD']='test-only-long-password';cls.http=server.ThreadingHTTPServer(('127.0.0.1',0),server.Handler);cls.thread=threading.Thread(target=cls.http.serve_forever,daemon=True);cls.thread.start();cls.base=f'http://127.0.0.1:{cls.http.server_port}'
 @classmethod
 def tearDownClass(cls):cls.http.shutdown();cls.http.server_close()
 def request(self,path,data=None,headers=None,opener=None):
  req=urllib.request.Request(self.base+path,data=json.dumps(data).encode() if data is not None else None,headers={'Content-Type':'application/json',**(headers or {})});return (opener or urllib.request.build_opener()).open(req)
 def test_anonymous_cannot_read_content(self):
  with self.assertRaises(urllib.error.HTTPError) as c:self.request('/api/content')
  self.assertEqual(c.exception.code,401)
 def test_anonymous_cannot_publish(self):
  with self.assertRaises(urllib.error.HTTPError) as c:self.request('/api/publish',{})
  self.assertEqual(c.exception.code,401)
 def test_login_and_csrf_enforcement(self):
  jar=http.cookiejar.CookieJar();opener=urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar));self.request('/api/login',{'password':'test-only-long-password'},opener=opener);data=json.load(self.request('/api/content',opener=opener));self.assertIn('csrf',data)
  with self.assertRaises(urllib.error.HTTPError) as c:self.request('/api/publish',{},opener=opener)
  self.assertEqual(c.exception.code,403)
 def test_cross_origin_login_rejected(self):
  with self.assertRaises(urllib.error.HTTPError) as c:self.request('/api/login',{'password':'test-only-long-password'},{'Origin':'https://attacker.invalid'})
  self.assertEqual(c.exception.code,403)
if __name__=='__main__':unittest.main()
