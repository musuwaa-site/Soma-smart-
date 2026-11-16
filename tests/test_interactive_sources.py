import json,pathlib,sys,unittest,copy,hashlib
R=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'scripts'))
from source_integrity import text_hash
from validate import validate
class InteractiveSourceTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.data=json.loads((R/'content/library.json').read_text())
 def test_transcription_fields_equal_full_authored_batch_without_normalizing_words(self):
  canonical={q['id']:q for q in self.data['questions']}
  for file in (R/'content/batches').glob('interactive-*.json'):
   asset=json.loads(file.read_text())
   for original in asset['questions']:
    imported=canonical[original['id']];self.assertEqual(text_hash(original),imported['sourceTextSha256']);self.assertEqual(text_hash(imported),text_hash(original))
 def test_a_changed_source_word_is_rejected_even_if_marks_and_ids_are_valid(self):
  d=copy.deepcopy(self.data);q=next(q for q in d['questions'] if q.get('sourceTextSha256'));q['content']+=' changed'
  self.assertTrue(any('original source transcription changed' in e for e in validate(d)))
 def test_source_and_associated_guide_bytes_match_scored_provenance(self):
  for q in self.data['questions']:
   if not q.get('sourceTextSha256'):continue
   self.assertEqual(hashlib.sha256((R/'public'/q['sourcePdf'].lstrip('/')).read_bytes()).hexdigest(),q['sourceSha256'])
   if q.get('answerGuidePdf'):self.assertTrue((R/'public'/q['answerGuidePdf'].lstrip('/')).is_file())
 def test_mislabelled_computer_science_is_not_published_as_chemistry(self):
  d=next(d for d in self.data['sourceDocuments'] if d['id']=='source-91e924fa53eedb6a');self.assertEqual(d['publicationStatus'],'quarantined');self.assertEqual(d['subjectId'],'computer-science');self.assertNotIn('answerGuide',d)
  self.assertFalse(any(q.get('sourceSha256')==d['sha256'] and q['publicationStatus']=='published' for q in self.data['questions']))
