import unittest
from karaca import SentenceSpliter

class TestSentenceSpliter(unittest.TestCase):

    def test_split_sentences_basic(self):
        text = "Merhaba. Nasılsın? Ben iyiyim."
        expected = ["Merhaba.", "Nasılsın?", "Ben iyiyim."]
        self.assertEqual(SentenceSpliter().split_sentences(text), expected)

    def test_split_sentences_with_exclamations(self):
        text = "Bu harika! Gerçekten mi?"
        expected = ["Bu harika!", "Gerçekten mi?"]
        self.assertEqual(SentenceSpliter().split_sentences(text), expected)

    # Diğer test senaryoları...

if __name__ == '__main__':
    unittest.main()
