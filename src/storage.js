let database;
export async function db() {
  if (database) return database;
  database = await new Promise((resolve, reject) => {
    const r = indexedDB.open("somasmart-student", 1);
    r.onupgradeneeded = () => r.result.createObjectStore("local");
    r.onsuccess = () => resolve(r.result);
    r.onerror = () => reject(r.error);
    r.onblocked = () =>
      reject(Error("Close other SomaSmart tabs to update storage."));
  });
  return database;
}
export async function get(key, fallback) {
  const d = await db();
  return new Promise((resolve, reject) => {
    const r = d.transaction("local").objectStore("local").get(key);
    r.onsuccess = () => resolve(r.result ?? fallback);
    r.onerror = () => reject(r.error);
  });
}
export async function set(key, value) {
  const d = await db();
  return new Promise((resolve, reject) => {
    const tx = d.transaction("local", "readwrite");
    tx.objectStore("local").put(value, key);
    tx.oncomplete = () => resolve();
    tx.onerror = () => reject(tx.error);
    tx.onabort = () =>
      reject(tx.error || Error("Storage transaction interrupted."));
  });
}
