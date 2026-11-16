import unittest,json,pathlib,hashlib,fitz
R=pathlib.Path(__file__).resolve().parents[1]
class SourceLibraryTests(unittest.TestCase):
 def test_full_source_papers_preserve_original_bytes_and_every_page(self):
  data=json.loads((R/'content/library.json').read_text());documents=data.get('sourceDocuments',[]);self.assertGreaterEqual(len(documents),9)
  for d in documents:
   p=R/'public'/d['sourcePdf'].lstrip('/');self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(),d['sha256']);doc=fitz.open(p);self.assertEqual(doc.page_count,d['pageCount']);self.assertEqual(len(d['pageImages']),doc.page_count);self.assertEqual(len(set(d['pageImages'])),doc.page_count)
   for path in d['pageImages']:self.assertTrue((R/'public'/path.lstrip('/')).is_file())
   doc.close()
 def test_documents_do_not_masquerade_as_scored_question_records(self):
  data=json.loads((R/'content/library.json').read_text());qids={q['id'] for q in data['questions']}
  for d in data['sourceDocuments']:self.assertNotIn(d['id'],qids);self.assertEqual(d['contentMode'],'source-document')
 def test_source_answer_guides_include_every_page_and_match_hash(self):
  data=json.loads((R/'content/library.json').read_text());guides=[d['answerGuide'] for d in data['sourceDocuments'] if d.get('answerGuide')];self.assertGreaterEqual(len(guides),33)
  for g in guides:
   p=R/'public'/g['sourcePdf'].lstrip('/');self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(),g['sha256'])
   with fitz.open(p) as doc:self.assertEqual(doc.page_count,g['pageCount']);self.assertEqual(len(g['pageImages']),doc.page_count)
   for path in g['pageImages']:self.assertTrue((R/'public'/path.lstrip('/')).is_file())
 def test_original_reading_exercises_retain_complete_source_context(self):
  data=json.loads((R/'content/library.json').read_text());lessons={l['id']:l for l in data['lessons']}
  for lid,index in [('kiswahili-f1-01',2),('english-f1-01',1),('english-f2-inference-summary',1)]:
   qs=[q for q in data['questions'] if lid in q['topicIds'] and q['sourceType']=='original'];self.assertTrue(qs)
   for q in qs:self.assertEqual(q['passage'],lessons[lid]['paragraphs'][index])
if __name__=='__main__':unittest.main()
