from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QFileDialog, QApplication
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtCore import QSize
from enum import Enum

class FileTypes(Enum):
    ALL_FILE = 'All Files (*)'
    IMAGE_FILE = 'Image Files (*.png *.jpg *.bmp *.gif)'
    PDF_FILE = 'PDF Files (*.pdf)'

class Widget_FilePath(QWidget):
    def __init__(self, parent: QWidget = None, text: str = None, file_type: str = FileTypes.ALL_FILE,
                 callback_on_upload=None, callback_on_download=None) -> None:
        super().__init__(parent)
        self.file_types = file_type
        self.callback_on_upload = callback_on_upload
        self.callback_on_download = callback_on_download
        self.layout = QVBoxLayout(self)

        if callback_on_upload:
            self.button_upload = QPushButton(parent=self, text='Upload')
            self.button_upload.setIcon(QIcon(QPixmap("icon_upload.png")))  # Replace with your actual icon path
            self.button_upload.clicked.connect(self.on_upload)
            self.layout.addWidget(self.button_upload)

        if callback_on_download:
            self.button_download = QPushButton(parent=self, text='Download')
            self.button_download.setIcon(QIcon(QPixmap("icon_download.png")))  # Replace with your actual icon path
            self.button_download.clicked.connect(self.on_download)
            self.layout.addWidget(self.button_download)

    def on_download(self):
        file_dialog = QFileDialog(self)
        #file_dialog.setDefaultSuffix('png')

        # Set the file type filter based on the specified file_type
        file_dialog.setNameFilter(self.file_types)

        file_path, _ = file_dialog.getSaveFileName(self, 'Save As', '', self.file_types)

        if not file_path:
            return
        self.callback_on_download(file_path=file_path)
        print(file_path)


    def on_upload(self):
        file_dialog = QFileDialog(self)
        file_path, _ = file_dialog.getOpenFileName(self, 'File path', '', self.file_types)

        if not file_path:
            return
        
        self.callback_on_upload(file_path=file_path)

        print(file_path)

def run_app():
    app = QApplication([])
    widget = Widget_FilePath(text="File Path Widget", file_type=FileTypes.PDF_FILE.value,
                 callback_on_upload='None', callback_on_download='None')
    widget.show()
    app.exec()

if __name__ == '__main__':
    run_app()
