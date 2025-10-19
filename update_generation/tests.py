import unittest
from generate import UpdateGenerator

class TestUpdateGenerator(unittest.TestCase):
    def setUp(self):
        self.generator = UpdateGenerator()

    def test_generate_update(self):
        input_text = ("The government has announced new measures to control the spread of the virus. "
                      "Vaccination drives are being expedited across states.")
        result = self.generator.generate_update(input_text)
        self.assertGreater(len(result) > 0)

    def test_cultural_adapt(self):
        text = "Stay safe and follow guidelines."
        culture_info = "India"
        adapted = self.generator.cultural_adapt(text, culture_info)
        self.assertIn(culture_info, adapted)

if __name__ == '__main__':
    unittest.main()
