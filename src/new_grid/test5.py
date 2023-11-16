import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QFrame, QVBoxLayout, QComboBox, QPushButton, QHBoxLayout
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import Qt, QRect

class SelectableFrame(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.is_selected = False

class DrawingWidget(QWidget):
    def __init__(self,size_grid=4):
        super().__init__()
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

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
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

            print("Selected frames:", self.selected_frames)

            # Redraw the widgets
            self.update()

    def paintEvent(self, event):
        painter = QPainter(self)

        # Draw the grid frames
        for i in range(self.grid_layout.count()):
            frame = self.grid_layout.itemAt(i).widget()
            rect = frame.geometry()
            row, col, _, _ = self.grid_layout.getItemPosition(i)

            # Draw a red border around selected frames
            if (row, col) in self.selected_frames:
                painter.setPen(QPen(QColor(255, 0, 0), 2))
                painter.drawRect(rect)

            # Draw the original grid frames
            else:
                painter.setPen(QPen(QColor(0, 0, 0), 1))
                painter.drawRect(rect)

        # Draw the overlay rectangle
        if self.selection_start is not None and self.selection_end is not None:
            painter.setPen(QPen(QColor(0, 0, 255), 1, Qt.DashLine))
            overlay_rect = QRect(self.selection_start, self.selection_end).normalized()
            painter.drawRect(overlay_rect)


class Tezt(QWidget):
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
        self.reset_button = QPushButton("Reset")
        # Set up a new layout with the selected size
        rows, cols = map(int, self.combo_box.currentText().split('x'))
        self.drawing_widget = DrawingWidget(size_grid=rows)

        self.layout_top = QHBoxLayout()
        self.layout_top.addWidget(self.combo_box)
        self.layout_top.addWidget(self.merge_button)
        self.layout_top.addWidget(self.reset_button)
        self.layout.addLayout(self.layout_top)
        self.layout.addWidget(self.drawing_widget)

        self.setLayout(self.layout)

    def onComboIndexChanged(self, index):
        selected_item = self.combo_box.currentText()

        # Clear the existing layout
        for i in reversed(range(self.drawing_widget.grid_layout.count())):
            widgetToRemove = self.drawing_widget.grid_layout.itemAt(i).widget()
            # remove it from the layout list
            self.drawing_widget.grid_layout.removeWidget(widgetToRemove)
            # remove it from the gui
            widgetToRemove.setParent(None)

        # Set up a new layout with the selected size
        rows, cols = map(int, selected_item.split('x'))
        for i in range(rows):
            for j in range(cols):
                frame = SelectableFrame(self.drawing_widget)
                self.drawing_widget.grid_layout.addWidget(frame, i, j)

        # Update the size of the drawing widget based on the new grid size
        self.drawing_widget.setFixedSize(800, 600)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Tezt()
    window.setWindowTitle('Grid with Selection and Drawing')
    # window.setGeometry(100, 100, 400, 400)
    window.show()
    sys.exit(app.exec_())
