from PyQt6.QtWidgets import *


class Widget_SelectFilePath(QPushButton):
    def __init__(self, parent: QWidget=None, text:str=None, icon_path:str=None, callback_on_selected=None) -> None:
        super().__init__(parent)
        self.clicked.connect(self.on_select_file_path)

    def on_select_file_path(self):
        # Open a file dialog to get the save path
        file_dialog = QFileDialog(self)
        file_dialog.setDefaultSuffix('png')
        file_path, _ = file_dialog.getSaveFileName(
            self, 'Save As', '', 'Images (*.png)')

        if not file_path:
            return
        print(file_path)
        if callback_on_selected:
            callback_on_selected(file_path = file_path)
            # file_bytes = file_to_bytes(file_path)
            # print(len(file_bytes))

def file_to_bytes(file_path:str):
    print(file_path)
    return
    with open(file_path, 'rb') as file:
        file_bytes = file.read()
    print(file_path)
    return file_bytes

def run_app():
    app = QApplication([])
    main_win = Widget_SelectFilePath(text="Test select file", callback_on_selected=file_to_bytes)
    main_win.show()
    app.exec()

if __name__ == '__main__':
    run_app()