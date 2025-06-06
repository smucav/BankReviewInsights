# 📊 BankReviewInsights
### *Customer Experience Analytics for Fintech Apps*

## 🧾 Overview
**BankReviewInsights** is a data analytics project focused on understanding customer sentiment and experience for mobile banking apps of three major Ethiopian banks:

- **Commercial Bank of Ethiopia (CBE)**
- **Bank of Abyssinia (BOA)**
- **Dashen Bank**

This project is part of the Omega Consultancy challenge and involves scraping Google Play Store reviews, preprocessing and analyzing the text data, and generating actionable insights.

---

## 1: Data Collection & Preprocessing

### 🎯 Objective
Scrape and clean Google Play Store reviews for the official apps of CBE, BOA, and Dashen Bank.

### 🔍 Scraping Details
Reviews were scraped using the [`google-play-scraper`](https://github.com/damiengo/google-play-scraper) package.

**App IDs:**

- **CBE**: `com.combanketh.mobilebanking` – *550 raw*, *360 processed*
- **BOA**: `com.boa.boaMobileBanking` – *540 raw*, *366 processed*
- **Dashen**: `com.dashen.dashensuperapp` – *448 raw*, *361 processed*

**Total Processed Reviews:** 1,087
**Columns in dataset:** `review`, `rating`, `date`, `bank`, `source`

---

### 🧹 Preprocessing
Implemented in the `ReviewPreprocessor` class (`scripts/preprocessor.py`):

- Removed duplicates based on review text, date, and bank
- Dropped rows with missing review, rating, or date (0% missing post-cleaning)
- Filtered non-English reviews: retained reviews with ≥60% ASCII characters and ≥2 alphabetic words
- Normalized dates to `YYYY-MM-DD` format

**Drop Rates:**

- **CBE:** 34.55%
- **BOA:** ~32%
- **Dashen:** 19.42%

---

### 📊 Exploratory Data Analysis (EDA)

EDA was conducted for each bank to understand customer feedback patterns:

- Rating distributions
- Monthly review volumes
- Review length histograms
- Word clouds of common terms

**EDA Notebooks:**

- `notebooks/eda_cbe.ipynb`
- `notebooks/eda_boa.ipynb`
- `notebooks/eda_dashen.ipynb`

**Example (BOA):**

- Reviews: 366
- Average Rating: 2.47
- Date Range: May 13, 2024 – June 3, 2025

---

## 🗃️ Directory Structure
```
BankReviewInsights/
├── data/
│ ├── raw/ # Unprocessed review data (CSV)
│ └── processed/ # Cleaned and filtered reviews (CSV)
├── notebooks/
│ ├── scrape_reviews_cbe.ipynb
│ ├── scrape_reviews_boa.ipynb
│ ├── scrape_reviews_dashen.ipynb
│ ├── eda_cbe.ipynb
│ ├── eda_boa.ipynb
│ └── eda_dashen.ipynb
├── scripts/
│ ├── scraper.py # Review scraper (BankReviewScraper class)
│ ├── preprocessor.py # Preprocessor (ReviewPreprocessor class)
│ └── combine_reviews.py # Combines individual review files
├── reports/ # Reports and visualizations (to be added)
├── tests/ # Unit tests for scripts (coming soon)
├── requirements.txt # Required Python packages
├── README.md # Project overview (this file)
```

## 📦 Installation

```bash
git clone https://github.com/your-username/BankReviewInsights.git
cd BankReviewInsights
pip install -r requirements.txt
```
