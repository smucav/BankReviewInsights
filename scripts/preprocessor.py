import pandas as pd
import re

class ReviewPreprocessor:
    def __init__(self, df: pd.DataFrame):
        self.df = df



    def is_ascii_english(self, text, min_english_chars=0.6, min_alpha_words=2):
        if not isinstance(text, str):
            return False

        text = text.strip()
        if not text:
            return False

        ascii_chars = sum(1 for c in text if ord(c) < 128)
        ratio = ascii_chars / len(text)

        # Require at least X% ASCII characters
        if ratio < min_english_chars:
            return False

        # Require some alphabetic words
        words = re.findall(r'\b[a-zA-Z]{3,}\b', text)
        return len(words) >= min_alpha_words


    def clean(self):
        initial_count = len(self.df)
        self.df.drop_duplicates(subset=['review', 'date', 'bank'], inplace=True)
        self.df.dropna(subset=['review', 'rating', 'date'], inplace=True)
        self.df['date'] = pd.to_datetime(self.df['date']).dt.date

        self.df['is_english'] = self.df['review'].apply(self.is_ascii_english)
        self.df = self.df[self.df['is_english']].drop(columns=['is_english'])

        final_count = len(self.df)
        print(f"Dropped {initial_count - final_count} rows ({(initial_count - final_count)/initial_count*100:.2f}%)")
        return self.df
