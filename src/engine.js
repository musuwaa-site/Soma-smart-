export function eligible(
  data,
  { form, subjectId, topics = [], source = "all" },
) {
  const groups = new Map();
  const root = (q) => {
    let current = q;
    const seen = new Set();
    while (current.parentQuestionId) {
      if (seen.has(current.id)) throw Error("Cyclic question group");
      seen.add(current.id);
      const parent = data.questions.find(
        (p) => p.id === current.parentQuestionId,
      );
      if (!parent) return null;
      current = parent;
    }
    return current.id;
  };
  for (const q of data.questions) {
    const id = root(q);
    if (!id) continue;
    if (!groups.has(id)) groups.set(id, []);
    groups.get(id).push(q);
  }
  const valid = (q) =>
    q.form === Number(form) &&
    q.subjectId === subjectId &&
    q.publicationStatus === "published" &&
    q.answerKey &&
    q.maximumMarks > 0 &&
    (source === "all" ||
      (source === "authentic"
        ? q.sourceType !== "original"
        : q.sourceType === source)) &&
    (q.sourceType === "original" ||
      (["cleared", "public-domain", "open-license"].includes(q.rightsStatus) &&
        q.verificationStatus === "verified"));
  return [...groups.values()]
    .filter(
      (group) =>
        group.every(valid) &&
        (!topics.length ||
          group.some((q) => q.topicIds.some((t) => topics.includes(t)))),
    )
    .flat();
}
export function generate(bank, count, seed = 1) {
  if (!Number.isInteger(count) || count < 1)
    throw Error("Choose a positive whole number of questions.");
  let state = Number(seed) >>> 0;
  const random = () => {
    state = (1664525 * state + 1013904223) >>> 0;
    return state / 4294967296;
  };
  const groups = new Map();
  for (const q of bank) {
    let root = q;
    const seen = new Set();
    while (root.parentQuestionId) {
      if (seen.has(root.id)) throw Error("Cyclic question group");
      seen.add(root.id);
      const parent = bank.find((p) => p.id === root.parentQuestionId);
      if (!parent) throw Error("Incomplete question group");
      root = parent;
    }
    const key = root.id;
    if (!groups.has(key)) groups.set(key, []);
    groups.get(key).push(q);
  }
  const shuffled = [...groups.values()];
  for (let i = shuffled.length - 1; i > 0; i--) {
    const j = Math.floor(random() * (i + 1));
    [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
  }
  const result = [];
  for (const group of shuffled)
    if (result.length + group.length <= count) result.push(...group);
  if (!result.length)
    throw Error(
      "No complete question group fits this selection. Increase the count or change topics.",
    );
  return result;
}
export function mark(q, answer, selfMark) {
  if (answer === undefined || answer === null || String(answer).trim() === "")
    return { status: "unanswered", earned: 0 };
  if (q.type === "mcq")
    return {
      status: answer === q.answerKey ? "correct" : "incorrect",
      earned: answer === q.answerKey ? q.maximumMarks : 0,
    };
  if (q.type === "matching") {
    const correct = q.answerKey;
    if (!Object.values(answer).some(Boolean))
      return { status: "unanswered", earned: 0 };
    const earned = Object.entries(correct).reduce(
      (n, [key, val]) => n + (answer[key] === val ? q.markIncrement : 0),
      0,
    );
    return {
      status:
        earned === q.maximumMarks
          ? "correct"
          : earned
            ? "partial"
            : "incorrect",
      earned,
    };
  }
  if (selfMark === undefined || selfMark === null || selfMark === "")
    return { status: "pending", earned: 0 };
  const earned = Number(selfMark),
    steps = earned / q.markIncrement;
  if (
    !Number.isFinite(earned) ||
    earned < 0 ||
    earned > q.maximumMarks ||
    Math.abs(steps - Math.round(steps)) > 1e-8
  )
    throw Error("Marks must be within the range and permitted increment.");
  return {
    status:
      earned === q.maximumMarks
        ? "correct"
        : earned === 0
          ? "incorrect"
          : "partial",
    earned,
  };
}
export function result(questions, answers = {}, marks = {}) {
  const rows = questions.map((q) => ({
    id: q.id,
    topics: q.topicIds,
    ...mark(q, answers[q.id], marks[q.id]),
  }));
  return {
    rows,
    earned: rows.reduce((n, r) => n + r.earned, 0),
    maximum: questions.reduce((n, q) => n + q.maximumMarks, 0),
    pending: rows.filter((r) => r.status === "pending").length,
  };
}
export function weakTopics(attempts) {
  const stats = {};
  for (const a of attempts.filter((a) => a.final)) {
    for (const r of a.result.rows) {
      for (const t of r.topics) {
        const s = (stats[t] ??= { earned: 0, maximum: 0, items: 0 });
        s.earned += r.earned;
        s.maximum += a.questions.find((q) => q.id === r.id).maximumMarks;
        s.items++;
      }
    }
  }
  return Object.entries(stats)
    .map(([id, s]) => ({ id, ...s, ratio: s.earned / s.maximum }))
    .sort((a, b) => a.ratio - b.ratio);
}
