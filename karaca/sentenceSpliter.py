
from typing import List
import re
import os
from pathlib import Path
karaca_path = os.path.dirname(os.path.abspath(__file__))
prefix_file = karaca_path+"/datas/nBreakPrefix.txt"
class SentenceSpliter:
    def __init__(self) -> None:
        self.name = "SentenceSpliter"
        with open(prefix_file, "r", encoding="utf-8") as file:
            self.non_breaking_prefixes_tr = file.read().splitlines()
        self.prefix_pattern = r"(?:^|\s)(" + "|".join(self.non_breaking_prefixes_tr) + r")\."

    def split_sentences(self, text: str) -> List[str]:
        text = re.sub(self.prefix_pattern, r"\1", text)

        return re.split(r"(?<=[.!?])\s", text)