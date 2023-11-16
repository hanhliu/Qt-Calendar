from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel

class StackedWidget(QWidget):
    clicked = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.selected = False
        self.load_ui()

    def load_ui(self):
        self.setStyleSheet("background-color: lightblue;")
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel()
        self.layout.addWidget(self.label)

    def mousePressEvent(self, event):
        self.selected = not self.selected
        self.updateStyle()
        self.clicked.emit()

    # def enterEvent(self, event):
    #     self.setStyleSheet("background-color: lightblue; border: 2px solid red;")
    #
    # def leaveEvent(self, event):
    #     if not self.selected:
    #         self.setStyleSheet("background-color: lightblue; border: 2px solid lightblue;")

    def setSelected(self, selected):
        self.selected = selected
        self.updateStyle()

    def updateStyle(self):
        if self.selected:
            self.setStyleSheet("background-color: lightblue; border: 2px solid blue;")
        else:
            self.setStyleSheet("background-color: lightblue; border: 2px solid lightblue;")

