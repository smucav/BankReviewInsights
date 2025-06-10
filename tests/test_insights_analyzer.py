import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
import os
from datetime import datetime
from scripts.insights_analyzer import ReviewAnalyzer

class TestReviewAnalyzer(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures."""
        self.dsn = "localhost:1521/XEPDB1"
        self.username = "bank_reviews"
        self.password = "Welcome123"
        self.output_dir = "test_plots"
        self.analyzer = ReviewAnalyzer(self.dsn, self.username, self.password, self.output_dir)

        # Sample DataFrame mimicking database output
        self.sample_data = pd.DataFrame({
            'BANK_NAME': ['CBE', 'BOA', 'Dashen'],
            'REVIEW_ID': [1, 2, 3],
            'REVIEW': [
                "Best app ever",
                "Login error",
                "Great service"
            ],
            'RATING': [5.0, 1.0, 4.0],
            'REVIEW_DATE': [
                pd.Timestamp('2025-06-04'),
                pd.Timestamp('2025-06-04'),
                pd.Timestamp('2025-06-04')
            ],
            'SOURCE': ['Google Play'] * 3,
            'SENTIMENT': ['positive', 'negative', 'positive'],
            'CONFIDENCE': [0.99, 0.99, 0.98],
            'THEME': ['Positive User Experience', 'Technical Issues', 'Customer Service'],
            'TOPIC_PROBABILITY': [0.99, 0.99, 0.98]
        })

    def tearDown(self):
        """Clean up test output directory."""
        if os.path.exists(self.output_dir):
            for file in os.listdir(self.output_dir):
                os.remove(os.path.join(self.output_dir, file))
            os.rmdir(self.output_dir)

    @patch('oracledb.connect')
    @patch('pandas.read_sql')
    def test_fetch_data_success(self, mock_read_sql, mock_connect):
        """Test successful data fetching from Oracle."""
        mock_conn = MagicMock()
        mock_connect.return_value.__enter__.return_value = mock_conn
        mock_read_sql.return_value = self.sample_data

        result = self.analyzer.fetch_data()
        self.assertTrue(result)
        self.assertIsNotNone(self.analyzer.df)
        self.assertEqual(len(self.analyzer.df), 3)
        mock_read_sql.assert_called_once()

    @patch('oracledb.connect')
    def test_fetch_data_failure(self, mock_connect):
        """Test data fetching failure due to Oracle error."""
        mock_connect.side_effect = Exception("Connection failed")
        result = self.analyzer.fetch_data()
        self.assertFalse(result)
        self.assertIsNone(self.analyzer.df)

    @patch('matplotlib.pyplot.savefig')
    @patch('matplotlib.pyplot.close')
    def test_plot_sentiment_trends(self, mock_close, mock_savefig):
        """Test sentiment trends plot generation."""
        self.analyzer.df = self.sample_data.copy()
        self.analyzer._plot_sentiment_trends()
        mock_savefig.assert_called_once_with(os.path.join(self.output_dir, 'sentiment_trends.png'))
        mock_close.assert_called_once()

    @patch('seaborn.boxplot')
    @patch('matplotlib.pyplot.savefig')
    @patch('matplotlib.pyplot.close')
    def test_plot_rating_distributions(self, mock_close, mock_savefig, mock_boxplot):
        """Test rating distributions plot generation."""
        self.analyzer.df = self.sample_data.copy()
        self.analyzer._plot_rating_distributions()
        mock_boxplot.assert_called_once()
        mock_savefig.assert_called_once_with(os.path.join(self.output_dir, 'rating_distributions.png'))
        mock_close.assert_called_once()

    @patch('matplotlib.pyplot.savefig')
    @patch('matplotlib.pyplot.close')
    def test_plot_theme_percentages(self, mock_close, mock_savefig):
        """Test theme percentages plot generation."""
        self.analyzer.df = self.sample_data.copy()
        self.analyzer._plot_theme_percentages()
        mock_savefig.assert_called_once_with(os.path.join(self.output_dir, 'theme_percentages.png'))
        mock_close.assert_called_once()

    @patch('wordcloud.WordCloud')
    @patch('matplotlib.pyplot.savefig')
    @patch('matplotlib.pyplot.close')
    def test_plot_keyword_clouds(self, mock_close, mock_savefig, mock_wordcloud):
        """Test keyword clouds generation for each bank."""
        mock_wc_instance = MagicMock()
        mock_wordcloud.return_value = mock_wc_instance
        self.analyzer.df = self.sample_data.copy()
        self.analyzer._plot_keyword_clouds()
        self.assertEqual(mock_savefig.call_count, 3)  # One per bank
        expected_calls = [
            os.path.join(self.output_dir, 'keyword_cloud_cbe.png'),
            os.path.join(self.output_dir, 'keyword_cloud_boa.png'),
            os.path.join(self.output_dir, 'keyword_cloud_dashen.png')
        ]
        actual_calls = [call[0][0] for call in mock_savefig.call_args_list]
        for expected in expected_calls:
            self.assertIn(expected, actual_calls)
        self.assertEqual(mock_close.call_count, 3)

    @patch('seaborn.countplot')
    @patch('matplotlib.pyplot.savefig')
    @patch('matplotlib.pyplot.close')
    def test_plot_sentiment_distribution(self, mock_close, mock_savefig, mock_countplot):
        """Test sentiment distribution plot generation."""
        self.analyzer.df = self.sample_data.copy()
        self.analyzer._plot_sentiment()
        mock_countplot.assert_called_once()
        mock_savefig.assert_called_once_with(os.path.join(self.output_dir, 'sentiment_distribution.png'))
        mock_close.assert_called_once()

    @patch('pandas.DataFrame.to_csv')
    def test_run_analysis_saves_data(self, mock_to_csv):
        """Test run_analysis saves processed data to CSV."""
        self.analyzer.df = self.sample_data.copy()
        self.analyzer.run_analysis()
        mock_to_csv.assert_called_once_with('data/processed/task4_data.csv', index=False)

    def test_run_analysis_no_data(self):
        """Test run_analysis handles missing data."""
        self.analyzer.df = None
        with self.assertLogs(level='INFO') as log:
            self.analyzer.run_analysis()
            self.assertIn("Data not found", log.output[0])

if __name__ == '__main__':
    unittest.main()
