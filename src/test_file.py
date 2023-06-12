from PySide6.QtWidgets import QApplication, QWidget, QGridLayout, QLabel, QPushButton, QStackedWidget, QTreeView, QAbstractItemView, QVBoxLayout
from PySide6.QtGui import QStandardItemModel, QStandardItem, QDrag
from PySide6.QtCore import Qt, QMimeData, QPoint


class DraggableLabel(QLabel):
    def __init__(self, text, position):
        super().__init__(text)
        self.position = position
        self.setAcceptDrops(True)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            drag = QDrag(self)
            mime_data = QMimeData()
            mime_data.setText(self.text())
            drag.setMimeData(mime_data)
            drag.exec_(Qt.MoveAction)

    def dragEnterEvent(self, event):
        print("HanhLT: accent drag Enter Event")
        if event.mimeData().hasFormat("text/plain"):
            event.acceptProposedAction()

    def dropEvent(self, event):
        print("HanhLT: accept drop event")
        mime_data = event.mimeData()
        if mime_data.hasText():
            print("HanhLT: mim data hasText  ")
            text = mime_data.text()
            event.acceptProposedAction()
            # Find the position of the dropped label in the grid layout
            position = self.position

            # Create a new QLabel with the dropped text
            new_label = QLabel(text)

            # Add the new QLabel to the QStackedWidget
            stacked_widget = self.parent()
            stacked_widget.addWidget(new_label)
            stacked_widget.setCurrentWidget(new_label)

            print(
                f"Added new QLabel with text '{text}' to the QStackedWidget at position: row={position.x()}, column={position.y()}")

        # Get the position of the dropped label from the custom property
            # position = self.property("position")
            # if position is not None:
            #     grid_position = position
            #     print(
            #         f"Added new QLabel with text '{text}' to the QStackedWidget at position: row={grid_position.x()}, column={grid_position.y()}")
            #
            #     # Create a new QLabel with the dropped text
            #     new_label = QLabel(text)
            #
            #     # Add the new QLabel to the QStackedWidget
            #     stacked_widget = self.parent().parent()
            #     stacked_widget.addWidget(new_label)
            #     stacked_widget.setCurrentWidget(new_label)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Create a QVBoxLayout to hold the tree view and the grid layout
        layout = QVBoxLayout(self)

        # Create a QTreeView
        self.tree_view = QTreeView(self)
        self.tree_view.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tree_view.setDragEnabled(True)
        self.tree_view.setAcceptDrops(False)
        self.tree_view.setDragDropMode(QAbstractItemView.InternalMove)
        self.tree_view.pressed.connect(self.start_drag)

        # Create a QStandardItemModel for the tree view
        self.tree_model = QStandardItemModel(self)
        self.tree_view.setModel(self.tree_model)

        # Add five QLabel items to the tree view
        for i in range(5):
            item = QStandardItem(f"Label {i+1}")
            self.tree_model.appendRow(item)

        # Add the tree view to the layout
        layout.addWidget(self.tree_view)

        # Create a QGridLayout
        grid_layout = QGridLayout()

        # Add four QStackedWidget items to the grid layout
        for i in range(16):
            # Create a QStackedWidget
            stacked_widget = QStackedWidget()

            # Create a QLabel and QPushButton
            label = DraggableLabel(f"Label {i+1}",  QPoint(i // 4, i % 4))
            button = QPushButton(f"Button {i+1}")

            # Add the QLabel and QPushButton to the QStackedWidget
            stacked_widget.addWidget(label)
            stacked_widget.addWidget(button)

            # Set the current widget in the QStackedWidget
            stacked_widget.setCurrentIndex(0)

            # Set the custom property to store the position
            label.setProperty("position", QPoint(i // 4, i % 4))

            # Add the QStackedWidget to the grid layout
            grid_layout.addWidget(stacked_widget, i // 4, i % 4)

        # Add the grid layout to the layout
        layout.addLayout(grid_layout)

        # Set the layout for the main window
        self.setLayout(layout)

    # Connect the signals for dragging
    def start_drag(self, index):
        print("HanhLT: start drag  ")
        item = self.tree_model.itemFromIndex(index)
        if item is not None and item.isDragEnabled():
            drag = QDrag(self.tree_view)
            mime_data = QMimeData()
            mime_data.setText(item.text())
            drag.setMimeData(mime_data)
            drag.exec(Qt.CopyAction)

# Create a Qt application
app = QApplication([])
window = MainWindow()
window.show()
app.exec()



