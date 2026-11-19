"""Restore the three remaining FTNA Mathematics questions with independent solutions."""
from source_integrity import text_hash

PAPER = 'necta-ftna-2025-mathematics-200032d2d5376daf'
# Each printed main question carries ten marks. Part splits are independent.
PARTS = [
('2(a)',3,5,'In a family of 15 children, 2/5 of them drink tea and 1/3 of them drink coffee. How many children drink none of the two drinks?',
 'Between 4 and 9 children, depending on how many drink both. If nobody drinks both, the answer is 4.',
 'Six drink tea and five drink coffee. With x drinking both, 11 − x drink either, leaving 4 + x. The paper gives no overlap, so 0 ≤ x ≤ 5.'),
('2(b)',3,5,'In a class of 40 students, 25 students passed English Language assessment. Find the percentage of students who failed the assessment.',
 '37.5%.','15 of the 40 students failed. Multiply 15/40 by 100.'),
('8(a)',9,5,'By using the following figure, prove that △ABC ~ △ABD.',
 'The triangles are similar by AA. The diagram gives the correspondence △ABC ~ △DBA.',
 'The right angle at A in ABC corresponds to the right angle at D in DBA. The triangles share the angle at B. The order printed on the paper swaps corresponding vertices. Credit a correct AA argument that identifies this discrepancy.'),
('8(b)',10,5,'In the following figure, BE bisects DÊF and DE = FE. Prove that △BEF ≡ △BED.',
 'The triangles are congruent by SAS.','BE is common, EF = ED, and angle BEF equals angle BED because BE bisects angle DEF. The equal angles lie between the equal sides.'),
('10(a)',12,5,'In a school of 120 students, 40 learn English, 60 learn Kiswahili and 30 learn both Kiswahili and English. How many students learn neither English nor Kiswahili?',
 '50 students.','40 + 60 − 30 = 70 learn at least one language. Subtract 70 from 120.'),
('10(b)',13,5,'The following marks were scored by students in a History test:',
 '30–39: 7; 40–49: 10; 50–59: 8; 60–69: 2; 70–79: 3. Percentage scoring 50–69: 33⅓%.',
 'Tally all 30 observations once. The two classes from 50 through 69 contain 8 + 2 = 10 students, giving 100 × 10/30. The original table and the rest of the printed question are shown above the answer control.')
]


def apply(data):
    paper = next(p for p in data['papers'] if p['id'] == PAPER)
    source = next(d for d in data['sourceDocuments'] if d.get('interactivePaperId') == PAPER)
    originals = [q for q in data['questions'] if q.get('paperId') == PAPER and q.get('subquestions')]
    assert len(originals) == 7
    rows = originals.copy()
    for number, page, marks, content, answer, why in PARTS:
        main = number.split('(')[0]
        q = {key: paper[key] for key in ('form','subjectId','sourceType','sourceReference','year','institution','rightsStatus','rightsEvidence')}
        q.update(id=PAPER+'-'+number.replace('(','-').replace(')',''), paperId=PAPER, questionNumber=number,
                 mainQuestionNumber=main, groupId=PAPER+'-main-'+main, sourceDocumentId=source['id'],
                 sourceSha256=source['sha256'], sourcePdf=source['sourcePdf'], sourceTitle=paper['title'],
                 publicationStatus='published', verificationStatus='verified', content=content,
                 type='calculation' if main!='8' else 'short', topicIds=['mathematics-f2-geometry-review' if main=='8' else 'mathematics-f2-number-revision'],
                 subtopicIds=[], sourcePages=[page], media=[dict(role='printed-question',path=source['pageImages'][page-1],alt=f'Original page {page}')],
                 options=[], answerKey=answer, feedbackExplanation=why, markingGuide=why,
                 maximumMarks=marks, markIncrement=1, marksProvenance='Independent allocation within the printed ten-mark question',
                 solutionProvenance='Independent SomaSmart solution')
        q['sourceTextSha256'] = text_hash(q)
        rows.append(q)
    rows.sort(key=lambda q:int(str(q.get('mainQuestionNumber') or q['questionNumber'])))
    data['questions']=[q for q in data['questions'] if q.get('paperId')!=PAPER]+rows
    paper.update(questionIds=[q['id'] for q in rows],completeScoredPaper=True,completePaper=True,
                 maximumMarks=100,publicationScope='complete-paper',excludedQuestions=[])
