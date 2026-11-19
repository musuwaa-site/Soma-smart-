import { selectSourceGroups, sourceGroupPages } from './source-practice.js';
import "./style.css";
import { verbatimContent, originalOptionLabel } from "./exam-format.js";
import { eligible, generate, result, weakTopics } from "./engine.js";
import { get, set } from "./storage.js";
import { loadLibrary, withStorageTimeout } from './startup.js';
const app = document.querySelector("#app");
let sourceAnswers = {};
let sourcePractice = {};
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
  offline = "Offline download paused",
  offlineMode = "initial",
  routeError = "",
  examFilter,
  privateDocs = [];
const subject = (id) => data.subjects.find((s) => s.id === id);
const lesson = (id) => data.lessons.find((s) => s.id === id);
const link = (path, text, cls = "button") =>
  `<a class="${cls}" href="#/${path}">${esc(text)}</a>`;
const notice = (text) => `<div class="notice">${esc(text)}</div>`;
const dashboardButton = () => link('exams', '← Back to exam dashboard', 'button secondary');
async function saveProfile() {
  await set("profile", profile);
}
function frame(body, active = "home") {
  app.innerHTML = `<header><a class="brand" href="#/"><img src="/icon.svg" alt="">SomaSmart</a><div class="row"><small id="offline" role="status">${esc(offline)}</small><button type="button" class="secondary" id="offline-action" hidden></button><select id="form" aria-label="Select form"><option value="1" ${profile.form === 1 ? "selected" : ""}>Form One</option><option value="2" ${profile.form === 2 ? "selected" : ""}>Form Two</option></select></div></header><main class="shell">${routeError ? notice(routeError) : ""}${body}<p class="footer">Development edition • Growing learning library • One local student profile. Clearing browser storage or changing devices can erase your progress.</p></main><nav aria-label="Main">${[
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
  updateOfflineButton();
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
      return `<a class="card" href="#/study/${s.id}"><span class="icon">${esc(s.icon)}</span><h3>${esc(s.name)}</h3><span class="muted">${ls.length} chapters • ${done} completed</span></a>`;
    })
    .join("");
}
function home() {
  const weak = weakTopics(attempts).filter(
    (t) => lesson(t.id)?.form === profile.form,
  );
  frame(
    `<div class="row"><span class="eyebrow">Your learning space / Form ${profile.form}</span><span class="pill">No account needed</span></div><section class="hero"><span class="eyebrow">Small steps. Strong foundations.</span><h1>Make today a<br>learning day.</h1><p>Read a chapter, work through an example, and put your understanding into practice.</p>${link(profile.lastLesson && lesson(profile.lastLesson)?.form === profile.form ? "lesson/" + profile.lastLesson : "study", "Continue learning →")}</section><div class="stats"><div class="stat"><strong>${profile.completed.length}</strong>Chapters completed</div><div class="stat"><strong>${attempts.filter((a) => a.final).length}</strong>Exams marked</div><div class="stat"><strong>${data.questions.filter(q => q.sourceType === "original").length}</strong>Original practice items</div></div>${notice("Development library: more lessons are being added to complete the syllabus. Full source papers and practice tests are available in Exams.")}<div class="row"><h2>Your subjects</h2>${link("study", "Explore library", "")}</div><div class="grid">${cards()}</div><h2>Today’s revision</h2>${
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
    `${link("study", "← All subjects", "")}<h1>${esc(s.name)}</h1><p class="muted">Form ${profile.form} • ${s.language === "sw" ? "Kiswahili" : "English"} • Official topic mapping pending</p><div class="split">${books.map((b) => `<section class="card"><span class="pill">Partial manuscript</span><h2>${esc(b.title)}</h2><p>${b.kind === "textbook" ? "Explanations, worked examples and glossary." : "Topic exercises, model answers and a short revision test."}</p>${b.introduction ? `<p>${esc(b.introduction)}</p>` : ""}<p><a href="/books/${b.id}.epub" download>Download current manuscript (EPUB)</a></p>${b.lessonIds.map((id) => link((b.kind === "textbook" ? "lesson/" : "workbook/") + id, lesson(id).title)).join("")}${b.mixedTestQuestionIds?.length ? `<p><button data-workbook-test="${b.id}">Mixed chapter revision test</button></p>` : ""}</section>`).join("")}</div><h2>Chapters</h2>${data.lessons
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
function questionContext(q) {
  return (q.passage ? `<blockquote>${esc(q.passage)}</blockquote>` : '') +
    (q.table ? `<table>${q.table.map(row => `<tr>${row.map(c => `<td>${esc(c)}</td>`).join('')}</tr>`).join('')}</table>` : '') +
    (q.media || []).map(m => `<img src="${esc(m.path)}" alt="${esc(m.alt || 'Question figure')}" style="max-width:100%">`).join('');
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
    `<article class="reader" lang="${l.language}">${link("study/" + l.subjectId, "← " + subject(l.subjectId).name, "")}<span class="pill">Form ${l.form} • ${l.completionStatus === "expanded-chapter" ? "Study chapter" : "Starter chapter"}</span><h1>${esc(l.title)}</h1><div class="book-tabs">${link("lesson/" + id, "Read", "button " + (workbook ? "secondary" : ""))}${link("workbook/" + id, "Revision workbook", "button " + (!workbook ? "secondary" : ""))}</div>${
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
      .filter((q) => q.sourceType === "original" && q.topicIds.includes(id) && (workbook ? q.resourceKind === "workbook" : q.resourceKind !== "workbook"))
      .map(
        (q, i) =>
          `<section class="card question"><h3>${i + 1}. ${verbatimContent(q)}</h3>${questionContext(q)}${q.options.length ? `<p>${q.options.map(esc).join(" / ")}</p>` : ""}<details><summary>Model answer & explanation</summary><p>${esc(typeof q.answerKey === "object" ? Object.entries(q.answerKey).map(([k,v]) => k + ": " + v).join("; ") : q.answerKey)}</p><p class="muted">${esc(q.markingGuide)}</p></details></section>`,
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
  document.querySelector("#start-practice").onclick = () => {
    const all = data.questions.filter(q => q.sourceType === "original" && q.topicIds.includes(id));
    const selected = all.filter(q => workbook ? q.resourceKind === "workbook" : q.resourceKind !== "workbook");
    startExam(selected.length ? selected : all, `Chapter revision: ${l.title}`);
  };
}
function sourcePaperReader(id, pageNumber=1, section='paper') {
  const doc = (data.sourceDocuments || []).find(d => d.id === id);
  if (!doc) throw Error('Source paper not found.');
  const showingAnswers = section === 'answers' && !!doc.answerGuide;
  const resource = showingAnswers ? doc.answerGuide : doc;
  const n = Math.min(Math.max(1, Number.isFinite(pageNumber) ? Math.floor(pageNumber) : 1),resource.pageCount);
  const path = k => 'paper-pages/'+id+'/'+k+(showingAnswers?'/answers':'');
  frame(`${dashboardButton()}<article class="reader"><h1>${esc(doc.title)}</h1><p class="muted">${showingAnswers?'Source answer guide':'Original paper'} · page ${n} of ${resource.pageCount}</p><p>${esc(showingAnswers ? resource.provenance : doc.note)}</p><div class="book-tabs">${link('paper-pages/'+id+'/1','Question paper',showingAnswers?'button secondary':'button')}${doc.answerGuide?link('paper-pages/'+id+'/1/answers','Source answer guide',showingAnswers?'button':'button secondary'):''}</div><div class="row">${n > 1 ? link(path(n-1),'← Previous page','button secondary') : '<span></span>'}${n < resource.pageCount ? link(path(n+1),'Next page →') : '<span>Last page</span>'}</div><figure><img src="${esc(resource.pageImages[n-1])}" alt="${showingAnswers?'Answer guide':'Original paper'} ${esc(doc.title)}, page ${n}." style="width:100%;height:auto"></figure><details><summary>My answers and working · saved on this device</summary><label for="paper-working">Use the original question numbers and subpart labels.</label><textarea id="paper-working" rows="12" placeholder="1(a)… 1(b)…">${esc(sourceAnswers[id]||'')}</textarea><p id="paper-save-status" class="save-status" role="status">Your paper notebook stays local. Source documents are not automatically graded.</p></details>${doc.practiceIndex && !showingAnswers ? `<p>${link("paper-practice/"+id,"Choose practice questions →")}</p>` : ""}${doc.interactivePaperId ? `<p><button data-source-exam="${esc(doc.interactivePaperId)}">Practise scored questions from this paper</button></p>` : ''}</article>`,'exams');
  document.querySelector('[data-source-exam]')?.addEventListener('click', event => openScoredPaper(event.currentTarget.dataset.sourceExam));
  document.querySelector('#paper-working').oninput = async event => {
    sourceAnswers[id] = event.target.value;
    try { await set('sourceAnswers', sourceAnswers); document.querySelector('#paper-save-status').textContent='Saved on this device'; }
    catch(error) { document.querySelector('#paper-save-status').textContent='Not saved: '+error.message; }
  };
}
function showSourcePractice(id, label) {
  const doc = data.sourceDocuments.find(p => p.id === id && p.practiceIndex);
  if (!doc) throw Error('Interactive source practice is unavailable for this paper.');
  const index = doc.practiceIndex;
  const saved = sourcePractice[id] ??= { selected: [], answers: {}, checked: {} };
  saved.marks ??= {};
  const route = 'paper-practice/' + id;
  const back = dashboardButton();
  const original = link('paper-pages/' + id + '/1', 'Full original paper', 'button secondary');
  const guide = doc.answerGuide ? link('paper-pages/' + id + '/1/answers', 'Source answer guide', 'button secondary') : '';
  const persistPractice = async () => {
    try {
      await set('sourcePractice', sourcePractice);
      const status = document.querySelector('#source-practice-status');
      if (status) status.textContent = 'Saved on this device.';
    } catch (error) {
      const status = document.querySelector('#source-practice-status');
      if (status) status.textContent = 'Could not save. ' + error.message;
      throw error;
    }
  };

  const selected = selectSourceGroups(index, saved.selected);
  const position = selected.findIndex(group => group.label === label);
  const graded = selected.filter(group => Number.isFinite(saved.marks[group.label]) &&
    doc.independentPracticeGuide?.groups[group.label]);
  const earned = graded.reduce((sum, group) => sum + saved.marks[group.label], 0);
  const available = graded.reduce((sum, group) => sum + doc.independentPracticeGuide.groups[group.label].maximumMarks, 0);
  const progressNote = graded.length ? `<p>Self-marked ${earned}/${available} across ${graded.length} of ${selected.length} selected questions.</p>` : '';
  if (position === -1) {
    frame(`${back}<h1>${esc(doc.title)}</h1>
      <p>Choose the original question groups you want to answer. Each group keeps its subparts together. ${doc.independentPracticeGuide ? 'Use the SomaSmart guide to record your own marks.' : 'This activity records your work for self-check without assigning marks.'}</p>
      <p>${original} ${guide}</p>
      ${progressNote}
      <form id="source-practice-picker" class="card">
        <label>When would you like to review your work?<select name="timing"><option value="immediate">Review each answer</option><option value="end" ${saved.timing === "end" ? "selected" : ""}>Review at the end</option></select></label><fieldset><legend>Questions to practise</legend>
          ${index.groups.map(group => `<label><input type="checkbox" name="source-group" value="${esc(group.label)}" ${saved.selected.length === 0 || saved.selected.includes(group.label) ? 'checked' : ''}> Question ${esc(group.label)} · page ${group.firstPage}${saved.checked[group.label] ? ' · reviewed' : ''}</label>`).join('')}
        </fieldset>
        <p id="source-practice-status" role="status"></p>
        <button>Start or resume selection →</button>
      </form>`, 'exams');
    document.querySelector('#source-practice-picker').onsubmit = async event => {
      event.preventDefault();
      const values = new FormData(event.currentTarget).getAll('source-group');
      if (!values.length) {
        document.querySelector('#source-practice-status').textContent = 'Select at least one question.';
        return;
      }
      saved.selected = values;
      saved.timing = event.currentTarget.elements?.timing?.value || "immediate";
      saved.finished = false;
      try {
        await persistPractice();
        location.hash = '#/' + route + '/' + encodeURIComponent(values[0]);
      } catch { /* The status message explains the failed save. */ }
    };
    return;
  }

  const group = selected[position];
  const model = doc.independentPracticeGuide?.groups[group.label];
  const review = saved.timing !== "end" || saved.finished;
  const groupLink = (item, title) => link(route + '/' + encodeURIComponent(item.label), title, 'button secondary');
  frame(`${back} ${link(route, '← Change selection', '')}<article class="reader">
    <h1>${esc(doc.title)}</h1>
    <h2>Question ${esc(group.label)}</h2>
    <p>${position + 1} of ${selected.length} selected · ${selected.filter(q => saved.checked[q.label]).length} reviewed</p>
    ${progressNote}
    <p>Answer the numbered question and its subparts on these original pages. The pages may also show nearby questions.</p>
    <p>${original}</p>
    ${group.firstPage > 1 ? `<details><summary>Original cover and instructions</summary><img src="${esc(doc.pageImages[0])}" alt="Original cover and instructions" loading="lazy" style="width:100%;height:auto"></details>` : ''}
    ${sourceGroupPages(doc, group).map((page, i) => `<figure><img src="${esc(page)}" alt="Original source page ${group.firstPage + i}" style="width:100%;height:auto"></figure>`).join('')}
    <label for="source-practice-answer">My answer and working</label>
    <textarea id="source-practice-answer" rows="8">${esc(saved.answers[group.label] || '')}</textarea>
    <p id="source-practice-status" role="status"></p>
    ${review ? `<details class="card" ${saved.marks[group.label] !== undefined ? 'open' : ''}><summary>Self-check this response</summary>
      <p>${model ? 'Compare your answer with the independent marking guide below.' : doc.answerGuide ? 'Compare your answer with the source guide using the printed question number.' : 'Re-read the original instructions and check that your answer covers every requested part. A source answer guide is unavailable.'}</p>
      ${model ? `<h3>${esc(doc.independentPracticeGuide.title)}</h3>

        ${model.parts.map(part => `<p><strong>${esc(part.label)} · ${part.marks} marks</strong><br>${esc(part.answer)}<br>${esc(part.rubric)}</p>`).join('')}` : ''}
      ${doc.answerGuide && !model ? `<details><summary>Compare with the source answers</summary>${doc.answerGuide.pageImages.map((url, i) => `<img loading="lazy" src="${esc(url)}" alt="Source answers, page ${i+1}" style="width:100%">`).join('')}</details>` : ''}
      ${model ? `<form id="source-practice-mark">
        <label>My mark out of ${model.maximumMarks}<input name="mark" type="number" min="0" max="${model.maximumMarks}" step="0.5" value="${saved.marks[group.label] ?? ''}" required></label>
        <button type="submit" class="secondary">Save my mark</button>
      </form>` : ''}
      <button type="button" class="secondary" id="source-practice-check">${saved.checked[group.label] ? 'Undo reviewed status' : 'Mark reviewed'}</button>
    </details>` : '<button id="finish-selection">Finish and review answers</button>'}
    <div class="row">
      ${position > 0 ? groupLink(selected[position - 1], '← Previous question') : ''}
      ${position + 1 < selected.length ? groupLink(selected[position + 1], 'Next question →') : link(route, 'Return to selection →')}
    </div>
  </article>`, 'exams');
  document.querySelector('#source-practice-answer').oninput = async event => {
    saved.answers[group.label] = event.target.value;
    try { await persistPractice(); } catch { /* Keep the draft in memory. */ }
  };
  const markForm = document.querySelector('#source-practice-mark');
  if (markForm && model) markForm.onsubmit = async event => {
    event.preventDefault();
    const mark = markForm.elements.mark.valueAsNumber;
    if (!Number.isFinite(mark) || mark < 0 || mark > model.maximumMarks || !Number.isInteger(mark * 2)) return;
    const previousMark = saved.marks[group.label];
    const previousChecked = saved.checked[group.label];
    saved.marks[group.label] = mark;
    saved.checked[group.label] = true;
    try {
      await persistPractice();
      render();
    } catch {
      if (previousMark === undefined) delete saved.marks[group.label];
      else saved.marks[group.label] = previousMark;
      saved.checked[group.label] = previousChecked;
    }
  };
  if (!review) {
    document.querySelector('#finish-selection').onclick = async () => { saved.finished = true; await persistPractice(); render(); };
    return;
  }
  document.querySelector('#source-practice-check').onclick = async () => {
    saved.checked[group.label] = !saved.checked[group.label];
    try {
      await persistPractice();
      render();
    } catch {
      saved.checked[group.label] = !saved.checked[group.label];
    }
  };
}

function exams() {
  examFilter ??= {
    form: profile.form,
    subjectId: "chemistry",
    topics: [],
    source: "original",
  };
  const list = eligible(data, examFilter);
  const subjectPapers = data.sourceDocuments.filter(doc =>
    doc.form === profile.form && doc.subjectId === examFilter.subjectId && doc.publicationStatus === 'published');
  const scoredCount = subjectPapers.filter(doc => doc.interactivePaperId).length;
  frame(
    `<span class="eyebrow">Examination centre</span><h1>Exam dashboard</h1>${draft ? `<section class="card"><h2>${esc(draft.title)}</h2>${link("exams/attempt", draft.submitted ? "Resume marking and review" : "Resume saved exam")}</section>` : ""}<p class="muted">Build a test from the actual embedded question bank.</p><section class="card"><div class="formgrid"><label>Subject<select id="exam-subject">${data.subjects.map((s) => `<option value="${s.id}" ${s.id === examFilter.subjectId ? "selected" : ""}>${esc(s.name)}</option>`).join("")}</select></label><label>Source<select id="exam-source">${[
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
      )}</fieldset><div class="formgrid"><label>Number of questions (linked parts stay together)<input id="count" type="number" min="1" max="${Math.max(1, list.length)}" value="${Math.min(5, list.length) || 1}"></label><label>Selection seed<input id="seed" type="number" value="2027"></label></div><p><strong>${list.length}</strong> eligible questions</p>${list.length ? '<button id="generate">Create examination →</button>' : `<div class="empty">No eligible embedded questions match this source. More papers are being checked against their originals. ${link("exams", "Choose original practice", "")}</div>`}<div id="exam-message" role="alert"></div></section><h2>Past-paper library</h2><p><strong>${subjectPapers.length} papers</strong> for Form ${profile.form === 1 ? "One" : "Two"} ${esc(subject(examFilter.subjectId).name)} · ${scoredCount} with scored questions · ${subjectPapers.length - scoredCount} for self-check only.</p><div class="grid">${subjectPapers.map(d => `<section class="card"><h3>${esc(d.title)}</h3><p>${d.pageCount} pages${d.answerGuide?" · source guide included":d.independentPracticeGuide?" · SomaSmart guide included":""}${d.curriculumStream==='vocational'?' · Vocational source':''}</p>${link('paper/'+d.id, d.interactivePaperId ? 'Practise scored questions' : 'Practise questions · self-check')}</section>`).join('') || '<p>No complete source documents match this subject and form yet.</p>'}</div><h2>Past-paper practice</h2><div class="grid">${data.papers.filter(p => p.sourceType !== "original" && p.form === profile.form && p.subjectId === examFilter.subjectId && p.publicationStatus === "published").map(p => `<section class="card"><span class="pill">Genuine past-paper questions</span><h3>${esc(p.title)}</h3><p>${p.questionIds.length} scored items • ${p.maximumMarks} available marks</p><p class="muted">${p.completeScoredPaper ? "Complete scored paper." : "Scored selection; source issues are excluded."} Original wording and linked materials are preserved. Written responses require self-marking.</p><button data-genuine-paper="${p.id}">Practise reviewed questions</button></section>`).join("") || '<p class="muted">No scored past-paper selection is available for this subject and form yet.</p>'}</div><h2>Prepared revision papers</h2><p class="muted">Original SomaSmart tests covering the published chapters; these are not past school or NECTA papers.</p><div class="grid">${data.papers.filter(p => p.sourceType === "original" && p.form === profile.form && p.publicationStatus === "published").map(p => `<section class="card"><h3>${esc(p.title)}</h3><p>${p.questionIds.length} items · ${p.maximumMarks} marks</p><button data-paper="${p.id}">Start revision paper</button></section>`).join("")}</div><h2>Private source documents</h2><section class="card"><p>Import a PDF you may lawfully use. Files stay on this device and are never published. These reference documents are not automatically transcribed or eligible for scored exams.</p><label>Choose a private PDF<input id="private-file" type="file" accept="application/pdf"></label><div id="private-status" role="status"></div>${privateDocs.map((p, i) => `<p><button class="secondary" data-private="${i}">${esc(p.name)}</button></p>`).join("")}</section><h2>Previous attempts</h2>${
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
  document.querySelectorAll('[data-genuine-paper]').forEach(button => button.onclick = () => {
    const paper = data.papers.find(p => p.id === button.dataset.genuinePaper);
    openScoredPaper(paper.id);
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
        if (draft && !draft.submitted) {
          document.querySelector("#exam-message").textContent = "Resume or discard your saved exam before opening a previous attempt.";
          window.scrollTo(0, 0);
          return;
        }
        draft = structuredClone(
          attempts.find((a) => a.id === b.dataset.review),
        );
        await set("draft", draft);
        location.hash = "#/exams/attempt";
      }),
  );
}
function openScoredPaper(id) {
  const paper = data.papers.find(p => p.id===id && p.publicationStatus==='published');
  if (!paper) throw Error('Scored paper not available.');
  const eligibleIds = new Set(eligible(data,{form:paper.form,subjectId:paper.subjectId,source:'authentic'}).map(q=>q.id));
  const questions = paper.questionIds.map(id=>data.questions.find(q=>q.id===id));
  if (!questions.length || questions.some(q=>!q || !eligibleIds.has(q.id))) throw Error('This source selection contains unresolved items.');
  if (draft?.questions?.[0]?.paperId === id && draft.title === paper.title) {
    location.hash = '#/exams/attempt';
    return;
  }
  const byId = new Map([...questions, ...(paper.reviewOnlyItems || [])].map(q => [q.id, q]));
  const practice = paper.practiceOrder ? paper.practiceOrder.map(id => byId.get(id)) : questions;
  return startExam(practice,paper.title);
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
    sourceInstructions: [...new Set(questions.flatMap(q => data.papers.find(p => p.id === q.paperId)?.sourceInstructions || []))],
    answers: {},
    marks: {},
    drawings: {},
    feedbackMode: null,
    checkedAnswers: {},
    submitted: false,
    final: false,
  };
  await set("draft", draft);
  location.hash = "#/exams/attempt";
}
function answerInput(q) {
  const answer = draft.answers[q.id];
  if (q.type === "mcq")
    return `<div class="options">${q.options.map((o, index) => `<label><input type="radio" name="${q.id}" data-answer="${q.id}" value="${esc(o)}" ${o === answer ? "checked" : ""} ${(draft.submitted || draft.checkedAnswers?.[q.id]) ? "disabled" : ""}>${originalOptionLabel(q,index)}${esc(o)}</label>`).join("")}</div>`;
  if (q.type === "matching")
    return (q.pairs || [])
      .map(
        (p) =>
          `<label>${esc(p.left)}<select data-match="${q.id}" data-key="${esc(p.id)}" ${(draft.submitted || draft.checkedAnswers?.[q.id]) ? "disabled" : ""}><option value="">Choose</option>${q.options.map((o) => `<option ${answer?.[p.id] === o ? "selected" : ""}>${esc(o)}</option>`).join("")}</select></label>`,
      )
      .join("");
  return `<textarea data-answer="${q.id}" aria-label="Answer to question ${q.questionNumber}" ${draft.submitted ? "readonly" : ""} placeholder="Write your answer or working here…">${esc(answer || "")}</textarea>${q.requiresDrawing ? '<p>Include the required drawing below or on paper before self-assessing drawing marks.</p>' : ''}<details ${draft.drawings?.[q.id] ? 'open' : ''}><summary>Drawing or diagram</summary><canvas data-drawing="${q.id}" width="640" height="360" aria-label="Drawing for question ${esc(q.questionNumber)}" style="width:100%;height:auto;background:white;border:1px solid #aabdb5;touch-action:none"></canvas>${draft.submitted ? '' : `<p>Draw with your finger or pointer. Your diagram is saved with this attempt.</p><button class="secondary" data-clear-drawing="${q.id}">Clear drawing</button>`}</details>`;
}
function sourceParts(q) {
  const seen = new Set();
  const context = text => {
    if (!text || seen.has(text)) return '';
    seen.add(text);
    return `<p class="source-stem">${esc(text)}</p>`;
  };
  return (q.sourceParts || []).map(part => `<div class="source-part">
    ${context(part.instructions)}${context(part.sharedContent)}${context(part.passage)}
    <p><strong>${esc(part.questionNumber)}.</strong> ${verbatimContent(part)}</p>
    ${questionContext({table:part.table})}
    ${(part.options || []).map((text, index) => `<p>${originalOptionLabel(part,index)}${esc(text)}</p>`).join('')}
  </div>`).join('');
}

function guidedReview(q) {
  const sw = q.subjectId === 'kiswahili' || q.subjectId === 'historia';
  return `<details class="guided-review" data-guided-review="${esc(q.id)}">
    <summary>${sw ? 'Mazungumzo ya marudio' : 'Guided review conversation'}</summary>
    <p>${sw ? 'Chagua swali la kuuliza kuhusu jibu lako.' : 'Choose a follow-up about your answer.'}</p>
    <div class="review-messages" role="log" aria-live="polite"></div>
    <div class="row">
      <button type="button" class="secondary" data-review-topic="answer">${sw ? 'Jibu ni lipi?' : 'What answers are accepted?'}</button>
      <button type="button" class="secondary" data-review-topic="marking">${sw ? 'Alama zinatolewaje?' : 'How is this marked?'}</button>
      <button type="button" class="secondary" data-review-topic="revise">${sw ? 'Nisome nini tena?' : 'What should I revise?'}</button>
    </div>
  </details>`;
}
function displayAnswer(q) {
  if (q.acceptedAnswerKeys) return q.acceptedAnswerKeys.join(' / ');
  if (q.answerKey && typeof q.answerKey === 'object') {
    return Object.entries(q.answerKey).map(([key, value]) =>
      `${key}. ${(q.acceptedMatchingAnswers?.[key] ?? [value]).join(' / ')}`).join('\n');
  }
  return q.answerKey || '';
}
function exam() {
  if (draft.feedbackMode === null && !draft.submitted) {
    frame(`${dashboardButton()}<article class="card"><h1>${esc(draft.title)}</h1>
      <h2>When would you like feedback?</h2>
      <p><button data-mode="immediate">Check each answer</button> See feedback as you practise.</p>
      <p><button data-mode="end">Mark at the end</button> See your answers after you submit.</p></article>`, 'exams');
    document.querySelectorAll('[data-mode]').forEach(button => button.onclick = async () => {
      draft.feedbackMode = button.dataset.mode;
      await set('draft', draft);
      exam();
    });
    return;
  }
  const instant = draft.feedbackMode === 'immediate' && !draft.submitted;
  const r = result(draft.questions, draft.answers, draft.marks);
  frame(
    `${dashboardButton()}<p class="eyebrow">${draft.submitted ? "Review & marking" : "Saved examination draft"} / Form ${draft.form}</p><h1>${esc(draft.title)}</h1><p class="muted">${draft.questions.length} questions • ${r.maximum} available marks • Written answers require your self-assessment.</p>${draft.sourceInstructions?.length ? `<details class="card"><summary>Original source instructions</summary>${draft.sourceInstructions.map(text => `<p>${esc(text)}</p>`).join("")}<p class="muted">A custom selection may contain fewer items than the original source paper.</p></details>` : ""}<div class="save-status" id="saved" role="status">Saved on this device</div>${draft.submitted ? `<section class="card"><span class="score">${r.earned}/${r.maximum}</span><p>${r.pending ? `${r.pending} written answers await self-marking. Score is provisional.` : "Marking complete."}</p></section>` : ""}${draft.questions
      .map((q, i) => {
        const row = r.rows[i];
        const showPrintedPages = !q.sourcePagePrompt || draft.questions[i-1]?.groupId !== q.groupId;
        const objective = ['mcq', 'matching'].includes(q.type);
        const reveal = draft.submitted || (instant && draft.checkedAnswers?.[q.id]);
        const status = {review:'Source question · unscored', correct:'Correct', incorrect:'Incorrect', partial:'Partly correct', unanswered:'Unanswered', pending:'Self-mark your answer'}[row.status] || 'Review your answer';
        const explanation = q.feedbackExplanation || data.questions.find(item => item.id === q.id)?.feedbackExplanation || q.workedSolution || q.markingGuide;
        return `<section class="card question"><div class="row"><span class="pill">${esc(q.sourceTitle)}</span><span class="muted">${q.reviewOnly ? "Unscored" : q.maximumMarks + " marks"} · ${esc(q.type)}</span></div><h3>${q.sourceType === "original" ? i + 1 : esc(q.questionNumber)}. ${verbatimContent(q)}</h3>${q.sharedContent ? `<p class="source-stem">${esc(q.sharedContent).replaceAll("\n", "<br>")}</p>` : ""}${q.instructions ? `<p>${esc(q.instructions)}</p>` : ""}${(showPrintedPages ? q.media || [] : []).map((m) => m.role === "source-page" ? `<details><summary>View original source page</summary><img src="${esc(m.path)}" alt="${esc(m.alt)}" loading="lazy" style="max-width:100%"></details>` : `<img src="${esc(m.path)}" alt="${esc(m.alt)}" loading="lazy" style="max-width:100%">`).join("")}${q.passage ? `<blockquote>${esc(q.passage)}</blockquote>` : ""}${q.table ? `<table>${q.table.map((row) => `<tr>${row.map((c) => `<td>${esc(c)}</td>`).join("")}</tr>`).join("")}</table>` : ""}${sourceParts(q)}${answerInput(q)}${instant && !objective && !reveal ? `<button class="secondary" data-compare="${esc(q.id)}">Compare with model answer</button>` : ''}${reveal ? `<div class="feedback" role="status"><strong>${esc(status)}</strong><p><b>Model answer</b><br>${esc(displayAnswer(q))}</p><p>${esc(explanation)}</p>${guidedReview(q)}${draft.submitted && !q.reviewOnly && !objective && draft.answers[q.id]?.trim() ? `<label>Your earned marks (0–${q.maximumMarks}, steps of ${q.markIncrement})<input data-marks="${q.id}" type="number" min="0" max="${q.maximumMarks}" step="${q.markIncrement}" value="${draft.marks[q.id] ?? ""}"></label>` : ""}</div>` : ""}</section>`;
      })
      .join(
        "",
      )}<div class="row">${dashboardButton()}${!draft.submitted ? '<button id="submit">Submit for marking</button>' : '<button id="finish">Save review & return</button>'}<button id="discard" class="secondary">${draft.submitted ? "Close review" : "Discard draft"}</button></div><p id="mark-error" role="alert"></p>`,
    "exams",
  );
  async function persist() {
    await set("draft", draft);
    const saved = document.querySelector("#saved");
    if (saved) saved.textContent = "Saved on this device";
  }
  document.querySelectorAll('[data-guided-review]').forEach(panel => {
    const question = draft.questions.find(q => q.id === panel.dataset.guidedReview);
    const log = panel.querySelector('.review-messages');
    panel.addEventListener('click', event => {
      const button = event.target.closest('[data-review-topic]');
      if (!button) return;
      const prompt = document.createElement('p');
      prompt.textContent = button.textContent;
      const reply = document.createElement('p');
      const topic = button.dataset.reviewTopic;
      const chapters = question.topicIds.map(lesson).filter(Boolean);
      if (topic === 'revise' && chapters.length) {
        for (const chapter of chapters) {
          const anchor = document.createElement('a');
          anchor.href = '#/lesson/' + chapter.id;
          anchor.textContent = chapter.title;
          reply.append(anchor, document.createElement('br'));
        }
      } else {
        reply.textContent = topic === 'marking' ? question.markingGuide :
          topic === 'revise' ? 'Review this question and compare your working with the model answer.' :
          [displayAnswer(question), question.workedSolution, question.guideDiscrepancy].filter(Boolean).join('\n\n');
      }
      const turn = document.createElement('div');
      turn.append(prompt, reply);
      log.append(turn);
    });
  });
  document.querySelectorAll('[data-drawing]').forEach(canvas => {
    const id = canvas.dataset.drawing, context = canvas.getContext('2d');
    context.lineWidth = 2.5; context.lineCap = 'round'; context.strokeStyle = '#142f28';
    if (draft.drawings?.[id]) { const saved = new Image(); saved.onload = () => context.drawImage(saved,0,0); saved.src = draft.drawings[id]; }
    if (draft.submitted) return;
    let drawing = false;
    const point = event => { const rect = canvas.getBoundingClientRect(); return [(event.clientX-rect.left)*canvas.width/rect.width,(event.clientY-rect.top)*canvas.height/rect.height]; };
    canvas.onpointerdown = event => { event.preventDefault(); canvas.setPointerCapture(event.pointerId); drawing = true; context.beginPath(); const [x,y]=point(event); context.moveTo(x,y); context.lineTo(x+.1,y+.1); context.stroke(); };
    canvas.onpointermove = event => { if (!drawing) return; event.preventDefault(); context.lineTo(...point(event)); context.stroke(); };
    const saveDrawing = async () => {
      if (!drawing) return; drawing=false; draft.drawings ??={}; draft.drawings[id]=canvas.toDataURL('image/png');
      if (!draft.answers[id]?.trim()) { draft.answers[id]='[Drawing supplied; review the diagram below.]'; document.querySelector(`[data-answer="${id}"]`).value=draft.answers[id]; }
      try { await persist(); } catch(error) { document.querySelector('#saved').textContent='Drawing not saved: '+error.message; }
    };
    canvas.onpointerup=saveDrawing; canvas.onpointercancel=saveDrawing;
    document.querySelector(`[data-clear-drawing="${id}"]`).onclick=async () => {
      context.clearRect(0,0,canvas.width,canvas.height); delete (draft.drawings||{})[id];
      if (draft.answers[id]==='[Drawing supplied; review the diagram below.]') { draft.answers[id]=''; document.querySelector(`[data-answer="${id}"]`).value=''; }
      try { await persist(); } catch(error) { document.querySelector('#saved').textContent='Not saved: '+error.message; }
    };
  });
  document.querySelectorAll("[data-answer]").forEach(
    (el) =>
      (el.oninput = async () => {
        const id = el.dataset.answer;
        draft.answers[id] = el.value;
        const check = instant && el.type === 'radio';
        if (check) (draft.checkedAnswers ??= {})[id] = true;
        try {
          await persist();
          if (check && location.hash === "#/exams/attempt") exam();
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
        const q = draft.questions.find(item => item.id === el.dataset.match);
        const check = instant && q.pairs.every(pair => draft.answers[q.id][pair.id]);
        if (check) (draft.checkedAnswers ??= {})[q.id] = true;
        await persist();
        if (check && location.hash === "#/exams/attempt") exam();
      }),
  );
  document.querySelectorAll('[data-compare]').forEach(button => button.onclick = async () => {
    (draft.checkedAnswers ??= {})[button.dataset.compare] = true;
    await persist();
    exam();
  });
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
      location.hash = "#/exams";
    };
  document.querySelector("#discard").onclick = async () => {
    if (!draft.submitted && !confirm("Discard this unfinished test?")) return;
    draft = null;
    await set("draft", null);
    location.hash = "#/exams";
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
    `<span class="eyebrow">Your progress</span><h1>See how far you’ve come.</h1><div class="stats"><div class="stat"><strong>${profile.completed.length}/${data.lessons.length}</strong>Available chapters completed</div><div class="stat"><strong>${attempts.filter((a) => a.final).length}</strong>Marked tests</div><div class="stat"><strong>${attempts.filter((a) => !a.final).length}</strong>Awaiting self-marking</div></div><h2>Topics to revisit</h2>${weak.length ? weak.map((t) => `<div class="card row"><div>${link("lesson/" + t.id, lesson(t.id)?.title || t.id, "")}<p class="muted">${t.items} assessed items · ${Math.round(t.ratio * 100)}% of available marks</p></div>${link("workbook/" + t.id, "Revise", "button secondary")}</div>`).join("") : '<div class="empty">Complete and mark an examination to see evidence-based recommendations.</div>'}<h2>Mistake notebook</h2>${mistakes.length ? mistakes.map(({ q, r }) => `<details class="card"><summary>${esc(q.content)} <span class="pill">${esc(r.status)}</span></summary><p>${esc(q.answerKey)}</p><p>${esc(q.markingGuide)}</p>${q.topicIds.length ? link("lesson/" + q.topicIds[0], "Revisit chapter", "") : ""}</details>`).join("") : '<p class="muted">Questions to revisit will be saved here after an exam.</p>'}<h2>Completed reading</h2>${profile.completed.map((id) => `<p>${link("lesson/" + id, lesson(id)?.title || id, "")}</p>`).join("") || '<p class="muted">Mark chapters complete as you finish reading.</p>'}`,
    "progress",
  );
}
async function render() {
  try {
    const [page, id, subpage, section] = location.hash.replace(/^#\/?/, "").split("/");
    if (page === "paper-practice") showSourcePractice(id, subpage ? decodeURIComponent(subpage) : undefined);
    else if (page === "paper-pages" || (page === "paper" && (section || Number(subpage) > 1))) sourcePaperReader(id, Number(subpage || 1), section);
    else if (page === "paper") {
      const doc = data.sourceDocuments.find(item => item.id === id);
      if (!doc) throw Error('Paper unavailable.');
      if (doc.interactivePaperId) await openScoredPaper(doc.interactivePaperId);
      else {
        location.replace('#/paper-practice/' + id);
      }
    }
    else if (page === "study") study(id);
    else if (page === "lesson" || page === "workbook")
      await reader(id, page === "workbook");
    else if (page === "exams" && id === "attempt" && draft) exam();
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
function updateOfflineButton() {
  const button = document.querySelector('#offline-action');
  if (!button) return;
  button.hidden = !['paused', 'running'].includes(offlineMode);
  button.textContent = offlineMode === 'running' ? 'Pause download' : 'Download for offline use';
  button.onclick = () => {
    const worker = navigator.serviceWorker?.controller;
    if (!worker) return;
    const pause = offlineMode === 'running';
    offlineMode = pause ? 'pausing' : 'running';
    setOffline(pause ? 'Pausing download…' : 'Starting offline download…');
    updateOfflineButton();
    worker.postMessage({type: pause ? 'PAUSE' : 'START'});
  };
}
function offlineState(mode, text) {
  offlineMode = mode;
  setOffline(text);
  updateOfflineButton();
}
async function provision() {
  const service = navigator.serviceWorker;
  if (!service) {
    offlineState('unsupported', 'Online use');
    return;
  }
  function status() {
    const worker = service.controller;
    if (!worker) return;
    const channel = new MessageChannel();
    channel.port1.onmessage = ({data}) => {
      channel.port1.close();
      if (worker !== service.controller || typeof data.running !== 'boolean') return;
      if (data.ready) offlineState('ready', 'Library ready offline');
      else if (data.running) offlineState('running', 'Downloading offline library…');
      else offlineState('paused', 'Offline download paused');
    };
    worker.postMessage({type: 'STATUS'}, [channel.port2]);
  }
  service.addEventListener('controllerchange', status);
  service.addEventListener('message', event => {
    if (event.source !== service.controller) return;
    const m = event.data;
    if (m.type === 'PROGRESS' && offlineMode !== 'pausing')
      offlineState('running', `Downloading offline: ${m.done}/${m.total}`);
    if (m.type === 'READY') offlineState('ready', 'Library ready offline');
    if (m.type === 'PAUSED') offlineState('paused', 'Offline download paused');
    if (m.type === 'ERROR') offlineState('paused', 'Download stopped: ' + m.message);
  });
  try {
    await service.register('/sw.js', {updateViaCache: 'none'});
    await service.ready;
    status();
  } catch {
    offlineState('unsupported', 'Online use · offline setup unavailable');
  }
}
async function boot() {
  try {
    data = await loadLibrary({onProgress(bytes) {
      const status=document.querySelector('#startup-status');
      if(status)status.textContent=`Loading learning library… ${(bytes/1048576).toFixed(1)} MB received`;
    }});
    const status=document.querySelector('#startup-status');
    if(status)status.textContent='Opening your saved progress…';
    profile = await withStorageTimeout(get("profile", {
      form: 1,
      completed: [],
      recent: [],
      lastLesson: null,
    }));
    [attempts,draft,privateDocs,sourceAnswers,sourcePractice] = await withStorageTimeout(Promise.all([
      get('attempts',[]),get('draft',null),get('privateDocuments',[]),get('sourceAnswers',{}),get('sourcePractice',{})
    ]));
    await render();
    await provision();
  } catch (e) {
    app.innerHTML = `<main class="shell"><h1>SomaSmart could not open</h1><p role="alert">${esc(e.message)}</p><p>Retrying does not delete your saved work.</p><button onclick="location.reload()">Retry opening SomaSmart</button></main>`;
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
