import "./style.css";
import { eligible, generate, result, weakTopics } from "./engine.js";
import { get, set } from "./storage.js";
const app = document.querySelector("#app");
const esc = (v) =>
  String(v ?? "").replace(
    /[&<>"']/g,
    (c) =>
      ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[
        c
      ],
  );
let data,
  profile,
  attempts,
  draft,
  offline = "Installing offline library…",
  routeError = "",
  examFilter,
  privateDocs = [];
const subject = (id) => data.subjects.find((s) => s.id === id);
const lesson = (id) => data.lessons.find((s) => s.id === id);
const link = (path, text, cls = "button") =>
  `<a class="${cls}" href="#/${path}">${esc(text)}</a>`;
const notice = (text) => `<div class="notice">${esc(text)}</div>`;
async function saveProfile() {
  await set("profile", profile);
}
function frame(body, active = "home") {
  app.innerHTML = `<header><a class="brand" href="#/"><img src="/icon.svg" alt="">SomaSmart</a><div class="row"><small id="offline" role="status">${esc(offline)}</small><select id="form" aria-label="Select form"><option value="1" ${profile.form === 1 ? "selected" : ""}>Form One</option><option value="2" ${profile.form === 2 ? "selected" : ""}>Form Two</option></select></div></header><main class="shell">${routeError ? notice(routeError) : ""}${body}<p class="footer">Development edition • Original starter content • One local student profile. Clearing browser storage or changing devices can erase your progress.</p></main><nav aria-label="Main">${[
    ["home", "", "Home"],
    ["study", "study", "Study"],
    ["exams", "exams", "Exams"],
    ["progress", "progress", "Progress"],
  ]
    .map(([id, path, label]) =>
      link(path, label, id === active ? "active" : ""),
    )
    .join(
      "",
    )}</nav><dialog id="definition"><h2 id="term-title"></h2><p id="term-definition"></p><button id="close-definition">Close</button></dialog>`;
  document.querySelector("#form").onchange = async (e) => {
    profile.form = Number(e.target.value);
    await saveProfile();
    examFilter = null;
    location.hash = "#/";
    render();
  };
  document.querySelector("#close-definition").onclick = () =>
    document.querySelector("dialog").close();
}
function cards() {
  return data.subjects
    .map((s) => {
      const ls = data.lessons.filter(
        (l) => l.form === profile.form && l.subjectId === s.id,
      );
      const done = ls.filter((l) => profile.completed.includes(l.id)).length;
      return `<a class="card" href="#/study/${s.id}"><span class="icon">${esc(s.icon)}</span><h3>${esc(s.name)}</h3><span class="muted">${ls.length} starter chapter • ${done} completed</span></a>`;
    })
    .join("");
}
function home() {
  const weak = weakTopics(attempts).filter(
    (t) => lesson(t.id)?.form === profile.form,
  );
  frame(
    `<div class="row"><span class="eyebrow">Your learning space / Form ${profile.form}</span><span class="pill">No account needed</span></div><section class="hero"><span class="eyebrow">Small steps. Strong foundations.</span><h1>Make today a<br>learning day.</h1><p>Read a chapter, work through an example, and put your understanding into practice.</p>${link(profile.lastLesson && lesson(profile.lastLesson)?.form === profile.form ? "lesson/" + profile.lastLesson : "study", "Continue learning →")}</section><div class="stats"><div class="stat"><strong>${profile.completed.length}</strong>Chapters completed</div><div class="stat"><strong>${attempts.filter((a) => a.final).length}</strong>Exams marked</div><div class="stat"><strong>${data.questions.length}</strong>Original practice items</div></div>${notice("This is a partial development library. Official 2027 curriculum alignment and complete books are not yet verified. Genuine past-paper questions are not yet cleared for publication.")}<div class="row"><h2>Your subjects</h2>${link("study", "Explore library", "")}</div><div class="grid">${cards()}</div><h2>Today’s revision</h2>${
      weak.length
        ? weak
            .slice(0, 3)
            .map(
              (t) =>
                `<div class="card">${link("lesson/" + t.id, lesson(t.id)?.title || t.id, "")} <span class="pill">${Math.round(t.ratio * 100)}% earned</span></div>`,
            )
            .join("")
        : `<div class="card">${link("lesson/" + data.lessons.find((l) => l.form === profile.form).id, "Start with a chapter, then try its exercises.", "")}</div>`
    }${
      profile.recent?.length
        ? `<h2>Recently studied</h2><div class="stats">${profile.recent
            .filter((id) => lesson(id)?.form === profile.form)
            .map((id) => link("lesson/" + id, lesson(id).title, "card"))
            .join("")}</div>`
        : ""
    }`,
  );
}
function study(sid) {
  if (!sid) {
    frame(
      `<span class="eyebrow">Study / Form ${profile.form}</span><h1>A little understanding.<br>A world of possibility.</h1><p class="muted">Read original chapters and work through revision activities.</p><div class="grid">${cards()}</div>`,
      "study",
    );
    return;
  }
  const s = subject(sid);
  if (!s) throw Error("Subject not found.");
  const books = data.books.filter(
    (b) => b.form === profile.form && b.subjectId === sid,
  );
  frame(
    `${link("study", "← All subjects", "")}<h1>${esc(s.name)}</h1><p class="muted">Form ${profile.form} • ${s.language === "sw" ? "Kiswahili" : "English"} • Official topic mapping pending</p><div class="split">${books.map((b) => `<section class="card"><span class="pill">Partial manuscript</span><h2>${esc(b.title)}</h2><p>${b.kind === "textbook" ? "Explanations, worked examples and glossary." : "Topic exercises, model answers and a short revision test."}</p>${b.introduction ? `<p>${esc(b.introduction)}</p>` : ""}${b.lessonIds.map((id) => link((b.kind === "textbook" ? "lesson/" : "workbook/") + id, lesson(id).title)).join("")}${b.mixedTestQuestionIds?.length ? `<p><button data-workbook-test="${b.id}">Mixed chapter revision test</button></p>` : ""}</section>`).join("")}</div><h2>Chapters</h2>${data.lessons
      .filter((l) => l.form === profile.form && l.subjectId === sid)
      .map(
        (l) =>
          `<div class="card row"><div><h3>${esc(l.title)}</h3><span class="muted">${profile.completed.includes(l.id) ? "✓ Completed" : "Ready to read"}</span></div>${link("lesson/" + l.id, "Read chapter →")}</div>`,
      )
      .join("")}`,
    "study",
  );
  document.querySelectorAll('[data-workbook-test]').forEach(button => button.onclick = () => {
    const book = data.books.find(b => b.id === button.dataset.workbookTest);
    startExam(book.mixedTestQuestionIds.map(id => data.questions.find(q => q.id === id)), book.title + ' • mixed revision');
  });
}
async function reader(id, workbook = false) {
  const l = lesson(id);
  if (!l) throw Error("Chapter not found.");
  profile.lastLesson = id;
  profile.recent = [
    id,
    ...(profile.recent || []).filter((x) => x !== id),
  ].slice(0, 6);
  await saveProfile();
  frame(
    `<article class="reader" lang="${l.language}">${link("study/" + l.subjectId, "← " + subject(l.subjectId).name, "")}<span class="pill">Form ${l.form} • Starter chapter</span><h1>${esc(l.title)}</h1><div class="book-tabs">${link("lesson/" + id, "Read", "button " + (workbook ? "secondary" : ""))}${link("workbook/" + id, "Revision workbook", "button " + (!workbook ? "secondary" : ""))}</div>${
      workbook
        ? `<p>Try these activities before revealing the model answers. Use the rubric to assess your reasoning; more than one valid wording may be possible.</p><button id="start-practice">Start chapter revision test</button>`
        : `<h2>Learning objectives</h2><ul>${l.objectives.map((o) => `<li>${esc(o)}</li>`).join("")}</ul>${l.paragraphs.map((p) => `<p>${esc(p)}</p>`).join("")}${l.diagram ? `<figure><img src="${esc(l.diagram)}" alt="${l.diagramAlt || (l.subjectId === "biology" ? "Simplified plant cell showing cell wall, membrane, vacuole and nucleus." : "Particle model of solid, liquid and gas.")}"><figcaption class="muted">Original SomaSmart schematic; not to scale.</figcaption></figure>` : ""}<h2>Key terms · Tap to explore</h2>${data.glossary
            .filter((g) => g.lessonId === id)
            .map(
              (g) =>
                `<button class="term" data-term="${esc(g.id)}">${esc(g.term)}</button>`,
            )
            .join(
              "",
            )}<h2>Worked examples</h2>${l.examples.map((x, i) => `<div class="example"><strong>${l.language === "sw" ? "Mfano" : "Example"} ${i + 1}</strong><p>${esc(x)}</p></div>`).join("")}<h2>Remember</h2><p>${esc(l.summary)}</p><button id="complete">${profile.completed.includes(id) ? "✓ Chapter completed" : "Mark chapter complete"}</button>`
    }<h2>${workbook ? "Practice activities & model answers" : "Check your understanding"}</h2>${data.questions
      .filter((q) => q.topicIds.includes(id) && (workbook ? q.resourceKind === "workbook" : q.resourceKind !== "workbook"))
      .map(
        (q, i) =>
          `<section class="card question"><h3>${i + 1}. ${esc(q.content)}</h3>${q.options.length ? `<p>${q.options.map(esc).join(" / ")}</p>` : ""}<details><summary>Model answer & explanation</summary><p>${esc(typeof q.answerKey === "object" ? Object.entries(q.answerKey).map(([k,v]) => k + ": " + v).join("; ") : q.answerKey)}</p><p class="muted">${esc(q.markingGuide)}</p></details></section>`,
      )
      .join(
        "",
      )}${workbook ? "" : `<button id="start-practice">Practise this chapter →</button>`}</article>`,
    "study",
  );
  document.querySelectorAll("[data-term]").forEach(
    (b) =>
      (b.onclick = () => {
        const g = data.glossary.find((g) => g.id === b.dataset.term);
        document.querySelector("#term-title").textContent = g.term;
        document.querySelector("#term-definition").textContent = g.definition;
        document.querySelector("dialog").showModal();
      }),
  );
  const complete = document.querySelector("#complete");
  if (complete)
    complete.onclick = async () => {
      if (!profile.completed.includes(id)) profile.completed.push(id);
      await saveProfile();
      complete.textContent = "✓ Chapter completed";
    };
  document.querySelector("#start-practice").onclick = () =>
    startExam(
      data.questions.filter((q) => q.topicIds.includes(id) && (workbook ? q.resourceKind === "workbook" : q.resourceKind !== "workbook")),
      `Chapter revision: ${l.title}`,
    );
}
function exams() {
  if (draft) {
    exam();
    return;
  }
  examFilter ??= {
    form: profile.form,
    subjectId: "chemistry",
    topics: [],
    source: "original",
  };
  const list = eligible(data, examFilter);
  frame(
    `<span class="eyebrow">Examination centre</span><h1>Practise with purpose.</h1><p class="muted">Build a test from the actual embedded question bank.</p><section class="card"><div class="formgrid"><label>Subject<select id="exam-subject">${data.subjects.map((s) => `<option value="${s.id}" ${s.id === examFilter.subjectId ? "selected" : ""}>${esc(s.name)}</option>`).join("")}</select></label><label>Source<select id="exam-source">${[
      ["original", "Original practice"],
      ["authentic", "Genuine papers only"],
      ["school", "School"],
      ["mock", "Mock"],
      ["necta", "NECTA"],
      ["all", "Combined (original + eligible genuine)"],
    ]
      .map(
        ([v, n]) =>
          `<option value="${v}" ${v === examFilter.source ? "selected" : ""}>${n}</option>`,
      )
      .join(
        "",
      )}</select></label></div><fieldset><legend>Topics · leave unchecked to use all</legend>${data.lessons
      .filter(
        (l) => l.form === profile.form && l.subjectId === examFilter.subjectId,
      )
      .map(
        (l) =>
          `<label><input type="checkbox" name="topic" value="${l.id}" ${examFilter.topics.includes(l.id) ? "checked" : ""}> ${esc(l.title)}</label>`,
      )
      .join(
        "",
      )}</fieldset><div class="formgrid"><label>Number of question parts<input id="count" type="number" min="1" max="${Math.max(1, list.length)}" value="${Math.min(5, list.length) || 1}"></label><label>Selection seed<input id="seed" type="number" value="2027"></label></div><p><strong>${list.length}</strong> eligible question parts</p>${list.length ? '<button id="generate">Create examination →</button>' : `<div class="empty">No eligible embedded questions match this source. Genuine papers require source, rights, extraction and marking verification. ${link("exams", "Choose original practice", "")}</div>`}<div id="exam-message" role="alert"></div></section><h2>Prepared revision papers</h2><p class="muted">Original SomaSmart tests covering the published chapters; these are not past school or NECTA papers.</p><div class="grid">${data.papers.filter(p => p.sourceType === "original" && p.form === profile.form && p.publicationStatus === "published").map(p => `<section class="card"><h3>${esc(p.title)}</h3><p>${p.questionIds.length} items · ${p.maximumMarks} marks</p><button data-paper="${p.id}">Start revision paper</button></section>`).join("")}</div><h2>Private source documents</h2><section class="card"><p>Import a PDF you may lawfully use. Files stay on this device and are never published. These reference documents are not automatically transcribed or eligible for scored exams.</p><label>Choose a private PDF<input id="private-file" type="file" accept="application/pdf"></label><div id="private-status" role="status"></div>${privateDocs.map((p, i) => `<p><button class="secondary" data-private="${i}">${esc(p.name)}</button></p>`).join("")}</section><h2>Previous attempts</h2>${
      attempts.length
        ? attempts
            .slice()
            .reverse()
            .map(
              (a) =>
                `<div class="card row"><span>${esc(a.title)}<br><small>${new Date(a.created).toLocaleDateString()} • ${a.final ? "Marked" : "Pending self-marking"}</small></span><button class="secondary" data-review="${a.id}">Review ${a.result.earned}/${a.result.maximum}</button></div>`,
            )
            .join("")
        : '<p class="muted">Your saved examinations will appear here.</p>'
    }`,
    "exams",
  );
  document.querySelectorAll('[data-paper]').forEach(button => button.onclick = () => {
    const paper = data.papers.find(p => p.id === button.dataset.paper);
    startExam(paper.questionIds.map(id => data.questions.find(q => q.id === id)), paper.title);
  });
  document.querySelector("#private-file").onchange = async (e) => {
    try {
      const file = e.target.files[0];
      if (!file) return;
      if (file.size > 30 * 1024 * 1024)
        throw Error("Choose a PDF below 30 MB.");
      const head = new TextDecoder().decode(
        await file.slice(0, 5).arrayBuffer(),
      );
      if (head !== "%PDF-") throw Error("This file is not a PDF.");
      const next = [
        ...privateDocs,
        { id: crypto.randomUUID(), name: file.name, blob: file },
      ];
      await set("privateDocuments", next);
      privateDocs = next;
      exams();
    } catch (error) {
      document.querySelector("#private-status").textContent = error.message;
    }
  };
  document.querySelectorAll("[data-private]").forEach(
    (b) =>
      (b.onclick = () => {
        const doc = privateDocs[Number(b.dataset.private)];
        const url = URL.createObjectURL(doc.blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = doc.name;
        a.click();
        setTimeout(() => URL.revokeObjectURL(url), 60000);
      }),
  );
  document.querySelector("#exam-subject").onchange = (e) => {
    examFilter.subjectId = e.target.value;
    examFilter.topics = [];
    exams();
  };
  document.querySelector("#exam-source").onchange = (e) => {
    examFilter.source = e.target.value;
    exams();
  };
  document.querySelectorAll("[name=topic]").forEach(
    (t) =>
      (t.onchange = () => {
        examFilter.topics = [
          ...document.querySelectorAll("[name=topic]:checked"),
        ].map((t) => t.value);
        exams();
      }),
  );
  const b = document.querySelector("#generate");
  if (b)
    b.onclick = () => {
      try {
        const n = Number(document.querySelector("#count").value);
        if (n > list.length)
          throw Error(
            `Only ${list.length} questions are available. Choose a smaller test.`,
          );
        startExam(
          generate(list, n, Number(document.querySelector("#seed").value)),
          `${subject(examFilter.subjectId).name} • Form ${profile.form}`,
        );
      } catch (e) {
        document.querySelector("#exam-message").textContent = e.message;
      }
    };
  document.querySelectorAll("[data-review]").forEach(
    (b) =>
      (b.onclick = async () => {
        draft = structuredClone(
          attempts.find((a) => a.id === b.dataset.review),
        );
        await set("draft", draft);
        exam();
      }),
  );
}
async function startExam(questions, title) {
  if (draft && !draft.submitted) {
    routeError =
      "Resume or discard your existing draft before starting another test.";
    location.hash = "#/exams";
    render();
    return;
  }
  draft = {
    id: crypto.randomUUID(),
    created: new Date().toISOString(),
    form: questions[0].form,
    title,
    questions,
    answers: {},
    marks: {},
    submitted: false,
    final: false,
  };
  await set("draft", draft);
  location.hash = "#/exams";
  exam();
}
function answerInput(q) {
  const answer = draft.answers[q.id];
  if (q.type === "mcq")
    return `<div class="options">${q.options.map((o) => `<label><input type="radio" name="${q.id}" data-answer="${q.id}" value="${esc(o)}" ${o === answer ? "checked" : ""} ${draft.submitted ? "disabled" : ""}>${esc(o)}</label>`).join("")}</div>`;
  if (q.type === "matching")
    return (q.pairs || [])
      .map(
        (p) =>
          `<label>${esc(p.left)}<select data-match="${q.id}" data-key="${esc(p.id)}" ${draft.submitted ? "disabled" : ""}><option value="">Choose</option>${q.options.map((o) => `<option ${answer?.[p.id] === o ? "selected" : ""}>${esc(o)}</option>`).join("")}</select></label>`,
      )
      .join("");
  return `<textarea data-answer="${q.id}" aria-label="Answer to question ${q.questionNumber}" ${draft.submitted ? "readonly" : ""} placeholder="Write your answer or working here…">${esc(answer || "")}</textarea>`;
}
function exam() {
  const r = result(draft.questions, draft.answers, draft.marks);
  frame(
    `<span class="eyebrow">${draft.submitted ? "Review & marking" : "Saved examination draft"} / Form ${draft.form}</span><h1>${esc(draft.title)}</h1><p class="muted">${draft.questions.length} question parts • ${r.maximum} available marks • Written answers require your self-assessment.</p><div class="save-status" id="saved" role="status">Saved on this device</div>${draft.submitted ? `<section class="card"><span class="score">${r.earned}/${r.maximum}</span><p>${r.pending ? `${r.pending} written answers await self-marking. Score is provisional.` : "Marking complete."}</p></section>` : ""}${draft.questions
      .map((q, i) => {
        const row = r.rows[i];
        return `<section class="card question"><div class="row"><span class="pill">${esc(q.sourceTitle)}</span><span class="muted">${q.maximumMarks} marks · ${esc(q.type)}</span></div><h3>${i + 1}. ${esc(q.content)}</h3>${q.instructions ? `<p>${esc(q.instructions)}</p>` : ""}${(q.media || []).map((m) => `<img src="${esc(m.path)}" alt="${esc(m.alt)}" style="max-width:100%">`).join("")}${q.passage ? `<blockquote>${esc(q.passage)}</blockquote>` : ""}${q.table ? `<table>${q.table.map((row) => `<tr>${row.map((c) => `<td>${esc(c)}</td>`).join("")}</tr>`).join("")}</table>` : ""}${answerInput(q)}${draft.submitted ? `<div class="feedback"><strong>${esc(row.status)} · ${row.earned}/${q.maximumMarks}</strong><p>Model answer: ${esc(typeof q.answerKey === "object" ? JSON.stringify(q.answerKey) : q.answerKey)}</p><p>${esc(q.markingGuide)}</p><small>${esc(q.solutionProvenance)} • ${esc(q.sourceReference)}</small>${!["mcq", "matching"].includes(q.type) && draft.answers[q.id]?.trim() ? `<label>Your earned marks (0–${q.maximumMarks}, steps of ${q.markIncrement})<input data-marks="${q.id}" type="number" min="0" max="${q.maximumMarks}" step="${q.markIncrement}" value="${draft.marks[q.id] ?? ""}"></label>` : ""}</div>` : ""}</section>`;
      })
      .join(
        "",
      )}<div class="row">${!draft.submitted ? '<button id="submit">Submit for marking</button>' : '<button id="finish">Save review & return</button>'}<button id="discard" class="secondary">${draft.submitted ? "Close review" : "Discard draft"}</button></div><p id="mark-error" role="alert"></p>`,
    "exams",
  );
  async function persist() {
    await set("draft", draft);
    document.querySelector("#saved").textContent = "Saved on this device";
  }
  document.querySelectorAll("[data-answer]").forEach(
    (el) =>
      (el.oninput = async () => {
        draft.answers[el.dataset.answer] = el.value;
        try {
          await persist();
        } catch (e) {
          document.querySelector("#saved").textContent =
            "Not saved: " + e.message;
        }
      }),
  );
  document.querySelectorAll("[data-match]").forEach(
    (el) =>
      (el.onchange = async () => {
        (draft.answers[el.dataset.match] ??= {})[el.dataset.key] = el.value;
        await persist();
      }),
  );
  document.querySelectorAll("[data-marks]").forEach(
    (el) =>
      (el.onchange = async () => {
        const id = el.dataset.marks;
        try {
          const next = {
            ...draft.marks,
            [id]: el.value === "" ? null : Number(el.value),
          };
          result(draft.questions, draft.answers, next);
          draft.marks = next;
          await record();
          exam();
        } catch (e) {
          document.querySelector("#mark-error").textContent = e.message;
        }
      }),
  );
  const submit = document.querySelector("#submit");
  if (submit)
    submit.onclick = async () => {
      draft.submitted = true;
      await record();
      exam();
    };
  const finish = document.querySelector("#finish");
  if (finish)
    finish.onclick = async () => {
      await record();
      draft = null;
      await set("draft", null);
      exams();
    };
  document.querySelector("#discard").onclick = async () => {
    if (!draft.submitted && !confirm("Discard this unfinished test?")) return;
    draft = null;
    await set("draft", null);
    exams();
  };
}
async function record() {
  draft.result = result(draft.questions, draft.answers, draft.marks);
  draft.final = draft.result.pending === 0;
  const i = attempts.findIndex((a) => a.id === draft.id);
  if (i >= 0) attempts[i] = structuredClone(draft);
  else attempts.push(structuredClone(draft));
  await set("attempts", attempts);
  await set("draft", draft);
}
function progress() {
  const weak = weakTopics(attempts);
  const mistakes = attempts.flatMap((a) =>
    (a.result?.rows || [])
      .filter((r) => ["incorrect", "partial", "unanswered"].includes(r.status))
      .map((r) => ({ a, r, q: a.questions.find((q) => q.id === r.id) })),
  );
  frame(
    `<span class="eyebrow">Your progress</span><h1>See how far you’ve come.</h1><div class="stats"><div class="stat"><strong>${profile.completed.length}/${data.lessons.length}</strong>Available chapters completed</div><div class="stat"><strong>${attempts.filter((a) => a.final).length}</strong>Marked tests</div><div class="stat"><strong>${attempts.filter((a) => !a.final).length}</strong>Awaiting self-marking</div></div><h2>Topics to revisit</h2>${weak.length ? weak.map((t) => `<div class="card row"><div>${link("lesson/" + t.id, lesson(t.id)?.title || t.id, "")}<p class="muted">${t.items} assessed items · ${Math.round(t.ratio * 100)}% of available marks</p></div>${link("workbook/" + t.id, "Revise", "button secondary")}</div>`).join("") : '<div class="empty">Complete and mark an examination to see evidence-based recommendations.</div>'}<h2>Mistake notebook</h2>${mistakes.length ? mistakes.map(({ q, r }) => `<details class="card"><summary>${esc(q.content)} <span class="pill">${esc(r.status)}</span></summary><p>${esc(q.answerKey)}</p><p>${esc(q.markingGuide)}</p>${link("lesson/" + q.topicIds[0], "Revisit chapter", "")}</details>`).join("") : '<p class="muted">Questions to revisit will be saved here after an exam.</p>'}<h2>Completed reading</h2>${profile.completed.map((id) => `<p>${link("lesson/" + id, lesson(id)?.title || id, "")}</p>`).join("") || '<p class="muted">Mark chapters complete as you finish reading.</p>'}`,
    "progress",
  );
}
async function render() {
  try {
    const [page, id] = location.hash.replace(/^#\/?/, "").split("/");
    if (page === "study") study(id);
    else if (page === "lesson" || page === "workbook")
      await reader(id, page === "workbook");
    else if (page === "exams") exams();
    else if (page === "progress") progress();
    else home();
    window.scrollTo(0, 0);
  } catch (e) {
    routeError = e.message;
    frame(
      `<h1>Something needs attention</h1><p>${esc(e.message)}</p>${link("", "Return home")}`,
    );
  }
}
function setOffline(text) {
  offline = text;
  const el = document.querySelector("#offline");
  if (el) el.textContent = text;
}
async function provision() {
  if (!("serviceWorker" in navigator)) {
    setOffline("Offline installation unsupported in this browser");
    return;
  }
  navigator.serviceWorker.addEventListener("message", (event) => {
    const m = event.data;
    if (m.type === "PROGRESS")
      setOffline(`Installing offline: ${m.done}/${m.total}`);
    if (m.type === "ERROR") setOffline("Setup incomplete: " + m.message);
  });
  try {
    const reg = await navigator.serviceWorker.register("/sw.js");
    await navigator.serviceWorker.ready;
    const channel = new MessageChannel();
    channel.port1.onmessage = (e) => {
      if (e.data.ready) setOffline("✓ Library ready offline");
      else
        setOffline("Offline setup incomplete — reconnect and reload to retry");
    };
    const worker = reg.active || navigator.serviceWorker.controller;
    worker?.postMessage({ type: "STATUS" }, [channel.port2]);
    if (navigator.storage?.persist) await navigator.storage.persist();
  } catch (e) {
    setOffline("Offline setup incomplete — reconnect and reload. " + e.message);
  }
}
async function boot() {
  try {
    const response = await fetch("/library.json");
    if (!response.ok) throw Error("Learning library could not be loaded.");
    data = await response.json();
    profile = await get("profile", {
      form: 1,
      completed: [],
      recent: [],
      lastLesson: null,
    });
    attempts = await get("attempts", []);
    draft = await get("draft", null);
    privateDocs = await get("privateDocuments", []);
    await render();
    await provision();
  } catch (e) {
    app.innerHTML = `<main class="shell"><h1>SomaSmart needs setup</h1><p>${esc(e.message)}</p><p>Check storage space and reconnect to finish installation.</p><button onclick="location.reload()">Retry setup</button></main>`;
  }
}
window.addEventListener("hashchange", render);
window.addEventListener("unhandledrejection", (event) => {
  setOffline(
    "Action not saved: " +
      (event.reason?.message || "Storage error. Check free space and retry."),
  );
});
boot();
