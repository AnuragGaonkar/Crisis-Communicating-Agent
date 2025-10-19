import unittest
from detect import MisinformationDetector

class TestMisinformationDetector(unittest.TestCase):
    def setUp(self):
        self.detector = MisinformationDetector()
    
    def test_untrained_predict(self):
        with self.assertRaises(ValueError):
            self.detector.predict("Test text")

    def test_train_and_predict(self):
        texts = ["This is true information", "Fake news alert"]
        labels = [0, 1]  
        self.detector.train(texts, labels)
        prediction = self.detector.predict("Fake news alert")
        self.assertEqual(prediction, 1)

if __name__ == '__main__':
    unittest.main()
