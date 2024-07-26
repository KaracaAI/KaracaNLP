import unittest
from karaca import Emotion

class TestEmotion(unittest.TestCase):

    def test_guess_happiness(self):
        self.assertEqual(Emotion.guess("Harika bir gün!"), "Tahmin Edilen Duygu: joy % 94.61")

    def test_guess_sadness(self):
        self.assertEqual(Emotion.guess("Bugün çok üzgünüm."), "Tahmin Edilen Duygu: sadness % 93.07")

    # Diğer test senaryoları...

if __name__ == '__main__':
    unittest.main()
