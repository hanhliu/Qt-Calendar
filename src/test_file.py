import os
import sys

from PySide6.QtCore import QItemSelection, QItemSelectionModel, Signal
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtWidgets import QWidget, QMainWindow, QApplication, QVBoxLayout, QTreeView, \
    QAbstractItemView, QPushButton

# # Get the index of item 3
# index = model.index(2, 0)
#
# # Create a selection model and set the current index to item 3
# selection_model = self.tree_view.selectionModel()
# selection = QItemSelection(index, index)
# selection_model.select(selection, QItemSelectionModel.Select)

class MainWindow(QMainWindow):
    temp_signal = Signal(str)
    def __init__(self):
        QMainWindow.__init__(self)
        self.load_ui()

    def load_ui(self):
        self.central_widget = QWidget()
        self.central_layout = QVBoxLayout()

        self.tree_view = QTreeView()
        model = QStandardItemModel()

        root_item = model.invisibleRootItem()
        # Create child items
        child_item1 = QStandardItem("Child 1")
        child_item2 = QStandardItem("Child 2")
        root_item.appendRow(child_item1)
        root_item.appendRow(child_item2)

        # Create a subchild item
        subchild_item = QStandardItem("Subchild")
        child_item1.appendRow(subchild_item)

        # Create sub-subchild items
        sub_subchild_item1 = QStandardItem("Subchild 1")
        sub_subchild_item2 = QStandardItem("Subchild 2")
        sub_subchild_item3 = QStandardItem("Subchild 3")
        sub_subchild_item4 = QStandardItem("Subchild 4")
        subchild_item.appendRow(sub_subchild_item1)
        subchild_item.appendRow(sub_subchild_item2)
        subchild_item.appendRow(sub_subchild_item3)
        subchild_item.appendRow(sub_subchild_item4)

        self.tree_view.setModel(model)
        self.tree_view.setSelectionMode(QTreeView.SelectionMode.SingleSelection)

        self.temp_signal.connect(self.highlight_item)

        self.central_layout.addWidget(self.tree_view)
        self.button = QPushButton("Button")
        self.button.clicked.connect(self.click_button)
        self.central_layout.addWidget(self.button)

        self.button_h = QPushButton("button2")
        self.central_layout.addWidget(self.button_h)
        self.central_widget.setLayout(self.central_layout)
        self.setCentralWidget(self.central_widget)

    # def highlight_item(self, data):
    #     self.tree_view.clearSelection()
    #     print("HanhLT: data ", data)
    #     model = self.tree_view.model()
    #     for row in range(model.rowCount()):
    #         item = model.item(row)
    #         if item.text() == data:
    #             index = model.indexFromItem(item)
    #             selection_model = self.tree_view.selectionModel()
    #             selection = QItemSelection(index, index)
    #             selection_model.select(selection, QItemSelectionModel.ClearAndSelect)

    def highlight_item(self, data):
        self.tree_view.clearSelection()
        print("HanhLT: data ", data)

        # Find the item in the model
        item = self.find_item_by_text(self.tree_view.model().invisibleRootItem(), data)

        if item is not None:
            # Select the item and its descendants
            index = self.tree_view.model().indexFromItem(item)
            selection_model = self.tree_view.selectionModel()
            selection = QItemSelection(index, index)
            selection_model.select(selection, QItemSelectionModel.ClearAndSelect)
        else:
            print(f"Item with text '{data}' not found.")

    def find_item_by_text(self, parent_item, target_text):
        # Recursive function to find an item by text
        for row in range(parent_item.rowCount()):
            item = parent_item.child(row)
            if item.text() == target_text:
                return item
            # Recursively search in child items
            found_item = self.find_item_by_text(item, target_text)
            if found_item is not None:
                return found_item

        return None

    def click_button(self):

        self.temp_signal.emit("Subchild 1")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
