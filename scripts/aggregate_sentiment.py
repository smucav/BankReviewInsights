import pandas as pd
import os
import logging

class SentimentAggregator:
    def __init__(self, input_path: str, output_dir: str = "./data/processed"):
        self.input_path = input_path
        self.output_dir = output_dir
        self.expected_columns = ['review_id', 'review', 'rating', 'date', 'bank', 'source', 'sentiment', 'confidence']
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)
        os.makedirs(self.output_dir, exist_ok=True)

    def load_data(self) -> pd.DataFrame:
        try:
            df = pd.read_csv(self.input_path)
            missing_cols = [col for col in self.expected_columns if col not in df.columns]
            if missing_cols:
                self.logger.error(f"Missing columns: {missing_cols}")
                raise ValueError(f"Missing columns: {missing_cols}")
            self.logger.info(f"Loaded {len(df)} reviews from {self.input_path}")
            return df
        except Exception as e:
            self.logger.error(f"Error loading data: {e}")
            raise

    def aggregate_sentiment(self, df: pd.DataFrame) -> pd.DataFrame:
        try:
            # Mean confidence by bank, rating, and sentiment
            agg = df.groupby(['bank', 'rating', 'sentiment'])['confidence'].agg(['mean', 'count']).reset_index()
            agg.columns = ['bank', 'rating', 'sentiment', 'mean_confidence', 'review_count']
            self.logger.info(f"Aggregated sentiment:\n{agg}")
            return agg
        except Exception as e:
            self.logger.error(f"Error aggregating sentiment: {e}")
            raise

    def save_results(self, agg: pd.DataFrame):
        try:
            output_path = os.path.join(self.output_dir, 'sentiment_aggregates.csv')
            agg.to_csv(output_path, index=False)
            self.logger.info(f"Saved aggregates to {output_path}")
        except Exception as e:
            self.logger.error(f"Error saving aggregates: {e}")
            raise

    def run(self):
        df = self.load_data()
        agg = self.aggregate_sentiment(df)
        self.save_results(agg)
        return agg

if __name__ == "__main__":
    aggregator = SentimentAggregator(input_path="./data/processed/sentiment_results.csv")
    try:
        results = aggregator.run()
    except Exception as e:
        print(f"Error running sentiment aggregation: {e}")
