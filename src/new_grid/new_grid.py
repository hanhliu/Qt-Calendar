import os
import sys

from PySide6.QtCore import Qt, QMimeData
from PySide6.QtGui import QDrag, QDropEvent, QDragEnterEvent
from PySide6.QtWidgets import QWidget, QMainWindow, QApplication, QVBoxLayout, QGridLayout, QPushButton, QLabel, \
    QStackedWidget

from grid_layout import GridWidget

class ItemGrid(QStackedWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.load_ui()
        self.setAcceptDrops(True)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            item_grid = self.childAt(event.position().toPoint())
            print(" item_grid = ", item_grid)
            if isinstance(item_grid, QLabel):
                # Start the drag operation
                drag = QDrag(self)
                mime_data = QMimeData()
                mime_data.setText(item_grid.text())
                drag.setMimeData(mime_data)
                # Execute the drag operation
                drag.exec()

    def mouseMoveEvent(self, event):
        if not (event.buttons() & Qt.LeftButton):
            return

        mime_data = QMimeData()
        drag = QDrag(self)
        drag.setMimeData(mime_data)
        drag.setHotSpot(event.position())

        drop_action = drag.exec(Qt.MoveAction)

    def dragEnterEvent(self, event: QDragEnterEvent):
        event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        if event.mimeData().hasText():
            dropped_text = event.mimeData().text()
            print(f"Item Dropped: {dropped_text}")
            event.acceptProposedAction()

    def load_ui(self):
        self.label = QLabel()
        self.setStyleSheet('background-color: lightblue;')
        self.addWidget(self.label)


class NewGrid(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.load_ui()

    def load_ui(self):
        self.central_widget = QWidget()
        self.central_widget.setFixedSize(1024, 576)
        self.central_layout = QVBoxLayout()
        self.central_layout.setContentsMargins(0, 0, 0, 0)

        grid_layout = QGridLayout()
        grid_layout.setSpacing(1)
        grid_layout.setContentsMargins(0, 0, 0, 0)

        array_custom = [
            {(0, 1), (1, 0), (1, 1), (0, 0)}
        ]

        new_data = []
        for item in array_custom:
            list_to_tuple = set()
            if isinstance(item, list):
                for list_item in item:
                    list_to_tuple.add(tuple(list_item))
                new_data.append(set(list_to_tuple))
            else:
                new_data.append(set(item))

        all_excluded_positions = set.union(*new_data)

        # Get the number of rows and columns in the grid
        rows = 4
        cols = 4

        # Calculate the width and height of each cell
        cell_width = int((self.central_widget.width()-1) / cols)
        cell_height = int((self.central_widget.height()-1) / rows)

        # Create items surrounding the largest_item
        for row in range(rows):
            for col in range(cols):
                if (row, col) in all_excluded_positions:
                    continue  # Skip the specified positions

                camera_frame_small = ItemGrid()
                camera_frame_small.label.setText(f"row - {row}, col - {col}")
                camera_frame_small.setFixedSize(cell_width, cell_height)
                grid_layout.addWidget(camera_frame_small, row, col)

        # Create items based on new_data
        for list_tuple in new_data:
            min_row = min(row for row, _ in list_tuple)
            min_col = min(col for _, col in list_tuple)
            max_row = max(row for row, _ in list_tuple)
            max_col = max(col for _, col in list_tuple)

            row_span = max_row - min_row + 1
            col_span = max_col - min_col + 1

            item_width = col_span * cell_width
            item_height = row_span * cell_height

            largest_item = ItemGrid()
            largest_item.label.setText("Largest Item")
            largest_item.setFixedSize(item_width, item_height)
            grid_layout.addWidget(largest_item, min_row, min_col, row_span, col_span)

        self.central_layout.addLayout(grid_layout)
        self.central_widget.setLayout(self.central_layout)
        self.setCentralWidget(self.central_widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NewGrid()
    window.show()
    sys.exit(app.exec())
