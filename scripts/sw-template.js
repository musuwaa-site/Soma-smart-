const VERSION = __VERSION__,
  ASSETS = __ASSETS__,
  CACHE = "somasmart-manual-" + VERSION,
  COMPLETE = "/.somasmart-complete";
async function broadcast(message) {
  for (const c of await self.clients.matchAll({ includeUncontrolled: true }))
    c.postMessage(message);
}
async function digest(response) {
  return [
    ...new Uint8Array(
      await crypto.subtle.digest("SHA-256", await response.arrayBuffer()),
    ),
  ]
    .map((v) => v.toString(16).padStart(2, "0"))
    .join("");
}
async function valid(cache) {
  for (const asset of ASSETS) {
    const response = await cache.match(asset.url);
    if (!response || (await digest(response)) !== asset.sha256) return false;
  }
  return true;
}
let job;
async function provision(signal) {
  const cache = await caches.open(CACHE);
  let next = 0, done = 0, failure;
  async function copyAssets() {
    while (!signal.aborted && !failure && next < ASSETS.length) {
      const asset = ASSETS[next++];
      try {
        const existing = await cache.match(asset.url);
        if (!existing || (await digest(existing)) !== asset.sha256) {
          if (signal.aborted) return;
          const response = await fetch(asset.url, {cache: "no-store", signal});
          if (!response.ok || (await digest(response.clone())) !== asset.sha256)
            throw Error("Missing or corrupted asset: " + asset.url);
          if (signal.aborted) return;
          await cache.put(asset.url, response);
        }
        if (!signal.aborted) await broadcast({type: "PROGRESS", done: ++done, total: ASSETS.length});
      } catch (error) { failure = error; }
    }
  }
  await Promise.all(Array.from({length: Math.min(6, ASSETS.length)}, copyAssets));
  if (signal.aborted) return;
  if (failure) throw failure;
  if (!(await valid(cache))) throw Error("Offline content validation failed");
  if (signal.aborted) return;
  await cache.put(COMPLETE, new Response(VERSION));
  await broadcast({type: "READY", version: VERSION});
}

self.addEventListener("install", event => event.waitUntil(self.skipWaiting()));
self.addEventListener("activate", event => event.waitUntil(self.clients.claim()));
self.addEventListener("message", event => {
  const type = event.data?.type;
  if (type === "START" && !job) {
    const controller = new AbortController();
    job = controller;
    event.waitUntil(provision(controller.signal).catch(error => {
      if (!controller.signal.aborted) return broadcast({type: "ERROR", message:
        error.name === "QuotaExceededError" ? "Not enough storage. Free space and retry." : error.message});
    }).finally(() => { if (job === controller) job = undefined; }));
  }
  if (type === "PAUSE") {
    job?.abort();
    job = undefined;
    event.waitUntil(broadcast({type: "PAUSED"}));
  }
  if (type === "STATUS") event.waitUntil((async () => {
    const cache = await caches.open(CACHE);
    const ready = !!(await cache.match(COMPLETE)) && await valid(cache);
    event.ports?.[0]?.postMessage({ready, running: !!job, version: VERSION});
  })());
});

async function previousResponse(path) {
  for (const name of (await caches.keys()).reverse()) {
    if (name === CACHE || !name.startsWith("somasmart-")) continue;
    const previous = await caches.open(name);
    if (name.startsWith("somasmart-manual-") && !(await previous.match(COMPLETE))) continue;
    const stored = await previous.match(path);
    if (stored) return stored;
  }
}
self.addEventListener("fetch", event => {
  const url = new URL(event.request.url);
  if (event.request.method !== "GET" || url.origin !== self.location.origin) return;
  const path = event.request.mode === "navigate" ? "/index.html" : url.pathname;
  event.respondWith((async () => {
    const cache = await caches.open(CACHE);
    const asset = ASSETS.find(item => item.url === path);
    if (asset && await cache.match(COMPLETE)) {
      const stored = await cache.match(path);
      if (stored && (await digest(stored.clone())) === asset.sha256) return stored;
    }
    try { return await fetch(event.request); }
    catch (error) {
      const response = await previousResponse(path);
      if (response) return response;
      throw error;
    }
  })());
});
