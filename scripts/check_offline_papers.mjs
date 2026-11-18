// Exercise the built service worker with a Cache API test double, then disconnect.
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { webcrypto } from 'node:crypto';
import { runInNewContext } from 'node:vm';
import { selectSourceGroups, sourceGroupPages } from '../src/source-practice.js';

const directory = process.argv[2] || 'dist';
const origin = 'https://offline.example';
let connected = true;
const cached = new Map();
const events = new Map();
const worker = {
  location: { origin },
  clients: { matchAll: async () => [], claim: async () => {} },
  skipWaiting: async () => {},
  addEventListener: (name, handle) => events.set(name, handle),
};
const storage = {
  match: async url => cached.has(url) ? new Response(cached.get(url)) : undefined,
  put: async (url, response) => cached.set(url, await response.arrayBuffer()),
};
runInNewContext(readFileSync(directory + '/sw.js', 'utf8'), {
  self: worker, caches: { open: async () => storage }, URL, Uint8Array, crypto: webcrypto,
  fetch: async url => {
    assert(connected, 'Worker tried to reach the network for ' + url);
    return new Response(readFileSync(directory + url));
  },
});
async function dispatch(name, event = {}) {
  let completion;
  const run = pending => { completion = pending; };
  events.get(name)({ ...event, waitUntil: run, respondWith: run });
  return completion;
}
async function offlineRead(path) {
  const response = await dispatch('fetch', { request: { url: origin + path, method: 'GET' } });
  assert(response.ok, path);
  return response;
}

await dispatch('install');
await dispatch('activate');
connected = false;
const data = await (await offlineRead('/library.json')).json();
const questions = new Map(data.questions.map(q => [q.id, q]));
const paperIds = new Map(data.papers.map(p => [p.id, p]));
const visited = new Set();
let groups = 0;
for (const doc of data.sourceDocuments) {
  if (doc.practiceIndex) {
    const all = doc.practiceIndex.groups.map(g => g.label);
    const selected = selectSourceGroups(doc.practiceIndex, all);
    assert.equal(selected.length, all.length);
    for (const group of selected) {
      const pages = sourceGroupPages(doc, group);
      assert(pages.length, doc.id + ' question ' + group.label);
      for (const path of pages) {
        if (!visited.has(path)) {
          assert((await (await offlineRead(path)).arrayBuffer()).byteLength > 0, path);
          visited.add(path);
        }
      }
      groups++;
    }
  } else {
    const paper = paperIds.get(doc.interactivePaperId);
    assert(paper?.questionIds.length, doc.id);
    for (const id of paper.questionIds) assert(questions.get(id)?.markingGuide, id);
  }
}
console.log(directory, data.sourceDocuments.length, 'interactive papers readable offline,',
  groups, 'question groups and', visited.size, 'distinct practice pages checked.');
