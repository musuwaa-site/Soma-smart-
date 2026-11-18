import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { studentRelease } from '../scripts/student-release.mjs';
import { selectSourceGroups, sourceGroupPages } from '../src/source-practice.js';

const library = studentRelease(JSON.parse(readFileSync('content/library.json')));
test('every released original paper has a scored selection or an original-page selection', () => {
  const indexed = library.sourceDocuments.filter(doc => doc.practiceIndex);
  assert.equal(indexed.length, 29);
  assert.equal(indexed.reduce((sum, doc) => sum + doc.practiceIndex.groups.length, 0), 282);
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
    assert(!library.questions.some(q => q.sourceSha256 === doc.sha256));
  }
});
