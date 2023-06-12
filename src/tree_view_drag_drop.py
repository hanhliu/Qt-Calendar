from PySide6.QtWidgets import QApplication, QTreeView, QLabel, QWidget, QVBoxLayout, QGridLayout
from PySide6.QtCore import Qt, QMimeData,QByteArray, QDataStream, QIODevice
from PySide6.QtGui import QDrag,  QStandardItemModel, QStandardItem


class QLabelWidget(QWidget):
    def __init__(self, label_content="Item Target"):
        super().__init__()
        self.label = label_content
        self.setWindowTitle("Drop Target")
        self.layout = QVBoxLayout()
        self.setFixedSize(200, 100)
        self.label = QLabel(self.label)
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat("text/plain"):
            event.acceptProposedAction()

    def dropEvent(self, event):
        mime_data = event.mimeData()
        if mime_data.hasText():
            text = mime_data.text()
            self.label.setText(text)
            event.acceptProposedAction()

# Create a Qt application
app = QApplication([])

# Create a QStandardItemModel
model = QStandardItemModel()

# Create the root item
root_item = QStandardItem("Root")
model.appendRow(root_item)

# Create 5 child items
for i in range(5):
    label = QLabel(f"Item {i+1}")
    item = QStandardItem(label.text())
    item.setDragEnabled(True)  # Enable dragging for items
    model.appendRow(item)

# Create the tree view and set the model
tree_view = QTreeView()
tree_view.setModel(model)

# Connect the signals for dragging
def start_drag(index):
    item = model.itemFromIndex(index)
    if item is not None and item.isDragEnabled():
        drag = QDrag(tree_view)
        mime_data = QMimeData()
        mime_data.setText(item.text())
        drag.setMimeData(mime_data)
        drag.exec(Qt.CopyAction)

tree_view.viewport().setAcceptDrops(True)
tree_view.setDragEnabled(True)
tree_view.setDragDropMode(QTreeView.DragOnly)
tree_view.setSelectionMode(QTreeView.SingleSelection)
tree_view.setSelectionBehavior(QTreeView.SelectRows)
tree_view.setDragDropOverwriteMode(False)
tree_view.setDropIndicatorShown(True)
tree_view.pressed.connect(start_drag)


grid_layout = QGridLayout()
# Create the target QWidget (QLabelWidget)
label_1 = QLabelWidget(label_content="Label 1")
grid_layout.addWidget(label_1, 0, 0)
label_2 = QLabelWidget(label_content="Label 2")
grid_layout.addWidget(label_2, 0, 1)
label_3 = QLabelWidget(label_content="Label 3")
grid_layout.addWidget(label_3, 1, 0)
label_4 = QLabelWidget(label_content="Label 4")
grid_layout.addWidget(label_4, 1, 1)

grid_widget = QWidget()
grid_widget.setLayout(grid_layout)

main_layout = QVBoxLayout()
main_layout.addWidget(tree_view)
main_layout.addWidget(grid_widget)
mai_widget = QWidget()
mai_widget.setLayout(main_layout)
mai_widget.show()

# Run the event loop
app.exec()
