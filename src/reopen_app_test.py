import sys

from PySide6 import QtCore
from PySide6.QtCore import QCoreApplication
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        # Create a button to reopen the application
        reopen_button = QPushButton("Reopen Application")
        reopen_button.clicked.connect(self.reopen_application)

        layout.addWidget(reopen_button)
        central_widget.setLayout(layout)

    def reopen_application(self):
        QtCore.QCoreApplication.quit()
        status = QtCore.QProcess.startDetached(sys.executable, sys.argv)
        print(status)

def main():
    app = QApplication(sys.argv)
    main_window = MyWindow()
    main_window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
