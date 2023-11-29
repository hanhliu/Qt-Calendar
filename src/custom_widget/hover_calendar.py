import sys
from PySide6.QtWidgets import QApplication, QWidget, QGridLayout, QVBoxLayout, QLabel
from PySide6.QtGui import QColor
from PySide6.QtCore import Signal, QObject


class ColorWidget(QWidget):
    clicked = Signal(QWidget)

    def __init__(self):
        super().__init__()
        self.setAutoFillBackground(True)

        self.label = QLabel(f"Label")
        self.label.setStyleSheet(f"background-color: white;")
        # Customize the widget's appearance or functionality here if needed
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)

    def mousePressEvent(self, event):
        self.clicked.emit(self)
        event.accept()


class ColorController(QObject):
    def __init__(self, widgets):
        super().__init__()
        self.widgets = widgets
        self.previous_widget = None
        for widget in self.widgets:
            widget.clicked.connect(self.handle_widget_clicked)

    def handle_widget_clicked(self, widget):
        if self.previous_widget and self.previous_widget != widget:
            self.previous_widget.label_image.setStyleSheet(f"background-color: white;")
        widget.label_image.setStyleSheet(f"background-color: green;")
        self.previous_widget = widget


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Create the main window
    window = QWidget()
    window.setWindowTitle('Grid Layout Example')

    # Create the grid layout
    grid_layout = QGridLayout()
    grid_layout.setColumnStretch(1, 1)  # Optional: Stretch the second column to fill the available space

    # Create the widgets and add them to the grid layout
    widgets = []
    for i in range(4):
        widget = ColorWidget()
        grid_layout.addWidget(widget, 0, i)  # Add the widget to row 0, column i
        widgets.append(widget)

    # Create the color controller
    controller = ColorController(widgets)

    # Set the layout on the main window
    window.setLayout(grid_layout)

    # Show the main window
    window.show()

    # Start the event loop
    sys.exit(app.exec())
