
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Ressourcen laden (einmalig)
try:
    stopwords.words("english")
except LookupError:
    nltk.download("stopwords")
try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    nltk.download("punkt")

EN_STOP = set(stopwords.words("english"))
DE_STOP = set(stopwords.words("german"))
ALL_STOP = EN_STOP | DE_STOP

def clean_text(text: str) -> str:
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r"[^a-zäöüß\s]", " ", text)
    tokens = word_tokenize(text)
    tokens = [t for t in tokens if t.isalpha() and t not in ALL_STOP and len(t) > 2]
    return " ".join(tokens)
