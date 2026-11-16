"""Restore ignored third-party acquisition workspace from tracked URL/hash metadata.
Not part of student provisioning. Source retrieval requires internet and lawful access.
"""
import json,pathlib,argparse
from documents import acquire,extract,ROOT
p=argparse.ArgumentParser();p.add_argument('--id');p.add_argument('--extract',action='store_true');a=p.parse_args()
for record in json.loads((ROOT/'acquisition/source-register.json').read_text()):
 if a.id and record['id']!=a.id:continue
 folder=ROOT/'acquisition/documents'/record['id']
 if (folder/'original.pdf').exists():print('Already present:',record['id']);continue
 try:
  folder=acquire(record['url'],record['category'],record['sourceTitle']);actual=json.loads((folder/'source.json').read_text())
  if actual['sha256']!=record['sha256']:raise ValueError('Source changed: hash mismatch; manual source review required')
  if a.extract:extract(folder)
  print('Restored:',record['id'])
 except Exception as error:print('NOT RESTORED:',record['id'],str(error))
