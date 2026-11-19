// Run the built student application against DOM and IndexedDB test doubles.
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { runInNewContext } from 'node:vm';
import { webcrypto } from 'node:crypto';

const directory = process.argv[2] || 'dist-hosted';
const library = readFileSync(directory + '/library.json');
const documents = JSON.parse(library).sourceDocuments;
const entry = readFileSync(directory + '/index.html', 'utf8').match(/src="(\/assets\/[^"]+\.js)"/)[1];
const bundle = readFileSync(directory + entry, 'utf8');
const local = new Map();
const db = {
  transaction() {
    const tx = { objectStore: () => ({
      get(key) {
        const request = { result: structuredClone(local.get(key)) };
        queueMicrotask(() => request.onsuccess());
        return request;
      },
      put(value, key) {
        local.set(key, structuredClone(value));
        queueMicrotask(() => tx.oncomplete());
      },
    }) };
    return tx;
  },
};
async function openApp(hash, expectedText) {
  const nodes = new Map();
  const node = selector => {
    if (!nodes.has(selector)) nodes.set(selector, {});
    return nodes.get(selector);
  };
  const handlers = new Map();
  const location = { hash, replace(next) { this.hash = next; } };
  const controls = new Map();
  const document = { querySelector: node, querySelectorAll: selector => controls.get(selector) || [], createElement: () => ({relList: {supports: () => true}}) };
  runInNewContext(bundle, {
    document, location, confirm: () => true, crypto: webcrypto, navigator: {}, window: { addEventListener: (k, cb) => handlers.set(k, cb), scrollTo() {} },
    indexedDB: {open() {
      const request = { result: db };
      queueMicrotask(() => request.onsuccess());
      return request;
    }},
    fetch: async path => {
      assert.equal(path, '/library.json');
      return new Response(library, {headers: {'content-type': 'application/json'}});
    },
    setTimeout, clearTimeout, AbortController, TextDecoder, structuredClone,
    FormData: class {constructor(form) {this.form = form;} getAll() {return this.form.selected;}},
  });
  for (let turn = 0; turn < 100 && !node('#app').innerHTML; turn++)
    await new Promise(resolve => setImmediate(resolve));
  assert(expectedText ? node('#app').innerHTML?.includes(expectedText) : node('#app').innerHTML?.includes('Questions to practise') || node('#app').innerHTML?.includes('My answer and working'));
  return { node, controls, location, render: () => handlers.get('hashchange')() };
}

const indexed = documents.filter(doc => doc.practiceIndex);
const base = id => '#/paper-practice/' + id;
let app = await openApp(base(indexed[0].id));
for (const doc of indexed) {
  app.location.hash = base(doc.id);
  await app.render();
  const label = doc.practiceIndex.groups.at(-1).label;
  const form = app.node('#source-practice-picker');
  form.selected = [label];
  await form.onsubmit({ preventDefault() {}, currentTarget: form });
  assert.equal(app.location.hash, base(doc.id) + '/' + encodeURIComponent(label));
  await app.render();
  assert(app.node('#app').innerHTML.includes('Question ' + label));
  const answer = 'My working for ' + doc.id;
  await app.node('#source-practice-answer').oninput({target: {value: answer}});
  await app.node('#source-practice-check').onclick();
  if (doc.independentPracticeGuide?.groups[label]) {
    const marks = app.node('#source-practice-mark');
    marks.elements = {mark: {valueAsNumber: 2.5}};
    await marks.onsubmit({preventDefault() {}});
    assert.equal(local.get('sourcePractice')[doc.id].marks[label], 2.5);
  }
  assert.equal(local.get('sourcePractice')[doc.id].answers[label], answer);
}
app = await openApp(app.location.hash);
for (const doc of indexed) {
  const label = doc.practiceIndex.groups.at(-1).label;
  app.location.hash = base(doc.id) + '/' + encodeURIComponent(label);
  await app.render();
  assert(app.node('#app').innerHTML.includes('My working for ' + doc.id));
  assert(app.node('#app').innerHTML.includes('Undo reviewed status'));
}
console.log(directory, indexed.length, 'paper selections, typed answers and review states restored after application restart.');

const question = JSON.parse(library).questions.find(q => q.type === 'short');
assert(question);
local.set('draft', {id:'saved-exam', title:'Saved exam', created:0, form:question.form,
  questions:[question], answers:{[question.id]:'Saved student response'}, marks:{}, submitted:false});
app = await openApp('#/exams/attempt', 'Back to exam dashboard');
assert.match(app.node('#app').innerHTML, /href="#\/exams">← Back to exam dashboard/);
app.location.hash = '#/exams';
await app.render();
assert.match(app.node('#app').innerHTML, /href="#\/exams\/attempt">Resume saved exam/);
app.location.hash = '#/exams/attempt';
await app.render();
assert(app.node('#app').innerHTML.includes('Saved student response'));
console.log('Saved exam returns to dashboard and resumes with response intact.');

const mcq = JSON.parse(library).questions.find(q => q.type === 'mcq' && q.sourceType !== 'original');
for (const mode of ['immediate','end']) {
  local.set('draft', {id:'timing', title:'Timing', questions:[mcq], answers:{}, marks:{},
    feedbackMode:null, submitted:false, form:mcq.form});
  app = await openApp('#/exams/attempt', 'When would you like feedback?');
  const choice = {dataset:{mode}};
  const option = {type:'radio', value:mode === 'immediate' ? mcq.answerKey : mcq.options.find(o => o !== mcq.answerKey), dataset:{answer:mcq.id}};
  app.controls.set('[data-mode]', [choice]);
  app.controls.set('[data-answer]', [option]);
  await app.render();
  await choice.onclick();
  assert(!app.node('#app').innerHTML.includes('Model answer'));
  await option.oninput();
  if (mode === 'end') {
    assert(!app.node('#app').innerHTML.includes('Model answer'));
    await app.node('#submit').onclick();
  }
  const review = app.node('#app').innerHTML;
  assert(review.includes(mode === 'immediate' ? 'Correct' : 'Incorrect') && review.includes(mcq.feedbackExplanation) && review.includes('Model answer') && review.includes('Guided review conversation'));
  assert(!review.includes('Open source paper PDF') && !review.includes('Original source marking guide'));
}
console.log('Immediate and end-of-exam feedback verified with a genuine multiple-choice item.');

local.delete('draft');
app = await openApp('#/exams', 'Exam dashboard');
const scoredPaper = documents.find(d => d.interactivePaperId);
app.location.hash = '#/paper/' + scoredPaper.id + '/1';
await app.render();
assert.equal(app.location.hash, '#/exams/attempt');
await app.render();
assert(app.node('#app').innerHTML.includes('Check each answer'));
const selfCheck = indexed.find(d => !d.interactivePaperId);
if (selfCheck) {
app.location.hash = '#/paper/' + selfCheck.id;
await app.render();
assert.equal(app.location.hash, base(selfCheck.id));
await app.render();
assert(app.node('#app').innerHTML.includes('Review at the end'));
}
console.log('Paper links enter scored or self-check practice directly.');

local.delete('draft');
app = await openApp('#/exams', 'Exam dashboard');
let opened = 0;
for (const doc of documents.filter(doc => doc.interactivePaperId)) {
  app.location.hash = '#/paper/' + doc.id;
  await app.render();
  const saved = local.get('draft');
  assert.equal(saved.questions[0].paperId,doc.interactivePaperId);
  const choice = {dataset:{mode:'immediate'}};
  app.controls.set('[data-mode]', [choice]);
  await app.render();
  await choice.onclick();
  const html = app.node('#app').innerHTML;
  for (const question of saved.questions) {
    const control = question.type === 'matching' ? 'data-match' : 'data-answer';
    assert(html.includes(control + '="' + question.id + '"'), question.id);
  }
  await app.node('#discard').onclick();
  opened++;
}
console.log('Opened', opened, 'papers and found an individual answer control for every included item.');
