from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton

from src.grid_custom.item_grid_model import ItemGridModel


class ItemGridType(QWidget):
    emit_size_signal = Signal(object)

    def __init__(self, title=None, image_path=None, type_division="GRID_STANDARD", model_grid: ItemGridModel = None):
        super().__init__()
        self.title = title
        self.image_path = image_path
        self.type_division = type_division
        self.model_grid = model_grid
        self.load_ui()

    def load_ui(self):
        # create layout
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_image = QLabel(self.model_grid.image_url)
        self.label_title = QLabel(str(self.model_grid.grid_count))
        self.label_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_title.setStyleSheet("font-weight: bold")
        self.layout.addWidget(self.label_image)
        self.layout.addWidget(self.label_title)
        self.setLayout(self.layout)

    def mousePressEvent(self, event):
        value = [self.model_grid, self.type_division]
        self.emit_size_signal.emit(value)
