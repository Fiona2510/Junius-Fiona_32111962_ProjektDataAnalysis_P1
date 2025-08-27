# NLP-Analyse von TripAdvisor Hotelbewertungen (mit DuckDB)

Dieses Projekt analysiert Hotelbewertungen mit NLP (BoW/TF‑IDF, LDA/NMF) und bestimmt die optimale Anzahl Themen über den **Coherence Score (c_v)**.
Neu: **DuckDB** als kostenfreie, lokale Analytics-DB für schnellen, reproduzierbaren Datenzugriff.

**Repository:** https://github.com/Fiona2510/Junius-Fiona_32111962_-ProjektDataAnalysis-_P1

## Warum DuckDB?
- **Schnell & leichtgewichtig:** In‑Process, kein Server nötig.
- **Klare Datenpipeline:** Import/Filter/Dedupe per SQL.
- **Kostenfrei & offline:** Eine Datei `data/tripadvisor.duckdb`.
- **Kompatibel:** pandas/scikit-learn/gensim bleiben unverändert.

> Für sehr kleine Daten reicht pandas allein. Für mittlere/große CSVs ist DuckDB i.d.R. sinnvoll.

## Struktur
```
Junius-Fiona_32111962_-ProjektDataAnalysis-_P1/
├─ data/
│  ├─ tripadvisor_hotel_reviews.csv
│  ├─ tripadvisor.duckdb
│  └─ reviews.parquet
├─ src/
│  ├─ preprocessing.py
│  ├─ topic_models.py
│  └─ data_store.py
├─ sql/
│  └─ bootstrap.sql
├─ notebooks/
│  └─ analysis.ipynb
├─ reports/
│  ├─ coherence_vs_k.pdf
│  └─ Phase2_Erarbeitungs_Reflexion.pdf
├─ requirements.txt
└─ .gitignore
```

## Schritt-für-Schritt

### 1) Installation
```bash
python -m venv venv
# macOS/Linux
source venv/bin/activate
# Windows
# .\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -c "import nltk; import ssl; ssl._create_default_https_context = ssl._create_unverified_context; import nltk; nltk.download('punkt'); nltk.download('stopwords')"
```

### 2) CSV in DuckDB importieren
**Variante A (Python):**
```bash
python -c "from src.data_store import bootstrap_from_csv; bootstrap_from_csv('data/tripadvisor_hotel_reviews.csv')"
```
**Variante B (SQL-Skript):**
```bash
python - <<'PY'
import duckdb
con = duckdb.connect('data/tripadvisor.duckdb')
con.execute(open('sql/bootstrap.sql','r',encoding='utf-8').read())
print('Bootstrapping done.')
PY
```

### 3) Notebook starten
```bash
jupyter notebook notebooks/analysis.ipynb
```
- Im Abschnitt **Datenquelle via DuckDB** wird die DB angelegt (falls noch nicht vorhanden) und die Daten geladen.
- Danach laufen Vektorisierung (BoW/TF‑IDF) und Topic‑Modelle (LDA/NMF) wie gehabt.
- Die optimale Topic‑Zahl wird über ein k‑Grid (standardmäßig 3–10) via **Coherence c_v** bestimmt.

### 4) Nützliche SQL-Beispiele
```sql
-- Nur Zeilen mit Textfeld
SELECT * FROM reviews WHERE review IS NOT NULL;

-- Stichprobe (schnell testen)
SELECT * FROM reviews USING SAMPLE 1000 ROWS;

-- Spalteninfo
PRAGMA table_info(reviews);
```

## Hinweise
- `src/data_store.py` kapselt die DB‑Erstellung und den Zugriff aus Python.
- Eine Parquet‑Kopie (`data/reviews.parquet`) wird optional erzeugt und kann direkt mit pandas geladen werden.
- Für Repro: baue die DB stets deterministisch aus der CSV (siehe `bootstrap.sql`).

## Lizenz
MIT
