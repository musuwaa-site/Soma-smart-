"""Attach original-page interactive practice indexes to the canonical release."""
import json

from validate import ROOT, validate

if __name__ == '__main__':
    library = ROOT / 'content/library.json'
    data = json.loads(library.read_text())
    new_sources = json.loads((ROOT / 'content/batches/016-legacy-ftna-sources.json').read_text())['sourceDocuments']
    existing = {doc['id'] for doc in data['sourceDocuments']}
    data['sourceDocuments'].extend(doc for doc in new_sources if doc['id'] not in existing)
    indexes = json.loads((ROOT / 'content/batches/014-source-practice-index.json').read_text())
    documents = {doc['id']: doc for doc in data['sourceDocuments'] if doc['publicationStatus'] == 'published'}
    if not indexes.keys() <= documents.keys():
        raise SystemExit('Source practice index references an unavailable paper.')
    for source_id, index in indexes.items():
        documents[source_id]['practiceIndex'] = index
    guides = json.loads((ROOT / 'content/batches/015-independent-marking-guides.json').read_text())
    for source_id, guide in guides.items():
        doc = documents[source_id]
        if guide['sourceSha256'] != doc['sha256']:
            raise SystemExit('Independent guide source hash mismatch.')
        labels = {group['label'] for group in doc['practiceIndex']['groups']}
        if not guide['groups'].keys() <= labels:
            raise SystemExit('Independent guide references an invalid question.')
        for group in guide['groups'].values():
            if group['maximumMarks'] != sum(part['marks'] for part in group['parts']):
                raise SystemExit('Independent guide has inconsistent marks.')
        doc['independentPracticeGuide'] = guide
    data['version'] = '0.10.0'
    problems = validate(data)
    if problems:
        raise SystemExit('\n'.join(problems))
    library.write_text(json.dumps(data, ensure_ascii=False, indent=2))
