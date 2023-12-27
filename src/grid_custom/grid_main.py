import math
import sys

from PySide6.QtGui import QPainter, QPen, QColor
from PySide6.QtWidgets import QApplication, QWidget, QGridLayout, QFrame, QVBoxLayout, QComboBox, QPushButton, \
    QHBoxLayout, QDialog, QMenu, QListWidget, QListWidgetItem, QLabel, QMainWindow, QWidgetAction

from PySide6.QtCore import Qt, QRect,Signal

from src.grid_custom.dialog_tezt import DialogTezt
from src.grid_custom.item_list_widget import ItemGridType
from src.grid_custom.selectable_frame import SelectableFrame


class MenuGridType(QMenu):
    sizeSelected = Signal(object)
    def __init__(self, parent=None):
        super().__init__(parent)
        self.load_ui()

    def load_ui(self):
        # create layout
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignTop)

        custom_widget = QWidget(self)
        self.custom_layout = QVBoxLayout()
        # Create items for the list
        items = [
            {"title": "1", "image_path": "IMG1"},
            {"title": "4", "image_path": "IMG2"},
            {"title": "6", "image_path": "IMG3"},
            {"title": "8", "image_path": "IMG4"},
            {"title": "9", "image_path": "IMG5"},
            {"title": "13", "image_path": "IMG6"},
            {"title": "16", "image_path": "IMG7"},
            {"title": "25", "image_path": "IMG8"},
            {"title": "36", "image_path": "IMG10"},
            {"title": "64", "image_path": "IMG11"},
        ]

        self.label_standard = QLabel("Standard Window Division")
        self.label_custom = QLabel("Custom Window Division")

        self.grid_standard = QGridLayout()
        # Add items to the grid layout
        row_standard, col_standard = 0, 0
        for data in items:
            item_widget = ItemGridType(data["title"], data["image_path"], type_division="GRID_STANDARD")
            item_widget.emit_size_signal.connect(self.select_value)
            self.grid_standard.addWidget(item_widget, row_standard, col_standard)
            col_standard += 1
            if col_standard == 6:
                col_standard = 0
                row_standard += 1

        # self.grid_custom = QGridLayout()
        # row_wide, col_wide = 0, 0
        # item_widget = ItemGridType("Edit", "EDIT", type_division="GRID_CUSTOM")
        # self.grid_custom.addWidget(item_widget, row_wide, col_wide)

        self.button_edit_grid = QPushButton("Edit")
        self.button_edit_grid.clicked.connect(self.show_dialog)

        self.custom_layout.addWidget(self.label_standard)
        self.custom_layout.addLayout(self.grid_standard)
        self.custom_layout.addWidget(self.label_custom)
        # self.custom_layout.addLayout(self.grid_custom)
        self.custom_layout.addWidget(self.button_edit_grid)

        custom_widget.setLayout(self.custom_layout)
        # Create a QWidgetAction to add the custom widget to the QMenu
        custom_action = QWidgetAction(self)
        custom_action.setDefaultWidget(custom_widget)
        self.addAction(custom_action)
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint | Qt.WindowType.Popup)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)

    def select_value(self, value):
        self.sizeSelected.emit(int(value[0]))
        # self.close()

    def show_dialog(self):
        self.dialog = DialogTezt()
        self.dialog.exec_()

class MainGrid(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.load_ui()

    def load_ui(self):
        self.setFixedSize(1024, 576)
        # Create the menu and show it
        self.menu = MenuGridType(self)
        self.menu.sizeSelected.connect(self.update_grid_size)

        # Create a single main layout
        self.main_layout = QVBoxLayout()

        # Create a grid layout for the SelectableFrames
        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(0)

        # Create a SelectableFrame for each cell in the grid
        for i in range(8):
            for j in range(7):
                frame = SelectableFrame(self)
                self.grid_layout.addWidget(frame, i, j)

        # Add the grid layout to the main layout
        self.main_layout.addLayout(self.grid_layout)

        self.menu_button = QPushButton("Grid")
        self.menu_button.clicked.connect(self.show_menu)

        # Add the menu button to the main layout
        self.main_layout.addWidget(self.menu_button)

        # Create a central widget and set the main layout on it
        self.setLayout(self.main_layout)

    def update_grid_size(self, size):

        # Clear the existing grid layout
        for i in reversed(range(self.grid_layout.count())):
            item = self.grid_layout.takeAt(i)
            if item.widget():
                item.widget().deleteLater()

        sqrt_size = int(math.sqrt(size))
        if sqrt_size * sqrt_size != size:
            if size == 6:
                self.create_grid_layout(3, 0, 0, 2, [(0, 0), (0, 1), (1, 0), (1, 1)])
            elif size == 8:
                self.create_grid_layout(4, 0, 0, 3, [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)])
            elif size == 13:
                self.create_grid_layout(4, 1, 1, 2, [(1, 1), (1, 2), (2, 1), (2, 2)])
        else:
            # Create a new grid layout with the updated size
            for i in range(sqrt_size):
                for j in range(sqrt_size):
                    frame = SelectableFrame(self)
                    self.grid_layout.addWidget(frame, i, j)

        # Update the main layout
        # self.setLayout(self.main_layout)
        self.update()

    def create_grid_layout(self, size, rows_start, cols_start, span, excluded_positions=None):
        # Create the largest item and add it to the grid layout
        largest_item = SelectableFrame(self)
        self.grid_layout.addWidget(largest_item, rows_start, cols_start, span, span)

        # Create items surrounding the largest item
        for row in range(size):
            for col in range(size):
                if (row, col) in excluded_positions:
                    continue  # Skip the specified positions
                item = SelectableFrame(self)
                self.grid_layout.addWidget(item, row, col)

    def show_menu(self):
        # Get the global position of the button
        position = self.menu_button.mapToGlobal(self.menu_button.rect().bottomLeft())
        self.menu.exec_(position)

    def paintEvent(self, event):
        painter = QPainter(self)

        # Draw the grid frames
        for i in range(self.grid_layout.count()):
            frame = self.grid_layout.itemAt(i).widget()
            rect = frame.geometry()
            row, col, _, _ = self.grid_layout.getItemPosition(i)
            painter.setPen(QPen(QColor(0, 0, 0), 2))
            painter.drawRect(rect)

