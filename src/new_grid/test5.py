import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QFrame, QVBoxLayout, QComboBox, QPushButton, \
    QHBoxLayout, QDialog, QMenu, QLabel, QMainWindow, QWidgetAction
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import Qt, QRect

from src.grid_custom.item_list_widget import ItemGridType


class SelectableFrame(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.is_selected = False

class DrawingWidget(QWidget):
    def __init__(self,size_grid=4):
        super().__init__()
        self.paint_borders = False
        self.testFlag = False
        self.size_grid = size_grid
        self.setFixedSize(800, 600)
        self.grid_layout = QGridLayout(self)
        self.grid_layout.setSpacing(0)

        # Create a SelectableFrame for each cell in the grid
        for i in range(self.size_grid):
            for j in range(self.size_grid):
                frame = SelectableFrame(self)
                self.grid_layout.addWidget(frame, i, j)

        self.selection_start = None
        self.selection_end = None
        self.selected_frames = set()  # Use a set to store the row and column indices of selected frames
        self.merged_frame = []

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.testFlag = True
            self.selection_start = event.pos()
            self.selection_end = event.pos()

            for i in range(self.grid_layout.count()):
                frame = self.grid_layout.itemAt(i).widget()
                frame.is_selected = False
                frame.update()

            self.selected_frames = set()  # Reset the set when a new selection starts
            self.update()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            self.selection_end = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            # Get the bounding rectangle of the selection
            selection_rect = QRect(self.selection_start, self.selection_end).normalized()

            for i in range(self.grid_layout.count()):
                frame = self.grid_layout.itemAt(i).widget()
                rect = frame.geometry()

                # Check if the frame intersects with the selection rectangle
                if rect.intersects(selection_rect):
                    row, col, _, _ = self.grid_layout.getItemPosition(i)
                    self.selected_frames.add((row, col))
                    frame.is_selected = True
                    frame.update()

            print("Selected frames:", self.selected_frames)
            # Clear the drawn rectangle
            self.selection_start = None
            self.selection_end = None
            self.testFlag = False
            # Redraw the widgets
            self.update()

    def paintEvent(self, event):
        painter = QPainter(self)

        # Draw the grid frames
        for i in range(self.grid_layout.count()):
            frame = self.grid_layout.itemAt(i).widget()
            rect = frame.geometry()
            row, col, _, _ = self.grid_layout.getItemPosition(i)
            if any((row, col) in frame for frame in self.merged_frame):
                if self.paint_borders:
                    painter.setPen(QPen(QColor(0, 0, 0), 1, Qt.DashLine))
                    # Draw bottom edge
                    painter.drawLine(rect.bottomLeft(), rect.bottomRight())
                    # Draw left edge
                    painter.drawLine(rect.bottomLeft(), rect.topLeft())
                else:
                    painter.setPen(QPen(QColor(0, 0, 0), 2))
                    painter.drawRect(rect)
            # Draw the original grid frames
            else:
                painter.setPen(QPen(QColor(0, 0, 0), 2))
                painter.drawRect(rect)

        # Draw the overlay rectangle
        if self.selection_start is not None and self.selection_end is not None:
            painter.setPen(QPen(QColor(0, 0, 255), 1, Qt.DashLine))
            overlay_rect = QRect(self.selection_start, self.selection_end).normalized()
            painter.drawRect(overlay_rect)

        # Draw a red border around the total selected area
        if self.selected_frames and not self.testFlag:
            min_row = min(row for row, _ in self.selected_frames)
            max_row = max(row for row, _ in self.selected_frames)
            min_col = min(col for _, col in self.selected_frames)
            max_col = max(col for _, col in self.selected_frames)

            # Calculate the position and size of the bounding rectangle
            start_rect = self.grid_layout.itemAtPosition(min_row, min_col).geometry().topLeft()
            end_rect = self.grid_layout.itemAtPosition(max_row, max_col).geometry().bottomRight()

            total_rect = QRect(start_rect, end_rect)
            painter.setPen(QPen(QColor(255, 0, 0), 2))
            painter.drawRect(total_rect)


class Tezt(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.load_ui()

    def load_ui(self):
        # create layout
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignTop)
        self.combo_box = QComboBox()
        self.combo_box.addItems(["2x2", "3x3", "4x4", "6x6"])
        default_index = self.combo_box.findText("3x3")
        self.combo_box.setCurrentIndex(default_index)
        self.combo_box.currentIndexChanged.connect(self.onComboIndexChanged)

        self.merge_button = QPushButton("Merge")
        self.merge_button.clicked.connect(self.mergeSelected)
        self.reset_button = QPushButton("Save")
        self.reset_button.clicked.connect(self.save_click)
        # Set up a new layout with the selected size
        self.rows, self.cols = map(int, self.combo_box.currentText().split('x'))
        self.drawing_widget = DrawingWidget(size_grid=self.rows)

        self.layout_top = QHBoxLayout()
        self.layout_top.addWidget(self.combo_box)
        self.layout_top.addWidget(self.merge_button)
        self.layout_top.addWidget(self.reset_button)
        self.layout.addLayout(self.layout_top)
        self.layout.addWidget(self.drawing_widget)

        self.setLayout(self.layout)

    def save_click(self):
        self.close()

    def mergeSelected(self):
        if len(self.drawing_widget.selected_frames) >= 2:
            self.drawing_widget.paint_borders = True
            new_merged_frame = [s for i, s in enumerate(self.drawing_widget.merged_frame) if
                                not any(e in self.drawing_widget.selected_frames for e in s)]

            # Append the new set
            new_merged_frame.append(self.drawing_widget.selected_frames)

            # Update the merged_frame attribute
            self.drawing_widget.merged_frame = new_merged_frame

            print("HanhLT: self.drawing_widget.merged_frame   ", self.drawing_widget.merged_frame)

            self.drawing_widget.testFlag = True
            # Clear the drawn rectangle
            self.drawing_widget.selection_start = None
            self.drawing_widget.selection_end = None
            # self.drawing_widget.selected_frames.clear()
            self.drawing_widget.update()

    def get_selected_positions(self):
        return [(i, j) for frame in self.drawing_widget.selected_frames for i in range(self.rows) for j in range(self.cols) if self.frames[i][j] is frame]

    def onComboIndexChanged(self, index):
        self.drawing_widget.merged_frame.clear()
        selected_item = self.combo_box.currentText()

        # Clear the drawn rectangle
        self.drawing_widget.selection_start = None
        self.drawing_widget.selection_end = None
        self.drawing_widget.selected_frames.clear()
        self.drawing_widget.update()

        # Clear the red borders on selected frames
        for i in range(self.drawing_widget.grid_layout.count()):
            frame = self.drawing_widget.grid_layout.itemAt(i).widget()
            frame.is_selected = False
            frame.update()

        # Clear the existing layout
        for i in reversed(range(self.drawing_widget.grid_layout.count())):
            widgetToRemove = self.drawing_widget.grid_layout.itemAt(i).widget()
            widgetToRemove.setParent(None)

        # Set up a new layout with the selected size
        self.rows, self.cols = map(int, selected_item.split('x'))
        for i in range(self.rows):
            for j in range(self.cols):
                frame = SelectableFrame(self.drawing_widget)
                self.drawing_widget.grid_layout.addWidget(frame, i, j)

        # Update the size of the drawing widget based on the new grid size
        self.drawing_widget.setFixedSize(800, 600)

class MenuGridType(QMenu):
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
            {"title": "Item 1", "image_path": "IMG1"},
            {"title": "Item 2", "image_path": "IMG2"},
            {"title": "Item 3", "image_path": "IMG3"},
            {"title": "Item 4", "image_path": "IMG4"},
            {"title": "Item 5", "image_path": "IMG5"},
            {"title": "Item 6", "image_path": "IMG6"},
            {"title": "Item 7", "image_path": "IMG7"},
            {"title": "Item 8", "image_path": "IMG8"},
            {"title": "Item 9", "image_path": "IMG9"},
            {"title": "Item 10", "image_path": "IMG10"},
            {"title": "Item 11", "image_path": "IMG11"},
        ]

        self.label_standard = QLabel("Standard Window Division")
        self.label_wide = QLabel("Wide Window Division")
        self.label_custom = QLabel("Custom Window Division")

        self.grid_standard = QGridLayout()
        # Add items to the grid layout
        row_standard, col_standard = 0, 0
        for data in items:
            item_widget = ItemGridType(data["title"], data["image_path"])
            self.grid_standard.addWidget(item_widget, row_standard, col_standard)
            col_standard += 1
            if col_standard == 6:
                col_standard = 0
                row_standard += 1

        self.grid_wide = QGridLayout()
        row_wide, col_wide = 0, 0
        for data in items:
            item_widget = ItemGridType(data["title"], data["image_path"])
            self.grid_wide.addWidget(item_widget, row_wide, col_wide)
            col_wide += 1
            if col_wide == 6:
                col_wide = 0
                row_wide += 1

        self.button_edit_grid = QPushButton("Edit")
        self.button_edit_grid.clicked.connect(self.show_dialog)

        self.custom_layout.addWidget(self.label_standard)
        self.custom_layout.addLayout(self.grid_standard)
        self.custom_layout.addWidget(self.label_wide)
        self.custom_layout.addLayout(self.grid_wide)
        self.custom_layout.addWidget(self.label_custom)
        self.custom_layout.addWidget(self.button_edit_grid)

        custom_widget.setLayout(self.custom_layout)
        # Create a QWidgetAction to add the custom widget to the QMenu
        custom_action = QWidgetAction(self)
        custom_action.setDefaultWidget(custom_widget)
        self.addAction(custom_action)
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint | Qt.WindowType.Popup)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)

    def show_dialog(self):
        self.dialog = Tezt()
        self.dialog.show()

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.load_ui()

    def load_ui(self):
        self.setFixedSize(1024, 768)

        # Create a single main layout
        main_layout = QVBoxLayout()

        # Create a grid layout for the SelectableFrames
        grid_layout = QGridLayout()
        grid_layout.setSpacing(0)

        # Create a SelectableFrame for each cell in the grid
        for i in range(4):
            for j in range(4):
                frame = SelectableFrame(self)
                frame.setFrameShape(QFrame.Panel)
                grid_layout.addWidget(frame, i, j)

        # Add the grid layout to the main layout
        main_layout.addLayout(grid_layout)

        self.menu_button = QPushButton("Grid")
        self.menu_button.clicked.connect(self.show_menu)

        # Add the menu button to the main layout
        main_layout.addWidget(self.menu_button)

        # Create a central widget and set the main layout on it
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def show_menu(self):
        # Get the global position of the button
        position = self.menu_button.mapToGlobal(self.menu_button.rect().bottomLeft())

        # Create the menu and show it
        menu = MenuGridType(self)
        menu.exec_(position)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setWindowTitle('Grid with Selection and Drawing')
    # window.setGeometry(100, 100, 400, 400)
    window.show()
    sys.exit(app.exec())
