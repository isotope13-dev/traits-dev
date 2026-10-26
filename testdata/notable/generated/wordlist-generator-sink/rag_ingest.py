"""Reading-order validation for PDF ingest (fixture: benign near miss)."""
import fitz


def word_pairs(words):
    return set(zip(words, words[1:]))


doc = fitz.open("norm.pdf")
page = doc[0]
native = page.get_text().split()
rebuilt = [w for row in page.get_text("words") for w in row[4:5]]
ours = word_pairs(rebuilt)
if len(ours & word_pairs(native)) < 20:
    raise SystemExit("regrouping diverged from native order")
