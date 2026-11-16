"""Merge a reviewed structured release without duplicate IDs or uncleared publication."""
import argparse,json,pathlib,sys
from validate import validate,ROOT
sys.path.insert(0,str(ROOT/'admin'));from server import atomic
p=argparse.ArgumentParser();p.add_argument('file');p.add_argument('--apply',action='store_true');a=p.parse_args();incoming=json.loads(pathlib.Path(a.file).read_text());data=json.loads((ROOT/'content/library.json').read_text())
for name in ['subjects','lessons','questions','books','papers','glossary']:
 existing={x['id'] for x in data[name]};new=incoming.get(name,[]);seen=set()
 for row in new:
  if row['id'] in existing or row['id'] in seen:raise SystemExit(f'Duplicate import rejected: {name}/{row["id"]}')
  seen.add(row['id'])
 data[name].extend(new)
errors=validate(data)
if errors:raise SystemExit('\n'.join(errors))
if a.apply:atomic(ROOT/'content/library.json',data)
print('Validated', 'and imported' if a.apply else '(dry run; pass --apply to persist)')
