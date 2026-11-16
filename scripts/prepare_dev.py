import pathlib,shutil
root=pathlib.Path(__file__).resolve().parents[1];shutil.copyfile(root/'content/library.json',root/'public/library.json')
