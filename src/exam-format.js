const escape = value => String(value ?? '').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
export function verbatimContent(q) {
  const text=q.content, ranges=[];
  for(const term of q.underlinedTerms || []) {
    const start=text.indexOf(term);
    if(start>=0) ranges.push([start,start+term.length]);
  }
  ranges.sort((a,b)=>a[0]-b[0]);let cursor=0,html='';
  for(const [start,end] of ranges) { if(start<cursor) continue; html+=escape(text.slice(cursor,start))+'<u>'+escape(text.slice(start,end))+'</u>';cursor=end; }
  return (html+escape(text.slice(cursor))).replaceAll('\n','<br>');
}
export function originalOptionLabel(q,index) {
  return q.optionLabels?.[index] ? `<strong>${escape(q.optionLabels[index])}.</strong> ` : '';
}
