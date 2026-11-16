"""Immutable source-transcription fields; scoring corrections stay separate."""
import json,hashlib
TEXT_FIELDS=['questionNumber','originalLabel','sharedContent','content','instructions','passage','options','optionLabels','rawOptions','pairs','table','subquestions','sourceUnderlining','underlinedWords','underlinedTerms']
def text_hash(q):
 return hashlib.sha256(json.dumps({k:q[k] for k in TEXT_FIELDS if k in q},ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
