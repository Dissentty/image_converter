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

        self.setWindowTitle("Конвертер")
        self.setGeometry(100, 100, 400, 200)
        #self.setWindowIcon(QIcon('icon.ico'))

        self.label = QLabel("Папка не выбрана", self)

        self.button = QPushButton("Выберите папку с изображениями", self)
        self.button.clicked.connect(self.select_location)

        self.converter_button = QPushButton("Начать конвертацию", self)
        self.converter_button.clicked.connect(self.convert)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.button)
        layout.addWidget(self.converter_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        self.selected_folder_path = ''

    def select_location(self):
        folder_path = QFileDialog.getExistingDirectory(self, 'Выберите папку')
        if folder_path:
            self.label.setText(f'Выбранная папка: {folder_path}')
            self.selected_folder_path = folder_path
            print(folder_path)

    def convert(self):
        if self.selected_folder_path != '':
            output_format = "PNG"
            final_path = self.selected_folder_path + "/converter_res"
            exist_folder = 0
            for filename in os.listdir(self.selected_folder_path):
                if filename == "converter_res":
                    print(filename)
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
                        output_filename = os.path.splitext(filename)[0] + f".{output_format.lower()}"
                        output_path = os.path.join(final_path, output_filename)
                        img.convert("RGB").save(output_path, output_format)
                        self.label.setText("dlfsl")
            self.label.setText("Конвертация завершена")
        else:
            self.label.setText("Не выбрана папка с изображениями")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(dark_theme)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())