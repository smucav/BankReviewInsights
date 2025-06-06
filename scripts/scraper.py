from google_play_scraper import reviews
import pandas as pd
from datetime import datetime

class BankReviewScraper:
    def __init__(self, app_id, bank_name):
        self.app_id = app_id
        self.bank_name = bank_name

    def fetch_reviews(self, count):
        try:
            result, _ = reviews(
                self.app_id,
                lang='en',
                country='et',
                count=count,  # Target 400+ reviews per bank
                filter_score_with=None
            )
            # Check if result is empty
            if not result:
                raise ValueError("No reviews returned. Check app_id or API access.")
            # Convert to DataFrame and inspect columns
            df = pd.DataFrame(result)
            df = df[['content', 'score', 'at']]
            df.rename(columns={'content': 'review', 'score': 'rating', 'at': 'date'}, inplace=True)
            df['bank'] = self.bank_name
            df['source'] = 'Google Play'
            return df
        except Exception as e:
            print(f"Error fetching reviews: {e}")
            return None
