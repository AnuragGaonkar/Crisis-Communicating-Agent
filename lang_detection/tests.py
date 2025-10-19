import unittest
from detect import detect_language

class TestLangDetect(unittest.TestCase):
    def test_known_language(self):
        self.assertEqual(detect_language("This is an English text."), 'en')
    def test_unknown(self):
        self.assertEqual(detect_language(""), 'unknown')

if __name__ == '__main__':
    unittest.main()
