# NLP-Analyse von TripAdvisor Hotelbewertungen (mit DuckDB auf Windows)

Dieses Projekt analysiert Hotelbewertungen mit NLP (BoW/TF‑IDF, LDA/NMF) und bestimmt die optimale Anzahl Themen über den Coherence Score (c_v).
Eine DuckDB wird als kostenfreie, lokale Analytics-DB für schnellen, reproduzierbaren Datenzugriff genutzt.

Windows-Hinweis: Long Paths ist auf Windows aktiviert worden, um Pfadprobleme zu vermeiden.

Repository: https://github.com/Fiona2510/Junius-Fiona_32111962_ProjektDataAnalysis_P1

## Warum DuckDB?
- Schnell & leichtgewichtig: In‑Process, kein Server nötig.
- Klare Datenpipeline: Import/Filter/Dedupe per SQL.
- Kostenfrei & offline: Eine Datei `data/tripadvisor.duckdb`.
- Kompatibel: pandas/scikit-learn/gensim bleiben unverändert.

## Struktur
```
Junius-Fiona_32111962_-ProjektDataAnalysis-_P1/
├─ data/
│  ├─ tripadvisor_hotel_reviews.csv
│  ├─ tripadvisor.duckdb
│  └─ reviews.parquet
├─ notebooks/
│  └─ analysis.ipynb
├─ src/
│  ├─ preprocessing.py
│  ├─ topic_models.py
│  └─ data_store.py
├─ sql/
│  └─ bootstrap.sql
├─ reports/
│  ├─ coherence_vs_k.pdf
│  ├─ topics_lda.csv
│  └─ topics_nmf.csv
├─ requirements.txt
├─ README.md
└─ .gitignore
```
## Schritt-für-Schritt

### 1) Installation
bat
py -m venv .venv
call .venv\Scripts\activate.bat
pip install -r requirements.txt
python -c "import nltk; import ssl; ssl._create_default_https_context = ssl._create_unverified_context; import nltk; nltk.download('punkt'); nltk.download('stopwords')"

### 2) CSV in DuckDB importieren
Lege die CSV hier ab: data\tripadvisor_hotel_reviews.csv, dann:
bat
python -c "from src.data_store import bootstrap_from_csv; bootstrap_from_csv('data\\tripadvisor_hotel_reviews.csv', overwrite=True)"

### 3) Notebook starten
bat
jupyter notebook notebooks\analysis.ipynb

Im Notebook der Reihe nach:
 - Daten aus DuckDB laden
 - Text-Cleaning → clean_review
 - BoW/TF-IDF + LDA/NMF (Sanity-Check)
 - Coherence-Grid (z. B. k = 3..10) → speichert reports/coherence_vs_k.pdf
 - Export Topics → reports/topics_lda.csv, reports/topics_nmf.csv

### 4) Ergebnisse
 - Optimale k: k_LDA = …, k_NMF = … (jeweils höchster c_v)
 - Typische Themen: Sauberkeit, Personal/Service, Lage, Preis-Leistung, Zimmer/Komfort
 - Interpretation: LDA liefert probabilistische Mischungen, NMF oft klarere Trennungen

Artefakte:
 - reports/coherence_vs_k.pdf
 - reports/topics_lda.csv
 - reports/topics_nmf.csv

## Hinweise
Teile des Codes (DuckDB-Integration, Coherence-Grid und Notebook) wurden mit Unterstützung von ChatGPT (Modell: GPT-5 Thinking) erstellt und von der Autorin überprüft und an die Aufgabenstellung angepasst.
