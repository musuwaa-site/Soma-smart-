"""Attach original-page interactive practice indexes to the canonical release."""
import json

from validate import ROOT, validate

if __name__ == '__main__':
    library = ROOT / 'content/library.json'
    data = json.loads(library.read_text())
    indexes = json.loads((ROOT / 'content/batches/014-source-practice-index.json').read_text())
    documents = {doc['id']: doc for doc in data['sourceDocuments'] if doc['publicationStatus'] == 'published'}
    if not indexes.keys() <= documents.keys():
        raise SystemExit('Source practice index references an unavailable paper.')
    for source_id, index in indexes.items():
        documents[source_id]['practiceIndex'] = index
    data['version'] = '0.8.0'
    problems = validate(data)
    if problems:
        raise SystemExit('\n'.join(problems))
    library.write_text(json.dumps(data, ensure_ascii=False, indent=2))
