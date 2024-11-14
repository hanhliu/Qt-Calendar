import os
import sys
from PySide6.QtWidgets import QWidget, QMainWindow, QApplication, QVBoxLayout, QLineEdit


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.load_ui()

    def load_ui(self):
        self.central_widget = QWidget()
        self.central_layout = QVBoxLayout()

        self.line_edit_1 = QLineEdit()
        self.line_edit_2 = QLineEdit()

        self.central_layout.addWidget(self.line_edit_1)
        self.central_layout.addWidget(self.line_edit_2)
        self.central_widget.setLayout(self.central_layout)
        self.setCentralWidget(self.central_widget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
