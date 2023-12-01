from typing import List

from PySide6.QtCore import Qt, QItemSelectionModel, Signal
from PySide6.QtGui import QStandardItemModel, QStandardItem, QPixmap
from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtWidgets import QWidget, QVBoxLayout, QListView, QHBoxLayout, QLabel

from src.grid_custom.item_grid_model import ItemGridModel


class ListGridCustom(QListView):
    signal_item_click = Signal(object)
    def __init__(self, parent=None):
        super().__init__(parent)
        self.today_index = None
        self.setFixedWidth(240)
        self.list_grid_custom: List[ItemGridModel] = []
        self.load_ui()

    def load_ui(self):
        self.setContentsMargins(0, 0, 0, 0)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.clicked.connect(self.item_clicked)
        self.list_view_model = QStandardItemModel()
        self.setModel(self.list_view_model)
        self.populate_grid_item()
        self.set_style_sheet()

    def item_clicked(self, index):
        item: ItemGridCustom = self.list_view_model.itemFromIndex(index)
        self.signal_item_click.emit(item.model)
        item.on_item_click()
    def set_style_sheet(self):
        pass
        # self.setStyleSheet("QListView { background-color: transparent; }")

    def populate_grid_item(self):
        self.today_index = self.list_view_model.rowCount()
        if self.list_grid_custom:
            self.add_items_to_list(self.list_grid_custom)

    def add_newest_item_grid(self, model: ItemGridModel):
        item_widget = ItemGridCustom(model=model)
        self.list_view_model.insertRow(self.today_index, item_widget)

        select_index = self.list_view_model.index(self.today_index, 0)
        selection_model = self.selectionModel()
        if selection_model is not None:
            selection_model.setCurrentIndex(select_index, QItemSelectionModel.SelectionFlag(QItemSelectionModel.ClearAndSelect | QItemSelectionModel.Rows))

        self.setIndexWidget(self.list_view_model.indexFromItem(item_widget), item_widget.main_widget)
        self.today_index += 1

    def add_items_to_list(self, list_items):
        for item_model in list_items:
            item = ItemGridCustom(model=item_model)
            self.list_view_model.appendRow(item)
            self.setIndexWidget(self.list_view_model.indexFromItem(item), item.main_widget)

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

        self.label_name_grid = QLabel(self.model.name)
        self.label_name_grid.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout_content.addWidget(self.image_grid)
        self.layout_content.addWidget(self.label_name_grid)

        self.main_layout.addLayout(self.layout_content)
        self.main_layout.addLayout(self.layout_state_choose)

        self.setSizeHint(self.main_widget.sizeHint())
        self.setData(self.main_widget, Qt.UserRole)

    def on_item_click(self):
        pass