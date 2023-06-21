from PySide6.QtCore import Qt, QMimeData
from PySide6.QtGui import QDrag, QStandardItemModel, QStandardItem
from PySide6.QtWidgets import QApplication, QTreeView, QAbstractItemView

class MyTreeView(QTreeView):
    def __init__(self):
        super().__init__()

        self.setDragEnabled(True)
        self.setSelectionMode(QAbstractItemView.SingleSelection)

        # Create a model and populate the tree view
        model = QStandardItemModel()
        root_item = model.invisibleRootItem()

        for i in range(5):
            item = QStandardItem(f"Item {i + 1}")
            root_item.appendRow(item)

        self.setModel(model)

    def mousePressEvent(self, event):
        # Override mousePressEvent to start the drag operation

        index = self.indexAt(event.pos())
        if index.isValid():
            item = self.model().itemFromIndex(index)
            if item and item.isDragEnabled():
                drag = QDrag(self)
                mime_data = QMimeData()
                mime_data.setText(item.text())
                drag.setMimeData(mime_data)
                drag.exec_(Qt.CopyAction)


app = QApplication([])
tree_view = MyTreeView()
tree_view.show()
app.exec()
