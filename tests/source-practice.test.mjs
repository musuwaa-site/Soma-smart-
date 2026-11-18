import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { studentRelease } from '../scripts/student-release.mjs';
import { selectSourceGroups, sourceGroupPages } from '../src/source-practice.js';

const library = studentRelease(JSON.parse(readFileSync('content/library.json')));
test('every released original paper has a scored selection or an original-page selection', () => {
  const indexed = library.sourceDocuments.filter(doc => doc.practiceIndex);
  assert.equal(library.sourceDocuments.length, new Set(library.sourceDocuments.map(doc => doc.sha256)).size);
  for (const form of [1, 2]) assert(library.sourceDocuments.filter(doc => doc.form === form).length >= 90);
  assert(indexed.length >= 103);
  assert(indexed.every(doc => doc.practiceIndex.groups.length > 0));
  assert(indexed.reduce((sum, doc) => sum + doc.practiceIndex.groups.length, 0) >= 1012);
  assert(library.sourceDocuments.every(doc => doc.interactivePaperId || doc.practiceIndex));
  for (const doc of indexed) {
    assert.equal(doc.practiceIndex.sourceSha256, doc.sha256);
    const groups = doc.practiceIndex.groups;
    assert.equal(selectSourceGroups(doc.practiceIndex, ['unknown']).length, 0);
    const selected = selectSourceGroups(doc.practiceIndex, [groups.at(-1).label, groups[0].label, groups[0].label]);
    assert.deepEqual(selected, [groups[0], groups.at(-1)]);
    for (const group of groups) {
      assert.equal(sourceGroupPages(doc, group).length, group.lastPage - group.firstPage + 1);
      assert.equal(sourceGroupPages(doc, group).at(0), doc.pageImages[group.firstPage - 1]);
    }
    const scored = library.questions.filter(q => q.sourceSha256 === doc.sha256);
    assert(scored.every(q => q.paperId === doc.interactivePaperId));
  }
});

test('reordered scans preserve all archive images and use the corrected reading order', () => {
  const document = library.sourceDocuments.find(doc => doc.id === 'source-0cb716c0571976ac');
  assert.equal(document.pageImages.length, 11);
  assert.equal(new Set(document.pageImages).size, 11);
  const group = document.practiceIndex.groups.find(item => item.label === '6');
  assert.deepEqual(sourceGroupPages(document,group).map(page=>page.split('/').at(-1)), ['page-007.jpg','page-006.jpg']);
});
test('independent marking guides are attached to exact papers and cover their printed totals', () => {
  const papers = library.sourceDocuments.filter(document => document.independentPracticeGuide);
  assert(papers.length >= 6);
  for (const doc of papers) {
  const guide = doc.independentPracticeGuide;
  assert.equal(guide.sourceSha256, doc.sha256);
  const labels = doc.practiceIndex.groups.map(group => group.label);
  assert(Object.keys(guide.groups).every(label => labels.includes(label)));
  const full = labels.length === Object.keys(guide.groups).length;
  const total = Object.values(guide.groups).reduce((sum, group) => sum + group.maximumMarks, 0);
  if (full) assert.equal(total, 100);
  if (doc.id === 'source-817d378b48f73ba6') assert.equal(total, 25);
  for (const group of Object.values(guide.groups)) {
    assert.equal(group.maximumMarks, group.parts.reduce((sum, part) => sum + part.marks, 0));
    assert(group.parts.every(part => part.answer && part.rubric));
  }
  }
});
