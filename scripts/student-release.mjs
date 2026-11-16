import {readFileSync,writeFileSync} from 'node:fs';
import {pathToFileURL} from 'node:url';
export function studentRelease(canonical) {
  const d=structuredClone(canonical);
  d.questions=d.questions.filter(q=>q.publicationStatus==='published');
  d.papers=d.papers.filter(p=>p.publicationStatus==='published');
  d.sourceDocuments=(d.sourceDocuments||[]).filter(p=>p.publicationStatus==='published');
  for(const p of d.papers){
    p.transcribedRecordCount=p.allTranscribedQuestionIds?.length || p.questionIds.length;
    p.heldRecordCount=p.draftQuestionIds?.length || 0;
    for(const field of ['allTranscribedQuestionIds','allQuestionIds','draftQuestionIds','heldQuestionIds'])delete p[field];
  }
  return d;
}
if(process.argv[1] && import.meta.url===pathToFileURL(process.argv[1]).href){
  writeFileSync(process.argv[2],JSON.stringify(studentRelease(JSON.parse(readFileSync('content/library.json'))),null,2));
}
