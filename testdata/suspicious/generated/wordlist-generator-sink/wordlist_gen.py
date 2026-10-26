"""Build a custom wordlist from a PDF (fixture: true-positive control)."""
import fitz


def word_pairs(words):
    return set(zip(words, words[1:]))


doc = fitz.open("report.pdf")
words = []
for page in doc:
    words += page.get_text().split()
pairs = word_pairs(words)
with open("custom_wordlist.txt", "w", encoding="utf-8") as wordlist:
    for first, second in sorted(pairs):
        wordlist.write(f"{first}{second}\n")
