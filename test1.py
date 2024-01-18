from PyQt6.QtWidgets import QMessageBox, QPushButton, QApplication
from functools import partial

class PopupMessageBox(QMessageBox):
    def __init__(self, title: str, message: str, button_text: str = "Đóng", callback_ok=None, **kwargs):
        super().__init__()
        self.setWindowTitle(title)
        self.setText(message)
        
        # Create a button with the specified text
        self.addButton(QPushButton(button_text), QMessageBox.ButtonRole.AcceptRole)
        
        # Connect the button click signal to the provided callback
        self.buttonClicked.connect(partial(callback_ok, **kwargs))

# Example usage:
def callback_function(**kwargs):
    print("Callback function called with arguments:", kwargs)

app = QApplication([])

popup = PopupMessageBox("Title", "This is a message", callback_ok=callback_function, additional_argument="Hello")
popup.exec()
