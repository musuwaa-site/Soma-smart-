"""Apply checked marking evidence while preserving the transcription batches."""
import json
from pathlib import Path

from source_integrity import TEXT_FIELDS, text_hash

BATCHES = Path(__file__).resolve().parents[1] / 'content/batches'


def resolve(paper, questions, lessons):
    by_id = {q['id']: q for q in questions}
    evidence = json.loads((BATCHES / 'held-resolution-evidence.json').read_text())
    for record in evidence['recommendations']:
        ids = record['questionIds']
        if set(ids) <= by_id.keys() and record['status'] == 'conditional-whole-main-aggregation':
            # The guide confirms the 10-mark total but contradicts it with “@2”.
            # Use an independent equal-credit practice rubric within that total.
            for identifier in ids:
                question = by_id[identifier]
                assert question['sourceSha256'] == record['sourceSha256']
                assert text_hash(question) == record['originalTranscriptionDigests'][identifier]
                question.update(answerKey=record['proposedSolution'][identifier],
                                maximumMarks=1, markIncrement=1,
                                marksProvenance='Source guide gives 10 marks for Question 1. Each of the ten items receives one mark under the independent SomaSmart practice rubric.',
                                markingGuide='Award one practice mark for the accepted option.',
                                solutionProvenance='Independently checked SomaSmart answer and practice rubric.',
                                guideDiscrepancy='The guide specifies both a 10-mark total and two marks per item for ten items. The practice rubric preserves the 10-mark source total. The accepted answers were checked against the original options.',
                                publicationStatus='published', verificationStatus='verified',
                                scoringEligible=True)
                question.pop('sourceIssue', None)
            continue
        if not set(ids) <= by_id.keys() or record['status'] not in {
            'resolved', 'resolved-with-explicit-multiple-accepted-keys'
        }:
            continue
        for identifier in ids:
            question = by_id[identifier]
            assert question['sourceSha256'] == record['sourceSha256']
            assert text_hash(question) == record['originalTranscriptionDigests'][identifier]

            def value(key):
                item = record[key]
                return item.get(identifier, item) if isinstance(item, dict) else item

            answer = value('proposedSolution')
            if isinstance(answer, dict):
                answer = '\n'.join(f'{direction.title()} {number}. {word}'
                                   for direction in ('across', 'down')
                                   for number, word in answer[direction].items())
            if isinstance(answer, list):
                question['acceptedAnswerKeys'] = answer
                answer = answer[0]
            question.update(answerKey=answer, maximumMarks=value('proposedMaximumMarks'),
                            markIncrement=value('proposedMarkIncrement'),
                            markingGuide=value('proposedMarkingGuide'),
                            marksProvenance=f"Source marking guide PDF pages {record['guidePages']}.",
                            solutionProvenance='Independently checked SomaSmart marking guidance.',
                            publicationStatus='published', verificationStatus='verified',
                            resolutionEvidence=record['sourceEvidence'])
            if record.get('guideDiscrepancy'):
                question['guideDiscrepancy'] = record['guideDiscrepancy']
            if len(ids) == 1:
                question['groupId'] = identifier
            question.pop('sourceIssue', None)

    if paper['form'] != 2 or paper['year'] != 2025 or paper['sourceType'] != 'necta':
        return
    evidence = json.loads((BATCHES / 'marking-evidence.json').read_text())
    subject = paper['subjectId']
    marking = next((item for item in evidence['subjects'] if item['subjectId'] == subject), None)
    if not marking:
        return
    allocation = marking['allocation']
    citation = f"NECTA FTNA format effective {evidence['legacyEdition']['effectiveFrom']}, PDF page {marking['pdfPage']}."
    allowed_topics = {lesson['id'] for lesson in lessons if lesson['form'] == 2 and lesson['subjectId'] == subject}
    hold = {'biology': {'5', '9'}, 'geography': {'7'}, 'kiswahili': {'6'}}[subject]
    for question in questions:
        if question['mainQuestionNumber'] in hold:
            question['sourceIssue'] = {
                'biology': 'Question 5 does not identify the yeast species. Question 9 omits a corresponding response label for one hazard.',
                'geography': 'The question about the coldest planet does not specify which temperature measure to use.',
                'kiswahili': 'The question treats a valid form of “anaumwa” as an error without specifying the intended distinction.',
            }[subject]
    for question in questions:
        main = question['mainQuestionNumber']
        if main not in ('1', '2') or not set(question['topicIds']) & allowed_topics:
            continue
        item = allocation['question1' if main == '1' else 'question2']
        question.update(maximumMarks=item['marksPerItem'] if main == '1' else item['totalMarks'],
                        markIncrement=item['marksPerItem'], marksProvenance=citation,
                        markingGuide='Use the independently checked answer. The mark allocation follows the cited NECTA format.',
                        publicationStatus='published', verificationStatus='verified',
                        markFormatEvidence=marking, scoringEligible=True,
                        sourceMaximumMarksUnknown=False)
        question.pop('sourceIssue', None)

    for number in map(str, range(3, 10)):
        parts = [q for q in questions if q['mainQuestionNumber'] == number]
        if not parts or number in hold or not all(q.get('answerKey') for q in parts):
            continue
        topics = list(dict.fromkeys(t for q in parts for t in q['topicIds'] if t in allowed_topics))
        if not topics:
            continue
        identifier = paper['id'] + '-whole-' + number
        record = {k: v for k, v in parts[0].items() if k not in TEXT_FIELDS}
        record.update(id=identifier, groupId=identifier, questionNumber=number,
                      type='short', options=[], content='',
                      sourceParts=[{k: q[k] for k in TEXT_FIELDS if k in q} for q in parts],
                      topicIds=topics, subtopicIds=topics,
                      media=list({m['path']: m for q in reversed(parts) for m in q['media']}.values()),
                      sourcePages=sorted({p for q in parts for p in q['sourcePages']}),
                      maximumMarks=allocation['questions3to9']['marksPerMainQuestion'],
                      markIncrement=0.5, marksProvenance=citation,
                      markIncrementProvenance='Independent self-assessment increment.',
                      markFormatEvidence=marking, publicationStatus='published', verificationStatus='verified',
                      scoringEligible=True, sourceMaximumMarksUnknown=False,
                      requiresDrawing=any('draw' in q['content'].lower() or 'diagram' in q['content'].lower() for q in parts),
                      answerKey='\n\n'.join(f"{q['questionNumber']}. {q['answerKey']}" for q in parts),
                      markingGuide='Compare every response with the worked answers. Award full credit for a complete correct response, partial credit for correct steps, and zero for no correct work. Enter one mark for the whole question. The NECTA format gives the total of 10 and leaves subpart weights unspecified.',
                      solutionProvenance='Independently prepared SomaSmart solutions and self-assessment guidance.')
        record.pop('sourceIssue', None)
        record['sourceTextSha256'] = text_hash(record)
        index = questions.index(parts[0])
        questions.insert(index, record)
        for part in parts:
            part['publicationStatus'] = 'included-in-whole-question'
            part['scoredInQuestionId'] = identifier
            part.pop('sourceIssue', None)
