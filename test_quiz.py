import unittest
from quiz_interactif import main_function  # Assurez-vous que cette importation correspond à votre script

class TestQuizInteractif(unittest.TestCase):
    def test_main_function(self):
        result = main_function()
        self.assertEqual(result, "Hello, World!")  # Assurez-vous que le résultat attendu est correct

if __name__ == '__main__':
    unittest.main()
