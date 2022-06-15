import re  # разбирем строку на отдельные слова
from docx import Document  # pip install python-docx
import pymorphy2  # pip install pymorphy2
from collections import Counter  # считаем самые частые слова
from wordcloud import WordCloud  # pip install wordcloud
from charset_normalizer import from_path  # нормализуем кодировку


class App:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def make_text_from_file(self):
        """
        делает строку из файла TXT или DOCX;
        пустая строка для остальных расширений
        """
        if self.file_path.endswith(".txt"):
            self.content = str(from_path(self.file_path).best())
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

    def make_wordcloud(self):
        """
        докстрока!
        """
        self.wordcloud = WordCloud(
            width=1920,
            height=1080,
            background_color='black'
        )
        self.wordcloud = self.wordcloud.generate_from_frequencies(
            self.most_frequent_words
        )

    def save_wordcloud_to_file(self, filename):
        """
        докстрока!
        """
        self.wordcloud.to_file(filename)


app = App("const.txt")
app.make_text_from_file()
app.make_words_from_text()
app.make_normalized_words("NOUN")
app.make_most_frequent_words(100)
app.make_wordcloud()
app.save_wordcloud_to_file("wordcloud.png")
