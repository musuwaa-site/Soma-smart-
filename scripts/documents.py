"""Acquire, extract text/layout/images and stage numbered questions for human review.
Never auto-publishes. OCR optional: tesseract executable for pages without text.
"""
import argparse, pathlib, json, hashlib, urllib.request, urllib.parse, re, datetime, subprocess, shutil
import fitz
ROOT=pathlib.Path(__file__).resolve().parents[1]
def acquire(url,category,title):
 safe=urllib.parse.quote(url,safe=':/?=&%'); raw=urllib.request.urlopen(safe,timeout=45).read()
 if not raw.startswith(b'%PDF'):raise ValueError('Source is not a PDF')
 sha=hashlib.sha256(raw).hexdigest(); folder=ROOT/'acquisition'/'documents'/sha[:16];folder.mkdir(parents=True,exist_ok=True); (folder/'original.pdf').write_bytes(raw)
 meta=dict(id=sha[:16],url=url,sourceTitle=title,category=category,acquiredAt=datetime.datetime.now(datetime.timezone.utc).isoformat(),sha256=sha,rightsStatus='unresolved',verificationStatus='unverified',publicationStatus='draft')
 (folder/'source.json').write_text(json.dumps(meta,indent=2));return folder

def extract(folder,ocr_language="eng"):
 folder=pathlib.Path(folder);doc=fitz.open(folder/'original.pdf');pages=[];questions=[]
 for n,page in enumerate(doc):
  text=page.get_text(sort=True);pix=page.get_pixmap(matrix=fitz.Matrix(1.3,1.3));image=folder/f'page-{n+1}.png';pix.save(image)
  native_text=text
  meaningful=re.sub(r'(?i)find this and other free resources at:?|https?://\S+|maktaba|tetea|find|resources','',text)
  scanned=len(set(re.findall(r'[A-Za-z]{2,}',meaningful)))<20
  ocr_used=False
  if scanned and shutil.which('tesseract'):
   ocr=subprocess.run(['tesseract',str(image),'stdout','-l',ocr_language],capture_output=True,text=True);text=ocr.stdout;ocr_used=True
  images=[]
  for j,img in enumerate(page.get_images(full=True)):
   info=doc.extract_image(img[0]);fn=f'image-{n+1}-{j}.{info["ext"]}';(folder/fn).write_bytes(info['image']);images.append(fn)
  tables=[]
  try:
   for table in page.find_tables().tables:tables.append(table.extract())
  except (AttributeError,ValueError):pass
  pages.append(dict(page=n+1,text=text,blocks=page.get_text('dict'),render=image.name,images=images,tables=tables,needsOCR=scanned and not ocr_used,ocrUsed=ocr_used,ocrLanguage=ocr_language if ocr_used else None,nativeText=native_text))
  chunks=re.split(r'(?m)^\s*(\d{1,2})[.)]\s+',text)
  for j in range(1,len(chunks)-1,2):
   content=chunks[j+1].strip()
   questions.append(dict(id=f'{folder.name}-p{n+1}-q{chunks[j]}',paperId=folder.name,questionNumber=chunks[j],content=content,sourcePage=n+1,sourceRender=image.name,media=images,maximumMarks=None,answerKey=None,rightsStatus='unresolved',verificationStatus='needs-human-review',publicationStatus='draft',extractionWarnings=['Page breaks and numbering require reconciliation.','Verify mathematical notation against rendered source.','Assign form, subject, curriculum mapping, marks and rights before import.']))
 # Strip binary image blocks while retaining their bounding boxes.
 for p in pages:
  for b in p['blocks'].get('blocks',[]):
   if 'image' in b:b.pop('image')
   if 'mask' in b:b.pop('mask')
 (folder/'extraction.json').write_text(json.dumps(dict(pages=pages,questions=questions),ensure_ascii=False,indent=2,default=str))
 (folder/'text.txt').write_text('\n\n'.join(p['text'] for p in pages));return len(pages),len(questions)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--url');p.add_argument('--category',default='candidate-paper');p.add_argument('--title',default='Unverified source');p.add_argument('--folder');p.add_argument('--ocr-language',default='eng');a=p.parse_args()
 f=acquire(a.url,a.category,a.title) if a.url else pathlib.Path(a.folder);print(f,extract(f,a.ocr_language))
