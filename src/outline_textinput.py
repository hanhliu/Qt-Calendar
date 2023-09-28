import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget
from PySide6.QtCore import Qt, QTimer

class Toast(QWidget):
    def __init__(self, message, timeout=3000):
        super().__init__()

        self.message = message
        self.timeout = timeout

        self.label = QPushButton(self.message)
        self.label.setFlat(True)
        self.label.clicked.connect(self.hide)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)

        self.setStyleSheet(
            "background-color: rgba(50, 50, 50, 180); color: white; border-radius: 5px; padding: 10px;"
        )

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setGeometry(0, 0, 0, 0)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.hide)
        self.timer.start(self.timeout)

    def show(self):
        super().show()
        self.setWindowOpacity(0.7)

    def hide(self):
        self.timer.stop()
        self.setWindowOpacity(0)
        self.deleteLater()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Toast Example")

        layout = QVBoxLayout()
        self.button = QPushButton("Show Toast")
        self.button.clicked.connect(self.show_toast)
        layout.addWidget(self.button)

        self.central_widget = QWidget()
        self.central_widget.setLayout(layout)
        self.setCentralWidget(self.central_widget)

    def show_toast(self):
        toast = Toast("Hello, this is a toast notification!", timeout=3000)
        toast.setGeometry(
            1920 / 2 - toast.width() / 2,
            1080 / 2 - toast.height() / 2,
            toast.width(),
            toast.height(),
        )
        toast.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
