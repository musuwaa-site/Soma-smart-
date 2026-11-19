import test from "node:test";
import assert from "node:assert/strict";
import vm from "node:vm";
import { webcrypto, createHash } from "node:crypto";
import { readFileSync } from "node:fs";
const content = new TextEncoder().encode("complete lesson library");
const sha = createHash("sha256").update(content).digest("hex");
function harness({ fail = false, quota = false, corrupt = false, stall = false } = {}) {
  const handlers = {},
    buckets = new Map([
      [
        "somasmart-previous",
        new Map([["/index.html", new Response("old working release")]]),
      ],
    ]);
  let ready = false,
    claimed = false;
  let calls = 0, aborted = false;
  const messages = [];
  const context = {
    AbortController,
    Response,
    URL,
    Uint8Array,
    Error,
    crypto: webcrypto,
    fetch: async (url, options) => {
      calls++;
      if (stall) await new Promise((resolve, reject) => options.signal.addEventListener("abort", () => {
        aborted = true; stall = false; reject(Error("Aborted"));
      }));
      if (fail) throw Error("Interrupted network");
      return new Response(corrupt ? "broken content" : content);
    },
    caches: {
      keys: async () => [...buckets.keys()],
      async open(key) {
        if (!buckets.has(key)) buckets.set(key, new Map());
        const store = buckets.get(key);
        return {
          match: async (key) =>
            store.get(typeof key === "string" ? key : key.url)?.clone(),
          put: async (key, val) => {
            if (quota) {
              const e = Error("Disk full");
              e.name = "QuotaExceededError";
              throw e;
            }
            store.set(key, val);
          },
        };
      },
    },
    self: {
      location: { origin: "https://soma.test" },
      clients: {
        matchAll: async () => [{postMessage: m => messages.push(m)}],
        claim: async () => {
          claimed = true;
        },
      },
      skipWaiting: async () => {
        ready = true;
      },
      addEventListener: (name, fn) => (handlers[name] = fn),
    },
  };
  const source = readFileSync("scripts/sw-template.js", "utf8")
    .replace("__VERSION__", '"new"')
    .replace(
      "__ASSETS__",
      JSON.stringify([{ url: "/index.html", sha256: sha }]),
    );
  vm.runInNewContext(source, context);
  async function fire(name, extra = {}) {
    let promise;
    handlers[name]({ ...extra, respondWith: (p) => (promise = p), waitUntil: (p) => (promise = p) });
    return await promise;
  }
  return {
    fire, messages,
    send(type) { return fire("message", {data:{type}}); },
    async status() {
      let result;
      await fire("message", {data:{type:"STATUS"}, ports:[{postMessage: m => result=m}]});
      return result;
    },
    get calls() {return calls;}, get aborted() {return aborted;},
    buckets,
    get ready() {
      return ready;
    },
    get claimed() {
      return claimed;
    },
  };
}
test("opening a new worker makes zero asset requests and leaves previous caches intact", async () => {
  const h = harness();
  await h.fire("install");
  await h.fire("activate");
  assert(h.claimed);
  assert.equal(h.calls, 0);
  assert.equal((await h.status()).ready, false);
  assert(h.buckets.has("somasmart-previous"));
});
for (const fault of ["fail", "quota", "corrupt"])
  test(fault + " prevents making a release ready and preserves previous content", async () => {
    const h = harness({[fault]: true});
    await h.send("START");
    assert(h.messages.some(m => m.type === "ERROR"));
    assert.equal((await h.status()).ready, false);
    assert(h.buckets.has("somasmart-previous"));
  });
test("explicit start installs and verifies assets including later corruption", async () => {
  const h = harness();
  await h.send("START");
  assert((await h.status()).ready);
  h.buckets.get("somasmart-manual-new").set("/index.html", new Response("corrupted"));
  assert.equal((await h.status()).ready, false);
});
test("pause aborts current requests and a later explicit start resumes", async () => {
  const h = harness({stall:true});
  const pending = h.send("START");
  while (!h.calls) await new Promise(resolve => setImmediate(resolve));
  await h.send("PAUSE");
  await pending;
  assert(h.aborted);
  assert.equal((await h.status()).running, false);
  assert(h.messages.some(m => m.type === "PAUSED"));
  assert(!h.messages.some(m => m.type === "ERROR"));
  await h.send("START");
  assert((await h.status()).ready);
});
test("an offline navigation can use the previous installation", async () => {
  const h = harness({fail:true});
  const response = await h.fire("fetch", {request:{method:"GET", url:"https://soma.test/", mode:"navigate"}});
  assert.equal(await response.text(), "old working release");
});
