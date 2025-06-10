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

## 📦 Installation

```bash
git clone https://github.com/your-username/BankReviewInsights.git
cd BankReviewInsights
pip install -r requirements.txt
```
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

## 4: Insights and Recommendations

### 🎯 Objective

Derive insights from sentiment and themes, visualize results, and recommend app improvements for **CBE**, **BOA**, and **Dashen** mobile banking apps.

### 🔍 Implementation

Insights:
Drivers:

**Ease of Use (Positive User Experience):** Dashen (67%, 243 reviews, 4.91 avg. rating) and CBE (60%, 217 reviews, 4.81) **praised for intuitive navigation (e.g., “Best Mobile Banking app ever”).**

**Responsive Customer Service:** Dashen (8%, 29 reviews, 4.97) and CBE (3%, 11 reviews, 5.0) **noted for support (e.g., “better service”).**


### Pain Points:

**Login/Re-registration Issues (Technical Issues):** BOA (12%, 45 reviews, 1.13) and CBE (4%, 13 reviews, 1.77) **face login errors (e.g., “physical presence for every app install”).**

**Negative User Experience:** BOA (47%, 172 reviews, 1.16) and CBE (18%, 63 reviews, 1.57) suffer from general dissatisfaction.

### Bank Comparison:

**Dashen:** Highest satisfaction (67% positive, 4.91 avg. rating), minimal technical issues (2%).

**CBE:** Balanced (60% positive, ~3.0 avg. rating), with Feature Requests (e.g., Amharic support).

**BOA:** Lowest satisfaction (47% negative, 2.47 avg. rating), high technical issues (12%).


**Visualizations:** Created 7 plots using scripts/insights_analyzer.py with Matplotlib/Seaborn:


Sentiment trends over time (`sentiment_trends.png`)

Rating distributions by bank (`rating_distributions.png`)

Theme percentages by bank (`theme_percentages.png`)

Keyword clouds per bank (e.g., `keyword_cloud_dashen_bank.png`)

Sentiment distribution by bank (`sentiment_distribution.png`)

### Recommendations:

Streamline login/re-registration for BOA and CBE using implicit app source verification (e.g., Google Play).

Implement Amharic UI for CBE to address Feature Requests.
Improve BOA’s app stability via usability testing to reduce crashes.

**Ethics**:
* Negative skew: Reviews over-represent dissatisfied users (BOA: 47% negative).
* Language bias: Excluded Amharic reviews, missing local feedback.
* Platform bias: Google Play data excludes iOS or in-person feedback.

**Report**: Documented in `report/README.md`.

## ✅ KPIs Achieved

* **2+ drivers/pain points with evidence (4 total).**

* **7 clear, labeled visualizations.**

* **3 practical recommendations.**

## 📂 Outputs
```
scripts/insights_analyzer.py: Analysis and visualization script.

plots/figures/: 7 plots.
```
- `report/README.md`: Insights, recommendations, and ethics.

- `requirements.txt`: Updated with matplotlib==3.9.2, seaborn==0.13.2, wordcloud==1.9.3.

## 📦 Usage
```
python scripts/insights_analyzer.py
cat task4_report.md
sqlplus bank_reviews/Welcome123@127.0.0.1:1521/XEPDB1
SELECT bank_name, COUNT(*) FROM Banks b JOIN Reviews r ON b.bank_id = r.bank_id GROUP BY bank_name;
```

## 🗃️ Directory Structure
```
BankReviewInsights/
├── data/
│   ├── raw/                  # Raw review CSVs
│   ├── processed/            # Cleaned & analyzed data
│   └── dumps/                # SQL dumps (bank_reviews.sql)
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
│   ├── keyword_extractor.py
│   ├── insert_data_oracle.py
│   └── insights_analyzer.py
├── plots/
│   └── figures/              # PNG visuals
├── reports/
│   ├── interim_report.tex
│   ├── interim_report.pdf
│   └── task4_report.md
├── tests/                    # (Coming soon)
├── requirements.txt
├── README.md
```


## 📦 Installation

```
git clone https://github.com/your-username/BankReviewInsights.git
cd BankReviewInsights
pip install -r requirements.txt
```


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

# Store in Oracle
python scripts/insert_data_oracle.py

# Insights and Recommendations
python scripts/insights_analyzer.py

# EDA
jupyter notebook notebooks/eda_themes.ipynb
```

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
* `matplotlib==3.9.2`
* `seaborn==0.13.2`
---

## 📜 Git Workflow

* **Branches:** `task-1`, `task-2`, `task-3`, `task-4`

* **Commits:** Scripts, notebooks, SQL dumps, visuals, and reports added

* **Pull Requests:** Merged `task-1`, `task-2`, `task-3`, `task-4` into `main`

## 🧪 Tests

Unit tests for the project are located in the `tests/` directory, implemented using Python's `unittest` framework. Tests cover key functionalities, such as data preprocessing, sentiment analysis, and visualization generation, ensuring code reliability and correctness. Run tests with:

```bash
python -m unittest discover tests
```
## 🔮 Next Steps

Future: Optimize database queries, enhance AI-driven insights, and explore iOS reviews.
