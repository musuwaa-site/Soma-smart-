"""Attach the complete scored Markaz mathematics paper and retain its page reader."""
import json
from pathlib import Path

from source_integrity import text_hash

SOURCE = "source-f1950e79f20619eb"
PAPER = "markaz-math-f1-april-2026"
BATCH = Path(__file__).resolve().parents[1] / "content/batches/027-markaz-mathematics-text.json"
INSTRUCTIONS = [
    "This paper consist of ten (10) questions",
    "Answer all questions",
    "Each question carries ten (10) marks",
    "Show clearly all the working and answers in the space provided",
    "All writing must be in blue or black ink, except drawing which must be in pencil.",
    "NECTA mathematical tables, geometric instruments and graph papers may be used where necessary",
    "Write your Assessment name at the top right corner of every page",
]


def apply(data):
    doc = next(doc for doc in data["sourceDocuments"] if doc["id"] == SOURCE)
    guide = doc["independentPracticeGuide"]
    texts = json.loads(BATCH.read_text())
    if guide["sourceSha256"] != doc["sha256"] or set(texts) != set(guide["groups"]):
        raise ValueError("Markaz text, guide and original source must match")
    common = {key: doc[key] for key in ("form", "subjectId", "sourceType", "institution", "year",
              "sourceReference", "sourcePdf", "rightsStatus", "rightsEvidence", "publicationStatus")}
    common.update(sourceDocumentId=SOURCE, sourceSha256=doc["sha256"], verificationStatus="verified")
    questions = []
    pages_by_question = [[2], [2], [2], [3], [3], [3], [3], [3, 4], [4], [4]]
    for n, pages in enumerate(pages_by_question, 1):
        number = str(n)
        model = guide["groups"][number]
        lesson = "mathematics-f1-real-numbers"
        if n in (2, 3):
            lesson = "mathematics-f1-recurring-decimal-prefix"
        if n in (1, 10):
            lesson = "mathematics-f1-01"
        question = dict(common, id=f"{PAPER}-q{n}", paperId=PAPER, questionNumber=number,
                        mainQuestionNumber=number, type="short" if n == 1 else "calculation",
                        requiresDrawing=n == 4, topicIds=[lesson], subtopicIds=[], content=texts[number],
                        sourceTitle=doc["title"], transcriptionBatch=BATCH.name, options=[],
                        sourcePages=pages, media=[dict(role="source-page", path=doc["pageImages"][p-1],
                        alt=f"Original Markaz Mathematics paper, page {p}") for p in pages],
                        maximumMarks=model["maximumMarks"], markIncrement=1,
                        marksProvenance="Printed paper, cover instruction iii",
                        markIncrementProvenance="Independent SomaSmart rubric",
                        answerKey="\n".join(f"{p['label']}. {p['answer']}" for p in model["parts"]),
                        markingGuide="\n".join(f"{p['label']} ({p['marks']} marks). {p['rubric']}" for p in model["parts"]),
                        solutionProvenance=guide["provenance"])
        question["sourceTextSha256"] = text_hash(question)
        questions.append(question)
    ids = [q["id"] for q in questions]
    paper = dict(common, id=PAPER, title=doc["title"], questionIds=ids, allTranscribedQuestionIds=ids,
                 draftQuestionIds=[], excludedQuestions=[], publicationScope="complete-paper",
                 totalSourceMainQuestions=10, completePaper=True, completeScoredPaper=True,
                 transcriptionComplete=True, maximumMarks=100, sourceMaximumMarks=100,
                 sourceInstructions=INSTRUCTIONS, timeAllowed="2:30 Hours")
    data["questions"] = [q for q in data["questions"] if q.get("paperId") != PAPER] + questions
    data["papers"] = [p for p in data["papers"] if p["id"] != PAPER] + [paper]
    doc.update(interactivePaperId=PAPER, questionTranscriptionStatus="complete")
    return data
