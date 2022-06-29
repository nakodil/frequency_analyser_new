from PyQt6 import QtWidgets, uic
from analyser import Analyser


class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        uic.loadUi('interface.ui', self)
        self.show()
        # свзяываем событие клика по кнопке с методом
        self.make_wordcloud_image_button.clicked.connect(self.run)

    def select_file(self):
        """
        Вызывает диалог выбора файла.
        Записвыает путь к выбранному файлу в виджет source_file_path_field
        """
        self.file_path = QtWidgets.QFileDialog.getOpenFileName(
            self,
            "",
            "",
            "texts (*.txt *.docx *.fb2)"
        )[0]
        self.source_file_path_field.setText(self.file_path)

    def run(self):
        """
        TODO:
        Забрать значения из виджетов.
        Деактивировать кнопку, если не выбран файл и хотя бы одна часть речи.
        Оживить прогресс-бар.
        Деактивировать интерфейс, пока идет создание картинки облака слов.
        """
        self.analyser = Analyser()
        self.analyser.file_path = "texts/text_short.docx"
        self.analyser.make_text_from_file()
        self.analyser.make_words_from_text()
        self.analyser.make_normalized_words("NOUN")
        self.analyser.make_most_frequent_words(100)
        self.analyser.make_wordcloud()
        self.analyser.save_wordcloud_to_file()
