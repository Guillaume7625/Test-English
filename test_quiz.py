import unittest
from quiz_interactif import main_function

class TestQuizInteractif(unittest.TestCase):
    def test_main_function(self):
        result = main_function()
        self.assertEqual(result, "Hello, World!")  # Make sure the expected result is correct

if __name__ == '__main__':
    unittest.main()
