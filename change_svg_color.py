from PySide6.QtCore import Qt, QByteArray
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton
from PySide6.QtSvgWidgets import QSvgWidget
import sys


class SvgWidget(QSvgWidget):
    def __init__(self, svg_path, parent=None):
        super().__init__(parent)
        self.svg_path = svg_path
        self.dark_mode = False  # Start in light mode by default
        self.setFixedSize(100, 100)
        self.loadSvgWithColor()  # Initial load

    def loadSvgWithColor(self):
        # Load SVG content
        with open(self.svg_path, 'r') as file:
            svg_data = file.read()

        # Set the color based on dark mode
        color = "#FFFFFF" if self.dark_mode else "#000000"

        # Replace the fill color in SVG path data
        svg_data = svg_data.replace('fill="#F7F0F7"', f'fill="{color}"')

        # Load modified SVG data
        self.load(QByteArray(svg_data.encode('utf-8')))

    def setDarkMode(self, enabled):
        self.dark_mode = enabled
        self.loadSvgWithColor()  # Reload with new color


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.svg_widget = SvgWidget("src/assets/ptz_icon/top.svg")

        # Toggle button for dark/light mode
        self.toggle_button = QPushButton("Toggle Dark/Light Mode")
        self.toggle_button.clicked.connect(self.toggle_dark_mode)

        # Set up layout
        layout = QVBoxLayout()
        layout.addWidget(self.svg_widget)
        layout.addWidget(self.toggle_button)
        self.setLayout(layout)

    def toggle_dark_mode(self):
        # Switch mode and update SVG fill color
        is_dark_mode = not self.svg_widget.dark_mode
        self.svg_widget.setDarkMode(is_dark_mode)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec())
