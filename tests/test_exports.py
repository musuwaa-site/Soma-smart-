import unittest,pathlib,subprocess,sys,json,zipfile,xml.etree.ElementTree as ET,hashlib,fitz
ROOT=pathlib.Path(__file__).resolve().parents[1]
class ExportTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.data=json.loads((ROOT/'content/library.json').read_text())
  for script in ['export_books.py','export_exams.py']:subprocess.run([sys.executable,str(ROOT/'scripts'/script)],cwd=ROOT,check=True,capture_output=True)
 def test_every_book_is_a_readable_epub_with_truthful_partial_label(self):
  for b in self.data['books']:
   path=ROOT/'public/books'/(b['id']+'.epub')
   with zipfile.ZipFile(path) as z:
    self.assertEqual(z.infolist()[0].filename,'mimetype');self.assertEqual(z.read('mimetype'),b'application/epub+zip');package=ET.fromstring(z.read('EPUB/package.opf'));title=package.find('.//{http://purl.org/dc/elements/1.1/}title').text
    if b['completionStatus']=='partial':self.assertIn('partial',title)
    chapters=[n for n in z.namelist() if '/chapter-' in n];self.assertEqual(len(chapters),len(b['lessonIds']))
    for name in chapters:
     node=ET.fromstring(z.read(name));self.assertGreater(len(' '.join(node.itertext())),500)
 def test_every_original_revision_paper_has_questions_and_independent_guide(self):
  for p in self.data['papers']:
   if p['sourceType']!='original':continue
   for suffix in ['.pdf','-answers.pdf']:
    doc=fitz.open(ROOT/'public/exams'/(p['id']+suffix));text=' '.join(page.get_text() for page in doc);self.assertGreater(len(text),500);self.assertIn('SomaSmart',text);doc.close()
 def test_exports_are_reproducible(self):
  paths=list((ROOT/'public/books').glob('*.epub'))+list((ROOT/'public/exams').glob('*.pdf'));before={p:hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
  for script in ['export_books.py','export_exams.py']:subprocess.run([sys.executable,str(ROOT/'scripts'/script)],cwd=ROOT,check=True,capture_output=True)
  self.assertEqual(before,{p:hashlib.sha256(p.read_bytes()).hexdigest() for p in paths})
if __name__=='__main__':unittest.main()
