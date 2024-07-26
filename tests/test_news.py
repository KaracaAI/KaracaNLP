import unittest
from karaca import News

class TestNews(unittest.TestCase):

    def test_guess_politics(self):
        self.assertEqual(News.guess("Yeni Windows açığı kapatıldı"), "Tahmin Edilen konu: technology % 77.67")

    def test_guess_sports(self):
        self.assertEqual(News.guess("Galatasaray maçı kazandı."), "Tahmin Edilen konu: sport % 78.80")

    def test_guess_entertainment(self):
        self.assertEqual(News.guess("Kansere yeni bir tedavi bulundu."), "Tahmin Edilen konu: health % 84.30")

    # Diğer test senaryoları...

if __name__ == '__main__':
    unittest.main()
