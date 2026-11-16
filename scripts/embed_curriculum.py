"""Embed the already-reviewed locator catalogue without requiring source PDF copies."""
import pathlib,json
ROOT=pathlib.Path(__file__).resolve().parents[1];p=ROOT/'content/library.json';d=json.loads(p.read_text());c=json.loads((ROOT/'content/curriculum-map.json').read_text());d['curriculum']['activities']=c['activities'];d['curriculum']['sources']=c['sources'];p.write_text(json.dumps(d,ensure_ascii=False,indent=2))
