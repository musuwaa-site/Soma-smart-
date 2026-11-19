"""Attach original-page interactive practice indexes to the canonical release."""
import json

from validate import ROOT, validate

if __name__ == '__main__':
    library = ROOT / 'content/library.json'
    data = json.loads(library.read_text())
    batches = ROOT / 'content/batches'
    existing = {doc['id']: doc for doc in data['sourceDocuments']}
    indexes = {}
    for filename in ('016-legacy-ftna-sources.json', '017-form-one-sources.json', '018-additional-sources.json', '021-reserve-sources.json', '022-f1-sources.json', '023-f2a-sources.json', '024-f2b-sources.json', '025-f2c-sources.json'):
        for doc in json.loads((batches / filename).read_text())['sourceDocuments']:
            previous = existing.get(doc['id'])
            if previous and previous['sha256'] != doc['sha256']:
                raise SystemExit(f"Conflicting source ID {doc['id']}")
            if previous:
                previous.update(doc)
                if previous['publicationStatus'] != 'published':
                    previous.pop('practiceIndex', None)
            else:
                existing[doc['id']] = doc
                data['sourceDocuments'].append(doc)
    for filename in ('014-source-practice-index.json', '017-form-one-index.json', '018-additional-index.json', '021-reserve-index.json', '022-f1-index.json', '023-f2a-index.json', '024-f2b-index.json', '025-f2c-index.json'):
        batch = json.loads((batches / filename).read_text())
        if indexes.keys() & batch.keys():
            raise SystemExit(f'Duplicate practice index in {filename}')
        indexes.update(batch)
    documents = {doc['id']: doc for doc in data['sourceDocuments'] if doc['publicationStatus'] == 'published'}
    if not indexes.keys() <= documents.keys():
        raise SystemExit('Source practice index references an unavailable paper.')
    for source_id, index in indexes.items():
        documents[source_id]['practiceIndex'] = index
    guides = {}
    for filename in ('015-independent-marking-guides.json', '019-milestone-guides.json', '020-additional-guides.json'):
        batch = json.loads((batches / filename).read_text())
        if guides.keys() & batch.keys():
            raise SystemExit(f'Duplicate independent guide in {filename}')
        guides.update(batch)
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
    from import_kigoma_business import apply
    data = apply(data)
    from import_markaz_math import apply as apply_math
    apply_math(data)
    explanations = {}
    for filename in ('028-objective-explanations.json', '029-matching-explanations.json', '030-written-science-explanations.json', '031-written-language-explanations.json', '032-written-other-explanations.json'):
        explanations.update(json.loads((batches / filename).read_text()))
    for question in data['questions']:
        if question['id'] in explanations:
            question['feedbackExplanation'] = explanations.pop(question['id'])
    if explanations:
        raise SystemExit('Feedback references missing questions')
    data['version'] = '0.14.0'
    problems = validate(data)
    if problems:
        raise SystemExit('\n'.join(problems))
    library.write_text(json.dumps(data, ensure_ascii=False, indent=2))
