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

                    # min_row = min(row for row, _ in self.merged_frame)
                    # max_row = max(row for row, _ in self.merged_frame)
                    # min_col = min(col for _, col in self.merged_frame)
                    # max_col = max(col for _, col in self.merged_frame)
                    #
                    # # Calculate the position and size of the bounding rectangle
                    # start_rect = self.grid_layout.itemAtPosition(min_row, min_col).geometry().topLeft()
                    # end_rect = self.grid_layout.itemAtPosition(max_row, max_col).geometry().bottomRight()
                    #
                    # total_rect = QRect(start_rect, end_rect)
                    # painter.setPen(QPen(QColor(0, 0, 0), 2))
                    # painter.drawRect(total_rect)

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
        self.merge_button.clicked.connect(self.mergeSelected)
        self.reset_button = QPushButton("Reset")
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

    def mergeSelected(self):
        if len(self.drawing_widget.selected_frames) >= 2:
            self.drawing_widget.paint_borders = True
            # Check if new_set shares any elements with sets in the list
            found_index = next((i for i, s in enumerate(self.drawing_widget.merged_frame) if any(e in s for e in self.drawing_widget.selected_frames)), None)
            matching_indices = [i for i, s in enumerate(self.drawing_widget.merged_frame) if any(e in self.drawing_widget.selected_frames for e in s)]
            # Remove all matching sets from the list
            for index in matching_indices:
                self.drawing_widget.merged_frame.pop(index)
            # if found_index is not None:
            #     # If found, remove the existing set
            #     self.drawing_widget.merged_frame.pop(found_index)

            # Append the new set
            self.drawing_widget.merged_frame.append(self.drawing_widget.selected_frames)

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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Tezt()
    window.setWindowTitle('Grid with Selection and Drawing')
    # window.setGeometry(100, 100, 400, 400)
    window.show()
    sys.exit(app.exec())

    # def mergeSelected(self):
    #     if len(self.drawing_widget.selected_frames) >= 2:
    #         # Find the minimum and maximum row and column indices of selected frames
    #         min_row = min(row for row, _ in self.drawing_widget.selected_frames)
    #         max_row = max(row for row, _ in self.drawing_widget.selected_frames)
    #         min_col = min(col for _, col in self.drawing_widget.selected_frames)
    #         max_col = max(col for _, col in self.drawing_widget.selected_frames)
    #
    #         # Calculate the total size of the merged frame
    #         total_rows = max_row - min_row + 1
    #         total_cols = max_col - min_col + 1
    #
    #         # Create the merged frame
    #         merged_frame = SelectableFrame()
    #
    #         # Add the merged frame to the grid layout
    #         self.drawing_widget.grid_layout.addWidget(
    #             merged_frame, min_row, min_col, total_rows, total_cols
    #         )
    #
    #         # Remove the selected frames from the grid layout
    #         for frame in self.drawing_widget.selected_frames:
    #             frame_widget = self.drawing_widget.grid_layout.itemAtPosition(*frame).widget()
    #             frame_widget.setParent(None)
    #
    #         # Clear the set of selected frames
    #         self.drawing_widget.selected_frames.clear()
    #         self.drawing_widget.selected_frames.add((min_row, min_col))
    #
    #         # Update the UI
    #         self.drawing_widget.update()