"""Rasterise the original local vector mark for Android PWA installation."""
import fitz,pathlib,json
P=pathlib.Path(__file__).resolve().parents[1]/'public';doc=fitz.open(stream=(P/'icon.svg').read_bytes(),filetype='svg');page=doc[0]
for n in [192,512]:page.get_pixmap(matrix=fitz.Matrix(n/page.rect.width,n/page.rect.height),alpha=False).save(P/f'icon-{n}.png')
m=json.loads((P/'manifest.webmanifest').read_text());m['icons']=[dict(src=f'/icon-{n}.png',sizes=f'{n}x{n}',type='image/png',purpose='any') for n in [192,512]];(P/'manifest.webmanifest').write_text(json.dumps(m,indent=2))
