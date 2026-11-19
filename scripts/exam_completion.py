"""Calculate item conversion completion directly from the published library."""
import json
import sys
from pathlib import Path

root = Path(__file__).resolve().parents[1]
data = json.loads((root / 'content/library.json').read_text())
papers = {paper['id']: paper for paper in data['papers']}
rows = []
for doc in data['sourceDocuments']:
    if doc['publicationStatus'] != 'published':
        continue
    paper = papers.get(doc.get('interactivePaperId'))
    pending = not bool(paper and (paper.get('completePaper') or paper.get('practiceOrder') or paper.get('transcriptionComplete')))
    rows.append(dict(sourceId=doc['id'], title=doc['title'], form=doc['form'],
                     subjectId=doc['subjectId'], converted=not pending,
                     scoredItems=len(paper['questionIds']) if paper else 0,
                     unscoredResponses=len(paper.get('reviewOnlyItems', [])) if paper else 0))
report = dict(papers=len(rows), papersWithIndividualControls=sum(row['converted'] for row in rows),
              remaining=[row for row in rows if not row['converted']], sources=rows)
(root / 'content/exam-completion.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
print(json.dumps({key:value for key,value in report.items() if key!='sources'},ensure_ascii=False,indent=2))
if '--require-complete' in sys.argv:
    if len(rows) != 180 or report['remaining']:
        raise SystemExit('Exam conversion is unfinished.')
