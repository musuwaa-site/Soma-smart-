import subprocess,sys
for script in ['seed_content.py','enrich.py','prepare_dev.py','inventory.py']:
 subprocess.run([sys.executable,'scripts/'+script],check=True)
