import re  # разбирем строку на отдельные слова
from docx import Document  # pip install python-docx
import pymorphy2  # pip install pymorphy2
from collections import Counter  # считаем самые частые слова

# делаем картинку из частых слов
from wordcloud import WordCloud  # pip install wordcloud
from PIL import Image
import matplotlib.pyplot as plt


class App:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def make_text_from_file(self):
        """
        делает строку из файла TXT или DOCX;
        пустая строка для остальных расширений
        """
        if self.file_path.endswith(".txt"):
            with open(self.file_path, "r", encoding="utf8") as file:
                self.content = file.read()
        elif self.file_path.endswith(".docx"):
            file = Document(self.file_path)
            self.content = " ".join([p.text for p in file.paragraphs])
        else:
            self.content = ""

    def make_words_from_text(self):
        """
        создает список русских слов со строчной буквы без знаков препинания
        """
        self.words = re.findall("[а-яё]+", self.content.lower())

    def make_normalized_words(self, *part_of_speech):
        """
        создаем список нормальных форм слов
        для определенных в part_of_speech частей речи
        https://pymorphy2.readthedocs.io/en/stable/user/grammemes.html#grammeme-docs
        """
        morph = pymorphy2.MorphAnalyzer()
        self.normalized_words = []
        for word in self.words:
            parse = morph.parse(word)[0]
            for part in part_of_speech:
                if part in parse.tag:
                    self.normalized_words.append(parse.normal_form)

    def make_most_frequent_words(self, num: int):
        """
        создает словарь длинной num из самых частых слов по убыванию частоты
        слово: частота
        """
        self.most_frequent_words = dict(Counter(
            app.normalized_words).most_common(num))

    def make_wordcloud_image(self, image_path):
        wc = WordCloud(
            background_color="black",
            max_words=1000,
            width=2000,
            height=1000,
            relative_scaling=0.25
        )
        wc_frequency = wc.generate_from_frequencies(self.most_frequent_words)
        plt.figure(figsize=(20, 10))  # умножается на dpi
        plt.axis("off")
        plt.imshow(wc_frequency)
        plt.savefig(image_path, dpi=100, facecolor='k', bbox_inches='tight')


app = App("text.txt")
app.make_text_from_file()
app.make_words_from_text()
app.make_normalized_words("NOUN")
app.make_most_frequent_words(100)
app.make_wordcloud_image("wordcloud.png")
