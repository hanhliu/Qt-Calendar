from PySide6.QtCore import Qt
from PySide6.QtGui import QStandardItem, QPixmap
from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel


class ItemGridCustom(QStandardItem):
    def __init__(self, model=None):
        super().__init__()
        self.model = model
        self.load_ui()

    def load_ui(self):
        self.main_widget = QWidget()
        self.main_layout = QHBoxLayout(self.main_widget)
        self.main_layout.setSpacing(2)

        self.layout_state_choose = QVBoxLayout()
        state_choose = QSvgWidget()
        state_choose.load("/Users/hanhluu/Documents/Project/Qt/calendar_project/assets/state_read.svg")
        state_choose.setFixedSize(10, 10)
        self.layout_state_choose.addWidget(state_choose)

        self.layout_content = QVBoxLayout()
        self.image_grid = QLabel()
        self.image_grid.setAlignment(Qt.AlignmentFlag.AlignCenter)
        pixmap = QPixmap("/Users/hanhluu/Documents/Project/Qt/calendar_project/assets/image_event.png")  # Replace with the actual image file path
        self.image_grid.setPixmap(pixmap)

        self.label_name_grid = QLabel(f"{self.model.grid_count} Divisions")
        self.label_name_grid.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout_content.addWidget(self.image_grid)
        self.layout_content.addWidget(self.label_name_grid)

        self.main_layout.addLayout(self.layout_content)
        self.main_layout.addLayout(self.layout_state_choose)

        self.setSizeHint(self.main_widget.sizeHint())
        self.setData(self.main_widget, Qt.UserRole)

    def on_item_click(self):
        pass