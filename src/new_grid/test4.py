import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QFrame
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import Qt, QRect

class SelectableFrame(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.is_selected = False


class DrawingWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.grid_layout = QGridLayout(self)
        self.grid_layout.setSpacing(0)

        # Create a SelectableFrame for each cell in the grid
        for i in range(4):
            for j in range(4):
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

                # Check and avoid drawing the borders at adjacent edges
                if (row - 1, col) not in self.selected_frames and row > 0 and (row - 1, col + 1) not in self.selected_frames:
                    painter.drawLine(rect.topLeft(), rect.bottomLeft())
                if (row + 1, col) not in self.selected_frames and row < 3 and (row + 1, col - 1) not in self.selected_frames:
                    painter.drawLine(rect.topRight(), rect.bottomRight())
                if (row, col - 1) not in self.selected_frames and col > 0 and (row - 1, col - 1) not in self.selected_frames:
                    painter.drawLine(rect.topLeft(), rect.topRight())
                if (row, col + 1) not in self.selected_frames and col < 3 and (row + 1, col + 1) not in self.selected_frames:
                    painter.drawLine(rect.bottomLeft(), rect.bottomRight())

            # Draw the original grid frames
            else:
                painter.setPen(QPen(QColor(0, 0, 0), 1))
                painter.drawRect(rect)

        # Draw the overlay rectangle
        if self.selection_start is not None and self.selection_end is not None:
            painter.setPen(QPen(QColor(0, 0, 255), 2, Qt.DashLine))
            overlay_rect = QRect(self.selection_start, self.selection_end).normalized()
            painter.drawRect(overlay_rect)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DrawingWidget()
    window.setWindowTitle('Grid with Selection and Drawing')
    window.setGeometry(100, 100, 400, 400)
    window.show()
    sys.exit(app.exec_())
