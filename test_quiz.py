import unittest
from quiz_interactif import main

class TestQuizInteractif(unittest.TestCase):
    def test_main_function(self):
        result = main()
        self.assertEqual(result, "Hello, World!")  # Make sure the expected result is correct

if __name__ == '__main__':
    unittest.main()
