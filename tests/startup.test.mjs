import test from 'node:test';
import assert from 'node:assert/strict';
import {loadLibrary,withStorageTimeout} from '../src/startup.js';
const library={subjects:[],lessons:[{title:'Kiswahili ≥ 1'}],questions:[],books:[]};
test('startup reads streamed Unicode library data and reports download progress',async()=>{
  const bytes=new TextEncoder().encode(JSON.stringify(library)),progress=[];
  const stream=new ReadableStream({start(c){for(let i=0;i<bytes.length;i+=3)c.enqueue(bytes.slice(i,i+3));c.close();}});
  const result=await loadLibrary({fetcher:async()=>new Response(stream,{headers:{'content-type':'application/json'}}),onProgress:n=>progress.push(n)});
  assert.deepEqual(result,library);assert.equal(progress.at(-1),bytes.length);assert(progress.length>1);
});
test('startup explains private-preview sign-in and denied access errors',async()=>{
  for(const status of [401,403])await assert.rejects(loadLibrary({fetcher:async()=>new Response('Sign in',{status})}),/private preview.*ChatGPT|private preview was denied/);
});
test('startup identifies an HTML sign-in page instead of presenting a JSON syntax error',async()=>{
  await assert.rejects(loadLibrary({fetcher:async()=>new Response('<html>Sign in</html>',{headers:{'content-type':'text/html'}})}),/sign-in or error page/);
});
test('startup aborts stalled connections with a retry message',async()=>{
  const fetcher=(_,options)=>new Promise((_,reject)=>options.signal.addEventListener('abort',()=>reject(new DOMException('Aborted','AbortError'))));
  await assert.rejects(loadLibrary({fetcher,stallTimeoutMs:10}),/connection stopped responding/);
});
test('startup reports unreachable network and incomplete content without losing saved progress',async()=>{
  await assert.rejects(loadLibrary({fetcher:async()=>{throw new TypeError('Failed to fetch');}}),/could not connect/);
  await assert.rejects(loadLibrary({fetcher:async()=>new Response('{"subjects":[]}',{headers:{'content-type':'application/json'}})}),/incomplete/);
});
test('unresponsive local storage is bounded and never cleared by recovery',async()=>{
  await assert.rejects(withStorageTimeout(new Promise(()=>{}),10),/saved progress has not been cleared/);
  assert.deepEqual(await withStorageTimeout(Promise.resolve({completed:['existing']})),{completed:['existing']});
});
