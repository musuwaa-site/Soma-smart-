"""Apply the scored Kigoma Business Studies transcription and retain its page reader."""
from import_interactive_papers import R, merge


def apply(data):
    version = data['version']
    merged, report = merge(data, [R / 'content/batches/026-kigoma-business-scored.json'])
    if len(report) != 1 or not report[0]['completeScoredPaper'] or report[0]['marks'] != 100:
        raise ValueError('Incomplete Kigoma Business Studies import')
    merged['version'] = version
    return merged
