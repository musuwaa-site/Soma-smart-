"""Attach answerable subparts to the indexed original pages of a paper."""
import hashlib
import json
from pathlib import Path
from source_integrity import text_hash

ROOT = Path(__file__).resolve().parents[1]


def apply(data):
    sources = {doc['id']: doc for doc in data['sourceDocuments']}
    for path in sorted((ROOT / 'content/conversions').glob('source-*.json')):
        body = json.loads(path.read_text())
        doc = sources[path.stem]
        paper_id = 'page-items-' + path.stem
        assert doc['publicationStatus'] == 'published' and body['sourceId'] == doc['id'] and doc['sha256'].startswith(doc['id'].removeprefix('source-'))
        assert doc.get('interactivePaperId') in (None, paper_id), doc['id']
        groups = doc['practiceIndex']['groups']
        assert set(body['groups']) == {g['label'] for g in groups}, doc['id']
        common = {k: doc[k] for k in ('form','subjectId','sourceType','year','institution',
            'sourceReference','sourcePdf','rightsStatus','rightsEvidence','publicationStatus')}
        common.update(sourceDocumentId=doc['id'], sourceSha256=doc['sha256'], verificationStatus='verified')
        records = []
        review = []
        order = []
        for group in groups:
            label = group['label']
            items = body['groups'][label]
            assert items and len(set(x['label'] for x in items)) == len(items), (path, label)
            pages = list(range(group['firstPage'], group['lastPage']+1))
            for item in items:
                tag = hashlib.sha256((label+'|'+item['label']).encode()).hexdigest()[:16]
                kind = {'mcq':'mcq','matching':'matching','written':'short','review':'short'}[item['type']]
                pairs = item.get('pairs', [])
                explanation = item['explanation'].strip()
                assert explanation and item['answer'], (path, item['label'])
                record = dict(common, id=f'{paper_id}-{tag}', paperId=paper_id,
                    groupId=f'{paper_id}-{label}', questionNumber=item['label'], mainQuestionNumber=label,
                    type=kind, content='Question on the original page', sourcePagePrompt=True,
                    sourceTitle=doc['title'], topicIds=[], subtopicIds=[], options=item.get('options', []),
                    sourcePages=pages, media=[dict(role='printed-question',path=doc['pageImages'][n-1],
                    alt=f"{doc['title']}, page {n}") for n in pages],
                    answerKey=item['answer'], requiresDrawing=bool(item.get('requiresDrawing')), markingGuide=explanation, feedbackExplanation=explanation,
                    solutionProvenance='Independent SomaSmart practice solution',
                    marksProvenance='Independent practice points', maximumMarks=len(pairs) or 1,
                    markIncrement=1 if kind != 'short' else 0.5)
                if kind == 'matching':
                    record['pairs'] = [dict(id=k,left=k) for k in pairs]
                if item.get('acceptedAnswers'):
                    record['acceptedAnswerKeys'] = item['acceptedAnswers']
                record['sourceTextSha256'] = text_hash(record)
                order.append(record['id'])
                if item['type'] == 'review':
                    record.update(reviewOnly=True, maximumMarks=0)
                    review.append(record)
                else:
                    records.append(record)
        ids = [q['id'] for q in records]
        paper = dict(common, id=paper_id, title=doc['title'], questionIds=ids, draftQuestionIds=[],
            reviewOnlyItems=review, practiceOrder=order, completePaper=not review, completeScoredPaper=not review, transcriptionComplete=False,
            totalSourceMainQuestions=len(groups), maximumMarks=sum(q['maximumMarks'] for q in records),
            practiceScoring=True, sourceInstructions=['Use the original printed instructions. SomaSmart awards one practice point per response or matched pair. Written answers allow half credit.'])
        data['questions'] = [q for q in data['questions'] if q.get('paperId') != paper_id] + records
        data['papers'] = [p for p in data['papers'] if p['id'] != paper_id] + [paper]
        doc.update(interactivePaperId=paper_id, questionTranscriptionStatus='page-backed-answerable-items')
