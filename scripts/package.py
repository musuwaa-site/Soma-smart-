"""Package the student web build and original content with stable ZIP timestamps."""
import zipfile,pathlib,hashlib,json
root=pathlib.Path(__file__).resolve().parents[1];out=root/'artifacts';out.mkdir(exist_ok=True)
def write(z,name,blob):
 info=zipfile.ZipInfo(str(name),(2026,11,16,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;z.writestr(info,blob)
web=out/'somasmart-development-web.zip';content=out/'somasmart-original-content-development.zip'
with zipfile.ZipFile(web,'w') as z:
 for p in sorted((root/'dist').rglob('*')):
  if p.is_file():write(z,p.relative_to(root/'dist'),p.read_bytes())
with zipfile.ZipFile(content,'w') as z:
 for kind in ['books','exams']:
  for p in sorted((root/'public'/kind).glob('*')):
   if p.is_file():write(z,kind+'/'+p.name,p.read_bytes())
 write(z,'CONTENT_INVENTORY.md',(root/'docs/CONTENT_INVENTORY.md').read_bytes())
 write(z,'STATUS.txt',b'Unfinished original SomaSmart development resources. EPUB books are partial manuscripts. Revision tests and answer guides are original, not genuine past examinations. Full curriculum coverage is not claimed.\n')
lines=[hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.name for p in [web,content]];(out/'SHA256SUMS').write_text('\n'.join(lines)+'\n');print('\n'.join(lines))
