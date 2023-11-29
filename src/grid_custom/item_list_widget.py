from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton


class ItemGridType(QWidget):
    emit_size_signal = Signal(object)

    def __init__(self, title=None, image_path=None, type_division="GRID_STANDARD"):
        super().__init__()
        self.title = title
        self.image_path = image_path
        self.type_division = type_division
        self.load_ui()

    def load_ui(self):
        # create layout
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_image = QLabel(self.image_path)
        self.label_title = QLabel(self.title)
        self.label_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_title.setStyleSheet("font-weight: bold")
        self.layout.addWidget(self.label_image)
        self.layout.addWidget(self.label_title)
        self.setLayout(self.layout)

    def mousePressEvent(self, event):
        value = [self.title, self.type_division]
        self.emit_size_signal.emit(value)
