import subprocess,sys
for script in ['seed_content.py','enrich.py','batch_two.py','workbook_batch.py','revision_papers.py','expansion_diagrams.py','embed_curriculum.py','prepare_dev.py','inventory.py']:
 subprocess.run([sys.executable,'scripts/'+script],check=True)
