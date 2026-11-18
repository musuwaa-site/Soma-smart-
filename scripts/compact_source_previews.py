"""Encode page previews in WebP without altering source PDFs or image dimensions."""
from concurrent.futures import ThreadPoolExecutor
from io import BytesIO
import json
from pathlib import Path
import sys

from PIL import Image

build = Path(sys.argv[1])
previews = sorted((build / 'source-papers').glob('*/page-*.jpg'))


def compact(path):
    with Image.open(path) as image:
        encoded = BytesIO()
        image.save(encoded, 'WEBP', quality=82, method=4)
    payload = encoded.getvalue()
    if len(payload) >= path.stat().st_size:
        return None
    replacement = path.with_suffix('.webp')
    replacement.write_bytes(payload)
    path.unlink()
    return ('/' + path.relative_to(build).as_posix(), '/' + replacement.relative_to(build).as_posix())


with ThreadPoolExecutor(max_workers=4) as pool:
    replacements = dict(pair for pair in pool.map(compact, previews) if pair)
Path(sys.argv[2]).write_text(json.dumps(replacements))
