from PyQt6.QtWidgets import QPushButton, QFileDialog, QWidget


CHOOSE_ALL_FILE_OPTION = 'All Files (*)'
CHOOSE_IMAGE_FILE_OPTION = 'Image Files (*.png *.jpg *.bmp *.gif)'
CHOOSE_PDF_FILE_OPTION = 'PDF Files (*.pdf)'

class Button_SelectFilePath(QPushButton):
    def __init__(self, parent: QWidget = None, text: str = None, file_types: str = 'All Files (*)',
                 callback_on_selected=None) -> None:
        super().__init__(text, parent)
        self.file_types = file_types
        self.callback_on_selected = callback_on_selected
        self.clicked.connect(self.on_select_file_path)

    def on_select_file_path(self):
        file_dialog = QFileDialog(self)
        file_path, _ = file_dialog.getOpenFileName(self, 'File path', '', self.file_types)

        if not file_path:
            return

        print(file_path)
        if self.callback_on_selected:
            self.callback_on_selected(file_path=file_path)

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