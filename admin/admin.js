let data, csrf;
const $ = (s) => document.querySelector(s);
async function api(url, body) {
  const r = await fetch(
    url,
    body
      ? {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRF-Token": csrf || "",
          },
          body: JSON.stringify(body),
        }
      : {},
  );
  const d = await r.json();
  if (!r.ok) throw Error(d.error);
  return d;
}
function status(s) {
  $("#status").textContent = s;
}
function records() {
  const list = data[$("#collection").value];
  $("#record").replaceChildren(
    ...list.map((x) => {
      const o = document.createElement("option");
      o.value = x.id;
      o.textContent = x.title || x.content || x.term || x.id;
      return o;
    }),
  );
  edit();
  $("#counts").textContent =
    `${data.lessons.length} lessons · ${data.questions.length} questions · ${data.papers.length} paper records. Complete curriculum verification is still required.`;
}
function edit() {
  const r = data[$("#collection").value].find(
    (x) => x.id === $("#record").value,
  );
  $("#editor").value = JSON.stringify(r || {}, null, 2);
  $("#preview").textContent =
    r?.content || r?.paragraphs?.join("\n\n") || r?.definition || "";
}
$("#login").onsubmit = async (e) => {
  e.preventDefault();
  try {
    await api("/api/login", { password: $("#password").value });
    $("#password").value = "";
    const d = await api("/api/content");
    csrf = d.csrf;
    data = d.content;
    $("#studio").hidden = false;
    $("#login").hidden = true;
    records();
    $("#sources").textContent = JSON.stringify(
      await api("/api/sources"),
      null,
      2,
    );
    status("Authenticated. Session expires in one hour.");
  } catch (e) {
    status(e.message);
  }
};
$("#collection").onchange = records;
$("#record").onchange = edit;
$("#apply").onclick = () => {
  try {
    const item = JSON.parse($("#editor").value);
    const list = data[$("#collection").value];
    const i = list.findIndex((x) => x.id === $("#record").value);
    if (i < 0) throw Error("Select a record first.");
    list[i] = item;
    records();
    status("Edit applied locally; save draft to persist.");
  } catch (e) {
    status(e.message);
  }
};
$("#add").onclick = () => {
  data[$("#collection").value].push({
    id: crypto.randomUUID(),
    publicationStatus: "draft",
  });
  records();
  $("#record").selectedIndex = $("#record").options.length - 1;
  edit();
};
for (const [id, path] of [
  ["save", "draft"],
  ["publish", "publish"],
])
  $("#" + id).onclick = async () => {
    try {
      const r = await api("/api/" + path, data);
      status(r.message || "Draft saved.");
    } catch (e) {
      status(e.message);
    }
  };
$("#import").onchange = async (e) => {
  try {
    const d = JSON.parse(await e.target.files[0].text());
    for (const key of [
      "lessons",
      "questions",
      "glossary",
      "papers",
      "books",
      "subjects",
    ])
      if (!Array.isArray(d[key]))
        throw Error("Expected a complete structured release.");
    data = d;
    records();
    status("Imported into local draft; review before publishing.");
  } catch (e) {
    status(e.message);
  }
};
