"""Extract official learning-activity cells to an ignored local review index.
Public mapping must use reviewed concise topic labels, not redistribute syllabus tables.
"""
import pathlib,json,re,fitz
ROOT=pathlib.Path(__file__).resolve().parents[1]
subjects={'f6b93b5819e5c582':'chemistry','0e0f96e61e9ec349':'physics','06537e79ec6d005a':'biology','a666f9276704c2d0':'mathematics','882332bb296bc693':'kiswahili','89a9dd3eb858f8d0':'geography','302a9bb91147e4ce':'business','5510fd3e38500baf':'historia','6daa1f44f86bd186':'english'}
output=[]
for id,sid in subjects.items():
 folder=ROOT/'acquisition/documents'/id;doc=fitz.open(folder/'original.pdf');form=0;previous=None
 for n,page in enumerate(doc):
  text=page.get_text();marker=re.search(r'(?:Table|Jedwali\s*(?:Na\.?)?)\s*([3-6])\s*[:.]',text,re.I)
  if marker and not re.search(r'\.{5,}|…',text):form=int(marker[1])-2
  if form not in [1,2]:continue
  tables=page.find_tables().tables
  for table in tables:
   rows=table.extract()
   for row in rows:
    if len(row)<6:continue
    cell=' '.join((row[2] or '').replace('\x07','').split())
    if not cell or any(h in cell.lower() for h in ['learning activities','shughuli za ujifunzaji']):continue
    chunks=re.split(r'(?=\([a-z]\)\s)',cell)
    for chunk in chunks:
     chunk=chunk.strip()
     if not chunk:continue
     if re.match(r'\([a-z]\)',chunk):
      previous={'id':f'{sid}-f{form}-activity-{sum(x["form"]==form and x["subjectId"]==sid for x in output)+1:02}','form':form,'subjectId':sid,'sourceId':id,'pdfPages':[n+1],'rawActivity':chunk,'verificationStatus':'extracted-needs-review'};output.append(previous)
     elif previous and previous['form']==form:
      previous['rawActivity']+=' '+chunk
      if n+1 not in previous['pdfPages']:previous['pdfPages'].append(n+1)
(ROOT/'acquisition/curriculum-review.json').write_text(json.dumps(output,ensure_ascii=False,indent=2))
for sid in subjects.values():
 for f in [1,2]:
  print('\n###',sid,'Form',f)
  for a in output:
   if a['subjectId']==sid and a['form']==f:print(a['id'],a['pdfPages'],a['rawActivity'])
