import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {eligible,generate,mark,result} from '../src/engine.js';
import {verbatimContent,originalOptionLabel} from '../src/exam-format.js';
import {studentRelease} from '../scripts/student-release.mjs';
const data=JSON.parse(readFileSync('content/library.json'));
const papers=data.papers.filter(p=>p.transcriptionComplete);
test('student release excludes draft transcriptions and quarantined source associations',()=>{
  const release=studentRelease(data);assert(release.questions.length<data.questions.length);
  assert(release.questions.every(q=>q.publicationStatus==='published'));
  assert(release.sourceDocuments.every(d=>d.publicationStatus==='published'));
  assert(!release.sourceDocuments.some(d=>d.subjectId==='computer-science'));
  assert(data.questions.some(q=>q.publicationStatus==='draft'));
});
test('every published source selection is exactly the eligible scored subset',()=>{
  assert(papers.length>=12);
  for(const p of papers){
    const bank=eligible(data,{form:p.form,subjectId:p.subjectId,source:'authentic'}).filter(q=>q.paperId===p.id);
    assert.deepEqual(bank.map(q=>q.id),p.questionIds);
    assert.equal(result(bank).maximum,p.maximumMarks);
    assert(bank.every(q=>q.sourceType!=='original' && q.sourceTextSha256));
    for(const id of p.draftQuestionIds)assert(!bank.some(q=>q.id===id));
  }
});
test('complete scored source papers retain their source total and require written self-marking',()=>{
  const complete=papers.filter(p=>p.completeScoredPaper);assert(complete.length>=3);
  for(const p of complete){
    const qs=p.questionIds.map(id=>data.questions.find(q=>q.id===id));
    assert.equal(qs.length,p.allTranscribedQuestionIds.length);
    assert.equal(result(qs).maximum,p.sourceMaximumMarks);
    const answers=Object.fromEntries(qs.map(q=>[q.id,q.answerKey]));
    const provisional=result(qs,answers);assert(provisional.pending>0);
    const marks=Object.fromEntries(qs.map(q=>[q.id,q.maximumMarks]));
    const final=result(qs,answers,marks);assert.equal(final.pending,0);assert.equal(final.earned,p.sourceMaximumMarks);
  }
});
test('real independent objective answers and source fractional marks grade correctly',()=>{
  const objective=data.questions.filter(q=>q.transcriptionBatch && q.publicationStatus==='published' && ['mcq','matching'].includes(q.type));assert(objective.length>=80);
  for(const q of objective){assert.equal(mark(q,q.answerKey).earned,q.maximumMarks);assert.equal(mark(q,'').status,'unanswered');}
  const fractional=data.questions.find(q=>q.transcriptionBatch && q.publicationStatus==='published' && q.maximumMarks===1.5);
  assert(fractional);assert.equal(mark(fractional,'written response',1.5).earned,1.5);assert.throws(()=>mark(fractional,'written response',1.25));
});
test('actual shared-material groups stay together through seeded custom selection',()=>{
  for(const p of papers){
    const bank=eligible(data,{form:p.form,subjectId:p.subjectId,source:'authentic'}).filter(q=>q.paperId===p.id);
    const picked=generate(bank,Math.min(12,bank.length),2027);const ids=new Set(picked.map(q=>q.id));assert.equal(ids.size,picked.length);
    for(const q of picked)for(const linked of bank.filter(x=>(x.groupId||x.id)===(q.groupId||q.id)))assert(ids.has(linked.id));
  }
});
test('a held dependent part excludes its whole shared-material group',()=>{
  const q=data.questions.find(q=>q.transcriptionBatch && q.publicationStatus==='published');
  const a={...q,id:'one',groupId:'shared'},b={...q,id:'two',groupId:'shared',publicationStatus:'draft'};
  assert.equal(eligible({...data,questions:[a,b]},{form:q.form,subjectId:q.subjectId,source:'authentic'}).length,0);
});
test('original repeated option labels and underlines render without rewriting text',()=>{
  const q=data.questions.find(q=>q.id.endsWith('english-3524b0fe8b23f712-q1-iii'));
  assert(q);assert.deepEqual(q.optionLabels,['A','B','A','D']);assert.match(originalOptionLabel(q,2),/>A\.</);
  const underlined=data.questions.find(q=>q.underlinedTerms?.includes('hodari'));assert(underlined);assert.match(verbatimContent(underlined),/<u>hodari<\/u>/);
  assert.equal(verbatimContent({content:'<script>\nA & B'}),'&lt;script&gt;<br>A &amp; B');
});
