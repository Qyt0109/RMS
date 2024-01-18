import sys
from PyQt6.QtWidgets import QApplication, QPushButton, QWidget
from PyQt6.QtGui import QPixmap, QPainter, QBitmap, QIcon
from PyQt6.QtCore import Qt

class RoundButton(QPushButton):
    def __init__(self, icon_path, parent=None):
        super().__init__(parent)
        self.setIconSize(self.size())
        self.setIcon(QIcon(icon_path))
        self.setFixedSize(150, 150)  # Set the size of the button
        self.setMask(self.createMask())

    def createMask(self):
        mask = QBitmap(self.size())
        mask.fill(Qt.GlobalColor.white)
        painter = QPainter(mask)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        painter.setBrush(Qt.GlobalColor.black)
        painter.drawEllipse(0, 0, self.width(), self.height())
        return mask

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QWidget()

    # Replace 'your_icon_path.png' with the path to your image file
    button = RoundButton('Frontend/Resources/Images/default-avatar.png', window)

    window.setGeometry(100, 100, 300, 200)
    window.show()

    sys.exit(app.exec())
