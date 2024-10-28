import os, sys
from PIL import Image
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QFileDialog, QVBoxLayout,
                             QLabel, QLineEdit, QWidget, QDialog, QHBoxLayout)
from PyQt5.QtGui import QIcon

dark_theme = """
QMainWindow {
    background-color: #2b2b2b;
}

QLabel {
    color: #ffffff;
}

QPushButton {
    background-color: #3c3f41;
    color: #ffffff;
    border: 1px solid #5a5a5a;
    padding: 5px;
}

QPushButton:hover {
    background-color: #4f4f51;
}

QPushButton:pressed {
    background-color: #2a2a2a;
}

QLineEdit {
    background-color: #3c3f41;
    color: #ffffff;
    border: 1px solid #5a5a5a;
    padding: 5px;
}

QDialog {
    background-color: #2b2b2b;
}

QFileDialog {
    background-color: #2b2b2b;
    color: #ffffff;
}

QMessageBox {
    background-color: #2b2b2b;
    color: #ffffff;
}
"""

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Конвертер by dissentty")
        self.setGeometry(100, 100, 400, 200)
        self.setWindowIcon(QIcon('icon.ico'))

        self.label = QLabel("Папка не выбрана", self)

        self.button = QPushButton("Выберите папку с изображениями", self)
        self.button.clicked.connect(self.select_location)

        self.converter_button = QPushButton("Начать конвертацию", self)
        self.converter_button.clicked.connect(self.convert)

        self.btn1 = QPushButton("PNG", self)
        self.btn1.setCheckable(True)
        self.btn1.clicked.connect(self.toggle_exclusive)

        self.btn2 = QPushButton("JPEG", self)
        self.btn2.setCheckable(True)
        self.btn2.clicked.connect(self.toggle_exclusive)

        hbox = QHBoxLayout()
        hbox.addWidget(self.btn1)
        hbox.addWidget(self.btn2)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.button)
        layout.addWidget(self.converter_button)
        layout.addLayout(hbox)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        self.selected_folder_path = ''

    def toggle_exclusive(self):
        clicked_button = self.sender()
        for button in [self.btn1, self.btn2]:
            if button != clicked_button:
                button.setChecked(False)
        self.update_button_styles()

    def update_button_styles(self):
        for button in [self.btn1, self.btn2]:
            if button.isChecked():
                button.setStyleSheet("background-color: lightgray")
            else:
                button.setStyleSheet("")

    def select_location(self):
        folder_path = QFileDialog.getExistingDirectory(self, 'Выберите папку')
        if folder_path:
            self.label.setText(f'Выбранная папка: {folder_path}')
            self.selected_folder_path = folder_path
            print(folder_path)

    def convert(self):
        none_format_flag = 0
        output_format = ''
        if self.selected_folder_path != '':
            final_path = self.selected_folder_path + "/converter_res"
            exist_folder = 0
            for filename in os.listdir(self.selected_folder_path):
                if filename == "converter_res":
                    exist_folder = 1
                else:
                    continue
            if exist_folder == 0:
                os.mkdir(final_path)
            self.label.setText(f"Ждите окончания конвертации")
            for filename in os.listdir(self.selected_folder_path):
                if filename.endswith((".png", ".jpg", ".jpeg")):
                    img_path = os.path.join(self.selected_folder_path, filename)
                    with Image.open(img_path) as img:
                        if self.btn1.isChecked():
                            output_format = "PNG"
                        if self.btn2.isChecked():
                            output_format = "JPEG"
                        if output_format != '':
                            output_filename = os.path.splitext(filename)[0] + f".{output_format.lower()}"
                            output_path = os.path.join(final_path, output_filename)
                            img.convert("RGB").save(output_path, output_format)
                        else:
                            none_format_flag = 1
                            self.label.setText("Выберите формат")
            if none_format_flag == 0:
                self.label.setText("Конвертация завершена")
                none_format_flag = 0
        else:
            self.label.setText("Не выбрана папка с изображениями")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(dark_theme)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())