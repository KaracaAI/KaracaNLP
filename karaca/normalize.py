from typing import List, Set, Union, Dict, Optional
from pathlib import Path
import re
import os
import warnings
from collections import Counter
import pickle
import string

karaca_path = os.path.dirname(os.path.abspath(__file__))
STOP_WORDS = str(Path(__file__).parent / "datas/stop_words.txt")
CHAR_FILE = str(Path(__file__).parent / "datas/ascii.pkl")
class Deasciifier:
    context_size = 10
    def __init__(self, input_string):
        with open(CHAR_FILE, "rb") as file:
            pattern_table = pickle.load(file)
        del file
        self.pattern_table = pattern_table
        self.input_string = input_string
        self.converted_string = input_string
        self.asciify_table = {
            "ç": "c",
            "Ç": "C",
            "ğ": "g",
            "Ğ": "G",
            "ö": "o",
            "Ö": "O",
            "ü": "u",
            "Ü": "U",
            "ı": "i",
            "İ": "I",
            "ş": "s",
            "Ş": "S",
        }
        self.turkish_downcase_asciify_table = {
            **{ch: ch.lower() for ch in string.ascii_uppercase},
            **{ch.lower(): ch.lower() for ch in string.ascii_uppercase},
            "ç": "c",
            "Ç": "c",
            "ğ": "g",
            "Ğ": "g",
            "ö": "o",
            "Ö": "o",
            "ü": "u",
            "Ü": "u",
            "ı": "i",
            "İ": "i",
            "ş": "s",
            "Ş": "s",
        }
        self.turkish_upcase_accents_table = {
            **{ch: ch.lower() for ch in string.ascii_uppercase},
            **{ch.lower(): ch.lower() for ch in string.ascii_uppercase},
            "ç": "C",
            "Ç": "C",
            "ğ": "G",
            "Ğ": "G",
            "ö": "O",
            "Ö": "O",
            "ü": "U",
            "Ü": "U",
            "ı": "I",
            "İ": "I",
            "ş": "S",
            "Ş": "S",
        }

    def set_char_at(self, str, position, char):
        return str[0:position] + char + str[position + 1 :]

    def convert_to_turkish(self):
        for index in range(len(self.converted_string)):
            char = self.converted_string[index]
            if self.turkish_need_correction(char, point=index):
                self.converted_string = self.set_char_at(self.converted_string, index, self.turkish_toggle_accent(char))
            else:
                self.converted_string = self.set_char_at(self.converted_string, index, char)

        return self.converted_string

    def turkish_toggle_accent(self, c):
        turkish_toggle_accent_table = {
            "c": "ç",
            "C": "Ç",
            "g": "ğ",
            "G": "Ğ",
            "o": "ö",
            "O": "Ö",
            "u": "ü",
            "U": "Ü",
            "i": "ı",
            "I": "İ",
            "s": "ş",
            "S": "Ş",
            "ç": "c",
            "Ç": "C",
            "ğ": "g",
            "Ğ": "G",
            "ö": "o",
            "Ö": "O",
            "ü": "u",
            "Ü": "U",
            "ı": "i",
            "İ": "I",
            "ş": "s",
            "Ş": "S",
        }
        return turkish_toggle_accent_table.get(c, c)

    def turkish_need_correction(self, char, point=0):
        ch = char
        tr = self.asciify_table.get(ch, ch)
        pl = self.pattern_table.get(tr.lower(), False)
        if pl != False:
            m = self.turkish_match_pattern(pl, point)
        else:
            m = False

        if tr == "I":
            if ch == tr:
                return not m
            else:
                return m
        else:
            if ch == tr:
                return m
            else:
                return not m

    def turkish_match_pattern(self, dlist, point=0):
        rank = 2 * len(dlist)
        str = self.turkish_get_context(Deasciifier.context_size, point=point)
        start = 0
        end = 0

        _len = len(str)
        while start <= Deasciifier.context_size:
            end = 1 + Deasciifier.context_size
            while end <= _len:
                context = str[start:end]
                r = dlist.get(context, False)
                if r and abs(r) < abs(rank):
                    rank = r
                end = 1 + end
            start = 1 + start

        return rank > 0

    def turkish_get_context(self, size=context_size, point=0):
        context = " " * (1 + (2 * size))
        context = context[0:size] + "X" + context[size + 1 :]
        i = 1 + size
        space = False
        index = point
        current_char = self.converted_string[index]

        index = index + 1

        while i < len(context) and not space and index < len(self.input_string):
            current_char = self.converted_string[index]
            x = self.turkish_downcase_asciify_table.get(current_char, False)
            if not x:
                if not space:
                    i = i + 1
                    space = True
            else:
                context = context[0:i] + x + context[i + 1 :]
                i = i + 1
                space = False
            index = index + 1

        context = context[0:i]

        index = point
        i = size - 1
        space = False

        index = index - 1
        while i >= 0 and index >= 0:
            current_char = self.converted_string[index]
            x = self.turkish_upcase_accents_table.get(current_char, False)
            if not x:
                if not space:
                    i = i - 1
                    space = True
            else:
                context = context[0:i] + x + context[i + 1 :]
                i = i - 1
                space = False
            index = index - 1

        return context


class Normalize:
    stpwrd = None
    def __init__(self):
        self.name = "Normalize"
        
    @classmethod
    def remove_stopwords(cls, text: str, stopwords: Union[Set[str], List[str]] = None) -> str:
        if stopwords is None:
            cls.load_stopwords(STOP_WORDS)
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
        return text.lower()

    @classmethod
    def upper_text(cls, text: str) -> str:
        return text.upper()

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
    def asciify(cls, text, charTable=None):
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
    def deasciify(cls, text: List[str]) -> List[str]:
        deasciify = Deasciifier(text)
        text = deasciify.convert()
        return text
