from typing import List, Set, Union
from pathlib import Path
import re
import os
import warnings
from collections import Counter


stop_words = str(Path(__file__).parent / "datas/stop_words.txt")
karaca_path = os.path.dirname(os.path.abspath(__file__))
class Normalize:
    stpwrd = None
    def __init__(self):
        self.name = "Normalize"
        
    @classmethod
    def remove_stopwords(cls, text: str, stopwords: Union[Set[str], List[str]] = None) -> str:
        if stopwords is None:
            cls.load_stopwords(stop_words)
            stopwords = cls.stpwrd
        elif isinstance(stopwords, list):
            stopwords = set(stopwords)

        cleaned_text = " ".join(word for word in text.split() if word.lower() not in stopwords)
        return cleaned_text

    @classmethod
    def load_stopwords(cls, stWordSource: Union[str, Set[str], List[str]]) -> None:
        if isinstance(stWordSource, str):
            with open(stWordSource, "r", encoding="utf-8") as f:
                cls.stpwrd = set(f.read().split())
        elif isinstance(stWordSource, (set, list)):
            cls.stpwrd = set(stWordSource)
        else:
            raise ValueError(
                "stWordSource must be a path to a file (str), a set of words (set), or a list of words (list)."
            )

    @classmethod
    def lower_text(cls, text: str) -> str:
        replacements = str.maketrans("IİĞÜŞÖÇ", "ıiğüşöç")
        return text.translate(replacements).lower()

    @classmethod
    def upper_text(cls, text: str) -> str:
        replacements = str.maketrans("ıiğüşöç", "IİĞÜŞÖÇ")
        return text.translate(replacements).upper()

    @classmethod
    def remove_punc(cls, text: str) -> str:
        text = re.sub(r'[^\w\s]', '', text)
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
        
    @classmethod
    def remove_number(cls, text,signed=True,decimal=True):
        if signed and decimal:
            pattern = r"(?<!\d)[-+]?\d*\.?\d+(?!\d)"
        elif signed:
            pattern = r"(?<!\d)[-+]?\d+(?!\d)"
        elif decimal:
            pattern = r"\d*\.?\d+"
        else:
            pattern = r"\d+"

        text = re.sub(pattern, "", text)

        text = re.sub(r"\s*,\s*", " ", text)
        text = re.sub(r"\s+", " ", text)

        text = re.sub(r"^,", "", text).strip()

        return text

    @classmethod
    def normalize_chars(cls, text, charTable=None):
        if charTable is None:
            charTable = str.maketrans("ğĞıİöÖüÜşŞçÇ", "gGiIoOuUsScC")

        text = text.translate(charTable)
        return text

    @classmethod
    def word_counter(cls, cumle):
        cumle = re.sub(r'[^\w\s]', ' ', cumle)
        kelimeler = cumle.split()
        return len(kelimeler)

    @classmethod
    def sentence_counter(cls, paragraf):
        cumleler = re.split(r'[.!?]', paragraf)
        cumleler = [cumle.strip() for cumle in cumleler if cumle.strip()]
        return len(cumleler)

    @classmethod
    def find_idioms(cls, text):
        text = Normalize.lower_text(text)
        def loadIdioms():
            idiomsFile = karaca_path + '/datas/idioms.txt'
            with open(idiomsFile, 'r', encoding='utf-8') as file:
                idiomsR = file.read().splitlines()
            return idiomsR
        datas = loadIdioms()
        idioms = [idiom for idiom in datas if idiom in text]

        return idioms
