import unittest
from analyze import SentimentAnalyzer

class TestSentimentAnalyzer(unittest.TestCase):
    def setUp(self):
        self.analyzer = SentimentAnalyzer()

    def test_positive_sentiment(self):
        result = self.analyzer.analyze_sentiment("I love this product!")
        self.assertEqual(result["sentiment"], "positive")

    def test_negative_sentiment(self):
        result = self.analyzer.analyze_sentiment("This is terrible.")
        self.assertEqual(result["sentiment"], "negative")

    def test_neutral_sentiment(self):
        result = self.analyzer.analyze_sentiment("It is a book.")
        self.assertEqual(result["sentiment"], "neutral")

if __name__ == '__main__':
    unittest.main()
