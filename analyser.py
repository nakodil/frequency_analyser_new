import re  # разбирем строку на отдельные слова
from docx import Document  # pip install python-docx
from bs4 import BeautifulSoup  # прасинг xml
import pymorphy2  # нормализация частей речи
from collections import Counter  # считаем самые частые слова
from wordcloud import WordCloud  # pip install wordcloud
from charset_normalizer import from_path  # нормализуем кодировку


class Analyser:
    def __init__(self):
        pass

    def make_text_from_file(self):
        """
        определяет расширение текстового файла,
        вызывает соответствуйющий метод для типов TXT, DOCX, FB2
        пустая строка для остальных типов
        """
        if self.file_path.endswith(".txt"):
            self.make_text_from_txt()
        elif self.file_path.endswith(".docx"):
            self.make_text_from_docx()
        elif self.file_path.endswith(".fb2"):
            self.make_text_from_fb2()
        else:
            self.content = ""  # FIXME: Wordcloud подавится пустой строкой!

    def make_text_from_txt(self):
        """
        Делает строку из TXT
        """
        self.content = str(from_path(self.file_path).best())

    def make_text_from_docx(self):
        """
        Делает строку из DOCX
        """
        file = Document(self.file_path)
        self.content = " ".join([p.text for p in file.paragraphs])

    def make_text_from_fb2(self):
        """
        Делает строку из FB2
        """
        with open(self.file_path, 'rb') as f:
            data = f.read()
        bs_data = BeautifulSoup(data, "xml")
        sections = bs_data.find_all('section')
        self.content = " ".join([s.text for s in sections])

    def make_words_from_text(self):
        """
        Создает список русских слов со строчной буквы без знаков препинания
        """
        self.words = re.findall("[а-яё]+", self.content.lower())

    def make_normalized_words(self, *part_of_speech: str):
        """
        Создает список нормальных форм слов
        для определенных в part_of_speech частей речи.
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
        Создает словарь длинной num из самых частых слов по убыванию частоты
        слово: частота
        """
        self.most_frequent_words = dict(Counter(
            self.normalized_words).most_common(num))

    def make_wordcloud(self):
        """
        Создает объект Wordcloud из словаря self.most_frequent_words
        TODO: определить аргументы и проборсить из к WordCloud
        """
        self.wordcloud = WordCloud(
            width=1920,
            height=1080,
            background_color='black'
        )
        self.wordcloud = self.wordcloud.generate_from_frequencies(
            self.most_frequent_words
        )

    def save_wordcloud_to_file(self, filename="wordcloud.png"):
        """
        сохраняет Wordcloud в файл filename
        """
        self.wordcloud.to_file(filename)
        print("Done!")
