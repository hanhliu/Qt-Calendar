import sys

from PySide6.QtWidgets import QApplication, QTreeView, QLabel, QWidget, QVBoxLayout, QGridLayout, QMainWindow
from PySide6.QtCore import Qt, QMimeData, QByteArray, QDataStream, QIODevice, QEvent
from PySide6.QtGui import QDrag,  QStandardItemModel, QStandardItem


class QLabelWidget(QWidget):
    def __init__(self, label_content="Item Target"):
        super().__init__()
        self.label = label_content
        self.setWindowTitle("Drop Target")
        self.layout = QVBoxLayout()
        # self.setStyleSheet('background-color: lightblue;')
        # self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.label)
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)
        self.setAcceptDrops(True)
        self.order_counter = 0

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat("text/plain"):
            event.acceptProposedAction()

    def dropEvent(self, event):
        mime_data = event.mimeData()
        if mime_data.hasText():
            text = mime_data.text()
            self.label.setText(text)
            event.acceptProposedAction()

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setGeometry(100, 100, 800, 600)
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

        # Create the tree view and set the model
        self.tree_view = QTreeView()
        self.tree_view.setObjectName("treevieww")
        self.tree_view.installEventFilter(self)
        self.tree_view.setFixedHeight(200)
        self.tree_view.setModel(self.model)

        # Connect the signals for dragging
        def start_drag(index):
            item = self.model.itemFromIndex(index)
            if item is not None and item.isDragEnabled():
                drag = QDrag(self.tree_view)
                mime_data = QMimeData()
                mime_data.setText(item.text())
                drag.setMimeData(mime_data)
                drag.exec(Qt.CopyAction)


        self.tree_view.viewport().setAcceptDrops(True)
        self.tree_view.setDragEnabled(True)
        self.tree_view.setDragDropMode(QTreeView.DragOnly)
        self.tree_view.setSelectionMode(QTreeView.SingleSelection)
        self.tree_view.setSelectionBehavior(QTreeView.SelectRows)
        self.tree_view.setDragDropOverwriteMode(False)
        self.tree_view.setDropIndicatorShown(True)
        self.tree_view.pressed.connect(start_drag)

        grid_layout = QGridLayout()
        grid_layout.setSpacing(1)
        # Largest item in the center
        ex_list = [{(0, 0), (0, 1), (1, 0), (1, 1)}, {(2, 2), (2, 3), (3, 2), (3, 3)}]

        # ex_list = [{(0, 0), (0, 1), (1, 0), (1, 1)}, {(0, 3), (0, 2), (1, 2), (1, 3)}]
        # ex_list = [{(2, 1), (2, 2), (1, 2), (1, 1)}]
        all_excluded_positions = set.union(*ex_list)
        # Create items surrounding the largest_item
        for list_tuple in ex_list:
            min_row = min(row for row, _ in list_tuple)
            min_col = min(col for _, col in list_tuple)
            max_row = max(row for row, _ in list_tuple)
            max_col = max(col for _, col in list_tuple)

            largest_item_rows = max_row - min_row + 1
            largest_item_cols = max_col - min_col + 1

            # all_excluded_positions = set.union(*excluded_positions)

            # Create items in the grid
            for row in range(4):
                for col in range(4):
                    if (row, col) == (min_row, min_col):
                        # Add the largest item
                        largest_item = QLabelWidget(f"Large {row} {col}")
                        largest_item.setStyleSheet('background-color: lightblue;')
                        grid_layout.addWidget(largest_item, row, col, largest_item_rows, largest_item_cols)

        for row in range(4):
            for col in range(4):
                if (row, col) in all_excluded_positions:
                    continue  # Skip positions covered by largest items
                label = QLabelWidget(f"Item {row} {col}")
                label.setStyleSheet('background-color: lightblue;')
                grid_layout.addWidget(label, row, col)

        # Create a list to store widgets and their positions
        widget_positions = []

        # Populate the list with widgets and their positions
        for index in range(grid_layout.count()):
            item = grid_layout.itemAt(index)
            row, col, row_span, col_span = grid_layout.getItemPosition(index)
            widget_positions.append((item.widget(), row, col, row_span, col_span))

        # Sort the list based on positions
        widget_positions.sort(key=lambda x: (x[1], x[2]))

        # Clear the existing widgets from the layout
        for i in reversed(range(grid_layout.count())):
            widget = grid_layout.itemAt(i).widget()
            grid_layout.removeWidget(widget)
            widget.setParent(None)

        # Rearrange widgets in the layout
        for new_index, (widget, row, col, row_span, col_span) in enumerate(widget_positions):
            grid_layout.addWidget(widget, row, col, row_span, col_span)

            # Optionally, set row and column stretch to manage spacing
            grid_layout.setRowStretch(row, 1)
            grid_layout.setColumnStretch(col, 1)

        # Update the layout
        grid_layout.update()

        # for index in range(grid_layout.count()):
        #     item = grid_layout.itemAt(index)
        #     row, col, row_span, col_span = grid_layout.getItemPosition(index)
        #
        #     # Now you have information about the item and its position
        #     print(f"Grid count {grid_layout.count()}   Item at position ({row}, {col}) with span ({row_span} rows, {col_span} columns) with index {index}")
        #
        #     # Access the widget associated with the item
        #     widget = item.widget()
        #     #
        #     # # Do something with the widget, if needed
        #     # if widget is not None:
        #     #     print("HanhLT: widget  ", widget)

        grid_widget = QWidget()
        grid_widget.setLayout(grid_layout)
        grid_widget.setObjectName("grid")
        grid_widget.installEventFilter(self)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.tree_view)
        main_layout.addWidget(grid_widget)
        mai_widget = QWidget()
        mai_widget.setLayout(main_layout)
        mai_widget.installEventFilter(self)
        self.setCentralWidget(mai_widget)

    def eventFilter(self, obj, event):
        if obj.objectName() == "treevieww":
            if event.type() == QEvent.Type.MouseButtonPress:
                print(f"HanhLT: press")
        if obj.objectName() == "grid":
            if event.type() == QEvent.Type.MouseButtonDblClick:
                print(f"HanhLT: gridd")

        return super().eventFilter(obj, event)

    def get_index(self, target_row, target_col, grid):
        for index in range(grid.count()):
            item = grid.itemAt(index)
            row, col, row_span, col_span = grid.getItemPosition(index)

            # Check if the target position is within the span of the item
            if (
                    row <= target_row < row + row_span
                    and col <= target_col < col + col_span
            ):
                return index
        # If no item is found within the span, calculate the index
        index_calculated = target_row * grid.columnCount() + target_col
        return index_calculated

    def handle_drop_event(self, dictionary, current_key, new_value):
        keys = list(dictionary.keys())
        if current_key in keys and not new_value in dictionary.values():
            print("HanhLT: case 1")

            keys = list(dictionary.keys())

            new_keys = [key + 1 if key >= current_key else key for key in keys]
            new_keys.insert(current_key, current_key)

            new_dict = {new_key: dictionary[key] for new_key, key in zip(new_keys, keys)}
            new_dict[current_key] = new_value

            dictionary.clear()
            dictionary.update(new_dict)

        elif current_key in keys and new_value in dictionary.values():
            # Case 2: Swap places with another item if new_value already exists
            for key, value in dictionary.items():
                print("HanhLT: case 2")
                if value == new_value:
                    dictionary[current_key], dictionary[key] = dictionary[key], dictionary[current_key]
                    break
        else:
            print("HanhLT: case 3")
            # Case 3: Drop to an empty position
            dictionary[current_key] = new_value

        print("HanhLT: dictionary  ", dictionary)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
