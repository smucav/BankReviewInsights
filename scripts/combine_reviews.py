
import pandas as pd
import os

class ReviewCombiner:
    def __init__(self, data_dir: str, bank_files: list):
        self.data_dir = data_dir
        self.bank_files = bank_files
        self.expected_columns = ['review_id', 'review', 'rating', 'date', 'bank', 'source']

    def combine(self) -> pd.DataFrame:
        dfs = []
        for bank_file in self.bank_files:
            file_path = os.path.join(self.data_dir, bank_file)
            if not os.path.exists(file_path):
                print(f"Warning: {file_path} not found")
                continue
            df = pd.read_csv(file_path)
            dfs.append(df)

        # Combine and add review_id
        all_reviews = pd.concat(dfs, ignore_index=True)
        all_reviews['review_id'] = range(1, len(all_reviews) + 1)
        # Ensure expected columns
        all_reviews = all_reviews[[col for col in self.expected_columns if col in all_reviews.columns]]

        # Save combined CSV
        output_path = os.path.join(self.data_dir, 'all_reviews.csv')
        all_reviews.to_csv(output_path, index=False)
        print(f"Combined {len(all_reviews)} reviews into {output_path}")
        return all_reviews

if __name__ == "__main__":
    combiner = ReviewCombiner(
        data_dir="data/processed/",
        bank_files=['cbe_reviews.csv', 'boa_reviews.csv', 'dashen_reviews.csv']
    )
    all_reviews = combiner.combine()
