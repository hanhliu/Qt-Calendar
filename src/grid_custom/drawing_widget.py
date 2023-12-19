import math

from PySide6.QtCore import Qt, QRect, Signal
from PySide6.QtGui import QPainter, QPen, QColor
from PySide6.QtWidgets import QWidget, QGridLayout

from src.grid_custom.item_grid_model import ItemGridModel
from src.grid_custom.selectable_frame import SelectableFrame


class DrawingWidget(QWidget):
    signal_update_data = Signal(list)
    def __init__(self, data_model: ItemGridModel=None):
        super().__init__()
        self.data_model = data_model
        self.testFlag = False
        self.color_rectangle_select = QColor(255, 0, 0)
        self.row, self.column = data_model.row, data_model.column
        self.setFixedSize(600, 450)
        self.grid_layout = QGridLayout(self)
        self.grid_layout.setSpacing(0)
        self.grid_layout.setContentsMargins(0, 0, 0, 0)

        self.create_grid()

        self.selection_start = None
        self.selection_end = None
        self.selected_frames = set()  # Use a set to store the row and column indices of selected frames
        self.merged_frame = data_model.data

    def create_grid(self):
        # Clear the existing layout
        for i in reversed(range(self.grid_layout.count())):
            item = self.grid_layout.takeAt(i)
            if item.widget():
                item.widget().deleteLater()

        # Create a SelectableFrame for each cell in the grid
        for i in range(self.row):
            for j in range(self.column):
                frame = SelectableFrame(self)
                self.grid_layout.addWidget(frame, i, j)

    def calculate_ui_and_update_model(self):
        pass

    def set_row_count(self, row_count):
        self.row = row_count
        self.create_grid()
        self.update()

    def set_column_count(self, column_count):
        self.column = column_count
        self.create_grid()
        self.update()

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

            # Clear the drawn rectangle
            self.selection_start = None
            self.selection_end = None
            self.testFlag = False
            self.mergeSelected()
            # Redraw the widgets
            self.update()

    def mergeSelected(self):
        if len(self.selected_frames) >= 2 and not self.testFlag:
            new_merged_frame = [s for i, s in enumerate(self.merged_frame) if
                                not any(e in self.selected_frames for e in s)]
            # Append the new set
            new_merged_frame.append(self.selected_frames)

            # Update the merged_frame attribute
            self.merged_frame = new_merged_frame
            self.testFlag = True
            self.selection_start = None
            self.selection_end = None
            self.emit_data()

    def calculate_remaining_items(self):
        total_items = self.row * self.column
        # Đếm số lượng ô đã được merge
        merged_items = sum(len(merged_set) - 1 for merged_set in self.merged_frame)
        self.remaining_items = total_items - merged_items
        return self.remaining_items

    def emit_data(self):
        remain_item = self.calculate_remaining_items()
        self.signal_update_data.emit([self.merged_frame, remain_item, self.row, self.column])

    def paintEvent(self, event):
        painter = QPainter(self)

        # Draw the grid frames
        for i in range(self.grid_layout.count()):
            frame = self.grid_layout.itemAt(i).widget()
            rect = frame.geometry()
            row, col, _, _ = self.grid_layout.getItemPosition(i)
            if any((row, col) in frame for frame in self.merged_frame):
                # if self.paint_borders:
                painter.setPen(QPen(QColor(0, 0, 0), 1, Qt.DashLine))
                painter.drawLine(rect.bottomLeft(), rect.bottomRight())
                painter.drawLine(rect.bottomLeft(), rect.topLeft())
                # else:
                #     painter.setPen(QPen(QColor(0, 0, 0), 2))
                #     painter.drawRect(rect)
            # Draw the original grid frames
            else:
                painter.setPen(QPen(QColor(0, 0, 0), 2))
                painter.drawRect(rect)

        if self.merged_frame:
            for merged_set in self.merged_frame:
                if merged_set:
                    min_row = min(row for row, _ in merged_set)
                    max_row = max(row for row, _ in merged_set)
                    min_col = min(col for _, col in merged_set)
                    max_col = max(col for _, col in merged_set)

                    # Calculate the position and size of the bounding rectangle
                    start_rect = self.grid_layout.itemAtPosition(min_row, min_col).geometry().topLeft()
                    end_rect = self.grid_layout.itemAtPosition(max_row, max_col).geometry().bottomRight()

                    total_rect = QRect(start_rect, end_rect)
                    painter.setPen(QPen(QColor(0, 0, 0), 2))
                    painter.drawRect(total_rect)

        # Draw the overlay select area rectangle
        if self.selection_start is not None and self.selection_end is not None:
            painter.setPen(QPen(QColor(0, 0, 255), 1, Qt.DashLine))
            overlay_rect = QRect(self.selection_start, self.selection_end).normalized()
            painter.drawRect(overlay_rect)

        # Draw a red border around the total selected area
        if self.selected_frames and not self.testFlag:
            self.min_row = min(row for row, _ in self.selected_frames)
            self.max_row = max(row for row, _ in self.selected_frames)
            self.min_col = min(col for _, col in self.selected_frames)
            self.max_col = max(col for _, col in self.selected_frames)

            # Calculate the position and size of the bounding rectangle
            start_rect = self.grid_layout.itemAtPosition(self.min_row, self.min_col).geometry().topLeft()
            end_rect = self.grid_layout.itemAtPosition(self.max_row, self.max_col).geometry().bottomRight()

            total_rect = QRect(start_rect, end_rect)
            painter.setPen(QPen(self.color_rectangle_select, 2))
            painter.drawRect(total_rect)

        painter.end()  # Ensure to end the painting operation
