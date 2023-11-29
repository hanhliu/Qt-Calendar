from PySide6.QtCore import Qt, QRect
from PySide6.QtGui import QPainter, QPen, QColor
from PySide6.QtWidgets import QWidget, QGridLayout

from src.grid_custom.selectable_frame import SelectableFrame


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
