from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import Qt
from Backend.Database.models import FileTypes
from Frontend.Helper.popups import *
from Backend.Services.file_handler import *

icon_download_file_path = "Frontend/Resources/Bootstrap/file-earmark-arrow-down.png"
icon_upload_file_path = "Frontend/Resources/Bootstrap/file-earmark-arrow-up.png"

sidemenu_stylesheet_normal = "border-radius: 5px; background-color: rgba(254, 175, 0, 40); padding: 5px 5px 5px 5px; text-align: left; padding-left: 10px;"
sidemenu_stylesheet_hover = "border-radius: 5px; background-color: rgba(254, 175, 0, 180); padding: 5px 5px 5px 5px; text-align: left; padding-left: 10px;"
home_button_stylesheet_normal = "background-color: rgba(54, 159, 212, 80); border-radius: 24px;"
home_button_stylesheet_hover = "background-color: rgba(54, 159, 212, 160); border-radius: 24px 24px 24px 24px;"

default_stylesheet_normal = "border-radius: 5px; background-color: rgba(54, 159, 212, 80); padding: 5px 5px 5px 5px;"
default_stylesheet_hover = "border-radius: 5px; background-color: rgba(54, 159, 212, 160); padding: 5px 5px 5px 5px;"

class ActionButton(QPushButton):
    def __init__(self,
                 parent: QWidget = None,
                 text: str = None,
                 icon_path=None,
                 signal=None,
                 stylesheet_normal: str = default_stylesheet_normal,
                 stylesheet_hover: str = default_stylesheet_hover):
        super().__init__(parent)
        if icon_path:
            self.setIcon(QIcon(QPixmap(icon_path)))
        self.setText(text)
        if signal:
            self.clicked.connect(signal)

        # Enable tracking mouse move events
        self.setMouseTracking(True)
        self.stylesheet_normal = stylesheet_normal
        self.stylesheet_hover = stylesheet_hover
        self.setStyleSheet(stylesheet_normal)

    def enterEvent(self, event):
        # Set the style on hover
        self.setStyleSheet(self.stylesheet_hover)

    def leaveEvent(self, event):
        # Reset the style when the mouse leaves
        self.setStyleSheet(self.stylesheet_normal)


class RoundButton(QPushButton):
    def __init__(self, icon_path, parent=None):
        super().__init__(parent)
        self.setIconSize(self.size())
        self.setIcon(QIcon(icon_path))
        self.setFixedSize(50, 50)  # Set the size of the button

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        painter.setBrush(QBrush(QColor(255, 255, 255, 255))
                         )  # Button background color
        painter.setPen(Qt.PenStyle.NoPen)

        # Draw a circle
        painter.drawEllipse(0, 0, self.width(), self.height())

        # Draw the icon
        icon_rect = self.icon().pixmap(self.width(), self.height()).rect()
        icon_rect.moveCenter(self.rect().center())
        painter.drawPixmap(icon_rect, self.icon().pixmap(
            self.width(), self.height()))

class Widget_FilePath(QWidget):
    def __init__(self,
                 parent: QWidget = None,
                 data:bytes = None,
                 file_type: str = FileTypes.ALL_FILE.value,
                 is_upload=None,
                 is_download=None) -> None:
        super().__init__(parent)
        self.data = data
        self.file_types = file_type
        self.callback_on_upload = is_upload
        self.callback_on_download = is_download
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.label_file_path = QLabel(self)
        self.label_file_path.setStyleSheet(
            "background-color:rgba(0, 0, 153, 30); padding: 5px 5px 5px 5ps;")
        self.label_file_path.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.layout.addWidget(self.label_file_path)
        frame = QFrame(self)
        layout = QHBoxLayout(frame)
        self.setLabelText()
        if is_upload:
            self.button_upload = ActionButton(parent=self, icon_path=icon_upload_file_path)
            layout.addWidget(self.button_upload)
            self.button_upload.clicked.connect(self.on_upload)
        if is_download:
            self.button_download = ActionButton(parent=self, icon_path=icon_download_file_path)
            layout.addWidget(self.button_download)
            self.button_download.clicked.connect(self.on_download)
            if not self.data:
                self.button_download.setDisabled(True)
        self.layout.addWidget(frame)

    def setLabelText(self):
        if self.data:
            self.label_file_path.setText("File available")
        else:
            self.label_file_path.setText("No file available")

    def on_download(self):
        if not self.data:
            return
        # Open a file dialog to get the save path
        file_dialog = QFileDialog(self)
        file_dialog.setNameFilter(self.file_types)
        file_path, _ = file_dialog.getSaveFileName(
            self, 'Save as', '', self.file_types)
        if not file_path:
            
            return
        bytes_to_file(file_path=file_path,
                      byte_data=self.data)

    def on_upload(self):
        file_dialog = QFileDialog(self)
        file_path, _ = file_dialog.getOpenFileName(self, 'File path', '', self.file_types)

        if not file_path:
            return
        self.data = file_to_bytes(file_path=file_path)
        self.setLabelText()
    
    def get_uploaded_data(self):
        return self.data

"""
def generate_qr_code(self):
    # Open a file dialog to get the save path
    file_dialog = QFileDialog(self)
    file_dialog.setDefaultSuffix('png')
    file_path, _ = file_dialog.getSaveFileName(
        self, 'Save QR Code As', '', 'Images (*.png)')

    if file_path:
        self.save_qr_code(data, file_path)

"""

"""
if __name__ == "__main__":
    app = QApplication([])

    # Test the select file to save button for all files
    save_button_all = Widget_SelectFilePath(text="Select file to save (All Files)",
                                            callback_on_selected=file_to_bytes,
                                            callback_on_save=lambda file_path: bytes_to_file(file_path, file_to_bytes(file_path)))
    save_button_all.show()

    # Test the select file to upload button for all files
    upload_button_all = Widget_SelectFilePath(text="Select file to upload (All Files)",
                                              callback_on_selected=upload_file)
    upload_button_all.show()

    # Test the select file to save button for image files
    save_button_images = Widget_SelectFilePath(text="Select image file to save",
                                               file_types='Image Files (*.png *.jpg *.bmp *.gif)',
                                               callback_on_selected=file_to_bytes,
                                               callback_on_save=lambda file_path: bytes_to_file(file_path, file_to_bytes(file_path)))
    save_button_images.show()

    # Test the select file to save button for PDF files
    save_button_pdf = Widget_SelectFilePath(text="Select PDF file to save",
                                            file_types='PDF Files (*.pdf)',
                                            callback_on_selected=file_to_bytes,
                                            callback_on_save=lambda file_path: bytes_to_file(file_path, file_to_bytes(file_path)))
    save_button_pdf.show()

    app.exec()
"""