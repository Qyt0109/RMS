import sys
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import Qt
import fitz  # PyMuPDF library

class PDFViewer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PDF Viewer")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.button_image = QPushButton(self)
        self.layout.addWidget(self.button_image)

        self.load_button = QPushButton("Load PDF", self)
        self.load_button.clicked.connect(self.load_pdf)
        self.layout.addWidget(self.load_button)

        self.page_number = 0
        self.doc = None

    def load_pdf(self):
        file_dialog = QFileDialog()
        file_dialog.setNameFilter("PDF Files (*.pdf)")
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)

        try:
            if file_dialog.exec() == QFileDialog.DialogCode.Accepted:
                file_path = file_dialog.selectedFiles()[0]
                self.doc = fitz.open(file_path)
                self.show_page()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error loading PDF: {str(e)}")


    def show_page(self):
        if self.doc is not None and 0 <= self.page_number < self.doc.page_count:
            page = self.doc[self.page_number]
            image = page.get_pixmap().to_image()
            
            q_image = QImage(
                image.samples, image.width, image.height, image.stride,
                QImage.Format.FormatRGB32
            )

            pixmap = QPixmap.fromImage(q_image)
            self.button_image.setIcon(QIcon(pixmap))


    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Left:
            self.page_number = max(0, self.page_number - 1)
            self.show_page()

        elif event.key() == Qt.Key.Key_Right:
            self.page_number = min(self.page_number + 1, self.doc.page_count() - 1)
            self.show_page()


def main():
    app = QApplication(sys.argv)
    viewer = PDFViewer()
    viewer.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
