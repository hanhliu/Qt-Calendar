import math
import sys

from PySide6.QtGui import QPainter, QPen, QColor, QStandardItemModel
from PySide6.QtWidgets import QApplication, QWidget, QGridLayout, QFrame, QVBoxLayout, QComboBox, QPushButton, \
    QHBoxLayout, QDialog, QMenu, QListWidget, QListWidgetItem, QLabel, QMainWindow, QWidgetAction, QListView

from PySide6.QtCore import Qt, QRect, Signal

from src.common_controller.common_qsettings import CommonQSettings
from src.common_controller.main_controller import MainController
from src.grid_custom.dialog_tezt import DialogTezt
from src.grid_custom.item_grid_model import ItemGridModel
from src.grid_custom.item_list_in_menu import ItemGridType
from src.grid_custom.selectable_frame import SelectableFrame


class MenuGridType(QMenu):
    signal_emit_size = Signal(object)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_controller = MainController()
        self.main_controller.list_divisions = CommonQSettings.get_instance().get_data_grid()
        self.load_ui()

    def load_ui(self):
        self.dialog = DialogTezt(list_divisions=self.main_controller.list_divisions)
        self.dialog.signal_save_trigger.connect(self.reload_grid_menu)
        self.load_standard_grid()
        self.load_custom_grid(self.main_controller.list_divisions)

        # create layout
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignTop)

        custom_widget = QWidget(self)
        self.custom_layout = QVBoxLayout()
        self.label_standard = QLabel("Standard Window Division")
        self.label_custom = QLabel("Custom Window Division")

        self.button_edit_grid = QPushButton("Edit")
        self.button_edit_grid.clicked.connect(self.show_dialog)
        self.grid_custom.addWidget(self.button_edit_grid, 1, 0)

        self.custom_layout.addWidget(self.label_standard)
        self.custom_layout.addLayout(self.grid_standard)
        self.custom_layout.addWidget(self.label_custom)
        self.custom_layout.addLayout(self.grid_custom)
        # self.custom_layout.addWidget(self.button_edit_grid)

        custom_widget.setLayout(self.custom_layout)
        # Create a QWidgetAction to add the custom widget to the QMenu
        custom_action = QWidgetAction(self)
        custom_action.setDefaultWidget(custom_widget)
        self.addAction(custom_action)
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint | Qt.WindowType.Popup)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)

    def load_standard_grid(self):
        standard_grid_models = [
            ItemGridModel(name="1", data=[], grid_count=1, row=1, column=1, image_url="url1"),
            ItemGridModel(name="4", data=[], grid_count=4, row=2, column=2, image_url="url4"),
            ItemGridModel(name="9", data=[], grid_count=9, row=3, column=3, image_url="url9"),
            ItemGridModel(name="16", data=[], grid_count=16, row=4, column=4, image_url="url16"),
            ItemGridModel(name="36", data=[], grid_count=36, row=6, column=6, image_url="url36"),
            ItemGridModel(name="64", data=[], grid_count=64, row=8, column=8, image_url="url64"),
        ]

        self.grid_standard = QGridLayout()
        self.grid_standard.setSpacing(2)
        # Add items to the grid layout
        row_standard, col_standard = 0, 0
        for data in standard_grid_models:
            item_widget = ItemGridType(model_grid=data, type_division="STANDARD_DIVISION")
            item_widget.emit_size_signal.connect(self.select_value)
            self.grid_standard.addWidget(item_widget, row_standard, col_standard)
            col_standard += 1
            if col_standard == 4:
                col_standard = 0
                row_standard += 1

    def load_custom_grid(self, list_grid):
        self.grid_custom = QGridLayout()
        row_custom, col_custom = 0, 0
        for data_custom in list_grid:
            print("HanhLT: data_custom  ", data_custom.grid_count)
            widget_custom = ItemGridType(model_grid=data_custom, type_division="CUSTOM_DIVISIONS")
            widget_custom.emit_size_signal.connect(self.select_value)
            self.grid_custom.addWidget(widget_custom, row_custom, col_custom)
            col_custom += 1
            if col_custom == 4:
                col_custom = 0
                row_custom += 1

    def reload_grid_menu(self, list_reload):
        for i in reversed(range(self.grid_custom.count())):
            widget = self.grid_custom.itemAt(i).widget()
            self.grid_custom.removeWidget(widget)
            widget.setParent(None)

        row_custom, col_custom = 0, 0
        for data_custom in list_reload:
            print("HanhLT: data_custom  ", data_custom.grid_count)
            widget_custom = ItemGridType(model_grid=data_custom, type_division="CUSTOM_DIVISIONS")
            widget_custom.emit_size_signal.connect(self.select_value)
            self.grid_custom.addWidget(widget_custom, row_custom, col_custom)
            col_custom += 1
            if col_custom == 6:
                col_custom = 0
                row_custom += 1

    def select_value(self, value):
        self.signal_emit_size.emit(value)
        # self.close()

    def show_dialog(self):
        self.dialog.exec_()


class MainGridTwo(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.load_ui()

    def load_ui(self):
        self.setFixedSize(1024, 768)
        # Create the menu and show it
        self.menu = MenuGridType(self)
        self.menu.signal_emit_size.connect(self.update_grid_size)

        # Create a single main layout
        self.main_layout = QVBoxLayout()

        # Create a grid layout for the SelectableFrames
        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(0)

        # Create a SelectableFrame for each cell in the grid
        for i in range(4):
            for j in range(4):
                frame = SelectableFrame(self)
                self.grid_layout.addWidget(frame, i, j)

        # Add the grid layout to the main layout
        self.main_layout.addLayout(self.grid_layout)

        self.menu_button = QPushButton("Grid")
        self.menu_button.clicked.connect(self.show_menu)

        # self.item_divisions = [
        #     ItemGridModel(name=f"6 Divisions", data=[{(0, 1), (1, 0), (1, 1), (0, 0)}], row=3, column=3, grid_count=6),
        #     ItemGridModel(name=f"8 Divisions",
        #                   data=[{(0, 1), (1, 2), (2, 1), (0, 0), (1, 1), (2, 0), (0, 2), (2, 2), (1, 0)}], row=4,
        #                   column=4, grid_count=8),
        #     ItemGridModel(name=f"10 Divisions",
        #                   data=[{(0, 1), (1, 0), (1, 1), (0, 0)}, {(1, 2), (0, 2), (0, 3), (1, 3)}], row=4, column=4,
        #                   grid_count=10),
        #     ItemGridModel(name=f"13 Divisions", data=[{(1, 1), (1, 2), (2, 1), (2, 2)}], row=4, column=4, grid_count=13)
        # ]
        #
        # self.dialog = DialogTezt(list_divisions=self.item_divisions)
        # self.main_layout.addWidget(self.dialog)

        # Add the menu button to the main layout
        self.main_layout.addWidget(self.menu_button)

        # Create a central widget and set the main layout on it
        self.setLayout(self.main_layout)

    def update_grid_size(self, data):
        model: ItemGridModel = data[0]
        type_grid = data[1]
        size = model.grid_count
        row = model.row
        col = model.column
        data_merge = model.data
        if type_grid == "STANDARD_DIVISION":
            self.create_standard_divisions(row, col)
        elif type_grid == "CUSTOM_DIVISIONS":
            self.create_custom_divisions(rows=row, cols=col, span_data=data_merge)

        self.update()

    def create_standard_divisions(self, rows, cols):
        for i in reversed(range(self.grid_layout.count())):
            item = self.grid_layout.takeAt(i)
            if item.widget():
                item.widget().deleteLater()

        # Create a new grid layout with the updated size
        for i in range(rows):
            for j in range(cols):
                frame = SelectableFrame(self)
                self.grid_layout.addWidget(frame, i, j)

    def create_custom_divisions(self, rows, cols, span_data):
        for i in reversed(range(self.grid_layout.count())):
            item = self.grid_layout.takeAt(i)
            if item.widget():
                item.widget().deleteLater()

        self.span_and_create_custom_divisions(size=rows, excluded_positions=span_data)

    def span_and_create_custom_divisions(self, size=None, excluded_positions=None):
        if excluded_positions is not None:
            all_excluded_positions = set.union(*excluded_positions)
            for list_tuple in excluded_positions:
                # Determine min_row, min_col, and span for the current largest_item
                min_row = min(row for row, _ in list_tuple)
                min_col = min(col for _, col in list_tuple)
                max_row = max(row for row, _ in list_tuple)
                max_col = max(col for _, col in list_tuple)

                row_span = max_row - min_row + 1
                col_span = max_col - min_col + 1
                # Create the largest_item and add it to the grid layout
                largest_item = SelectableFrame(self)
                self.grid_layout.addWidget(largest_item, min_row, min_col, row_span, col_span)

                # Create items surrounding the largest_item
                for row in range(size):
                    for col in range(size):
                        if (row, col) in all_excluded_positions:
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
        painter.end()
