
from functools import partial

from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

class PopupOk(QMessageBox):
    def __init__(self, parent:QWidget=None, title: str=None, message: str=None, button_text: str = "Ok", stylesheet: str = "", callback_ok=None, **kwargs):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setText(message)
        self.setStyleSheet(stylesheet)
        self.addButton(QPushButton(button_text),
                       QMessageBox.ButtonRole.AcceptRole)
        if callback_ok:
            self.buttonClicked.connect(partial(callback_ok, **kwargs))


class PopupYesNo(QDialog):
    def __init__(self, parent=None, title="", message="", yes_button_text="Yes", no_button_text="No", stylesheet="", callback_yes=None, callback_no=None, **kwargs):
        super().__init__(parent)

        self.setWindowTitle(title)

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.StandardButton.Yes | QDialogButtonBox.StandardButton.No)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        message_label = QLabel(message)
        self.layout.addWidget(message_label)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

        # Use QDialog.DialogCode.Accepted to check if the user clicked "Yes"

        if callback_yes:
            yes_button = self.buttonBox.button(QDialogButtonBox.StandardButton.Yes)
            yes_button.setText(yes_button_text)
            yes_button.clicked.connect(lambda: callback_yes(**kwargs))

        if callback_no:
            no_button = self.buttonBox.button(QDialogButtonBox.StandardButton.No)
            no_button.setText(no_button_text)
            no_button.clicked.connect(lambda: callback_no(**kwargs))



class PopupClose(QDialog):
    def __init__(self, title: str, message: str, callback_ok=None):
        super().__init__()

        self.setWindowTitle(title)

        QBtn = QDialogButtonBox.StandardButton.Ok

        self.buttonBox = QDialogButtonBox(QBtn)

        self.layout = QVBoxLayout()
        label_message = QLabel(message)
        self.layout.addWidget(label_message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

        dlg = QMessageBox(self)
        dlg.setWindowTitle("I have a question!")
        dlg.setText("This is a simple dialog")
        button = dlg.exec()

        if button == QMessageBox.StandardButton.Ok:
            print("OK!")