# 📊 BankReviewInsights

## Customer Experience Analytics for Fintech Apps

---

## 🧾 Overview

**BankReviewInsights** is a data analytics project focused on understanding customer sentiment and experience for mobile banking apps of three major Ethiopian banks:

* **Commercial Bank of Ethiopia (CBE)**
* **Bank of Abyssinia (BOA)**
* **Dashen Bank**

The project analyzes **1,087 Google Play Store reviews** to uncover satisfaction drivers and pain points using a modular pipeline for:

* Data collection
* Preprocessing
* Sentiment analysis
* Thematic analysis

---

## 🧹 1: Data Collection & Preprocessing

### 🎯 Objective

Scrape and clean Google Play Store reviews for the official apps of **CBE**, **BOA**, and **Dashen Bank**.

### 🔍 Scraping Details

Reviews were scraped using the `google-play-scraper` package.

**App IDs:**

* `com.combanketh.mobilebanking` (CBE) – 550 raw → 360 processed
* `com.boa.boaMobileBanking` (BOA) – 540 raw → 366 processed
* `com.dashen.dashensuperapp` (Dashen) – 448 raw → 361 processed

**Total Processed Reviews:** `1,087`

**Dataset Columns:** `review_id`, `review`, `rating`, `date`, `bank`, `source`

### 🧹 Preprocessing (in `scripts/preprocessor.py`)

Implemented using the `ReviewPreprocessor` class:

* Removed duplicates (based on review text, date, and bank)
* Dropped rows with missing values (0% missing post-cleaning)
* Filtered non-English reviews (≥60% ASCII characters and ≥2 alphabetic words)
* Normalized dates to `YYYY-MM-DD`
* Handled common misspellings (e.g., "masha alla" → "mashallah")

**Drop Rates:**

* CBE: `34.55%`
* BOA: `~32%`
* Dashen: `19.42%`

**Output:** `data/processed/all_reviews.csv`

---

## 📊 2: Sentiment and Thematic Analysis

### 🎯 Objective

Quantify review sentiment and identify recurring themes to uncover satisfaction drivers and pain points.

### 🔍 Sentiment Analysis (in `scripts/sentiment_analyzer.py`)

Using `distilbert-base-uncased-finetuned-sst-2-english`:

* Labeled reviews as **positive**, **negative**, or **neutral** with confidence scores
* Applied custom overrides:

  * Non-text (e.g., names) → neutral
  * Positive/negative keyword matching
  * Rating-based override (e.g., 1-star with positive keywords → recheck)

**Coverage:** `99.8%` (with `95.3%` non-neutral)

**Output:** `data/processed/sentiment_results.csv`

**Aggregation:** `scripts/aggregate_sentiment.py`

* Computed mean confidence by bank, rating, sentiment
* Example: CBE 1-star reviews → `95% negative`, mean confidence `0.98`

**Output:** `data/processed/sentiment_aggregates.csv`
**Visualization:** `plots/figures/sentiment_aggregates.png`

### 🗂️ Thematic Analysis (in `scripts/thematic_analyzer.py`)

* Preprocessing: Tokenization, lemmatization, stopword removal (retaining key words like "best")
* **LDA Model:** Trained 3-topic model (coherence \~`0.51`)
* Themes Mapped:

#### 🎯 Themes Identified (6 total):

1. **Positive User Experience**: e.g., "Best mobile banking app"
2. **Technical Issues**: e.g., "you have to register again..."
3. **Security Issues**: e.g., "it is not safety"
4. **Negative User Experience**: e.g., "a childish app..."
5. **Feature Request**: e.g., "add Amharic"
6. **Customer Service**: e.g., "better service"

**Coverage:** `92.4%` of reviews assigned themes

**Output:** `data/processed/thematic_results.csv`

### 🏷️ Keyword Extraction (in `scripts/keyword_extractor.py`)

* Used TF-IDF to extract top unigrams/bigrams per bank
* Outputs to: `data/processed/keywords_by_bank.csv`

### 🔎 Theme Grouping Logic

| Sentiment | Keywords                       | Theme                    |
| --------- | ------------------------------ | ------------------------ |
| Positive  | praise                         | Positive User Experience |
| Negative  | technical (slowloading, crash) | Technical Issues         |
| Negative  | security (safety)              | Security Issues          |
| Negative  | generic criticism (worst, bad) | Negative User Experience |
| Positive  | feature suggestions (add)      | Feature Request          |
| Positive  | service/support praise         | Customer Service         |

**Themes by Bank:**

* **CBE:** 6 themes
* **BOA:** 5 themes
* **Dashen:** 5 themes

### 📊 Visualizations

* Theme % by bank → `plots/figures/theme_percentage.png`
* Sentiment-theme correlation heatmap → `plots/figures/sentiment_theme_correlation.png`
* Word clouds → e.g., `wordcloud_positive_user_experience.png`
* Interactive LDA → `data/processed/lda_topics.html`

---

## 📈 EDA for Themes (in `notebooks/eda_themes.ipynb`)

* Summarized theme distributions
* Visualized sentiment-theme correlations
* Word cloud inspections
* Validated KPIs: >90% sentiment coverage, ≥3 themes/bank

---

## 📝 Interim Report

Compiled in `reports/interim_report.tex` → PDF: `interim_report.pdf`

Includes:

* Task 1 & 2 summaries
* Sentiment aggregates
* Theme insights and visuals

---

## 🔧 Pipeline

**Scripts:**

* `sentiment_analyzer.py`
* `aggregate_sentiment.py`
* `thematic_analyzer.py`
* `keyword_extractor.py`

**Data Flow:**

```
data/processed/all_reviews.csv
  → sentiment_results.csv
  → thematic_results.csv
```

**Outputs:**

* `sentiment_aggregates.csv`
* `keywords_by_bank.csv`
* `theme_summary.csv`
* `plots/`, `lda_model.gensim`

---

## ✅ KPIs Achieved

* **Sentiment Coverage:** `99.8%`
* **Themes:** 4–6 themes per bank
* **Codebase:** Modular, reproducible

---

## 🗃️ Directory Structure

```
BankReviewInsights/
├── data/
│   ├── raw/                  # Raw review CSVs
│   └── processed/            # Cleaned & analyzed data
├── notebooks/
│   ├── scrape_reviews_*.ipynb
│   ├── eda_*.ipynb
│   └── eda_themes.ipynb
├── scripts/
│   ├── scraper.py
│   ├── preprocessor.py
│   ├── combine_reviews.py
│   ├── sentiment_analyzer.py
│   ├── aggregate_sentiment.py
│   ├── thematic_analyzer.py
│   └── keyword_extractor.py
├── plots/
│   └── figures/              # PNG visuals
├── reports/
│   ├── interim_report.tex
│   └── interim_report.pdf
├── tests/                   # (Coming soon)
├── requirements.txt
├── README.md
```

---

## 📦 Installation

```bash
git clone https://github.com/your-username/BankReviewInsights.git
cd BankReviewInsights
pip install -r requirements.txt
```

---

## 🚀 Usage

```bash
# Scrape Reviews
jupyter notebook notebooks/scrape_reviews_cbe.ipynb

# Preprocess
python scripts/preprocessor.py

# Sentiment Analysis
python scripts/sentiment_analyzer.py
python scripts/aggregate_sentiment.py

# Thematic Analysis
python scripts/thematic_analyzer.py
python scripts/keyword_extractor.py

# EDA
jupyter notebook notebooks/eda_themes.ipynb

# Compile Report
latexmk -pdf reports/interim_report.tex
```

---

## 📚 Dependencies

See `requirements.txt`. Key libraries:

* `pandas==2.2.3`
* `google-play-scraper==1.2.7`
* `transformers==4.44.2`
* `gensim==4.3.3`
* `scikit-learn==1.5.2`
* `nltk==3.9.1`
* `pyLDAvis==3.4.1`
* `wordcloud==1.9.3`
* `oracledb==2.4.1`

---

## 📜 Git Workflow

* **Branch:** `task-2` for Task 2
* **Commits:** Scripts, notebooks, reports added
* **PR:** Merged `task-2` into `main`

---

## 3: Store Cleaned Data in Oracle

### 🎯 Objective
Store the processed reviews in an Oracle XE database to simulate enterprise data workflows.

### 🔍 Implementation
- **Setup**: Installed Oracle XE 21c via Docker (`container-registry.oracle.com/database/express:21.3.0-xe`).
- **Schema**:
  - `Banks`: Stores bank details (`bank_id`, `bank_name`) with 3 rows (CBE, BOA, Dashen).
  - `Reviews`: Stores reviews (`review_id`, `bank_id`, `review`, `rating`, `review_date`, `source`, `sentiment`, `confidence`, `theme`, `topic_probability`) with 1,087 rows.
- **Data Insertion**: Used `scripts/insert_data_oracle.py` with `oracledb` to load `data/processed/thematic_results.csv`.
- **SQL Dump**: Exported schema and data to `sql/bank_reviews.sql`

### ✅ KPIs Achieved
- Working Python connection and insert script (`insert_data_oracle.py`).
- `Reviews` table populated with 1,087 entries.
- SQL dump committed to GitHub.

### 📂 Outputs
- `scripts/insert_data_oracle.py`: Python script for data insertion.
- `sql/bank_reviews.sql`: Schema and bank data.

2. **4:** Build dashboard for stakeholder insights
