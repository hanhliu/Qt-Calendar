from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QGridLayout, QLabel

from stack_widget import StackedWidget

class MergedWidget(QWidget):
    def __init__(self, merged_items=None, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        # Create labels for each merged item
        for item in merged_items:
            label = QLabel(f'Merged Item {item}')
            self.layout.addWidget(label)

class GridWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.selected_items = []
        self.item_positions = {}
        self.load_ui()

    def load_ui(self):
        # create layout
        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(1)
        self.update_layout_structure()

        for i, row in enumerate(self.layout_structure):
            for j, item_type in enumerate(row):
                if item_type == 'StackedWidget':
                    cell_widget = StackedWidget()
                    cell_widget.clicked.connect(self.handle_item_click)
                    self.grid_layout.addWidget(cell_widget, i, j)
                elif item_type == 'MergedWidget':
                    merged_widget = MergedWidget(merged_items=['Merged Item'])
                    self.grid_layout.addWidget(merged_widget, i, j, merged_widget.layout.rowCount(), merged_widget.layout.columnCount())

        self.setLayout(self.grid_layout)

    def handle_item_click(self):
        sender = self.sender()  # Get the sender of the signal
        if sender not in self.selected_items:
            self.selected_items.append(sender)
            self.item_positions[sender] = (self.grid_layout.rowCount() - 1, self.grid_layout.columnCount() - 1)
        else:
            self.selected_items.remove(sender)
            del self.item_positions[sender]

        self.update_selection()

    def update_selection(self):
        if len(self.selected_items) > 1:
            # Replace the selected items with a MergedWidget
            merged_widget = MergedWidget(merged_items=[item.label.text() for item in self.selected_items])
            self.grid_layout.addWidget(merged_widget, 0, 0, 2, 2)  # Hardcoded span for illustration

            # Update the layout structure and recreate the layout
            self.update_layout_structure()
            self.create_layout_from_structure()

            # Clear the set of selected items
            self.selected_items.clear()

    def update_layout_structure(self):
        # Update the layout structure based on the current selected items
        self.layout_structure = [['StackedWidget'] * 3 for _ in range(3)]  # Default layout structure

        if len(self.selected_items) > 1:
            # If multiple items are selected, update the structure accordingly
            for item in self.selected_items:
                index = self.grid_layout.indexOf(item)
                row, col, rowspan, colspan = self.grid_layout.getItemPosition(index)
                for r in range(row, row + rowspan):
                    for c in range(col, col + colspan):
                        self.layout_structure[r][c] = 'MergedWidget'

    def create_layout_from_structure(self):
        # Remove all widgets from the layout
        for i in reversed(range(self.grid_layout.count())):
            item = self.grid_layout.itemAt(i)
            self.grid_layout.removeItem(item)
            widget = item.widget()
            if widget:
                widget.setParent(None)

        # Recreate the layout based on the updated structure
        for i, row in enumerate(self.layout_structure):
            for j, item_type in enumerate(row):
                if item_type == 'StackedWidget':
                    cell_widget = StackedWidget()
                    cell_widget.clicked.connect(self.handle_item_click)
                    self.grid_layout.addWidget(cell_widget, i, j)
                elif item_type == 'MergedWidget':
                    merged_widget = MergedWidget(merged_items=['Merged Item'])
                    self.grid_layout.addWidget(merged_widget, i, j, merged_widget.layout.rowCount(), merged_widget.layout.columnCount())


    def mousePressEvent(self, event):
        print("HanhLT: chay vao press ")
        pass

    def mouseMoveEvent(self, event):
        print("HanhLT: chay vao move")
        pass

    def mouseReleaseEvent(self, event):
        print("HanhLT: chay vao release ")
        pass

    def enterEvent(self, event):
        # self.setCursor(Qt.PointingHandCursor)
        pass
