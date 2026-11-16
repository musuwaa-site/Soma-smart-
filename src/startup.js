export function responseError(response) {
  if (response.status===401) return 'This private preview requires your ChatGPT sign-in. Open it in a browser signed into the same ChatGPT account.';
  if (response.status===403) return 'Access to this private preview was denied. Open it in a browser signed into the same ChatGPT account. If it still fails, note the displayed error code.';
  return `The learning library could not be downloaded (HTTP ${response.status}). Reconnect and retry.`;
}

export async function loadLibrary({fetcher=fetch,onProgress=()=>{},stallTimeoutMs=45000}={}) {
  const controller=new AbortController();let timer;
  const arm=()=>{clearTimeout(timer);timer=setTimeout(()=>controller.abort(),stallTimeoutMs);};
  arm();
  try {
    const response=await fetcher('/library.json',{signal:controller.signal});
    if(!response.ok)throw Error(responseError(response));
    if(!response.headers.get('content-type')?.includes('application/json'))throw Error('The server returned a sign-in or error page instead of the learning library. Open this private preview in your signed-in browser and retry.');
    let text;
    if(response.body?.getReader){
      const reader=response.body.getReader(),decoder=new TextDecoder();let bytes=0;const chunks=[];
      while(true){
        const {done,value}=await reader.read();if(done)break;
        arm();bytes+=value.byteLength;chunks.push(decoder.decode(value,{stream:true}));onProgress(bytes);
      }
      chunks.push(decoder.decode());text=chunks.join('');
    }else text=await response.text();
    const data=JSON.parse(text);
    if(!Array.isArray(data.subjects)||!Array.isArray(data.lessons)||!Array.isArray(data.questions)||!Array.isArray(data.books))throw Error('The downloaded learning library is incomplete. Retry the download.');
    return data;
  }catch(error){
    if(controller.signal.aborted)throw Error('The connection stopped responding while loading the library. Reconnect and retry; your saved progress has not been cleared.');
    if(error instanceof SyntaxError)throw Error('The learning library download could not be read. Reconnect and retry; your saved progress has not been cleared.');
    if(error instanceof TypeError)throw Error('SomaSmart could not connect to its learning library. Check your connection and open the private preview in your signed-in browser.');
    throw error;
  }finally{clearTimeout(timer);}
}

export function withStorageTimeout(operation,timeoutMs=15000) {
  let timer;
  return Promise.race([operation,new Promise((_,reject)=>{timer=setTimeout(()=>reject(Error('Local storage is not responding. Close other SomaSmart tabs and open this preview in your browser. Your saved progress has not been cleared.')),timeoutMs);})]).finally(()=>clearTimeout(timer));
}
