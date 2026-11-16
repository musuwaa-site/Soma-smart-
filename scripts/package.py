import zipfile,pathlib,hashlib,json
root=pathlib.Path(__file__).resolve().parents[1];out=root/'artifacts';out.mkdir(exist_ok=True)
with zipfile.ZipFile(out/'somasmart-development-web.zip','w',compression=zipfile.ZIP_DEFLATED) as z:
 for p in (root/'dist').rglob('*'):
  if p.is_file():z.write(p,p.relative_to(root/'dist'))
sha=hashlib.sha256((out/'somasmart-development-web.zip').read_bytes()).hexdigest();(out/'SHA256SUMS').write_text(sha+'  somasmart-development-web.zip\n');print(sha)
