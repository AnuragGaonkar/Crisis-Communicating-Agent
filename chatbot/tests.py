import unittest
from bot import CrisisChatbot

class TestCrisisChatbot(unittest.TestCase):
    def setUp(self):
        self.chatbot = CrisisChatbot()

    def test_get_response(self):
        response = self.chatbot.get_response("What should I do during a flood?")
        self.assertTrue(isinstance(response, str))
        self.assertTrue(len(response) > 0)

if __name__ == '__main__':
    unittest.main()
