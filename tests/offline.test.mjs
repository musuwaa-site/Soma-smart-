import test from "node:test";
import assert from "node:assert/strict";
import vm from "node:vm";
import { webcrypto, createHash } from "node:crypto";
import { readFileSync } from "node:fs";
const content = new TextEncoder().encode("complete lesson library");
const sha = createHash("sha256").update(content).digest("hex");
function harness({ fail = false, quota = false, corrupt = false } = {}) {
  const handlers = {},
    buckets = new Map([
      [
        "somasmart-previous",
        new Map([["/index.html", new Response("old working release")]]),
      ],
    ]);
  let ready = false,
    claimed = false;
  const context = {
    Response,
    URL,
    Uint8Array,
    Error,
    crypto: webcrypto,
    fetch: async () => {
      if (fail) throw Error("Interrupted network");
      return new Response(corrupt ? "broken content" : content);
    },
    caches: {
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
        matchAll: async () => [],
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
    handlers[name]({ ...extra, waitUntil: (p) => (promise = p) });
    await promise;
  }
  return {
    fire,
    buckets,
    get ready() {
      return ready;
    },
    get claimed() {
      return claimed;
    },
  };
}
test("complete validated content is required before worker activation", async () => {
  const h = harness();
  await h.fire("install");
  assert(h.ready);
  await h.fire("activate");
  assert(h.claimed);
  assert(h.buckets.has("somasmart-previous"));
});
for (const fault of ["fail", "quota", "corrupt"])
  test(`${fault} prevents release switch and retains previous release`, async () => {
    const h = harness({ [fault]: true });
    await assert.rejects(h.fire("install"));
    assert(!h.ready);
    assert(!h.claimed);
    assert(h.buckets.has("somasmart-previous"));
  });
test("ready status checks cached integrity, including later corruption", async () => {
  const h = harness();
  await h.fire("install");
  let status;
  await h.fire("message", {
    data: { type: "STATUS" },
    ports: [{ postMessage: (m) => (status = m) }],
  });
  assert(status.ready);
  h.buckets.get("somasmart-new").set("/index.html", new Response("corrupt"));
  await h.fire("message", {
    data: { type: "STATUS" },
    ports: [{ postMessage: (m) => (status = m) }],
  });
  assert(!status.ready);
});
test("activation rejects missing content without clearing previous version", async () => {
  const h = harness();
  await assert.rejects(h.fire("activate"));
  assert(!h.claimed);
  assert(h.buckets.has("somasmart-previous"));
});
