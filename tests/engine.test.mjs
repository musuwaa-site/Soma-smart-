import test from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { eligible, generate, mark, result, weakTopics } from "../src/engine.js";
const data = JSON.parse(readFileSync("content/library.json"));
test("18 form-subject combinations have usable learning and practice", () => {
  for (const s of data.subjects)
    for (const form of [1, 2]) {
      assert(
        data.lessons.some(
          (l) =>
            l.subjectId === s.id &&
            l.form === form &&
            l.paragraphs.length >= 3 &&
            l.paragraphs.join("").length > 650 &&
            l.examples.length >= 3,
        ),
      );
      assert(eligible(data, { subjectId: s.id, form }).length >= 6);
    }
});
test("authentic filter never includes originals", () =>
  assert.equal(
    eligible(data, { form: 1, subjectId: "chemistry", source: "authentic" })
      .length,
    0,
  ));
test("deterministic selection has no repeated ids", () => {
  const a = generate(data.questions, 10, 42);
  assert.deepEqual(a, generate(data.questions, 10, 42));
  assert.equal(new Set(a.map((q) => q.id)).size, 10);
});
test("selection never exceeds inventory or breaks groups", () => {
  const bank = [{ id: "a" }, { id: "b", parentQuestionId: "a" }, { id: "c" }];
  const picked = generate(bank, 2);
  assert.equal(
    picked.some((q) => q.id === "a"),
    picked.some((q) => q.id === "b"),
  );
  assert(generate(bank, 99).length === 3);
});
test("objective grades are exact and blanks remain unanswered", () => {
  const q = data.questions.find((q) => q.type === "mcq");
  assert.equal(mark(q, q.answerKey).earned, q.maximumMarks);
  assert.equal(mark(q, "wrong").status, "incorrect");
  assert.equal(mark(q, "").status, "unanswered");
});
test("written answers require marking; exact increments enforced", () => {
  const q = data.questions.find((q) => q.type === "short");
  assert.equal(mark(q, "my response").status, "pending");
  assert.equal(mark(q, "my response", 1).status, "partial");
  for (const n of [-1, 99, 0.5, NaN])
    assert.throws(() => mark(q, "response", n));
});
test("unanswered questions contribute possible marks", () => {
  const qs = data.questions.slice(0, 3);
  const r = result(qs);
  assert.equal(
    r.maximum,
    qs.reduce((s, q) => s + q.maximumMarks, 0),
  );
  assert.equal(r.earned, 0);
});
test("topic recommendations derive only from final attempts", () => {
  const q = data.questions[0];
  const a = {
    questions: [q],
    result: result([q], { [q.id]: "wrong" }),
    final: true,
  };
  assert.equal(weakTopics([a])[0].ratio, 0);
  assert.equal(weakTopics([{ ...a, final: false }]).length, 0);
});
test("unverified third-party data cannot enter scored exams", () => {
  const bad = {
    ...data.questions[0],
    sourceType: "necta",
    rightsStatus: "unresolved",
  };
  assert.equal(
    eligible({ ...data, questions: [bad] }, { form: 1, subjectId: "chemistry" })
      .length,
    0,
  );
});
test("matching grades by verified increment", () => {
  assert.equal(
    mark(
      {
        type: "matching",
        maximumMarks: 2,
        markIncrement: 1,
        answerKey: { a: "x", b: "y" },
      },
      { a: "x", b: "z" },
    ).earned,
    1,
  );
});
test("topic filters select the whole group including shared parent", () => {
  const q = data.questions[0];
  const a = { ...q, id: "root", topicIds: ["one"] };
  const b = { ...q, id: "child", parentQuestionId: "root", topicIds: ["two"] };
  const selected = eligible(
    { ...data, questions: [a, b] },
    { form: 1, subjectId: "chemistry", topics: ["two"] },
  );
  assert.deepEqual(
    selected.map((q) => q.id),
    ["root", "child"],
  );
});
test("a draft subpart makes its entire group ineligible", () => {
  const q = data.questions[0];
  assert.equal(
    eligible(
      {
        ...data,
        questions: [
          { ...q, id: "parent" },
          {
            ...q,
            id: "child",
            parentQuestionId: "parent",
            publicationStatus: "draft",
          },
        ],
      },
      { form: 1, subjectId: "chemistry" },
    ).length,
    0,
  );
});

test('prepared original papers stay separate from authentic past-paper inventory', () => {
  const originals = data.papers.filter(p => p.sourceType === 'original');
  assert.equal(originals.length, 18);
  for (const p of originals) {
    assert.equal(new Set(p.questionIds).size, p.questionIds.length);
    const questions = p.questionIds.map(id => data.questions.find(q => q.id === id));
    assert(questions.every(q => q && q.sourceType === 'original' && q.form === p.form && q.subjectId === p.subjectId));
    assert.equal(questions.reduce((n,q) => n + q.maximumMarks, 0), p.maximumMarks);
  }
});
test('every workbook has distinct exercises and a mixed revision selection', () => {
  for (const b of data.books.filter(b => b.kind === 'workbook')) {
    assert(b.mixedTestQuestionIds.length >= 5);
    for (const id of b.lessonIds) assert(data.questions.some(q => q.topicIds.includes(id) && q.resourceKind === 'workbook'));
    assert(b.mixedTestQuestionIds.every(id => data.questions.find(q => q.id === id)?.resourceKind === 'workbook'));
  }
});
test('published partial curriculum references point to the correct official form and subject', () => {
  const activities = new Map(data.curriculum.activities.map(a => [a.id,a]));
  for (const l of data.lessons) for (const ref of l.curriculumRefs || []) {
    const a = activities.get(ref.activityId);
    assert(a); assert.equal(a.form,l.form); assert.equal(a.subjectId,l.subjectId);
    assert.deepEqual(a.pdfPages,ref.pdfPages); assert.equal(ref.scope,'partial-support');
  }
});
test('corrected form placements preserve stable chapter IDs', () => {
  for (const [id,form] of [['physics-f2-01',1],['mathematics-f2-01',1],['geography-f1-01',2]]) {
    assert.equal(data.lessons.find(l=>l.id===id).form,form);
    assert(data.questions.filter(q=>q.topicIds.includes(id)).every(q=>q.form===form));
  }
});
