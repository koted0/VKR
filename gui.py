from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QFileDialog, QLabel, QTextEdit, QComboBox)
from PyQt5.QtCore import QThread, pyqtSignal
from padd import OCR
from process_text import process_text
from translate import translate_text, get_translation_languages
import json


def _load_json_file(file: str = 'output.json'):
    with open(file, 'r', encoding='utf-8') as f:
        return json.load(f)


def _collect_text():
    return process_text(_load_json_file())


class LoadFileThread(QThread):
    file_loaded = pyqtSignal()

    def __init__(self, file_name):
        super().__init__()
        self.file_name = file_name

    def run(self):
        ocr = OCR(self.file_name)
        ocr.save_extracted_text_to_json()
        self.file_loaded.emit()


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        top_layout = QHBoxLayout()
        text_layout = QHBoxLayout()

        self.source_text = QTextEdit()
        self.translated_text = QTextEdit()

        source_text_label = QLabel('Source Text')
        translated_text_label = QLabel('Translated Text')
        self.language_combobox = self._create_language_combobox()

        open_file_button = QPushButton('Open File', self)
        save_file_button = QPushButton('Save File', self)

        text_layout.addWidget(self.source_text)
        text_layout.addWidget(self.translated_text)

        top_layout.addWidget(open_file_button)
        top_layout.addWidget(source_text_label)
        top_layout.addStretch()
        top_layout.addWidget(self.language_combobox)
        top_layout.addStretch()
        top_layout.addWidget(translated_text_label)
        top_layout.addWidget(save_file_button)

        open_file_button.clicked.connect(self._open_file)
        save_file_button.clicked.connect(self._save_text)

        main_layout.addLayout(top_layout)
        main_layout.addLayout(text_layout)

        self.setLayout(main_layout)
        self.setWindowTitle('Translator')
        self.show()

    @classmethod
    def _create_language_combobox(cls):
        language_combobox = QComboBox()
        languages = get_translation_languages()
        [language_combobox.addItem(language_name, language_code)
         for language_name, language_code in languages.items()]
        return language_combobox

    def _translate_text(self):
        print('text translation started')
        source_text = _collect_text()
        splitted_text = source_text.split('\n\n')
        print('text collected')
        selected_language_code = self.language_combobox.currentData()
        translated_text = []
        for i in splitted_text:
            translated_text.append(translate_text(i, target_lang=selected_language_code))

        translated_text = '\n'.join(translated_text)
        self.display_source_text(source_text)
        self.display_translated_text(translated_text)

    def _open_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, 'Open File', '', 'PDF Files (*.pdf);;Image Files (*.jpg '
                                                                          '*.jpeg *.png)')
        if file_name:
            print(f'File Selected: {file_name}')
            self.load_file_thread = LoadFileThread(file_name)
            self.load_file_thread.file_loaded.connect(self._translate_text)
            self.load_file_thread.start()

    def _save_text(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Сохранить текст", "",
                                                   "Текстовые файлы (*.txt);;Все файлы (*)")

        if file_name:
            with open(file_name, 'w', encoding='utf-8') as file:
                file.write(self.translated_text.toPlainText())

    def display_source_text(self, content):
        self.source_text.setPlainText(content)

    def display_translated_text(self, content):
        self.translated_text.setPlainText(content)
