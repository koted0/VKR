import json
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QFileDialog, QLabel, QTextEdit)
from PyQt5.QtCore import QThread, pyqtSignal
from padd import OCR
from process_text import process_text
from translate import translate_text


def _load_json_file(json_file: str = 'output.json'):
    with open(json_file, 'r', encoding='utf-8') as file:
        return json.load(file)


def _collect_text():
    return process_text(_load_json_file())


class LoadPDFThread(QThread):
    pdf_loaded = pyqtSignal()

    def __init__(self, file_name):
        super().__init__()
        self.file_name = file_name

    def run(self):
        ocr = OCR(self.file_name)
        ocr.save_extracted_text_to_json()
        self.pdf_loaded.emit()


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()

        top_layout = QHBoxLayout()
        open_file_button = QPushButton('Open File', self)
        open_file_button.clicked.connect(self.open_file)
        top_layout.addWidget(open_file_button)

        top_layout.addWidget(QLabel('ORIGINAL TEXT'))

        top_layout.addStretch()

        top_layout.addWidget(QLabel('TRANSLATED TEXT'))

        save_text_button = QPushButton('SAVE TEXT', self)
        save_text_button.clicked.connect(self.save_text)
        top_layout.addWidget(save_text_button)

        main_layout.addLayout(top_layout)

        text_layout = QHBoxLayout()
        self.original_text = QTextEdit()
        self.translated_text = QTextEdit()
        text_layout.addWidget(self.original_text)
        text_layout.addWidget(self.translated_text)

        main_layout.addLayout(text_layout)

        self.setLayout(main_layout)
        self.setWindowTitle('My App')
        self.show()

    def open_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, 'Open File', '', 'PDF Files (*.pdf)')
        if file_name:
            print(f'File selected: {file_name}')
            self.load_pdf_thread = LoadPDFThread(file_name)
            self.load_pdf_thread.pdf_loaded.connect(self._translate_text)
            self.load_pdf_thread.start()


    def save_text(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getSaveFileName(self, "Сохранить текст", "",
                                                   "Текстовые файлы (*.txt);;Все файлы (*)", options=options)
        if file_name:
            with open(file_name, 'w', encoding='utf-8') as file:
                file.write(self.translated_text.toPlainText())

    def split_text(text):
        text_list = text.split('\n\n')
        return text_list

    def _translate_text(self):
        print('text translation started')
        original_text = _collect_text()
        splited_text = original_text.split('\n\n')
        print('text collected')
        translated_text = []
        for i in splited_text:
            translated_text.append(translate_text(i))

        translated_text = '\n'.join(translated_text)
        self.display_original_text(original_text)
        self.display_translated_text(translated_text)

    def display_original_text(self, content):
        self.original_text.setPlainText(content)

    def display_translated_text(self, content):
        self.translated_text.setPlainText(content)
