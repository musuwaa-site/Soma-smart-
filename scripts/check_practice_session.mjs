// Run the built student application against DOM and IndexedDB test doubles.
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { runInNewContext } from 'node:vm';

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
  const location = { hash };
  const document = { querySelector: node, querySelectorAll: () => [], createElement: () => ({relList: {supports: () => true}}) };
  runInNewContext(bundle, {
    document, location, navigator: {}, window: { addEventListener: (k, cb) => handlers.set(k, cb), scrollTo() {} },
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
  return { node, location, render: () => handlers.get('hashchange')() };
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
