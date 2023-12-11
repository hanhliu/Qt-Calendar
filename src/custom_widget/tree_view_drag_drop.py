import sys

from PySide6.QtWidgets import QApplication, QTreeView, QLabel, QWidget, QVBoxLayout, QGridLayout, QMainWindow
from PySide6.QtCore import Qt, QMimeData,QByteArray, QDataStream, QIODevice
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
        tree_view = QTreeView()
        tree_view.setFixedHeight(200)
        tree_view.setModel(self.model)

        # Connect the signals for dragging
        def start_drag(index):
            item = self.model.itemFromIndex(index)
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
        grid_layout.setSpacing(1)
        # Largest item in the center

        ex_list = [{(0, 0), (0, 1), (1, 0), (1, 1)}, {(0, 3), (0, 2), (1, 2), (1, 3)}]
        all_excluded_positions = set.union(*ex_list)
        # Create items surrounding the largest_item
        for list_tuple in ex_list:
            min_row = min(row for row, _ in list_tuple)
            min_col = min(col for _, col in list_tuple)
            max_row = max(row for row, _ in list_tuple)
            max_col = max(col for _, col in list_tuple)

            row_span = max_row - min_row + 1
            col_span = max_col - min_col + 1
            largest_item = QLabelWidget(f"Large {min_row} {min_col}")
            largest_item.setStyleSheet('background-color: lightblue;')
            grid_layout.addWidget(largest_item, min_row, min_col, row_span, col_span)

            for row in range(4):
                for col in range(4):
                    if (row, col) in all_excluded_positions:
                        continue  # Skip the specified positions
                    label = QLabelWidget(f"Item {row} {col}")
                    label.setStyleSheet('background-color: lightblue;')
                    grid_layout.addWidget(label, row, col)

        position = grid_layout.getItemPosition(2)
        print("HanhLT: position   ", position)

        grid_widget = QWidget()
        grid_widget.setLayout(grid_layout)

        main_layout = QVBoxLayout()
        main_layout.addWidget(tree_view)
        main_layout.addWidget(grid_widget)
        mai_widget = QWidget()
        mai_widget.setLayout(main_layout)
        mai_widget.show()
        self.setCentralWidget(mai_widget)

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
