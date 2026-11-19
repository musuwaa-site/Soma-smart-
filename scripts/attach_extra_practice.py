"""Expose reviewed source discrepancies as optional, unscored interactive responses."""
import copy
import re

# These originals do not identify a unique option or supply the required figure.
UNDETERMINED = {
    'mkalama-f1-2025-chemistry-d059bebfa47291f7-1-v':
        'The printed word is “Painting”. Painting does not mean a sudden loss of any of these things. If “fainting” was intended, it means a temporary loss of consciousness.',
    'morogoro-f1-2025-physics-fdf35496ef2658db-q1-iii':
        'The density cannot be calculated from this copy because the referenced figures are missing. Density requires mass and volume.',
    'morogoro-f1-2025-physics-fdf35496ef2658db-q1-ix':
        'Re-examine, revise or reject a hypothesis when repeated evidence contradicts it. None of the printed options states this.',
    'moshi-f1-2026-english-5e07c19752944cd8-q5-B-iv':
        'The printed sentence does not admit a natural unique completion using the intended tense. For a future deadline one could write “I will have completed my exams by then”.'
}


def apply(data):
    by_id = {q['id']: q for q in data['questions']}
    for paper in data['papers']:
        held = list(paper.get('draftQuestionIds', []))
        if not held or paper.get('publicationStatus') != 'published':
            continue
        items = []
        for identifier in held:
            original = by_id[identifier]
            assert original['publicationStatus']=='draft' and original['sourceIssue'] and original['rightsStatus']=='cleared'
            item = copy.deepcopy(original)
            item.update(id='practice-'+identifier, reviewOnly=True, maximumMarks=0,
                        publicationStatus='published', topicIds=[],
                        feedbackExplanation=original['sourceIssue'])
            if identifier in UNDETERMINED:
                item['answerKey'] = UNDETERMINED[identifier]
            elif identifier.endswith('82d4ba0ae1a6bac4-q1-iv'):
                item['acceptedAnswerKeys'] = ['A Tension force','C Frictional force']
            if identifier not in UNDETERMINED and item['type'] in ('mcq','matching'):
                item['reviewKeyAvailable'] = True
            items.append(item)
        paper['reviewOnlyItems'] = items
        def main(q):
            number = re.search(r'\d+', str(q['questionNumber']))
            return int(number.group()) if number else 0
        positions = {k:i for i,k in enumerate(paper.get('allTranscribedQuestionIds', []))}
        rows = [by_id[k] for k in paper['questionIds']] + items
        rows.sort(key=lambda q:(main(q), positions.get(q['id'].removeprefix('practice-'), -1)))
        paper['practiceOrder'] = [q['id'] for q in rows]
