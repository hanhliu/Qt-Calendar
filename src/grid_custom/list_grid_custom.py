from typing import List

from PySide6.QtCore import Qt, QItemSelectionModel, Signal
from PySide6.QtGui import QStandardItemModel
from PySide6.QtWidgets import QListView

from src.grid_custom.item_grid_custom_in_list import ItemGridCustom
from src.grid_custom.item_grid_model import ItemGridModel


class ListGridCustom(QListView):
    signal_item_click = Signal(object)
    def __init__(self, parent=None, divisions_list=None):
        super().__init__(parent)
        self.divisions_list = divisions_list
        self.today_index = None
        self.setFixedWidth(180)
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
        clicked_item: ItemGridCustom = self.list_view_model.itemFromIndex(index)
        self.signal_item_click.emit(clicked_item.model)

        # Handle visibility of state_choose for each item in the list
        for row in range(self.list_view_model.rowCount()):
            item = self.list_view_model.item(row, 0)
            item_widget = self.indexWidget(self.list_view_model.indexFromItem(item))

            if item_widget:
                if item == clicked_item:
                    item.state_choose.setVisible(True)
                else:
                    item.state_choose.setVisible(False)
    def set_style_sheet(self):
        pass
        # self.setStyleSheet("QListView { background-color: transparent; }")

    def populate_grid_item(self):
        self.today_index = self.list_view_model.rowCount()

        '''Chưa biết là lưu local hay lưu global nên note lại để nhớ cần phải add vào list_grid_custom để sau khi mở lại app sẽ có các list đã tạo'''
        # self.list_grid_custom = self.divisions_list.copy()
        for i in self.divisions_list:
            self.list_grid_custom.append(i)

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

        if self.list_view_model.rowCount() > 0:
            index_to_select = self.list_view_model.index(0, 0)
            self.setCurrentIndex(index_to_select)
            current_item = self.list_view_model.itemFromIndex(index_to_select)
            if current_item:
                current_item_widget = self.indexWidget(index_to_select)
                if current_item_widget:
                    current_item.state_choose.setVisible(True)

    def update_grid_items(self, new_divisions_list):
        # Clear existing items
        self.list_view_model.clear()
        self.list_grid_custom = []

        # Update data
        self.divisions_list = new_divisions_list

        # Populate the grid with new data
        self.populate_grid_item()