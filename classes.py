import pickle
import string
from typing import List, Optional, Dict, Set, Union, Tuple
from pathlib import Path
import re
import zeyrek
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
import nltk
charFile = str(Path(__file__).parent / "turkishChar.pkl")
ST_WR_PATH = str(Path(__file__).parent / "txt/stop_words.txt")
BW_WR_PATH = str(Path(__file__).parent / "kufur.txt")
PATH = str(Path(__file__).parent / "TR_non_breaking_prefixes.txt")

class Deasciifier:


    def __init__(self, ascii_string: str):
        self.ascii_string = ascii_string
        self.converted_string = ascii_string

        # Türkçe ASCII tablosunu yükleme
        try:
            with open(charFile, "rb") as file:
                self.turkish_pattern_table = pickle.load(file)
        except FileNotFoundError:
            raise RuntimeError(f"Character file {charFile} not found.")
        except pickle.PickleError:
            raise RuntimeError(f"Error occurred while loading the character file {charFile}.")

        # Türkçe karakter dönüştürme tabloları
        self.turkish_asciify_table = {
            "ç": "c", "Ç": "C", "ğ": "g", "Ğ": "G", "ö": "o", "Ö": "O",
            "ü": "u", "Ü": "U", "ı": "i", "İ": "I", "ş": "s", "Ş": "S",
        }
        self.turkish_downcase_asciify_table = {
            **{ch: ch.lower() for ch in string.ascii_uppercase},
            **{ch.lower(): ch.lower() for ch in string.ascii_uppercase},
            **self.turkish_asciify_table
        }
        self.turkish_upcase_accents_table = {
            **{ch: ch.lower() for ch in string.ascii_uppercase},
            **{ch.lower(): ch.lower() for ch in string.ascii_uppercase},
            **{k: v.upper() for k, v in self.turkish_asciify_table.items()}
        }

    def set_char_at(self, string: str, position: int, char: str) -> str:
        return string[:position] + char + string[position + 1:]

    def convert_to_turkish(self) -> str:
        result = []
        for index, char in enumerate(self.converted_string):
            if self.turkish_need_correction(char, index):
                result.append(self.turkish_toggle_accent(char))
            else:
                result.append(char)
        return ''.join(result)

    def turkish_toggle_accent(self, c: str) -> str:
        turkish_toggle_accent_table = {
            "c": "ç", "C": "Ç", "g": "ğ", "G": "Ğ", "o": "ö", "O": "Ö",
            "u": "ü", "U": "Ü", "i": "ı", "I": "İ", "s": "ş", "S": "Ş",
            "ç": "c", "Ç": "C", "ğ": "g", "Ğ": "G", "ö": "o", "Ö": "O",
            "ü": "u", "Ü": "U", "ı": "i", "İ": "I", "ş": "s", "Ş": "S",
        }
        return turkish_toggle_accent_table.get(c, c)

    def turkish_need_correction(self, char: str, point: int) -> bool:
        ch = char
        tr = self.turkish_asciify_table.get(ch, ch)
        pl = self.turkish_pattern_table.get(tr.lower())
        if pl is not None:
            m = self.turkish_match_pattern(pl, point)
        else:
            m = False

        if tr == "I":
            return not m if ch == tr else m
        else:
            return m if ch == tr else not m

    def turkish_match_pattern(self, dlist: Dict[str, int], point: int) -> bool:
        context_size = 10
        rank = 2 * len(dlist)
        context = self.turkish_get_context(self.context_size, point)
        _len = len(context)

        for start in range(self.context_size + 1):
            end = start + self.context_size + 1
            while end <= _len:
                s = context[start:end]
                r = dlist.get(s)
                if r and abs(r) < abs(rank):
                    rank = r
                end += 1

        return rank > 0

    def turkish_get_context(self, size: int, point: int) -> str:
        left_context = " " * size
        right_context = " " * size

        left_index = point - 1
        right_index = point + 1

        while len(left_context) < size and left_index >= 0:
            char = self.converted_string[left_index]
            x = self.turkish_upcase_accents_table.get(char, char)
            left_context = x + left_context
            left_index -= 1

        while len(right_context) < size and right_index < len(self.converted_string):
            char = self.converted_string[right_index]
            x = self.turkish_downcase_asciify_table.get(char, char)
            right_context += x
            right_index += 1

        return left_context + self.converted_string[point] + right_context[:size]


class Normalize:
    STOP_WORDS = None
    def convert_group(number: int, ones: list, tens: list) -> str:
        word = ""
        if number >= 100:
            if number // 100 != 1:
                word += ones[number // 100] + " yüz"
            else:
                word += "yüz"
            number = number % 100
        if number >= 10:
            word += " " + tens[number // 10 - 1]
            number = number % 10
        if number > 0:
            word += " " + ones[number]
        return word.strip()
    def numberToWord(number: int) -> str:
        negative_expression = None
        if int(number) < 0:
            number = str(number).split("-")[1]
            negative_expression = "eksi"
            number = int(number)
        ones = ["sıfır", "bir", "iki", "üç", "dört", "beş", "altı", "yedi", "sekiz", "dokuz"]
        tens = ["on", "yirmi", "otuz", "kırk", "elli", "altmış", "yetmiş", "seksen", "doksan"]
        scales = ["", "bin", "milyon", "milyar", "trilyon", "katrilyon", "kentilyon", "Sekstilyon", "Septilyon", "Oktilyon", "Nonilyon", "Desilyon", "Undesilyon", "Dodesilyon", "Tredesilyon", "Katordesilyon", "Kendesilyon", "Seksdesilyon", "Septendesilyon", "Oktodesilyon", "Novemdesilyon", "Vigintilyon"]
        word = ""

        if number == 0:
            return ones[0]

        group = 0
        while number > 0:
            number, remainder = divmod(number, 1000)
            if remainder > 0:
                group_description = Normalize.convert_group(remainder, ones, tens)
                if group > 0:
                    group_description += " " + scales[group]
                ne = " " if negative_expression is None else f"{negative_expression}"
                word = " " + group_description + word
            group += 1

        return ne+word
    @classmethod
    def remove_stopwords(cls, text: str, stopwords: Union[Set[str], List[str]] = None) -> str:
        if stopwords is None:
            cls.load_stopwords(ST_WR_PATH)
            stopwords = cls.STOP_WORDS
        elif isinstance(stopwords, list):
            stopwords = set(stopwords)

        cleaned_text = " ".join(word for word in text.split() if word.lower() not in stopwords)
        return cleaned_text
    @classmethod
    def remove_bad_words(cls, text: str, stopwords: Union[Set[str], List[str]] = None) -> str:
        if stopwords is None:
            cls.load_stopwords(BW_WR_PATH)  # Replace with your actual stopwords file path
            stopwords = cls.STOP_WORDS
        elif isinstance(stopwords, list):
            stopwords = set(stopwords)

        # Sort stopwords by length (longest first) to avoid partial matches
        sorted_stopwords = sorted(stopwords, key=len, reverse=True)
        
        # Create a regex pattern to match all stopwords
        pattern = re.compile(r'\b(?:' + '|'.join(re.escape(word) for word in sorted_stopwords) + r')\b', re.IGNORECASE)
        
        # Find all matches to count the removed stopwords
        matches = pattern.findall(text)
        num_removed = len(matches)
        
        # Remove all stopwords from text
        cleaned_text = pattern.sub('', text)
        
        # Normalize spaces
        cleaned_text = re.sub(' +', ' ', cleaned_text).strip()

        return cleaned_text, num_removed

    @classmethod
    def load_stopwords(cls, stop_words_source: Union[str, Set[str], List[str]]) -> None:
        if isinstance(stop_words_source, str):
            with open(stop_words_source, "r", encoding="utf-8") as f:
                cls.STOP_WORDS = set(f.read().split())
        elif isinstance(stop_words_source, (set, list)):
            cls.STOP_WORDS = set(stop_words_source)
        else:
            raise ValueError(
                "stop_words_source must be a path to a file (str), a set of words (set), or a list of words (list)."
            )
class SentenceSplitter:
    def __init__(self) -> None:
        with open(PATH, "r", encoding="utf-8") as file:
            self.non_breaking_prefixes_tr = file.read().splitlines()
        self.prefix_pattern = r"(?:^|\s)(" + "|".join(self.non_breaking_prefixes_tr) + r")\."

    def split_sentences(self, text: str) -> List[str]:
        text = re.sub(self.prefix_pattern, r"\1", text)

        return re.split(r"(?<=[.!?])\s", text)

class TextRootDTMVectorizer:
    nltk.download("punkt", quiet=True)
    def __init__(self, dataframe: pd.DataFrame, column_name: str) -> None:
        self.dataframe = dataframe
        self.column_name = column_name
        self.analyzer = zeyrek.MorphAnalyzer()
        self.vectorizer = CountVectorizer()

    def _analyze_word(self, word: str) -> Optional[str]:
        analysis = self.analyzer.analyze(word)
        if len(analysis) > 0:
            root = analysis[0][0][1]
            return root
        else:
            return None

    def fit_transform(self) -> pd.DataFrame:
        processed_texts = []
        for text in self.dataframe[self.column_name]:
            words = nltk.word_tokenize(text)
            processed_words = [self._analyze_word(word) for word in words]
            processed_words = [root for root in processed_words if root is not None]
            processed_texts.append(" ".join(processed_words))

        X = self.vectorizer.fit_transform(processed_texts)

        return pd.DataFrame(X.toarray(), columns=self.vectorizer.get_feature_names_out())