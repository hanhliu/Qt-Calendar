import sys

from PySide6.QtWidgets import QApplication, QTreeView, QLabel, QWidget, QVBoxLayout, QGridLayout, QMainWindow, \
    QStyledItemDelegate
from PySide6.QtCore import Qt, QMimeData,QByteArray, QDataStream, QIODevice
from PySide6.QtGui import QDrag,  QStandardItemModel, QStandardItem


class QtCheckStateRole:
    pass


class CheckDelegate(QStyledItemDelegate):
    def editorEvent(self, event, model, option, index):
        if event.button() == Qt.LeftButton:
            item = model.itemFromIndex(index)
            if item.isCheckable():
                # Toggle the check state
                new_check_state = Qt.Checked if item.checkState() == Qt.Unchecked else Qt.Unchecked
                item.setCheckState(new_check_state)
                model.setData(index, new_check_state, QtCheckStateRole)  # Update item's data
            return True
        return super().editorEvent(event, model, option, index)

class CustomTreeView(QTreeView):
    def __init__(self):
        super().__init__()

    def mousePressEvent(self, event):
        index = self.indexAt(event.pos())
        if index.isValid():
            item = self.model().itemFromIndex(index)
            if item.isCheckable():
                item.setCheckState(Qt.Checked if item.checkState() == Qt.Unchecked else Qt.Unchecked)
                return  # Prevent the default behavior
        super().mousePressEvent(event)

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.load_ui()

    def load_ui(self):
        # Create a QStandardItemModel
        # Create a standard item model
        self.model = QStandardItemModel()
        # Create root item
        root_item = QStandardItem("Root")
        root_item.setCheckable(True)
        self.model.appendRow(root_item)

        # Create child items
        child_item1 = QStandardItem("Child 1")
        child_item1.setCheckable(True)
        child_item2 = QStandardItem("Child 2")
        child_item2.setCheckable(True)
        root_item.appendRow(child_item1)
        root_item.appendRow(child_item2)

        # Create a subchild item
        subchild_item = QStandardItem("Subchild")
        subchild_item.setCheckable(True)
        child_item1.appendRow(subchild_item)

        # Create sub-subchild items
        sub_subchild_item1 = QStandardItem("Subchild 1")
        sub_subchild_item1.setCheckable(True)
        sub_subchild_item2 = QStandardItem("Subchild 2")
        sub_subchild_item2.setCheckable(True)
        sub_subchild_item3 = QStandardItem("Subchild 3")
        sub_subchild_item3.setCheckable(True)
        sub_subchild_item4 = QStandardItem("Subchild 4")
        sub_subchild_item4.setCheckable(True)
        subchild_item.appendRow(sub_subchild_item1)
        subchild_item.appendRow(sub_subchild_item2)
        subchild_item.appendRow(sub_subchild_item3)
        subchild_item.appendRow(sub_subchild_item4)

        # Create the tree view and set the model
        tree_view = CustomTreeView()
        tree_view.setModel(self.model)
        # tree_view.setItemDelegate(CheckDelegate())
        tree_view.setSelectionMode(QTreeView.SingleSelection)
        tree_view.setSelectionBehavior(QTreeView.SelectRows)
        tree_view.setDragDropOverwriteMode(False)

        main_layout = QVBoxLayout()
        main_layout.addWidget(tree_view)
        mai_widget = QWidget()
        mai_widget.setLayout(main_layout)
        mai_widget.show()
        self.setCentralWidget(mai_widget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
