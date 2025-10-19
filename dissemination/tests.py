import unittest
from distribute import DisseminationSystem

class TestDisseminationSystem(unittest.TestCase):
    def setUp(self):
        self.system = DisseminationSystem()

    def test_distribute_valid_channel(self):
        result = self.system.distribute("Test message", "email")
        self.assertIn("Message sent via email", result)

    def test_distribute_invalid_channel(self):
        with self.assertRaises(ValueError):
            self.system.distribute("Test message", "fax")

if __name__ == '__main__':
    unittest.main()
