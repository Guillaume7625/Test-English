import unittest
from quiz_interactif import main_function  # Assurez-vous que cette importation correspond à votre script

class TestQuizInteractif(unittest.TestCase):
    def test_main_function(self):
        result = main_function()
        self.assertEqual(result, expected_result)  # Remplacez expected_result par la valeur attendue

if __name__ == '__main__':
    unittest.main()
