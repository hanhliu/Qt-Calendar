import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QWidget, QStackedWidget, QVBoxLayout, QTextEdit, QGridLayout, QMainWindow


class NewGrid(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.load_ui()

    def load_ui(self):
        self.showMaximized()
        self.central_widget = QWidget()
        self.central_layout = QVBoxLayout()

        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(0)

        for row in range(0, 2):
            for col in range(0, 2):
                item = QWidget()
                item.setStyleSheet('background-color: lightblue;')
                self.grid_layout.addWidget(item, row, col)
        self.central_layout.addLayout(self.grid_layout)

        self.central_widget.setLayout(self.central_layout)
        self.setCentralWidget(self.central_widget)
        # Connect resizeEvent to a custom method
        self.central_widget.resizeEvent = self.on_resize_event

    def on_resize_event(self, event):
        print(f"HanhLT: on_resize_eventv")
        for row in range(0, 2):
            for col in range(0, 2):
                item = self.grid_layout.itemAtPosition(row, col)
                if item is not None:
                    stacked_widget = item.widget()
                    if isinstance(stacked_widget, QWidget):
                        item_size = stacked_widget.size()
                        print(f"Size of item at position ({row}, {col}): {item_size.width()} x {item_size.height()}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NewGrid()
    window.show()
    sys.exit(app.exec())
