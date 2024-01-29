
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QToolButton
class ButtonTitleBar(QToolButton):
    def __init__(self, parent=None, svg_path=None):
        super().__init__(parent)
        self.svg_path = svg_path
        self.load_ui()

    def load_ui(self):
        self.setIcon(QIcon(self.svg_path))
        self.setStyleSheet('''
            QToolButton { 
                background-color: transparent; 
            }
        ''')