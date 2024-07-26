import unittest
from karaca import Normalize

class TestNormalize(unittest.TestCase):

    def test_normalize_with_numbers(self):
        self.assertEqual(Normalize.lower_text("Bugün 2 elma yedim."), "bugun 2 elma yedim.")

    def test_normalize_with_numbers(self):
        self.assertEqual(Normalize.upper_text("Bugün 2 elma yedim."), "BUGÜN 2 ELMA YEDİM.")

    def test_normalize_with_numbers(self):
        self.assertEqual(Normalize.remove_punc("Bugün 2 elma yedim."), "Bugün 2 elma yedim")

    def test_normalize_with_numbers(self):
        self.assertEqual(Normalize.remove_number("Bugün 2 elma yedim."), "Bugün 2 elma yedim.")

    def test_normalize_with_numbers(self):
        self.assertEqual(Normalize.word_counter("Bugün 2 elma yedim."), 4)

    def test_normalize_with_numbers(self):
        self.assertEqual(Normalize.sentence_counter("Bugün 2 elma yedim."), 1)

    def test_normalize_with_numbers(self):
        self.assertEqual(Normalize.find_idioms("El elden üstündür."), ["el elden üstündür"])

    def test_normalize_with_numbers(self):
        self.assertEqual(Normalize.remove_stopwords("Bir kaç elma yedim."), "elma yedim.")

    # Diğer test senaryoları...
    
if __name__ == '__main__':
    unittest.main()
