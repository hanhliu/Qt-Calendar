import os
import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QMainWindow, QApplication, QVBoxLayout, QGridLayout, QPushButton, QLabel, \
    QSizePolicy, QStackedWidget, QTextEdit, QStackedLayout


class NewGrid(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.load_ui()

    def load_ui(self):
        self.root_stacked_widget = QStackedWidget()
        test_widget = QTextEdit()
        test_widget.setStyleSheet('background-color: lightblue;')
        # self.root_stacked_widget.addWidget(test_widget)
        # #  self.root_stackedwidget.widget(0).hide() để mắt người không thấy được hiệu ứng resize frame
        # self.root_stacked_widget.widget(0).hide()
        self.root_stacked_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.root_layout = QVBoxLayout()
        self.showMaximized()

        grid_layout = QGridLayout()
        grid_layout.setSpacing(1)

        # Twelve items surrounding the largest item
        for row in range(0, 3):
            for col in range(0, 3):
                camera_frame = QTextEdit()
                # camera_frame.setFixedSize(40, 30)
                # camera_frame.setStyleSheet('background-color: lightblue;')
                root_camera_widget = QStackedWidget()
                root_camera_widget.setFixedSize(40, 30)
                root_camera_widget.addWidget(camera_frame)
                grid_layout.addWidget(root_camera_widget, row, col)
        camera_frame = QTextEdit()
        camera_frame.setStyleSheet('background-color: red;')
        self.root_layout.addLayout(grid_layout)

        # Get the size of each item in the grid
        for row in range(0, 3):
            for col in range(0, 3):
                item = grid_layout.itemAtPosition(row, col)
                if item is not None:
                    stacked_widget = item.widget()
                    if isinstance(stacked_widget, QStackedWidget):
                        # Get the current widget from the QStackedWidget
                        current_widget = stacked_widget.currentWidget()
                        if current_widget is not None:
                            item_size = current_widget.size()

                            print(
                                f"HanhLT: Size of item at position ({row}, {col}): {item_size.width()} x {item_size.height()}")
        widget = QWidget()
        widget.setLayout(self.root_layout)
        self.root_stacked_widget.addWidget(widget)

        temp_layout = QVBoxLayout()
        temp_layout.addWidget(self.root_stacked_widget)

        temp_widget = QWidget()
        temp_widget.setLayout(temp_layout)
        self.setCentralWidget(temp_widget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NewGrid()
    window.show()
    sys.exit(app.exec())
