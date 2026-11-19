import test from 'node:test';import assert from 'node:assert/strict';import {readFileSync} from 'node:fs';import {createHash} from 'node:crypto';import {eligible,generate,result} from '../src/engine.js';
const data=JSON.parse(readFileSync('content/library.json'));const bank=eligible(data,{form:2,subjectId:'mathematics',source:'necta'}).filter(q=>q.paperId==='necta-ftna-2025-mathematics-200032d2d5376daf' && q.subquestions?.length);
test('first authentic selection preserves seven complete main groups and eighteen labelled parts',()=>{assert.equal(bank.length,7);assert.equal(bank.reduce((n,q)=>n+q.subquestions.length,0),18);assert.deepEqual(bank.map(q=>q.questionNumber),['1','3','4','5','6','7','9']);const picked=generate(bank,7,2025);assert.equal(result(picked).maximum,70);assert(picked.every(q=>q.subquestions.every(s=>s.parentQuestionId===q.id)));});
test('authentic source bytes and source mark evidence match published provenance',()=>{for(const q of bank){const bytes=readFileSync('public'+q.sourcePdf);assert.equal(createHash('sha256').update(bytes).digest('hex'),q.sourceSha256);assert.equal(q.maximumMarks,10);assert.match(q.marksProvenance,/instruction 3/);assert.match(q.markingGuide,/not an official NECTA scheme/);assert.equal(q.rightsEvidence.type,'owner-attestation-in-chat');}});
test('genuine written answers remain pending until independently self-assessed',()=>{const q=bank[0];const r=result([q],{[q.id]:q.answerKey});assert.equal(r.pending,1);assert.equal(r.earned,0);const final=result([q],{[q.id]:q.answerKey},{[q.id]:8});assert.equal(final.pending,0);assert.equal(final.earned,8);});
test('checked numeric solutions reproduce source conditions',()=>{assert.equal(((50/5+5)-(8*4-2))/5,-3);assert.equal(Math.round((65600+13400+29700)/1000)*1000,109000);assert.equal(33/(4+5+6+7)*7,10.5);assert(Math.abs(2500/8500*100-500/17)<1e-12);assert.equal((5+2)+(2+2)+5,16);for(const [m,n] of [[3,-2],[-1,4],[0,7]])assert.equal(7*m-2*(5*n-4*m)+11*n-5*m,10*m+n);assert.equal(-2*.5-(-5)-4,0);assert.equal(2*.5-(-3)-4,0);assert(Math.abs(8**(-2/3)+(3**-2)/(2**-3)-41/36)<1e-12);assert(Math.abs(Math.sqrt(2)/(Math.sqrt(3)+Math.sqrt(2))-(Math.sqrt(6)-2))<1e-12);assert.equal(Math.round(30*Math.sin(70*Math.PI/180)*10)/10,28.2);assert.equal(Math.hypot(5,12),13);});
test('independent solutions explain the overlap and vertex-order ambiguities',()=>{
 const paper=data.papers.find(p=>p.id===bank[0].paperId);
 assert(paper.completePaper);assert.equal(paper.maximumMarks,100);
 const items=data.questions.filter(q=>q.paperId===paper.id);
 assert.match(items.find(q=>q.questionNumber==='2(a)').answerKey,/4 and 9/);
 assert.match(items.find(q=>q.questionNumber==='8(a)').answerKey,/DBA/);
 assert.match(items.find(q=>q.questionNumber==='10\(b\)').answerKey,/33⅓/);
});
