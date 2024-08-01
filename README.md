# Karaca NLP

Karaca is a library designed for various natural language processing tasks in Turkish. This repository includes the following functionalities:

- **Normalize**: Normalize Turkish text by converting it to lowercase and removing punctuation.
- **SentenceSpliter**: Split text into individual sentences.
- **Emotion**: Guess the emotion expressed in a given text.
- **News**: Categorize news articles into predefined categories.
- **Deasciifier**: Convert ASCII-encoded Turkish text into its original form with diacritics and special characters.

## Installation

To install the Karaca library, clone the repository and install the required dependencies:

```sh
git clone https://github.com/KaracaAI/KaracaNLP.git
cd karaca
pip install -r requirements.txt
```

## Usage

### Normalize

```
from karaca import Normalize

text = "Merhaba, dünya!"
normalized_text = Normalize.lower_text(text)
print(normalized_text)
# Output: merhaba dünya
```

### SentenceSpliter

```
from karaca import SentenceSpliter

text = "Merhaba. Nasılsın? Ben iyiyim."
sentences = SentenceSpliter(text)
print(sentences)
# Output: ["Merhaba.", "Nasılsın?", "Ben iyiyim."]
```

### Emotion

```
from karaca import Emotion

text = "Harika bir gün!"
emotion = Emotion.guess(text)
print(emotion)
# Output: "Tahmin Edilen Duygu: joy % 94.61"
```

### News

```
from karaca import News

text = "Yeni Windows açığı kapatıldı"
category = News.guess(text)
print(category)
# Output: "Tahmin Edilen konu: technology % 77.67"

```

### Deasciifier

```
from Karaca import Deasciifier

my_ascii_turkish_txt = "Turkiye'nin baskenti Ankara'dir. Iklimi genellikle sicak ve kuraktir. Istanbul, Turkiye'nin en buyuk sehridir ve kulturel olarak cok zengindir."
deasciifier = Deasciifier(my_ascii_turkish_txt)
my_deasciified_turkish_txt = deasciifier.convert_to_turkish()
print(my_deasciified_turkish_txt)
# Output: "Türkiye'nin başkenti Ankara'dır. İklimi genellikle sıcak ve kuraktır. İstanbul, Türkiye'nin en büyük şehridir ve kültürel olarak çok zengindir."
```

## Testing

```sh
python -m unittest discover -s tests
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or new features.

## License
This project is licensed under the Apache License 2.0. See the [LICENSE](LICENSE) file for details.
